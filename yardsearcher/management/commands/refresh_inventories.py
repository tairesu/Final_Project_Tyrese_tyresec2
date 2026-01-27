from django.core.management.base import BaseCommand
from yardsearcher.models import Junkyard, Vehicle
from datetime import datetime
from django.db.models import Q
from yardsearcher.utils.known_yards import KNOWN_YARDS as KNOWN_YARDS

def get_junkyard_id(yard) ->int:
    return Junkyard.objects.get(address=yard['address']).pk or None

class Command(BaseCommand):
	help = "Refreshes Vehicle Table"

	def handle(self, *args, **options):
		""" 
			Initializes all junkyard scrapers and upserts their results into Vehicle models 
			(Also deletes vehicles that are physically removed from the junkyard )

		"""
		for yard in KNOWN_YARDS:
			self.stdout.write(f"Refreshing {yard['name']} Inventory")
			yard['id'] = get_junkyard_id(yard)
			scraper = yard['class']("") if 'params' not in yard.keys() else yard['class']("", params=yard['params'])
			scraper.handle_queries()
			self.stdout.write(self.style.SUCCESS(f"\tResults are in"))
			self.cache_scraper_results(scraper.results_as_list(), yard)
			self.stdout.write(self.style.SUCCESS(f"Successfully refreshed {yard['name']}'s inventory!\n"))

	def cache_scraper_results(self, results, yard):
		""" 
			Upserts or deletes vehicles on Vehicle model 
		"""
		assert len(results) > 0
		print(f"\tCaching {len(results)} results")
		models_list = []
		scraped_identifiers = [] # Ex: ['stk0192','stk1111']

		# Format results to django model instances (<Vehicle>) 
		for result in results:
			vehicle_instance = self.format_result(result, yard)
			scraped_identifiers.append(vehicle_instance.junkyard_identifier)
			models_list.append(vehicle_instance)
		self.upsert_models_list(models_list)
		self.handle_removed_results(scraped_identifiers, yard['id'])
	
	def format_result(self, result, yard):
		"""
		Turns any scraped result into a <Vehicle> instance
		"""
		year = result['year']
		make = result['make']
		model = result['model']
		# some result keys require more handling because junkyard inventory column headers differ
		# Ex: JUP uses 'vehicle_row' while LKQ's may say 'row'  
		row = self.extract_row(result)
		junkyard_identifier = self.extract_junkyard_identifier(result)
		color = self.extract_color(result)
		space = self.extract_space(result)
		available_date = self.extract_date(result, yard['date_format'])
		vin = self.extract_vin(result)
		return Vehicle(junkyard_id=yard['id'], year=year, make=make, model=model, available_date=available_date, row=row, space=space, color=color, junkyard_identifier=junkyard_identifier, vin=vin)

	def extract_row(self, result):
		"""
		Returns the 'Row' value from a junkyard scraper's results attr
		"""
		row = 0
		# Junkyards may name the 'row' attrtibute differently
		if 'row' in result.keys() and len(result['row']) > 0:
			row = result['row']  # Pyp
		elif 'vehicle row' in result.keys() and len(result['vehicle row']) > 0:
			row = result['vehicle row'] # Jup
		return int(row)

	def extract_junkyard_identifier(self, result):
		junkyard_identifier = ""
		if 'stock#' in result.keys():
			junkyard_identifier = result['stock#']
		elif 'stock #' in result.keys():
			junkyard_identifier = result['stock #']
		return junkyard_identifier

	def extract_color(self, result):
		color = ""
		if 'color' in result.keys():
			color = result['color']
		return color

	def extract_space(self, result):
		space = 0
		if 'space' in result.keys() and len(result['space']) > 0:
			space = result['space']
		return space

	def extract_date(self, result, date_format):
		date = ''
		if 'date set in yard' in result.keys():
			date = result['date set in yard']
		elif 'available' in result.keys():
			date = result['available'] 
		return datetime.strptime(date, date_format)

	def extract_vin(self, result):
		vin = ""
		if 'vin' in result.keys():
			vin = result['vin']
		return vin

	def upsert_models_list(self, models_list):
		# Upsert list of <Vehicle> instances
		Vehicle.objects.bulk_create(models_list, update_conflicts=True, unique_fields=['junkyard_identifier','junkyard'], update_fields=['year','make','model'])
		self.stdout.write(self.style.SUCCESS(f"\t- Upserted {len(models_list)} Vehicles"))

	def handle_removed_results(self, scraped_identifiers, junkyard_id):
		"""
			Removes vehicles from <Vehicle> model that have id of junkyard_id and are NOT in freshly scraped results 
		"""
		different_identifiers = Vehicle.objects.filter(Q(junkyard_id=junkyard_id) & ~Q(junkyard_identifier__in=scraped_identifiers) )
		print(f"\t Different identifiers: {different_identifiers}")
		if len(different_identifiers) > 0:
			self.stdout.write(f"\t- Deleting {len(different_identifiers)} vehicles: \n {different_identifiers}")
			different_identifiers.delete()
		

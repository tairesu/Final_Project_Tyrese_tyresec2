from django.core.management.base import BaseCommand
from yardsearcher.models import Junkyard, Vehicle
from yardsearcher.utils.jup import Jup
from yardsearcher.utils.lkq import LKQSearch
from datetime import datetime
from django.db.models import Q

ALLOWED_YARDS = {

	'Joliet U-Pull-It': {
		'class': Jup,
		'id' : 1,
		'date_format': '%m.%d.%y'
	},
}
ALLOWED_YARDS2 = [
	{
		'name': 'Joliet U-Pull-It',
		'class': Jup,
		'id': 1,
		'date_format': '%m.%d.%y',
	},
	{
		'name': 'LKQ Blue Island',
		'class': LKQSearch,
		'id': 2,
		'date_format': '%m/%d/%Y',
	},
]

class Command(BaseCommand):
	help = "Refreshes Vehicle Table"

	def handle(self, *args, **options):
		""" 
			Initializes all junkyard scrapers and upserts their results into Vehicle models 
			(Also deletes vehicles that are physically removed from the junkyard )

		"""
		for junkyard in ALLOWED_YARDS2:
			self.stdout.write(f"Refreshing {junkyard['name']}")
			scraper = junkyard['class']("")
			scraper.handle_queries()
			self.cache_scraper_results(scraper.results_as_list(), junkyard)
			self.stdout.write(self.style.SUCCESS(f"\nSuccessfully refreshed {junkyard['name']}'s inventory!\n"))

	def cache_scraper_results(self, results, junkyard_meta):
		""" 
			Upserts or deletes vehicles on Vehicle model 
		"""
		assert len(results) > 0
		models_list = []
		scraped_identifiers = [] # Ex: ['stk0192','stk1111']

		# Format results to django model instances (<Vehicle>) 
		for result in results:
			vehicle_instance = self.format_result(result, junkyard_meta)
			scraped_identifiers.append(vehicle_instance.junkyard_identifier)
			models_list.append(vehicle_instance)
		self.upsert_models_list(models_list)
		self.handle_removed_results(scraped_identifiers, junkyard_meta['id'])

	def format_result(self, result, junkyard_meta):
		"""
		Turns any scraped result into an instance of the <Vehicle> model
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
		available_date = self.extract_date(result, junkyard_meta['date_format'])
		vin = self.extract_vin(result)
		return Vehicle(junkyard_id=junkyard_meta['id'], year=year, make=make, model=model, available_date=available_date, row=row, space=space, color=color, junkyard_identifier=junkyard_identifier, vin=vin)

	def extract_row(self, result):
		row = 0
		if 'vechicle_row' in result.keys():
			row = result['vechicle_row']
		return row

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
		if 'space' in result.keys():
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
			Removes vehicles from <Vehicle> model that have the same junkyard_id and are NOT in freshly scraped results 
		"""
		different_identifiers = Vehicle.objects.filter(Q(junkyard_id=junkyard_id) & ~Q(junkyard_identifier__in=scraped_identifiers) )
		print(f"\t Different identifiers: {different_identifiers}")
		different_identifiers.delete()
		if len(different_identifiers) > 0:
			self.stdout.write(f"\t- Deleting {len(different_identifiers)} vehicles: \n {different_identifiers}")
		else:
			pass

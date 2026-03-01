from django.core.management.base import BaseCommand
from yardsearcher.models import Junkyard, Vehicle

from django.db.models import Q
from yardsearcher.utils.known_yards import KNOWN_YARDS as KNOWN_YARDS
from yardsearcher.utils.extractors import *

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
			try:
				self.stdout.write(f"Refreshing {yard['name']} Inventory")
				yard['id'] = get_junkyard_id(yard)
				scraper = yard['class']("") if 'params' not in yard.keys() else yard['class']("", params=yard['params'])
				scraper.handle_queries()
				self.stdout.write(self.style.SUCCESS(f"\tResults are in"))
				self.cache_scraper_results(scraper.results_as_list(), yard)
				self.stdout.write(self.style.SUCCESS(f"Successfully refreshed {yard['name']}'s inventory!\n"))
			except Exception as e:
				self.stdout.write(self.style.ERROR(f"Skipping over {yard['name']}'s inventory because:\n {e}"))
				continue
				

	def cache_scraper_results(self, results, yard):
		""" 
			Upserts or deletes vehicles on Vehicle model 
		"""
		assert len(results) > 0
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
		try:
			# some result keys require more handling because junkyard inventory column headers differ
			return Vehicle(
       			junkyard_id=yard['id'],
          		year=result['year'],
            	make=result['make'],
            	model=result['model'],
             	available_date=extract_date(result, yard['date_format']), 
              	row=extract_row(result),
               	space=extract_space(result), 
                color=extract_color(result),
                junkyard_identifier=extract_junkyard_identifier(result),
                vin=extract_vin(result)
            )
		except ValueError as e:
			print(f"{e} appeared at this result: {result}")
			raise ValueError

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
		

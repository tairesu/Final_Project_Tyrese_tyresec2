from django.core.management.base import BaseCommand
from yardsearcher.models import Junkyard, Vehicle
from yardsearcher.utils.jup import Jup
from yardsearcher.utils.lkq import LKQSearch
from datetime import datetime

ALLOWED_YARDS = {

	'Joliet U-Pull-It': {
		'class': Jup,
		'id' : 1,
		'date_format': '%m.%d.%y'
	},
}

class Command(BaseCommand):
	help = "Refreshes junkyard and vehicle data"
	current_yard = ''
	current_yard_id = 0

	def handle(self, *args, **options):
		self.stdout.write("Starting inventory refresh...")
		# Pipe the inventory results of each scraper into process_inventory
		for yard in ALLOWED_YARDS.keys():
			self.current_yard = yard
			self.current_yard_id = ALLOWED_YARDS[yard]['id']
			yard_class = ALLOWED_YARDS[yard]['class']("") # Init scraper class
			yard_class.handle_queries()
			self.stdout.write(f"Processing {yard_class.name}")
			self.process_inventory(yard_class.results_as_list())
			self.stdout.write(self.style.SUCCESS(f"Successfully refreshed {yard} inventory!"))

	def process_inventory(self, results_list ):
		""" 
			Format results from results_list to populate the database 
		"""
		assert len(results_list) > 0
		models_list = []
		# Will capture identifiers from scraped results: ['stk0192','stk1111']
		scraped_identifiers = []

		for car_dict in results_list:
			year = car_dict['year']
			make = car_dict['make']
			model = car_dict['model']

			# some keys may require further extraction
			# a jup key may be 'stock#' while lkq 'stock #'  
			row = self.extract_row(car_dict)
			space = self.extract_space(car_dict)
			color = self.extract_color(car_dict)
			junkyard_indentifier = self.extract_junkyard_identifier(car_dict)
			vin = self.extract_vin(car_dict)
			available_date = self.extract_date(car_dict)
			scraped_identifiers.append(junkyard_indentifier)
			models_list.append(Vehicle(junkyard_id=self.current_yard_id, year=year, make=make, model=model, available_date=available_date, row=row, space=space, color=color, junkyard_indentifier=junkyard_indentifier, vin=vin))

		Vehicle.objects.bulk_create(models_list, update_conflicts=True, unique_fields=['junkyard_indentifier','junkyard'], update_fields=['year','make','model'])
		different_identifiers = Vehicle.objects.exclude(junkyard_indentifier__in=scraped_identifiers)

		print(f"{scraped_identifiers}")
		print(f"'{len(different_identifiers)}Vehicles that are no longer there: '{different_identifiers}")
		different_identifiers.delete()

	def extract_junkyard_identifier(self, car_dict):
		junkyard_identifier = ""
		if 'stock#' in car_dict.keys():
			junkyard_identifier = car_dict['stock#']
		elif 'stock #' in car_dict.keys():
			junkyard_identifier = car_dict['stock #']
		return junkyard_identifier

	def extract_color(self, car_dict):
		color = ""
		if 'color' in car_dict.keys():
			color = car_dict['color']
		return color

	def extract_row(self, car_dict):
		row = 0
		if 'vechicle_row' in car_dict.keys():
			row = car_dict['vechicle_row']
		return row

	def extract_space(self, car_dict):
		space = 0
		if 'space' in car_dict.keys():
			space = car_dict['space']
		return space

	def extract_date(self, car_dict):
		date = ''
		yard_date_format = ALLOWED_YARDS[self.current_yard]['date_format']
		if 'date set in yard' in car_dict.keys():
			date = car_dict['date set in yard']
		elif 'available' in car_dict.keys():
			date = car_dict['available'] 
		return datetime.strptime(date, yard_date_format)

	def extract_vin(self, car_dict):
		vin = ""
		if 'vin' in car_dict.keys():
			vin = car_dict['vin']
		return vin
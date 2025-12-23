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

	def handle(self, *args, **options):
		#Vehicle.objects.all().deletebulk update or create django ()
		self.stdout.write("Starting inventory refresh...")
		for yard in ALLOWED_YARDS.keys():
			yard_class = ALLOWED_YARDS[yard]['class']("")
			yard_class.handle_queries()
			self.stdout.write(f"Processing {yard_class.name}")
			self.current_yard = yard
			self.process_inventory(yard_class.results_as_list(), ALLOWED_YARDS[yard]['id'])
  			self.stdout.write(self.style.SUCCESS(f"Successfully refreshed {yard} inventory!"))

	def process_inventory(self, results_list, yard_id):
		""" 
			Format results from results_list to populate the database 
		"""
		assert len(results_list) > 0
		models_list = []
		# Will capture identifiers from scraped results 
		scraped_identifiers = []

		for car_dict in results_list:
			year = car_dict['year']
			make = car_dict['make']
			model = car_dict['model']
			row = car_dict['vehicle row'] if 'vehicle row' in car_dict.keys() else 0
			space = car_dict['space'] if 'space' in car_dict.keys() else 0
			color = car_dict['color'] if 'color' in car_dict.keys() else ""
			junkyard_indentifier = car_dict['stock#'] if 'stock#' in car_dict.keys() or 'stock #' in car_dict.keys() else ""
			vin = car_dict['vin'] if 'vin' in car_dict.keys() else ""
			available_date = self.extract_date(car_dict)
			scraped_identifiers.append(junkyard_indentifier)
			models_list.append(Vehicle(junkyard_id=yard_id, year=year, make=make, model=model, available_date=available_date, row=row, space=space, color=color, junkyard_indentifier=junkyard_indentifier, vin=vin))

		Vehicle.objects.bulk_create(models_list, update_conflicts=True, unique_fields=['junkyard_indentifier','junkyard'], update_fields=['year','make','model'])
		different_identifiers = Vehicle.objects.exclude(junkyard_indentifier__in=scraped_identifiers)
		print(f"{scraped_identifiers}")
		print(f"{different_identifiers}")

	def extract_date(self, car_dict):
		date = ''
		yard_date_format = ALLOWED_YARDS[self.current_yard]['date_format']
		if 'date set in yard' in car_dict.keys():
			date = car_dict['date set in yard']
		elif 'available' in car_dict.keys():
			date = car_dict['available'] 
		return datetime.strptime(date, yard_date_format)

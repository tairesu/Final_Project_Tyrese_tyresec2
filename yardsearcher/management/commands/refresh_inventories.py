from django.core.management.base import BaseCommand
from yardsearcher.models import Junkyard, Vehicle
from yardsearcher.utils.jup import Jup
from yardsearcher.utils.lkq import LKQSearch

ALLOWED_YARDS = {

	'Joliet U-Pull-It': {
		'class': Jup,
		'id' : 1,
		'date_format': '%y.%d.%m'
	},
}

class Command(BaseCommand):
	help = "Refreshes junkyard and vehicle data"
	
	def handle(self, *args, **options):
		self.stdout.write("Starting inventory refresh...")
		for yard in ALLOWED_YARDS.keys():
			yard_class = ALLOWED_YARDS[yard]['class']("")
			self.stdout.write(f"Processing {yard_class.name}")
			yard_class.handle_queries()
			self.process_inventory(yard_class.results_as_list(), ALLOWED_YARDS[yard]['id'])

	def process_inventory(self, results_list, yard_id):
		assert len(results_list) > 0
		print(results_list)
		models_list = []
		for car_dict in results_list:
			year = car_dict['year']
			make = car_dict['make']
			model = car_dict['model']
			row = car_dict['vehicle row'] if 'vehicle_row' in car_dict.keys() else 0
			space = car_dict['space'] if 'space' in car_dict.keys() else 0
			color = car_dict['color'] if 'color' in car_dict.keys() else ""
			junkyard_indentifier = car_dict['stock#'] if 'stock#' in car_dict.keys() or 'stock #' in car_dict.keys() else ""
			vin = car_dict['vin'] if 'vin' in car_dict.keys() else ""
			models_list.append(Vehicle(junkyard_id=yard_id, year=year, make=make, model=model, row=row, space=space, color=color, junkyard_indentifier=junkyard_indentifier, vin=vin))

		print(models_list)

			
				
       # self.stdout.write(self.style.SUCCESS("Successfully refreshed data!"))


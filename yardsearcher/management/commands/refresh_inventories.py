from django.core.management.base import BaseCommand
from yardsearcher.models import Junkyard, Vehicle
from yardsearcher.utils.jup import Jup
from yardsearcher.utils.lkq import LKQSearch

ALLOWED_YARDS = [Jup]

class Command(BaseCommand):
	help = "Refreshes junkyard and vehicle data"
	

	def handle(self, *args, **options):
		self.stdout.write("Starting data refresh...")
		for yard in ALLOWED_YARDS:
			yard_class = yard("")
			self.stdout.write(f"Processing {yard_class.name}")
			yard_class.handle_queries()
			self.process_inventory(yard_class.data_as_dict())

	def process_inventory(self, yard_inventory={}):
		assert len(yard_inventory['results']) > 0
		for car in yard_inventory['results']:
			for i,col in yard_inventory['result_headers']:
				Vehicle.objects.create(col[i])
				


       # self.stdout.write(self.style.SUCCESS("Successfully refreshed data!"))


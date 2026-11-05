from django.core.management.base import BaseCommand
from yardsearcher.models import Generation
from yardsearcher.utils.known_gens import handle as readAllJSON
from django.conf import settings
import os

class Command(BaseCommand):
	help = "Bulk creates/inserts vehicle generations"
	def handle(self, *args, **options):
		try:
			filename = os.path.join(settings.BASE_DIR, 'yardsearcher/utils/all.json')
			self.insert_gens(gens=readAllJSON(filename))
		except Exception as e:
			print(e)

	def insert_gens(self, gens: dict)-> None:
		print(gens)
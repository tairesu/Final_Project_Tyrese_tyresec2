from django.contrib import admin
from yardsearcher.models import (
    Junkyard,
    Vehicle,
    Scrape,
)


# Register your models here.
admin.site.register(Junkyard)
admin.site.register(Vehicle)
admin.site.register(Scrape)
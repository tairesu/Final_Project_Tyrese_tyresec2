from django.contrib import admin
from yardsearcher.models import (
    Junkyard,
    Vehicle,
    Scrape,
    Review,
    Generation
)


# Register your models here.
admin.site.register(Junkyard)
admin.site.register(Vehicle)
admin.site.register(Scrape)
admin.site.register(Review)
admin.site.register(Generation)
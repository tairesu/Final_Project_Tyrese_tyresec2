from django.contrib import admin
from yardsearcher.models import (
    Junkyard,
    Vehicle,
)


# Register your models here.
admin.site.register(Junkyard)
admin.site.register(Vehicle)
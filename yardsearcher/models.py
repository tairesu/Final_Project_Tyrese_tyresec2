from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from geopy.geocoders import Nominatim


# Create your models here.
class Junkyard(models.Model):
    junkyard_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=False)
    address = models.CharField(max_length=100, blank=False)
    city = models.CharField(max_length=50, blank=False)
    state = models.CharField(max_length=2, blank=False)
    zip_code = models.IntegerField(max_length=5, blank=False)
    website = models.URLField(blank=True, max_length=255)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('_detail', kwargs={'pk': self.pk})

    def get_latlong(self)-> tuple:
        geolocator = Nominatim(user_agent='scraphounds')
        location = geolocator.geocode(f'{self.address} {self.city},{self.state} {self.zip_code}')
        return (location.latitude, location.longitude) if location.latitude else ()


class Vehicle(models.Model):
    vehicle_id = models.AutoField(primary_key=True)
    junkyard = models.ForeignKey(Junkyard, related_name='vehicles', on_delete=models.CASCADE)
    junkyard_indentifier = models.CharField(max_length=30, blank=False)
    year = models.IntegerField(blank=False)
    make = models.CharField(max_length=40, blank=False)
    model = models.CharField(max_length=40, blank=False)
    color = models.CharField(max_length=20, blank=True)
    row = models.IntegerField(blank=False)
    space = models.IntegerField(blank=True)
    vin = models.CharField(max_length=17, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.year} {self.make} {self.model}'


class UserAllowedYard(models.Model):
    user = models.ForeignKey(User, related_name='allowed_yards', on_delete=models.CASCADE)
    junkyard = models.ForeignKey(Junkyard, related_name='allowed_yards', on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.user} allowed {self.junkyard}'
    
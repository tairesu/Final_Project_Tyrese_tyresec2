from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Junkyard(models.Model):
    junkyard_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=False)
    address = models.CharField(max_length=100, blank=False)
    city = models.CharField(max_length=50, blank=False)
    state = models.CharField(max_length=2, blank=False)
    zip_code = models.IntegerField(max_length=5, blank=False)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})

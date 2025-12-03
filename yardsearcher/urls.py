"""
URL configuration for scraphounds project.

"""
from django.contrib import admin
from django.urls import path, include
from yardsearcher.views import results_view

urlpatterns = [
    path('results/', results_view, name="results_urlpattern"),
]

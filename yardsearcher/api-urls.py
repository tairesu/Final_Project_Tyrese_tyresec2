"""
URL configuration for scraphounds project.

"""
from django.urls import path, include
from yardsearcher.views import (
    api_test_json_response
)

urlpatterns = [
    path('api/sortTable/', api_test_json_response, name="results_urlpattern"),
]

"""
URL configuration for scraphounds project.

"""
from django.urls import path, include
from yardsearcher.views import (
    api_test_json_response,
    api_sort_table
)

urlpatterns = [
    path('api/sortTable/', api_sort_table, name="api_sort_table_urlpattern"),
]

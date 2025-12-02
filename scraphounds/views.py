from django.shortcuts import render
from django.http.response import HttpResponse

# Create your views here.
def root_view(request):
    return HttpResponse("<h1>Home Page Coming Soon...</h1>")
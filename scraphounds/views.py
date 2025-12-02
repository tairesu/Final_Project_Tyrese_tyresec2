from django.shortcuts import render
from django.http.response import HttpResponse

# Create your views here.
def root_view(request):
    return render(request, "yardsearcher/base.html")
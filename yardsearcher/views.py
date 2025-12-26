from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from yardsearcher.utils.jup import *
from yardsearcher.utils.lkq import *
from django.views.generic import View
from yardsearcher.utils.queries import *
from django.db.models import Q
from django.db.models.functions import Lower
from yardsearcher.models import (
	Vehicle,
	Junkyard
)

def get_query_results(queries):
	results = []
	for query in queries:
		params = {
			'model__icontains': query['model'],
			'make__icontains': query['make'],
		}
		# If a range of years are present
		if 'minYear' and 'maxYear' in query:
			params['year__gte'] = query['minYear']
			params['year__lte'] = query['maxYear']
		else: 
			params['year'] = query['year']

	return Vehicle.objects.filter(**params)

def results_view(request):
	"""
		renders fetched junkyard results to results.html template
	"""
	context = {}
	if request.method == "GET":
		#query = request.GET.get('q')
		query = "2005-2009 honda civic"
		queries = get_query_conditionals(query)
		results = get_query_results(queries)
		print(results)

	#return render(request, 'yardsearcher/results.html', context)


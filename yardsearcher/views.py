import json
from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from yardsearcher.utils.jup import *
from yardsearcher.utils.lkq import *
from django.views.generic import View
from yardsearcher.utils.queries import *
from django.db.models import Q, Count
from django.db.models.functions import Lower
from yardsearcher.models import (
	Vehicle,
	Junkyard
)

def get_avg(li):
	dividend = len(li) if len(li) > 0 else 1
	return sum(li) / dividend

def get_query_results(queries):
	"""
	Returns vehicles matching searched queries
	"""
	
	constructed_query = construct_db_query(queries)
	print(f"generated query: {constructed_query}")
	return Vehicle.objects.filter(constructed_query)


def construct_db_query(queries):
	""" 
	Constructs a single Q object from list of query dicts
	"""
	constructed_query = Q()
	for query in queries:
		print(f"constructing Q value of {query}")
		condition = Q()
		# If a range of years are present
		if 'minYear' in query and 'maxYear' in query:
			condition &= Q(year__gte=query['minYear'], year__lte=query['maxYear'] )
		if 'year' in query: 
			condition &= Q(year=query['year'])
		if 'make' in query:
			condition &= Q(make__icontains=query['make']) | Q(model__icontains=query['make'])
		if 'model' in query:
			condition &= Q(model__icontains=query['model']) | Q(make__icontains=query['model'])
		constructed_query |= condition

	return constructed_query

def format_results(results, t0):
	lats = []
	longs = []
	formatted_results = []
	unique_yards = Junkyard.objects.all()
	for junkyard in unique_yards:
		lats.append(junkyard.lat)
		longs.append(junkyard.long)
		formatted_result = {
			'name': junkyard.name,
			'results': results.filter(junkyard_id=junkyard.pk),
			'lat': junkyard.lat,
			'long': junkyard.long,
			'time_elapsed': time.time() - t0,
			'meta': junkyard
				
		}
		formatted_result['num_results'] = len(formatted_result['results'])
		if formatted_result['num_results']>0:
			formatted_results.append(formatted_result)
	return (formatted_results, get_avg(lats), get_avg(longs))

def results_view(request):
	"""
		renders fetched junkyard results to results.html template
	"""
	context = {}
	if request.method == "GET":
		
		query = request.GET.get('q')
		t0 = time.time()
		queries = get_query_conditionals(query)
		results = get_query_results(queries)
		formatted_results, avg_lat, avg_long = format_results(results, t0)
		context = {
			'fetched_yard_data': formatted_results,
			'query': query,
			'avg_lat': avg_lat,
			'avg_long': avg_long,
			'total_yards': Junkyard.objects.all().count,
			'total_vehicles': Vehicle.objects.all().count
		}
		return render(request, 'yardsearcher/emergent-res-fusion.html', context)



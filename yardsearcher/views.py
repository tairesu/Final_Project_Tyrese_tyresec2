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
	Construct Q objects and returns vehicles matching search on Q objects
	"""
	combined_query = Q()
	for query in queries:
		condition = Q(make__icontains=query['make'], model__icontains=query['model'])
		# If a range of years are present
		if 'minYear' and 'maxYear' in query:
			condition &= Q(year__gte=query['minYear'], year__lte=query['maxYear'] )
		elif 'year' in query: 
			condition &= Q(year=query['year'])
		elif 'year' or 'minYear' or 'maxYear' not in query:
			pass
		combined_query |= condition
	print(f" condition: {combined_query}")
	return Vehicle.objects.filter(combined_query) 
	
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
			'elem_id': junkyard.name.replace(" ",""),
			'lat': junkyard.lat,
			'long': junkyard.long,
			'time_elapsed': time.time() - t0
				
		}
		formatted_result['num_results'] = len(formatted_result['results'])
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
			'avg_long': avg_long
		}
		return render(request, 'yardsearcher/results.html', context)


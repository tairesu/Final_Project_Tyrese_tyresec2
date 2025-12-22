from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from yardsearcher.utils.jup import *
from yardsearcher.utils.lkq import *
from django.views.generic import View

def results_view(request):
	"""
		renders fetched junkyard results to results.html template
	"""
	context = {}
	if request.method == "GET":
		query = request.GET.get('q') or " "
		fetched_yard_data = []

		# Grab data from various inventories based on query 
		jup_search = Jup(query)
		jup_search.handle_queries()
		fetched_yard_data.append(jup_search.data_as_dict())
		lkq_blue_search = LKQSearch(query)
		lkq_blue_search.handle_queries()
		fetched_yard_data.append(lkq_blue_search.data_as_dict())

		print(f"view longs: {YardSearch.longs}")
		print(f"view lats: {YardSearch.lats}")
		n = len(YardSearch.longs)
		avg_lat = sum(YardSearch.lats) / n
		avg_long = sum(YardSearch.longs) / n
		context['fetched_yard_data'] = fetched_yard_data
		context['query'] = query
		context['avg_lat'] = avg_lat
		context['avg_long'] = avg_long

	return render(request, 'yardsearcher/results.html', context)


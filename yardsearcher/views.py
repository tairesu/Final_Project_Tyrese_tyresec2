from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse


def results_view(request):
	"""
		renders fetched junkyard results to results.html template
	"""
	context = {}
	if request.method == "GET":
		context['query'] = request.GET.get('q') or " "

	return render(request, 'yardsearcher/results.html', context)
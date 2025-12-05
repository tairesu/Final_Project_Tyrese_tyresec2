from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse


def results_view(request):
	"""
		renders fetched junkyard results to results.html template
	"""
	context = {}
	if request.method == "GET":
		context['query'] = request.GET.get('q') or " "
		context['fetched_yard_data'] = [
      		{
				"name" : "Joliet U-Pull It",
				"elem_id" : "jap",
				"num_results" : 0,
				"time_elapsed" : 1.3,
				"result_headers" : ("make","model","year","date entered","stk"),
				"results" : [
        			("Honda", "Civic", 1977, "11/22/2000", 234243),
           		],
            },
      ]

	return render(request, 'yardsearcher/results.html', context)
# tester for queries py 
from yardsearcher.utils.queries import *
from django.db.models import Q, Count
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

if __name__ == '__main__':
	#extract_conditionals(test_query)
	#print(get_query_conditionals(test_query))
test_query = '2005-2009 honda civic'
queries = get_query_conditionals(test_query)
results = get_query_results(queries)
unique_yards = results.values('junkyard').annotate(num_results=Count('junkyard_id'))
"""
#WTF DO I WANT? RESULTS FROM EACH JUNKYARD LIKE SO  
fetched_yard_data = [{
	'results': [],
	'elem_id': '',
	'name': '',
	'time_elapsed': 2,

"""



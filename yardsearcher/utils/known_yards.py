
from yardsearcher.utils.jup import Jup
from yardsearcher.utils.lkq import LKQSearch

# Information on Junkyards are manually registered here. 
KNOWN_YARDS = [
	{
		'name': 'Joliet U-Pull It',
		'city': 'Joliet',
		'state': 'IL',
		'lat': 41.5224678,
		'long': -88.0560742,
		'address': '1014 E Washington St',
		'zip_code': 60433,
		'class': Jup,
		'date_format': '%m.%d.%y',
	},
 	{
		'name': 'Pick Your Part - Blue Island',
		'city': 'Dixmoor',
		'state': 'IL',
		'address': '2247 141st Street',
		'zip_code': 60406,
		'lat': 41.632102,
		'long': -87.672252,
		'class': LKQSearch,
		'date_format': '%m/%d/%Y',
		'params': {
			'store_id':1582,
			'referer_suffix': 'blue-island-1582'
		},
	},
	{
		'name': 'Pick Your Part - Chicago South',
		'class': LKQSearch,
		'date_format': '%m/%d/%Y',
		'city': 'Chicago',
		'lat': 41.8373,
		'long': -87.7126,
		'state': 'IL',
		'zip_code': 60623,
		'address': '3130 S. St Louis Ave.',
		'params': {
			'store_id':1585,
			'referer_suffix': 'chicago-south-1585'
		},
	},
]

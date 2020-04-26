import search
from django.conf import settings

class OurchiveSearch:
	config = {
	    'spotify_client_key': 'THE_SPOTIFY_CLIENT_KEY',
	    'spotify_client_secret': 'THE_SPOTIFY_CLIENT_SECRET',
	    'pandora_client_key': 'THE_PANDORA_CLIENT_KEY',
	    'pandora_client_secret': 'THE_PANDORA_CLIENT_SECRET',
	    'local_music_location': '/usr/data/music'
	}

	def __init__(self):
		searcher = search.factory.create(settings.SEARCH_BACKEND, **config)

	def do_search(self, **kwargs):
		print('generic search')

	def term_search(self, **kwargs):
		# check object being searched (default all), then:
		# multi match query on work
		# multi match query on bookmark
		# match query on user
		# match query on tags
		print('term search')

	def facet_filter(self, **kwargs):
		# check object being searched (default all), then:
		# facet filter on work
		# facet filter on bookmark
		# facet filter on user
		# facet filter on tags
		print('facet filter')

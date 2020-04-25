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

	def facet_filter(self, **kwargs):
		print('facet filter')

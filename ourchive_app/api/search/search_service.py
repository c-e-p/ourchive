from . import search
from django.conf import settings

class OurchiveSearch:
	def __init__(self):
		config = {}
		self.searcher = search.factory.create(settings.SEARCH_BACKEND, **config)

	def do_search(self, **kwargs):
		results = {}
		if ('work') in kwargs:
			results['work'] = self.searcher.search_works(**kwargs['work'])
		if ('bookmark') in kwargs:
			results['bookmark'] = searcher.search_bookmarks(kwargs['bookmark'])
		if ('tag') in kwargs:
			results['tag'] = searcher.search_tags(kwargs['tag'])
		if ('user') in kwargs:
			results['user'] = searcher.search_users(kwargs['user'])
		return results


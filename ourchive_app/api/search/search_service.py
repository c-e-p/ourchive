from . import search
from django.conf import settings
from api.models import OurchiveSetting

class OurchiveSearch:
	def __init__(self):
		config = {}
		search_backend = OurchiveSetting.objects.filter(name='Search Provider').first().value
		self.searcher = search.factory.create(search_backend, **config)

	def do_search(self, **kwargs):
		results = {}
		if ('work') in kwargs:
			results['work'] = self.searcher.search_works(**kwargs['work'])
		if ('bookmark') in kwargs:
			results['bookmark'] = self.searcher.search_bookmarks(**kwargs['bookmark'])
		if ('tag') in kwargs:
			results['tag'] = self.searcher.search_tags(**kwargs['tag'])
		if ('user') in kwargs:
			results['user'] = self.searcher.search_users(**kwargs['user'])
		return results


from api.models import Work, Tag, Chapter, TagType, WorkType, Bookmark, Comment, Message, NotificationType, Notification, OurchiveSetting
import object_factory

class ElasticSearchProvider:
	def init_provider():
		print('init provider')
	def search_works():
		print('search works')
	def search_bookmarks():
		print('search bookmarks')
	def search_users():
		print('search users')
	def filter_results():
		# word count
		# audio length
		# chapter count
		# specific tags
		# complete		
		print('perform filtered/faceted search')
	def get_facets():
		# get count by work type
		# get count by tag type
		# get count by admin tags
		print('get available facets')

class ElasticSearchServiceBuilder:
    def __init__(self):
        self._instance = None

    def __call__(self, port, **_ignored):
        if not self._instance:
            self._instance = ElasticSearchProvider()
        return self._instance

class PostgresProvider:
	def init_provider():
		print('init provider')

class PostgresServiceBuilder:
    def __init__(self):
        self._instance = None

    def __call__(self, **_ignored):
        if not self._instance:
            self._instance = PostgresProvider()
        return self._instance


factory = object_factory.ObjectFactory()
factory.register_builder('ELASTICSEARCH', ElasticSearchServiceBuilder())
factory.register_builder('POSTGRES', PostgresServiceBuilder())
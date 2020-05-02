from api.models import Work, Tag, Chapter, TagType, WorkType, Bookmark, Comment, Message, NotificationType, Notification, OurchiveSetting
import object_factory

class ElasticSearchProvider:
	def init_provider():
		print('init provider')
	def search_works(self, **kwargs):
		# word count
		# audio length
		# chapter count
		# specific tags
		# complete		
		print('search works')
	def search_bookmarks(self, **kwargs):
		print('search bookmarks')
	def search_users(self, **kwargs):
		print('search users')
	def search_tags(self, **kwargs):
		print('search users')
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
	from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
	def init_provider():
		print('init provider')
	def search_works(self, **kwargs):
		filters = kwargs['filter']
		work_filters = {
			'is_complete__exact': filters['complete'],
			'chapters__audio_length__gte': filters['audio_length'],
			'chapters__image_format__in': filters['image_formats'],
			'tags__text__in': filters['tags']
			}
		# todo word count	
		vector = SearchVector('title', weight='A') + SearchVector('summary', weight='B') + SearchVector('chapters__title', weight='B') \
		+ SearchVector('chapters__text', weight'D') + SearchVector('tags__text', weight='A') + SearchVector('chapters__summary', weight='C')
		query = SearchQuery(kwargs['term'])
		result = Work.objects.filter(**work_filters).annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.3).order_by('rank')
		return result
	def search_bookmarks(self, **kwargs):
		filters = kwargs['filter']
		bookmark_filters = {
			'is_complete__exact': filters['complete'],
			'bookmarks__rating__in': filters['image_formats'],
			'tags__text__in': filters['tags']
			}
		# todo word count	
		vector = SearchVector('title', weight='A') + SearchVector('description', weight='B') + SearchVector('bookmark__title', weight='A') \
		+ SearchVector('tags__text', weight='B') + SearchVector('bookmark__description', weight='C')
		query = SearchQuery(kwargs['term'])
		result = Bookmark.objects.filter(**work_filters).annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.3).order_by('rank')
		return result
	def search_users(self, **kwargs):
		result = User.objects.filter(username__search=kwargs['filter']['term'])
		return result
	def search_tags(self, **kwargs):
		filters = kwargs['filter']
		tag_filters = {
			'tag_type__label__in': filters['tag_types']
			}
		result = Tag.objects.filter(**tag_filters).filter(text__search=filters['term'])
	def get_facets():
		# get count by work type
		# get count by tag type
		# get count by admin tags
		print('get available facets')

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
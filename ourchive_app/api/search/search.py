from api.models import Work, Tag, Chapter, TagType, WorkType, Bookmark, BookmarkComment, ChapterComment, Message, NotificationType, Notification, OurchiveSetting
from api import object_factory
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
import json

class ElasticSearchProvider:
	from elasticsearch import Elasticsearch
	from elasticsearch_dsl import Search, Q
	def init_provider():
		print('init provider')
	def search_works(self, **kwargs):
		q = Q("multi_match", query=kwargs['filter']['term'], fields=['title', 'summary', 'chapter__title', 'chapters__summary', 'tags__text'])
		filters = kwargs['filter']

		client = Elasticsearch()

		s = Search(using=client, index="work")
		if 'complete' in filters:
			s = s.filter("term", is_complete=True)
		if 'audio_length' in filters:
			s = s.filter("range", chapters__audio_length={
                        "gt": filters['audio_length']
                    })
		if 'image_formats' in filters:
			s = s.filter("terms", chapters__image_format=filters['image_formats'])
		if 'image_formats' in filters:
			s = s.filter("terms", tags__text_format=filters['tags'])
		s = s.query(q)
		response = s.execute()
		return response

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
	
	def init_provider():
		print('init provider')
	def search_works(self, **kwargs):
		filters = kwargs['filter']
		work_filters = {}
		if 'complete' in filters:
			work_filters['is_complete__exact'] = filters['complete']
		if 'audio_length' in filters:
			work_filters['chapters__audio_length__gte'] = filters['audio_length']
		if 'image_formats' in filters:
			work_filters['chapters__image_format__in'] = filters['image_formats']
		if 'tags' in filters:
			work_filters['tags__text__in'] = filters['tags']
			
		# todo word count	
		vector = SearchVector('title', weight='A') + SearchVector('summary', weight='B') + SearchVector('chapters__title', weight='B') + SearchVector('chapters__text', weight='D') + SearchVector('tags__text', weight='A') + SearchVector('chapters__summary', weight='C')
		query = SearchQuery(kwargs['term'])
		resultset = Work.objects.filter(**work_filters).annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.2).order_by('rank')
		result_json = []
		for result in resultset:
			result_dict = result.__dict__
			result_dict.pop('_state', None)
			result_dict.pop('uid', None)
			result_dict.pop('created_on', None)
			result_dict.pop('updated_on', None)
			result_json.append(result_dict)
		return result_json
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
factory.register_builder('Default', PostgresServiceBuilder())
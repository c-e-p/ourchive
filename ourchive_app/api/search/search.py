from api.models import Work, Tag, User, Chapter, TagType, WorkType, Bookmark, BookmarkComment, ChapterComment, Message, NotificationType, Notification, OurchiveSetting
from api import object_factory
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
import json
from psycopg2.extensions import adapt
import re
from django.db.models import Q

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

	# ref: https://www.julienphalip.com/blog/adding-search-to-a-django-site-in-a-snap/
	def normalize_query(self, query_string,
	                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
	                    normspace=re.compile(r'\s{2,}').sub):
	    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
	        and grouping quoted words together.
	        Example:

	        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
	        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

	    '''
	    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

	def get_query(self, query_string, search_fields):
	    ''' Returns a query, that is a combination of Q objects. That combination
	        aims to search keywords within a model by testing the given search fields.

	    '''
	    query = None # Query to search for every search term        
	    terms = self.normalize_query(query_string)
	    for term in terms:
	        or_query = None # Query to search for a given term in each field
	        for field_name in search_fields:
	            q = Q(**{"%s__icontains" % field_name: term})
	            if or_query is None:
	                or_query = q
	            else:
	                or_query = or_query | q
	        if query is None:
	            query = or_query
	        else:
	            query = query & or_query
	    return query
	
	def init_provider():
		print('init provider')
	def search_works(self, **kwargs):
		filters = kwargs['filter']
		work_filters = {}
		if 'complete' in filters and filters['complete'] != "":
			work_filters['is_complete__exact'] = filters['complete']
		if 'audio_length' in filters and filters['audio_length'] != "":
			work_filters['chapters__audio_length__gte'] = filters['audio_length']
		if 'image_formats' in filters and filters['image_formats'] != "":
			work_filters['chapters__image_format__in'] = filters['image_formats']
		if 'tags' in filters and filters['tags'] != "":
			work_filters['tags__text__in'] = filters['tags']
		# todo word count	

		query = self.get_query(kwargs['term'], ['title', 'summary',])
		resultset = Work.objects.filter(**work_filters).filter(query)
		result_json = []
		for result in resultset:
			result_dict = result.__dict__
			print(result_dict)
			result_dict.pop('_state', None)
			result_dict.pop('uid', None)
			result_dict.pop('created_on', None)
			result_dict.pop('updated_on', None)
			result_json.append(result_dict)
		return result_json
	def search_bookmarks(self, **kwargs):
		filters = kwargs['filter']
		bookmark_filters = {}
		if 'complete' in filters and filters['complete'] != "":
			bookmark_filters['is_complete__exact'] = filters['complete']
		if 'ratings' in filters and filters['ratings'] != "":
			bookmark_filters['bookmarks__rating__in'] = filters['ratings']
		if 'tags' in filters and filters['tags'] != "":
			bookmark_filters['tags__text__in'] = filters['tags']

		# todo word count	
		vector = SearchVector('title', weight='A') + SearchVector('description', weight='A') + SearchVector('rating', weight='A')
		query = SearchQuery(kwargs['term'])
		resultset = Bookmark.objects.filter(**bookmark_filters).annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.3).order_by('rank')
		result_json = []
		for result in resultset:
			result_dict = result.__dict__
			result_dict.pop('_state', None)
			result_dict.pop('uid', None)
			result_dict.pop('created_on', None)
			result_dict.pop('updated_on', None)
			result_json.append(result_dict)
		return result_json
	def search_users(self, **kwargs):
		filters = kwargs['filter']
		vector = SearchVector('username', weight='A')
		query = SearchQuery(kwargs['term'])
		resultset = User.objects.filter(is_active=True).annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.3).order_by('rank')
		result_json = []
		for result in resultset:
			result_dict = result.__dict__
			result_dict.pop('_state', None)
			result_dict.pop('uid', None)
			result_dict.pop('created_on', None)
			result_dict.pop('updated_on', None)
			result_dict.pop('password', None)
			result_dict.pop('is_superuser', None)
			result_dict.pop('first_name', None)
			result_dict.pop('last_name', None)
			result_dict.pop('is_staff', None)
			result_dict.pop('email', None)
			result_dict.pop('date_joined', None)
			result_dict.pop('last_login', None)
			result_dict.pop('is_active', None)
			result_json.append(result_dict)
		return result_json
	def search_tags(self, **kwargs):
		filters = kwargs['filter']
		tag_filters = {}
		if 'tag_types' in filters and filters['tag_types'] != []:
			tag_filters['tag_type__label__in'] = filters['tag_types']
		if kwargs['term'] != "":
			tag_filters['text__icontains'] = kwargs['term']
		vector = SearchVector('tag_type__label', weight='B') + SearchVector('text', weight='A')
		query = SearchQuery(kwargs['term'])
		resultset = Tag.objects.filter(**tag_filters).annotate(rank=SearchRank(vector, query)).order_by('-rank')
		result_json = []
		for result in resultset:
			result_dict = result.__dict__
			result_dict.pop('_state', None)
			result_dict.pop('uid', None)
			result_dict.pop('created_on', None)
			result_dict.pop('updated_on', None)
			result_json.append(result_dict)
		return result_json
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
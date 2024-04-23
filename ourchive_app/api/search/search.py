from api.models import AttributeValue, Work, Tag, User, Chapter, TagType, WorkType, \
                       Bookmark, BookmarkComment, BookmarkCollection, ChapterComment, \
                       Message, NotificationType, Notification, OurchiveSetting, AttributeType
from api import object_factory
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
import json
import re
from django.db.models import Q
from .search_obj import WorkSearch, BookmarkSearch, TagSearch, UserSearch, CollectionSearch, FilterFacet, ResultFacet
from django.contrib.postgres.search import TrigramDistance, TrigramWordDistance
from api.utils import get_star_count
from django.core.paginator import Paginator
from django.conf import settings
from copy import deepcopy


class ElasticSearchProvider:
    from elasticsearch import Elasticsearch
    from elasticsearch_dsl import Search, Q

    def init_provider():
        print('init provider')

    def search_works(self, **kwargs):
        q = Q("multi_match", query=kwargs['filter']['term'], fields=[
              'title', 'summary', 'chapter__title', 'chapters__summary', 'tags__text'])
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


class ElasticSearchServiceBuilder:
    def __init__(self):
        self._instance = None

    def __call__(self, port, **_ignored):
        if not self._instance:
            self._instance = ElasticSearchProvider()
        return self._instance


class PostgresProvider:

    def __init__(self):
        self.work_search = WorkSearch()
        self.bookmark_search = BookmarkSearch()
        self.tag_search = TagSearch()
        self.collection_search = CollectionSearch()
        self.user_search = UserSearch()

    def init_provider():
        print('init provider')

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
        query = None  # Query to search for every search term
        terms = self.normalize_query(query_string)
        for term in terms:
            or_query = None  # Query to search for a given term in each field
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

    def build_filter_query(self, filter_array, filter_text, existing_query):
        if len(filter_array) > 0:
            or_query = None
            for array_item in filter_array:
                q = Q(**{filter_text: array_item})
                if or_query is None:
                    or_query = q
                else:
                    or_query = or_query | q
            if existing_query is None:
                existing_query = or_query
            else:
                existing_query = existing_query | or_query
        return existing_query

    def build_range_query(self, filter_obj, existing_query):
        if len(filter_obj['ranges']) < 1:
            return existing_query
        or_query = None
        for array_item in filter_obj['ranges']:
            q_high = Q(**{filter_obj['less_than']: array_item[0]})
            q_low = Q(**{filter_obj['greater_than']: array_item[1]})
            if or_query is None:
                or_query = (q_high & q_low)
            else:
                or_query = or_query | (q_high & q_low)
        if existing_query is None:
            existing_query = or_query
        else:
            existing_query = existing_query | or_query
        return existing_query

    def build_filters(self, filters, mode, include):
        full_filters = None
        for field in filters:
            join_filters = None
            if '_range' in field:
                join_filters = self.build_range_query(
                    filters[field], join_filters)
            else:
                for key in filters[field]:
                    join_filters = self.build_filter_query(
                        filters[field][key], key, join_filters)
            if join_filters:
                if not include:
                    join_filters = ~join_filters
                if full_filters is None:
                    full_filters = join_filters
                else:
                    if mode == "all":
                        full_filters = Q(full_filters & join_filters)
                    elif mode == "any":
                        full_filters = Q(full_filters | join_filters)
                    else:
                        full_filters = Q(full_filters & join_filters)
        return full_filters

    def process_results(self, resultset, page, obj, base_string='/search/?'):
        page_size = settings.REST_FRAMEWORK['PAGE_SIZE']
        paginator = Paginator(resultset, page_size)
        count = paginator.count if resultset else 0
        resultset = paginator.get_page(page) if resultset else []
        next_params = None if not resultset or not resultset.has_next(
        ) else f"{base_string}limit={page_size}&page={page+1}&object_type={obj.__name__}"
        prev_params = None if not resultset or not resultset.has_previous(
        ) else f"{base_string}limit={page_size}&page={page-1}&object_type={obj.__name__}"
        return [resultset, {"count": count, "prev_params": prev_params, "next_params": next_params}]

    # todo: move to kwargs or obj. my god.
    def run_queries(self, filters, query, obj, trigram_fields, term, page=1, order_by='-updated_on', has_drafts=False, trigram_max=0.85, require_distinct=True, has_private=False, has_filterable=False):
        resultset = None
        page = int(page)
        # filter on query first, then use filters (more exact, used when searching within) to narrow
        if query is not None:
            resultset = obj.objects.filter(query)
        if filters is not None:
            if self.include_mode == "all" and filters[0]:
                for q_item in filters[0].children:
                    resultset = resultset.filter(q_item) if resultset else obj.objects.filter(q_item)
            else:
                if not resultset and filters[0]:
                    resultset = obj.objects.filter(filters[0])
                elif filters[0]:
                    resultset = resultset.filter(filters[0])
            if self.exclude_mode == "any" and filters[1]:
                for q_item in filters[1].children:
                    resultset = resultset.filter(~Q(q_item)) if resultset else obj.objects.filter(q_item)
            else:
                if not resultset and filters[1]:
                    resultset = obj.objects.filter(filters[1])
                elif filters[1]:
                    resultset = resultset.filter(filters[1])
        if resultset is not None and has_drafts:
            resultset = resultset.filter(draft=False)
        if resultset is not None and has_private:
            resultset = resultset.filter(is_private=False)
        if resultset is not None and len(resultset) == 0 and query:
            # if exact matching & filtering produced no results, let's do limited trigram searching
            if len(trigram_fields) > 1:
                resultset = obj.objects.annotate(zero_distance=TrigramWordDistance(
                    term, trigram_fields[0])).annotate(one_distance=TrigramWordDistance(term, trigram_fields[1]))
                if filters[0] and filters[1]:
                    resultset = resultset.filter(
                        Q((Q(zero_distance__lte=trigram_max) | Q(one_distance__lte=trigram_max)) & filters[0] & filters[1]))
                elif filters[0]:
                    resultset = resultset.filter(
                        Q((Q(zero_distance__lte=trigram_max) | Q(one_distance__lte=trigram_max)) & filters[0]))
                elif filters[1]:
                    resultset = resultset.filter(
                        Q((Q(zero_distance__lte=trigram_max) | Q(one_distance__lte=trigram_max)) & filters[1]))
                else:
                    resultset = resultset.filter(zero_distance__lte=trigram_max).filter(
                        one_distance__lte=trigram_max)
                if resultset is not None and has_drafts:
                    resultset = resultset.filter(draft=False)
                resultset = resultset.order_by(
                    'zero_distance', 'one_distance', order_by)
            else:
                resultset = obj.objects.annotate(
                    zero_distance=TrigramWordDistance(term, trigram_fields[0]))
                if filters[0] and filters[1]:
                    resultset = resultset.filter(
                        Q((Q(zero_distance__lte=trigram_max) & filters[0] & filters[1])))
                elif filters[0]:
                    resultset = resultset.filter(
                        Q((Q(zero_distance__lte=trigram_max) & filters[0])))
                elif filters[1]:
                    resultset = resultset.filter(
                        Q((Q(zero_distance__lte=trigram_max) & filters[1])))
                else:
                    resultset = resultset.filter(zero_distance__lte=trigram_max)
                if resultset is not None and has_drafts:
                    resultset = resultset.filter(draft=False)
                resultset = resultset.order_by('zero_distance', order_by)
            require_distinct = False
        if resultset and has_filterable:
            resultset = resultset.filter(filterable=True)
        if require_distinct and resultset:
            # remove any dupes & apply order_by
            resultset = resultset.order_by(order_by).distinct()
        return self.process_results(resultset, page, obj)

    def get_filters(self, search_object):
        include_filters = self.build_filters(
            search_object.filter.include_filters, search_object.include_mode, True)
        exclude_filters = self.build_filters(
            search_object.filter.exclude_filters, search_object.exclude_mode, False)
        return [include_filters, exclude_filters]

    def get_user_dict(self, users):
        users_dict = []
        for result in users:
            user = {
                'id': result.id,
                'username': result.username
            }
            users_dict.append(user)
        return users_dict

    def build_work_resultset(self, resultset, reserved_fields):
        # build final resultset
        result_json = []
        for result in resultset:
            chapters = list(result.chapters.all())
            username = result.user.username
            tags = []
            for tag in result.tags.all():
                tag_dict = {}
                tag_dict["tag_type"] = tag.tag_type.label
                tag_dict["text"] = tag.text
                tag_dict["display_text"] = tag.display_text
                tag_dict["id"] = tag.id
                tags.append(tag_dict)
            attributes = []
            for attribute in result.attributes.all():
                attribute_dict = {}
                attribute_dict["attribute_type"] = attribute.attribute_type.display_name
                attribute_dict["name"] = attribute.name
                attribute_dict["display_name"] = attribute.display_name
                attribute_dict["id"] = attribute.id
                attribute_dict["order"] = attribute.order
                attributes.append(attribute_dict)
            users = self.get_user_dict(result.users.all())
            work_type = None if result.work_type is None else result.work_type.type_name
            result_dict = result.__dict__
            for field in reserved_fields:
                result_dict.pop(field, None)
            result_dict["user"] = username
            result_dict["users"] = users
            result_dict["work_type_name"] = work_type
            result_dict["tags"] = tags
            result_dict["attributes"] = attributes
            result_dict["chapter_count"] = len(chapters)
            result_json.append(result_dict)
        return result_json

    def build_bookmark_resultset(self, resultset, reserved_fields):
        result_json = []
        for result in resultset:
            username = result.user.username
            tags = []
            for tag in result.tags.all():
                tag_dict = {}
                tag_dict["tag_type"] = tag.tag_type.label
                tag_dict["text"] = tag.text
                tag_dict["display_text"] = tag.display_text
                tag_dict["id"] = tag.id
                tags.append(tag_dict)
            attributes = []
            for attribute in result.attributes.all():
                attribute_dict = {}
                attribute_dict["attribute_type"] = attribute.attribute_type.display_name
                attribute_dict["name"] = attribute.name
                attribute_dict["display_name"] = attribute.display_name
                attribute_dict["id"] = attribute.id
                attribute_dict["order"] = attribute.order
                attributes.append(attribute_dict)
            result_dict = result.__dict__
            result_dict["tags"] = tags
            result_dict["user"] = username
            result_dict["attributes"] = attributes
            result_dict["work"] = {}
            result_dict["work"]["id"] = result.work.id
            result_dict["work"]["title"] = result.work.title
            result_dict["work"]["user_id"] = result.work.user_id
            for field in reserved_fields:
                result_dict.pop(field, None)
            result_json.append(result_dict)
        return result_json

    def build_collection_resultset(self, resultset, reserved_fields):
        result_json = []
        for result in resultset:
            username = result.user.username
            tags = []
            for tag in result.tags.all():
                tag_dict = {}
                tag_dict["tag_type"] = tag.tag_type.label
                tag_dict["text"] = tag.text
                tag_dict["display_text"] = tag.display_text
                tag_dict["id"] = tag.id
                tags.append(tag_dict)
            attributes = []
            for attribute in result.attributes.all():
                attribute_dict = {}
                attribute_dict["attribute_type"] = attribute.attribute_type.display_name
                attribute_dict["name"] = attribute.name
                attribute_dict["display_name"] = attribute.display_name
                attribute_dict["id"] = attribute.id
                attribute_dict["order"] = attribute.order
                attributes.append(attribute_dict)
            users = self.get_user_dict(result.users.all())
            result_dict = result.__dict__
            result_dict["tags"] = tags
            result_dict["attributes"] = attributes
            result_dict["user"] = username
            result_dict["users"] = users
            for field in reserved_fields:
                result_dict.pop(field, None)
            result_json.append(result_dict)
        return result_json

    def search_works(self, **kwargs):
        self.work_search.from_dict(kwargs)
        work_filters = self.get_filters(self.work_search)
        # TODO: this is global - shouldn't really be here
        self.include_mode = self.work_search.include_mode
        self.exclude_mode = self.work_search.exclude_mode
        # build query
        query = self.get_query(self.work_search.term, self.work_search.term_search_fields)
        if not query and not work_filters:
            return {'data': []}
        resultset = self.run_queries(work_filters, query, Work, [
                                     'title', 'summary'], self.work_search.term, kwargs['page'], self.work_search.order_by, True)
        result_json = self.build_work_resultset(resultset[0], self.work_search.reserved_fields)
        print(self.work_search.filter.include_filters)
        print(self.work_search.filter.exclude_filters)
        return {'data': result_json, 'page': resultset[1]}

    def search_bookmarks(self, **kwargs):
        self.bookmark_search.from_dict(kwargs)
        bookmark_filters = self.get_filters(self.bookmark_search)
        query = self.get_query(self.bookmark_search.term, self.bookmark_search.term_search_fields)
        if not query and not bookmark_filters:
            return {'data': []}
        resultset = self.run_queries(bookmark_filters, query, Bookmark, [
                                     'title', 'description'], self.bookmark_search.term, kwargs.get('page', 1), self.bookmark_search.order_by, True, .85, True, True)
        result_json = self.build_bookmark_resultset(resultset[0], self.bookmark_search.reserved_fields)
        return {'data': result_json, 'page': resultset[1]}

    def search_collections(self, **kwargs):
        self.collection_search.from_dict(kwargs)
        collection_filters = self.get_filters(self.collection_search)
        query = self.get_query(self.collection_search.term,
                               self.collection_search.term_search_fields)
        if not query and not collection_filters:
            return {'data': []}
        resultset = self.run_queries(collection_filters, query, BookmarkCollection, [
                                     'title', 'short_description'], self.collection_search.term, kwargs.get('page', 1), self.collection_search.order_by, True)
        result_json = self.build_collection_resultset(resultset[0], self.collection_search.reserved_fields)
        return {'data': result_json, 'page': resultset[1]}

    def search_users(self, **kwargs):
        self.user_search.from_dict(kwargs)
        query = self.get_query(self.user_search.term, self.user_search.term_search_fields)
        if query is None:
            return {'data': []}
        resultset = User.objects.filter(is_active=True).filter(query)[:20]
        result_json = []
        for result in resultset:
            result_dict = result.__dict__
            for field in self.user_search.reserved_fields:
                result_dict.pop(field, None)
            result_json.append(result_dict)
        return {'data': result_json, 'page': {}}

    def autocomplete_tags(self, term, tag_type, fetch_all=False):
        results = []
        resultset = None
        term = term.lower()
        if tag_type:
            resultset = Tag.objects.filter(
                tag_type__type_name=tag_type).filter(tag_type__filterable=True).filter(filterable=True).filter(Q(text__icontains=term) | Q(display_text__icontains=term))
        else:
            resultset = Tag.objects.annotate(zero_distance=TrigramWordDistance(term, 'text'))
            resultset = resultset.filter(zero_distance__lte=.85)
            resultset = resultset.order_by('zero_distance', 'text')
            resultset = resultset[:10]
        if resultset is None:
            resultset = Tag.objects.filter(
                tag_type__type_name=tag_type).filter(tag_type__filterable=True).filter(filterable=True) if fetch_all else []
        for result in resultset:
            results.append({"tag": result.text, "display_text": result.display_text,
                            "id": result.id, "type": result.tag_type.label, "type_name": result.tag_type.type_name})
        return results

    def autocomplete_bookmarks(self, term, user):
        results = []
        resultset = None
        term = term.lower()
        resultset = Work.objects.filter(user__id=user,draft=False).filter(
            Q(title__icontains=term) | Q(summary__icontains=term))
        for result in resultset:
            work_dict = vars(result)
            if '_state' in work_dict:
                work_dict.pop('_state')
            results.append({"work": work_dict})
        return results

    def autocomplete_users(self, term, user):
        results = []
        resultset = None
        term = term.lower()
        resultset = User.objects.filter(
            Q(username__icontains=term))
        for result in resultset:
            user_dict = vars(result)
            if '_state' in user_dict:
                user_dict.pop('_state')
            results.append(user_dict)
        return results

    def search_tags(self, **kwargs):
        self.tag_search.from_dict(kwargs)
        tag_filters = self.get_filters(self.tag_search)
        query = self.get_query(self.tag_search.term, self.tag_search.term_search_fields)
        if not query and not tag_filters:
            return {'data': []}
        resultset = self.run_queries(tag_filters, query, Tag, [
                                     'text'], self.tag_search.term, kwargs.get('page', 1), self.tag_search.order_by, False, 0.6, False, False, True)
        result_json = []
        if resultset is None:
            return result_json
        for result in resultset[0]:
            tag_type = result.tag_type.label
            result_dict = result.__dict__
            for field in self.tag_search.reserved_fields:
                result_dict.pop(field, None)
            result_dict['tag_type'] = tag_type
            result_json.append(result_dict)
        return {'data': result_json, 'page': resultset[1]}

    def filter_by_tag(self, **kwargs):
        self.work_search.from_dict(kwargs['work_search'])
        work_filters = self.get_filters(self.work_search)
        self.bookmark_search.from_dict(kwargs['bookmark_search'])
        bookmark_filters = self.get_filters(self.bookmark_search)
        self.collection_search.from_dict(kwargs['collection_search'])
        collection_filters = self.get_filters(self.collection_search)

        page = kwargs['page'] if 'page' in kwargs else 1
        

        if 'page' in kwargs['work_search']:
            self.work_search.page = int(kwargs['work_search']['page'])
        if 'page' in kwargs['bookmark_search']:
            self.bookmark_search.page = int(kwargs['bookmark_search']['page'])
        if 'page' in kwargs['collection_search']:
            self.collection_search.page = int(kwargs['collection_search']['page'])

        tag = Tag.objects.get(pk=kwargs['tag_id'])
        works = Work.objects.filter(tags__id__exact=tag.id)
        if work_filters[0]:
            works = works.filter(work_filters[0])
        if work_filters[1]:
            works = works.filter(work_filters[1])
        works = works.filter(draft=False).distinct().order_by('-updated_on')
        bookmarks = Bookmark.objects.filter(tags__id__exact=tag.id)
        if bookmark_filters[0]:
            bookmarks = bookmarks.filter(bookmark_filters[0])
        if bookmark_filters[1]:
            bookmarks = bookmarks.filter(bookmark_filters[1])
        bookmarks = bookmarks.filter(draft=False).order_by('-updated_on').distinct()
        collections = BookmarkCollection.objects.filter(tags__id__exact=tag.id)
        if collection_filters[0]:
            collections = collections.filter(collection_filters[0])
        if collection_filters[1]:
            collections = collections.filter(collection_filters[1])
        collections = collections.filter(draft=False).order_by('-updated_on').distinct()

        base_string = f'/tags/{kwargs["tag_id"]}?tag_id={kwargs["tag_id"]}&'

        works_processed = self.process_results(works, self.work_search.page, Work, base_string)
        bookmarks_processed = self.process_results(bookmarks, self.bookmark_search.page, Bookmark, base_string)
        collections_processed = self.process_results(collections, self.collection_search.page, BookmarkCollection, base_string)

        # tag result object
        result_json = []
        tag_type = tag.tag_type.label
        result_dict = tag.__dict__
        for field in self.tag_search.reserved_fields:
            result_dict.pop(field, None)
        result_dict['tag_type'] = tag_type
        result_json.append(result_dict)
        tag_results = {'data': result_json, 'page': {'count': len(result_json)}}

        work_results = {'data': self.build_work_resultset(works_processed[0], self.work_search.reserved_fields), 'page': works_processed[1]}
        bookmark_results = {'data': self.build_bookmark_resultset(bookmarks_processed[0], self.bookmark_search.reserved_fields), 'page': bookmarks_processed[1]}
        collection_results = {'data': self.build_collection_resultset(collections_processed[0], self.collection_search.reserved_fields), 'page': collections_processed[1]}
        results = {}
        results['work'] = work_results
        results['bookmark'] = bookmark_results
        results['collection'] = collection_results
        results['tag'] = tag_results
        results['user'] = {'data': [], 'page': {}}
        return results

    def filter_by_attribute(self, **kwargs):
        self.work_search.from_dict(kwargs['work_search'])
        work_filters = self.get_filters(self.work_search)
        self.bookmark_search.from_dict(kwargs['bookmark_search'])
        bookmark_filters = self.get_filters(self.bookmark_search)
        self.collection_search.from_dict(kwargs['collection_search'])
        collection_filters = self.get_filters(self.collection_search)

        page = kwargs['page'] if 'page' in kwargs else 1

        if 'page' in kwargs['work_search']:
            self.work_search.page = int(kwargs['work_search']['page'])
        if 'page' in kwargs['bookmark_search']:
            self.bookmark_search.page = int(kwargs['bookmark_search']['page'])
        if 'page' in kwargs['collection_search']:
            self.collection_search.page = int(kwargs['collection_search']['page'])

        attribute = AttributeValue.objects.get(pk=kwargs['attr_id'])
        works = Work.objects.filter(attributes__id__exact=attribute.id)
        if work_filters[0]:
            works = works.filter(work_filters[0])
        if work_filters[1]:
            works = works.filter(work_filters[1])
        works = works.filter(draft=False).order_by('-updated_on').distinct()
        bookmarks = Bookmark.objects.filter(attributes__id__exact=attribute.id)
        if bookmark_filters[0]:
            bookmarks = bookmarks.filter(bookmark_filters[0])
        if bookmark_filters[1]:
            bookmarks = bookmarks.filter(bookmark_filters[1])
        bookmarks = bookmarks.filter(draft=False).order_by('-updated_on').distinct()
        collections = BookmarkCollection.objects.filter(attributes__id__exact=attribute.id)
        if collection_filters[0]:
            collections = collections.filter(collection_filters[0])
        if collection_filters[1]:
            collections = collections.filter(collection_filters[1])
        collections = collections.filter(draft=False).order_by('-updated_on').distinct()

        base_string = f'/attributes/{kwargs["attr_id"]}?attr_id={kwargs["attr_id"]}&'

        works_processed = self.process_results(works, self.work_search.page, Work, base_string)
        bookmarks_processed = self.process_results(bookmarks, self.bookmark_search.page, Bookmark, base_string)
        collections_processed = self.process_results(collections, self.bookmark_search.page, BookmarkCollection, base_string)

        # tag result object
        tag_results = {'data': {}, 'page': {'count': 0}}

        work_results = {'data': self.build_work_resultset(works_processed[0], self.work_search.reserved_fields), 'page': works_processed[1]}
        bookmark_results = {'data': self.build_bookmark_resultset(bookmarks_processed[0], self.bookmark_search.reserved_fields), 'page': bookmarks_processed[1]}
        collection_results = {'data': self.build_collection_resultset(collections_processed[0], self.collection_search.reserved_fields), 'page': collections_processed[1]}
        results = {}
        results['work'] = work_results
        results['bookmark'] = bookmark_results
        results['collection'] = collection_results
        results['tag'] = tag_results
        results['user'] = {'data': [], 'page': {}}
        return results

    def process_tag_tags(self, tags, tags_dict):
        for result in tags:
            if result['display_text'] not in tags_dict[result['tag_type']]['tags']:
                tags_dict[result['tag_type']]['tags'].append({'label': result['display_text'], 'checked': False})
        return tags_dict

    def process_chive_tags(self, tags, tags_dict):
        for result in tags:
            if len(result['tags']) > 0:
                tags_dict = self.process_tag_tags(result['tags'], tags_dict)
        return tags_dict

    def get_fe_filter_tag(self, tag, tags_dict):
        tag_objs = Tag.objects.filter(display_text__iexact=tag).all()
        if tag_objs:
            for tag_obj in tag_objs:
                tags_dict[tag_obj.tag_type.label]['tags'].append({'label': tag_obj.display_text, 'checked': True})
        return tags_dict

    def process_exclude_tags(self, tags_dict):
        for tag in self.work_search.filter.exclude_filters['tags']['tags__text__icontains']:
            tags_dict = self.get_fe_filter_tag(tag, tags_dict)
        for tag in self.bookmark_search.filter.exclude_filters['tags']['tags__text__icontains']:
            tags_dict = self.get_fe_filter_tag(tag, tags_dict)
        for tag in self.collection_search.filter.exclude_filters['tags']['tags__text__icontains']:
            tags_dict = self.get_fe_filter_tag(tag, tags_dict)
        return tags_dict

    def process_include_tags(self, tags_dict):
        for tag in self.work_search.filter.include_filters['tags']['tags__text__icontains']:
            tags_dict = self.get_fe_filter_tag(tag, tags_dict)
        for tag in self.bookmark_search.filter.include_filters['tags']['tags__text__icontains']:
            tags_dict = self.get_fe_filter_tag(tag, tags_dict)
        for tag in self.collection_search.filter.include_filters['tags']['tags__text__icontains']:
            tags_dict = self.get_fe_filter_tag(tag, tags_dict)
        return tags_dict

    def build_final_tag_facets(self, tag_id, tag_filter_name, tags_dict):
        result_json = []
        for key in tags_dict:
            if len(tags_dict[key]['tags']) > 0:
                tag_filter_vals = []
                vals = set()
                for val in tags_dict[key]['tags']:
                    label = val['label']
                    checked_tag = val['checked']
                    if not checked_tag:
                        # tag is checked if the user is browsing a specific tag
                        # but if it was set true because it's part of a frontend filter we don't even need to check this
                        checked_tag = True if (tag_id and tag_filter_name and tag_filter_name == label) else False
                    if label not in vals:
                        tag_filter_vals.append(FilterFacet(label, checked_tag))
                        vals.add(label)
                    else:
                        for tag_val in tag_filter_vals:
                            if tag_val.label == label:
                                tag_val.checked = checked_tag
                result_json.append(ResultFacet(tags_dict[key]['type_id'], key, tag_filter_vals, 'tag').to_dict())
        return result_json

    def get_tag_facets(self, tag_id, results, result_json):
        tag_filter_name = None
        if tag_id:
            tag_filter = Tag.objects.filter(id=tag_id).first()
            if tag_filter:
                tag_filter_name = tag_filter.display_text
        tags_dict = {}
        for tag_type in TagType.objects.all():
            tags_dict[tag_type.label] = {'tags': [], 'type_id': tag_type.id, 'type_label': tag_type.label}
        tags_dict = self.process_chive_tags(results['work']['data'], tags_dict)
        tags_dict = self.process_chive_tags(results['bookmark']['data'], tags_dict)
        tags_dict = self.process_chive_tags(results['collection']['data'], tags_dict)
        tags_dict = self.process_tag_tags(results['tag']['data'], tags_dict)
        exclude_tags_dict = self.process_exclude_tags(deepcopy(tags_dict))
        tags_dict = self.process_include_tags(tags_dict)
        include_json = self.build_final_tag_facets(tag_id, tag_filter_name, tags_dict)
        exclude_json = self.build_final_tag_facets(tag_id, tag_filter_name, exclude_tags_dict)
        return {'include_facets': include_json, 'exclude_facets': exclude_json}

    def get_fe_filter_attr(self, attr, attr_dict):
        attrs = AttributeValue.objects.filter(display_name__iexact=attr).all()
        for attr in attrs:
            type_name = attr.attribute_type.display_name
            display_name = attr.display_name
            if type_name not in attr_dict:
                attr_dict[type_name] = [{'label': display_name, 'checked': True}]
            else:
                label_found = False
                for attr_val in attr_dict[type_name]['attrs']:
                    if attr_val['label'] == display_name:
                        label_found = True
                        attr_val['checked'] = True
                        break
                if not label_found:
                    attr_dict[type_name]['attrs'].append({'label': display_name, 'checked': True})
        return attr_dict

    def process_exclude_attrs(self, attr_dict):
        for attr in self.work_search.filter.exclude_filters['attributes']['attributes__name__icontains']:
            attr_dict = self.get_fe_filter_attr(attr, attr_dict)
        for tag in self.bookmark_search.filter.exclude_filters['attributes']['attributes__name__icontains']:
            attr_dict = self.get_fe_filter_attr(attr, attr_dict)
        for attr in self.collection_search.filter.exclude_filters['attributes']['attributes__name__icontains']:
            attr_dict = self.get_fe_filter_attr(attr, attr_dict)
        return attr_dict

    def process_include_attrs(self, attr_dict):
        for attr in self.work_search.filter.include_filters['attributes']['attributes__name__icontains']:
            attr_dict = self.get_fe_filter_attr(attr, attr_dict)
        for attr in self.bookmark_search.filter.include_filters['attributes']['attributes__name__icontains']:
            attr_dict = self.get_fe_filter_attr(attr, attr_dict)
        for attr in self.collection_search.filter.include_filters['attributes']['attributes__name__icontains']:
            attr_dict = self.get_fe_filter_attr(attr, attr_dict)
        return attr_dict

    def process_chive_attributes(self, results, attributes_dict):
        for result in results:
            if len(result['attributes']) > 0:
                for attribute in result['attributes']:
                    if attribute['attribute_type'] not in attributes_dict:
                        attributes_dict[attribute['attribute_type']] = [{'label': attribute['display_name'], 'checked': False}]
                    else:
                        label_found = False
                        for attr_val in attributes_dict[attribute['attribute_type']]['attrs']:
                            if attr_val['label'] == attribute['display_name']:
                                label_found = True
                                break
                        if not label_found:
                            attributes_dict[attribute['attribute_type']]['attrs'].append({'label': attribute['display_name'], 'checked': False})
        return attributes_dict

    def build_final_attribute_facets(self, attr_dict):
        result_json = []
        for key in attr_dict:
            if len(attr_dict[key]['attrs']) > 0:
                attribute_filter_vals = []
                for val in attr_dict[key]['attrs']:
                    label = val['label']
                    checked_tag = val['checked']
                    attribute_filter_vals.append(FilterFacet(label, checked_tag))
                result_json.append(ResultFacet(attr_dict[key]['type_id'], key, attribute_filter_vals, 'attribute').to_dict())
        return result_json

    def get_attribute_facets(self, results):
        attributes_dict = {}
        for attribute_type in AttributeType.objects.all():
            attributes_dict[attribute_type.display_name] = {'attrs': [], 'type_id': attribute_type.id, 'type_label': attribute_type.display_name}
        attributes_dict = self.process_chive_attributes(results['work']['data'], attributes_dict)
        attributes_dict = self.process_chive_attributes(results['bookmark']['data'], attributes_dict)
        attributes_dict = self.process_chive_attributes(results['collection']['data'], attributes_dict)
        attributes_dict = self.process_include_attrs(attributes_dict)
        exclude_attrs_dict = self.process_exclude_attrs(deepcopy(attributes_dict))
        attributes_dict = self.build_final_attribute_facets(attributes_dict)
        exclude_attrs_dict = self.build_final_attribute_facets(exclude_attrs_dict)
        return {'include_facets': attributes_dict, 'exclude_facets': exclude_attrs_dict}

    def get_result_facets(self, results, tag_id=None):
        # todo: refactor - move attribute & tag processing to individual functions,
        # change facet dicts to pull from consts, use translation on labels,
        # move ranges to a dynamic number
        result_json = {'include_facets': [], 'exclude_facets': []}
        work_types = WorkType.objects.all()
        work_types_list = []
        for work_type in work_types:
            work_types_list.append(
                {"label": work_type.type_name})
        work_types_dict = {}
        work_types_dict["label"] = "Work Type"
        work_types_dict["values"] = work_types_list
        work_types_dict["object_type"] = 'work'
        result_json['include_facets'].append(work_types_dict)
        result_json['exclude_facets'].append(work_types_dict)

        # todo move to separate class
        word_count_dict = {}
        word_count_dict["label"] = "Work Word Count"
        word_count_dict["object_type"] = 'work'
        word_count_dict["filters"] = ["word_count_gte", "word_count_lte"]
        word_count_dict["values"] = [{"label": "From", "filter_val": "word_count_gte", "type": "text_range"},
                                     {"label": "To","filter_val": "word_count_lte", "type": "text_range"}]
        result_json['include_facets'].append(word_count_dict)
        result_json['exclude_facets'].append(word_count_dict)

        # todo move to db setting
        audio_length_dict = {}
        audio_length_dict["label"] = "Audio Length"
        audio_length_dict["values"] = [{"label": "Under 30:00", "filter_val": "audio_length_range|ranges|0|30"},
                                       {"label": "30:00 - 1:00:00",
                                           "filter_val": "audio_length_range|ranges|30|60"},
                                       {"label": "1:00:00 - 2:00:00",
                                           "filter_val": "audio_length_range|ranges|60|120"},
                                       {"label": "2:00:00 - 3:00:00",
                                        "filter_val": "audio_length_range|ranges|120|180"},
                                       {"label": "3:00:00+", "filter_val": "audio_length_range|ranges|20000|180"}]
        result_json['include_facets'].append(audio_length_dict)
        result_json['exclude_facets'].append(audio_length_dict)

        # todo move to db setting
        complete_dict = {}
        complete_dict["label"] = "Completion Status"
        complete_dict["object_type"] = 'work'
        complete_dict["values"] = [{"label": "Complete", "filter_val": "1"},
                                   {"label": "Work In Progress", "filter_val": "0"}]
        result_json['include_facets'].append(complete_dict)
        result_json['exclude_facets'].append(complete_dict)

        tag_facets = self.get_tag_facets(tag_id, results, result_json)
        result_json['include_facets'] = result_json['include_facets'] + tag_facets['include_facets']
        result_json['exclude_facets'] = result_json['exclude_facets'] + tag_facets['exclude_facets']
        attr_facets = self.get_attribute_facets(results)
        result_json['include_facets'] = result_json['include_facets'] + attr_facets['include_facets']
        result_json['exclude_facets'] = result_json['exclude_facets'] + attr_facets['exclude_facets']

        stars = OurchiveSetting.objects.get(name='Rating Star Count')
        bookmark_rating_dict = {}
        bookmark_rating_dict["label"] = "Rating"
        bookmark_rating_dict["values"] = []
        stars = get_star_count(stars)
        for star in stars:
            bookmark_rating_dict["values"].append(
                {"label": f"{star}", "filter_val": f"rating_gte${star}"})
        result_json['include_facets'].append(bookmark_rating_dict)
        result_json['exclude_facets'].append(bookmark_rating_dict)

        return result_json


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

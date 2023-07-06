class WorkFilter(object):
    def __init__(self):
        self.include_filters = {
            'audio_length_range': {
                'ranges': [],
                'greater_than': 'chapters__audio_length__gte',
                'less_than': 'chapters__audio_length__lte',
            },
            'image_formats': {
                'chapters__image_format__icontains': [],
            },
            'complete': {
                'is_complete__exact': [],
            },
            'tags': {
                'tags__text__icontains': [],
            },
            'word_count': {
                'word_count__gte': [],
                'word_count__lte': [],
            },
            'word_count_range': {
                'ranges': [],
                'greater_than': 'word_count__gte',
                'less_than': 'word_count__lte'
            },
            'type': {
                'work_type__type_name__icontains': []
            }
        }
        self.exclude_filters = {
            'audio_length_range': {
                'ranges': [],
                'greater_than': 'chapters__audio_length__gte',
                'less_than': 'chapters__audio_length__lte',
            },
            'image_formats': {
                'chapters__image_format__icontains': [],
            },
            'complete': {
                'is_complete__exact': [],
            },
            'tags': {
                'tags__text__icontains': [],
            },
            'word_count': {
                'word_count__gte': [],
                'word_count__lte': [],
            },
            'word_count_range': {
                'ranges': [],
                'greater_than': 'word_count__gte',
                'less_than': 'word_count__lte'
            },
            'type': {
                'work_type__type_name__icontains': []
            }
        }

    def from_dict(self, dict_obj, include=True):
        if include:
            self.include_filters['complete']['is_complete__exact'] = dict_obj.get('complete', [])
            self.include_filters['image_formats']['chapters__image_format__icontains'] = dict_obj.get('image_formats', [])
            self.include_filters['tags']['tags__text__icontains'] = dict_obj.get('tags', [])
            for range_tuple in dict_obj.get('audio_length_range', []):
                self.include_filters['audio_length_range']['ranges'].append(range_tuple)
            self.include_filters['word_count']['word_count__lte'] = dict_obj.get('word_count_lte', [])
            self.include_filters['word_count']['word_count__gte'] = dict_obj.get('word_count_gte', [])
            self.include_filters['type']['work_type__type_name__exact'] = dict_obj.get('work_type', [])
            for range_tuple in dict_obj.get('word_count_range', []):
                self.include_filters['word_count_range']['ranges'].append(range_tuple)
        else:
            self.exclude_filters['complete']['is_complete__exact'] = dict_obj.get('complete', [])
            self.exclude_filters['image_formats']['chapters__image_format__icontains'] = dict_obj.get('image_formats', [])
            self.exclude_filters['tags']['tags__text__icontains'] = dict_obj.get('tags', [])
            for range_tuple in dict_obj.get('audio_length_range', []):
                self.exclude_filters['audio_length_range']['ranges'].append(range_tuple)
            self.exclude_filters['word_count']['word_count__lte'] = dict_obj.get('word_count_lte', [])
            self.exclude_filters['word_count']['word_count__gte'] = dict_obj.get('word_count_gte', [])
            self.exclude_filters['type']['work_type__type_name__exact'] = dict_obj.get('work_type', [])
            for range_tuple in dict_obj.get('word_count_range', []):
                self.exclude_filters['word_count_range']['ranges'].append(range_tuple)

    def to_dict(self):
        self_dict = self.__dict__
        return self_dict


class BookmarkFilter(object):
    def __init__(self):
        self.include_filters = {
            'rating': {
                'rating__gte': [],
            },
            'complete': {
                'is_complete__exact': [],
            },
            'tags': {
                'tags__text__icontains': [],
            }
        }
        self.exclude_filters = {
            'rating': {
                'rating__gte': [],
            },
            'complete': {
                'is_complete__exact': [],
            },
            'tags': {
                'tags__text__icontains': [],
            }
        }

    def from_dict(self, dict_obj, include=True):
        if include:
            self.include_filters['complete']['is_complete__exact'] = dict_obj.get('complete', [])
            self.include_filters['rating']['rating__exact'] = dict_obj.get('rating_gte', [])
            self.include_filters['tags']['is_complete__exact'] = dict_obj.get('tags', [])
        else:
            self.exclude_filters['complete']['is_complete__exact'] = dict_obj.get('complete', [])
            self.exclude_filters['rating']['rating__exact'] = dict_obj.get('rating_gte', [])
            self.exclude_filters['tags']['is_complete__exact'] = dict_obj.get('tags', [])

    def to_dict(self):
        self_dict = self.__dict__
        return self_dict


class TagFilter(object):
    def __init__(self):
        self.include_filters = {
            'tag_type': {
                'tag_type__label__exact': [],
            },
            'text': {
                'text__icontains': [],
            }
        }
        self.exclude_filters = {
            'tag_type': {
                'tag_type__label__exact': [],
            },
            'text': {
                'text__icontains': [],
            }
        }

    def from_dict(self, dict_obj, include=True):
        if include:
            self.include_filters['tag_type']['tag_type__label__exact'] = dict_obj.get('tag_type', [])
            self.include_filters['text']['text__icontains'] = dict_obj.get('text', [])
        else:
            self.exclude_filters['tag_type']['tag_type__label__exact'] = dict_obj.get('tag_type', [])
            self.exclude_filters['text']['text__icontains'] = dict_obj.get('text', [])

    def to_dict(self):
        self_dict = self.__dict__
        return self_dict


class CollectionFilter(object):
    def __init__(self):
        self.include_filters = {
            'attributes': {
                'attributes__name__icontains': [],
            },
            'complete': {
                'is_complete__exact': [],
            },
            'tags': {
                'tags__text__icontains': [],
            }
        }
        self.exclude_filters = {
            'attributes': {
                'attributes__name__icontains': [],
            },
            'complete': {
                'is_complete__exact': [],
            },
            'tags': {
                'tags__text__icontains': [],
            }
        }

    def from_dict(self, dict_obj, include=True):
        if include:
            self.include_filters['complete']['is_complete__exact'] = dict_obj.get('complete', [])
            self.include_filters['tags']['tags__text__icontains'] = dict_obj.get('tags', [])
            self.include_filters['attributes']['attributes__name__icontains'] = dict_obj.get('attributes', [])
        else:
            self.exclude_filters['complete']['is_complete__exact'] = dict_obj.get('complete', [])
            self.exclude_filters['tags']['tags__text__icontains'] = dict_obj.get('tags', [])
            self.exclude_filters['attributes']['attributes__name__icontains'] = dict_obj.get('attributes', [])

    def to_dict(self):
        self_dict = self.__dict__
        return self_dict


class BookmarkSearch(object):
    def __init__(self):
        self.filter = BookmarkFilter()
        self.term = ""
        self.mode = ""
        self.order_by = ""
        self.reserved_fields = ['_state', 'uid', 'created_on', 'updated_on']
        self.term_search_fields = ['title', 'description']
        self.page = 1

    def from_dict(self, dict_obj):
        self.filter.from_dict(dict_obj['include_filter'])
        self.filter.from_dict(dict_obj['exclude_filter'], False)
        self.term = dict_obj['term']
        self.mode = dict_obj['mode'].lower() if 'mode' in dict_obj else 'all'
        self.order_by = dict_obj['order_by'].lower() if 'order_by' in dict_obj else ''

    def to_dict(self):
        self.filter = self.filter.to_dict()
        self_dict = self.__dict__
        self_dict.pop('reserved_fields')
        self_dict.pop('term_search_fields')
        return self_dict


class CollectionSearch(object):
    def __init__(self):
        self.filter = CollectionFilter()
        self.term = ""
        self.mode = ""
        self.order_by = ""
        self.reserved_fields = ['_state', 'uid', 'created_on', 'updated_on']
        self.term_search_fields = ['title', 'short_description']
        self.page = 1

    def from_dict(self, dict_obj):
        self.filter.from_dict(dict_obj['include_filter'])
        self.filter.from_dict(dict_obj['exclude_filter'], False)
        self.term = dict_obj['term']
        self.mode = dict_obj['mode'].lower() if 'mode' in dict_obj else 'all'
        self.order_by = dict_obj['order_by'].lower() if 'order_by' in dict_obj else ''

    def to_dict(self):
        self.filter = self.filter.to_dict()
        self_dict = self.__dict__
        self_dict.pop('reserved_fields')
        self_dict.pop('term_search_fields')
        return self_dict


class TagSearch(object):
    def __init__(self):
        self.filter = TagFilter()
        self.term = ""
        self.mode = ""
        self.order_by = ""
        self.reserved_fields = ['_state', 'uid', 'created_on', 'updated_on']
        self.term_search_fields = ['text']
        self.page = 1

    def from_dict(self, dict_obj):
        self.filter.from_dict(dict_obj['include_filter'])
        self.filter.from_dict(dict_obj['exclude_filter'], False)
        self.term = dict_obj['term']
        self.mode = dict_obj['mode'].lower() if 'mode' in dict_obj else 'all'
        self.order_by = dict_obj['order_by'].lower() if 'order_by' in dict_obj else ''

    def to_dict(self):
        self.filter = self.filter.to_dict()
        self_dict = self.__dict__
        self_dict.pop('reserved_fields')
        self_dict.pop('term_search_fields')
        return self_dict


class UserSearch(object):
    def __init__(self):
        self.filter = None
        self.term = ""
        self.order_by = ""
        self.reserved_fields = ['_state', 'uid', 'created_on', 'updated_on', 'password', 'is_superuser', 'first_name',
                                'last_name', 'is_staff', 'email', 'date_joined', 'last_login', 'is_active']
        self.term_search_fields = ['username']
        self.page = 1

    def from_dict(self, dict_obj):
        self.term = dict_obj['term']

    def to_dict(self):
        self.filter = self.filter
        self_dict = self.__dict__
        self_dict.pop('reserved_fields')
        self_dict.pop('term_search_fields')
        return self_dict


class WorkSearch(object):
    def __init__(self):
        self.filter = WorkFilter()
        self.term = ""
        self.mode = ""
        self.order_by = ""
        self.reserved_fields = ['_state', 'uid', 'created_on', 'updated_on']
        self.term_search_fields = ['title', 'summary',
                                   'chapters__title', 'chapters__summary']
        self.page = 1

    def from_dict(self, dict_obj):
        self.filter.from_dict(dict_obj['include_filter'])
        self.filter.from_dict(dict_obj['exclude_filter'], False)
        self.term = dict_obj['term']
        self.mode = dict_obj['mode'].lower() if 'mode' in dict_obj else 'all'
        self.order_by = dict_obj['order_by'].lower() if 'order_by' in dict_obj else ''

    def to_dict(self):
        self.filter = self.filter.to_dict()
        self_dict = self.__dict__
        self_dict.pop('reserved_fields')
        self_dict.pop('term_search_fields')
        return self_dict


class GlobalSearch(object):
    def __init__(self):
        self.work_search = WorkSearch().to_dict()
        self.bookmark_search = BookmarkSearch().to_dict()
        self.tag_search = TagSearch().to_dict()
        self.user_search = UserSearch().to_dict()
        self.collection_search = CollectionSearch().to_dict()

    def to_dict(self):
        return self.__dict__

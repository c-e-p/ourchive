import json

class WorkFilter(object):
	def __init__(self):
		self.complete = []
		self.image_formats = []
		self.tags = []
		self.audio_length = []

	def from_dict(self, dict_obj):
		self.complete = dict_obj['complete']
		self.image_formats = dict_obj['image_formats']
		self.tags = dict_obj['tags']
		self.audio_length = dict_obj['audio_length']


class BookmarkFilter(object):
	def __init__(self):
		self.complete = []
		self.ratings = []
		self.tags = []

class TagFilter(object):
	def __init__(self):
		self.tag_types = []


class BookmarkSearch(object):
	def __init__(self):
		self.filter = BookmarkFilter().__dict__
		self.term = ""

	def to_dict(self):
		return self.__dict__

class TagSearch(object):
	def __init__(self):
		self.filter = TagFilter().__dict__
		self.term = ""

	def to_dict(self):
		return self.__dict__

class UserSearch(object):
	def __init__(self):
		self.filter = None
		self.term = ""

	def to_dict(self):
		return self.__dict__

class WorkSearch(object):
	def __init__(self):
		self.filter = WorkFilter()
		self.term = ""
		self.reserved_fields = ['_state', 'uid', 'created_on', 'updated_on']
		
	def from_dict(self, dict_obj):
		self.filter.from_dict(dict_obj['filter'])
		self.term = dict_obj['term']

	def to_dict(self):
		self.filter = self.filter.__dict__
		return self.__dict__

class GlobalSearch(object):
	def __init__(self):
		self.work_search = WorkSearch().to_dict()
		self.bookmark_search = BookmarkSearch().__dict__
		self.tag_search = TagSearch().__dict__
		self.user_search = UserSearch().__dict__

	def to_dict(self):
		return self.__dict__
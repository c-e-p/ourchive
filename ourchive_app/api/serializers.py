from django.contrib.auth.models import User, Group
from rest_framework import serializers
from api.models import Work

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class WorkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Work
        fields = ('id', 'uid', 'title', 'work_summary', 'work_notes', 'is_complete', 'process_status', 'word_count',
        	'cover_url', 'cover_alt_text', 'epub_id', 'zip_id', 'created_on', 'updated_on', 'anon_comments_permitted',
        	'comments_permitted')
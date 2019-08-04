from django.contrib.auth.models import User, Group
from rest_framework import serializers
from api.models import Work, Tag

class UserSerializer(serializers.ModelSerializer):
    works = serializers.PrimaryKeyRelatedField(many=True, queryset=Work.objects.all())
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', 'groups', 'works']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class WorkSerializer(serializers.HyperlinkedModelSerializer):
    tags = TagSerializer(many=True, required=False)
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Work
        fields = ['id', 'user', 'uid', 'title', 'work_summary', 'work_notes', 'is_complete', 'process_status', 'word_count',
        	'cover_url', 'cover_alt_text', 'epub_id', 'zip_id', 'created_on', 'updated_on', 'anon_comments_permitted',
        	'comments_permitted', 'tags']
        
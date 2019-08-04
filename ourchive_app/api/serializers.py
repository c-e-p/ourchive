from django.contrib.auth.models import User, Group
from rest_framework import serializers
from api.models import Work, Tag, Chapter

class UserSerializer(serializers.HyperlinkedModelSerializer):
    work_set = serializers.HyperlinkedRelatedField(many=True, view_name='work-detail', read_only=True)
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', 'groups', 'work_set']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = '__all__'


class WorkSerializer(serializers.HyperlinkedModelSerializer):
    tags = TagSerializer(many=True, required=False)
    user = serializers.HyperlinkedRelatedField(view_name='user-detail', format='html', read_only=True)
    chapter_set = serializers.HyperlinkedRelatedField(many=True, view_name='chapter-detail', queryset=Chapter.objects.all())
    id = serializers.HyperlinkedIdentityField(view_name='work-detail', read_only=True)
    class Meta:
        model = Work
        fields = ['id', 'user', 'uid', 'title', 'work_summary', 'work_notes', 'is_complete', 'process_status', 'word_count',
        	'cover_url', 'cover_alt_text', 'epub_id', 'zip_id', 'created_on', 'updated_on', 'anon_comments_permitted',
        	'comments_permitted', 'tags', 'chapter_set']


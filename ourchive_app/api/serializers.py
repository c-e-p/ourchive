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

class ChapterSerializer(serializers.HyperlinkedModelSerializer):
    work = serializers.HyperlinkedRelatedField(view_name='work-detail', queryset=Work.objects.all())
    user = serializers.HyperlinkedRelatedField(view_name='user-detail', format='html', read_only=True)
    id = serializers.HyperlinkedIdentityField(view_name='chapter-detail', read_only=True)
    class Meta:
        model = Chapter
        fields = '__all__'


class WorkSerializer(serializers.HyperlinkedModelSerializer):
    tags = TagSerializer(many=True, required=False)
    user = serializers.HyperlinkedRelatedField(view_name='user-detail', format='html', read_only=True)
    chapters = serializers.HyperlinkedRelatedField(view_name='chapter-detail', format='html', read_only=True, many=True)
    id = serializers.HyperlinkedIdentityField(view_name='work-detail', read_only=True)
    class Meta:
        model = Work
        fields = '__all__'


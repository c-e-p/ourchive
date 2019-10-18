from django.contrib.auth.models import User, Group
from rest_framework import serializers
from api.models import Work, Tag, Chapter, TagType, WorkType

class UserSerializer(serializers.HyperlinkedModelSerializer):
    work_set = serializers.HyperlinkedRelatedField(many=True, view_name='work-detail', read_only=True)
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', 'groups', 'work_set']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class TagTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TagType
        fields = '__all__'

class WorkTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WorkType
        fields = '__all__'

class TagSerializer(serializers.HyperlinkedModelSerializer):
    tag_type = serializers.HyperlinkedRelatedField(view_name='tagtype-detail', queryset=TagType.objects.all())
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

    def update(self, work, validated_data):
        tags = validated_data.pop('tags')
        tag_id = tags[0]['text']
        tag_type = tags[0]['tag_type']
        tag, created = Tag.objects.get_or_create(text=tag_id, tag_type=tag_type)
        work.tags.add(tag)
        work.save()
        Work.objects.update(**validated_data)        
        return work

    def create(self, validated_data):
        tag = None
        if 'tags' in validated_data:
            tags = validated_data.pop('tags')
            tag_id = tags[0]['text']
            tag_type = tags[0]['tag_type']
            tag, created = Tag.objects.get_or_create(text=tag_id, tag_type=tag_type)
        work = Work.objects.create(**validated_data)
        if tag is not None:
            work.tags.add(tag)
        work.save()
        return work

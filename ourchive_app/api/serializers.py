from django.contrib.auth.models import User, Group
from rest_framework import serializers
from api.models import Work, Tag, Chapter, TagType, WorkType, Bookmark, Comment, Message, NotificationType, Notification, OurchiveSetting

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
    id = serializers.IntegerField()
    class Meta:
        model = WorkType
        fields = '__all__'

class TagSerializer(serializers.HyperlinkedModelSerializer):
    tag_type = serializers.HyperlinkedRelatedField(view_name='tagtype-detail', queryset=TagType.objects.all())
    class Meta:
        model = Tag
        fields = '__all__'

    def update(self, tag, validated_data):
        tag_type = TagType.objects.get(validated_data['tag_type'])
        if (tag_type.admin_administrated):
            user = serializers.CurrentUserDefault()
            if (user.is_superuser):
                tag = Tag.objects.create(**validated_data)
                return tag
            else:
                return None
        else:
            Tag.objects.update(**validated_data)        
            return tag 

    def create(self, validated_data):
        tag_type = TagType.objects.get(validated_data['tag_type'])
        if (tag_type.admin_administrated):
            user = serializers.CurrentUserDefault()
            if (user.is_superuser):
                tag = Tag.objects.create(**validated_data)
                return tag
            else:
                return None
        tag = Tag.objects.create(**validated_data)
        return tag

class NotificationTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NotificationType
        fields = '__all__'

class OurchiveSettingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OurchiveSetting
        fields = '__all__'

class NotificationSerializer(serializers.HyperlinkedModelSerializer):
    notification_type = serializers.HyperlinkedRelatedField(view_name='notificationtype-detail', queryset=NotificationType.objects.all())
    class Meta:
        model = Notification
        fields = '__all__'

class ReplySerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(view_name='user-detail', format='html', read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(view_name='user-detail', format='html', read_only=True)
    replies = ReplySerializer(many=True, required=False)
    class Meta:
        model = Comment
        fields = '__all__'

class MessageSerializer(serializers.HyperlinkedModelSerializer):
    to_user = serializers.HyperlinkedRelatedField(view_name='user-detail', format='html', read_only=False, queryset=User.objects.all())
    from_user = serializers.HyperlinkedRelatedField(view_name='user-detail', format='html', read_only=True)
    user = serializers.HyperlinkedRelatedField(view_name='user-detail', format='html', read_only=True)
    class Meta:
        model = Message
        fields = '__all__'

class ChapterSerializer(serializers.HyperlinkedModelSerializer):
    work = serializers.HyperlinkedRelatedField(view_name='work-detail', queryset=Work.objects.all())
    user = serializers.HyperlinkedRelatedField(view_name='user-detail', format='html', read_only=True)
    id = serializers.HyperlinkedIdentityField(view_name='chapter-detail', read_only=True)
    comments = CommentSerializer(many=True, required=False)
    word_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Chapter
        fields = '__all__'

    def update(self, chapter, validated_data):
        validated_data['word_count'] = 0 if not validated_data['text'] else len(validated_data['text'].split())
        chapter = Chapter.objects.filter(id=chapter.id)
        chapter.update(**validated_data)        
        return chapter.first()

    def create(self, validated_data):
        validated_data['word_count'] = 0 if not validated_data['text'] else len(validated_data['text'].split())
        chapter = Chapter.objects.create(**validated_data)
        return chapter


class WorkSerializer(serializers.HyperlinkedModelSerializer):
    tags = TagSerializer(many=True, required=True)
    user = serializers.HyperlinkedRelatedField(view_name='user-detail', format='html', read_only=True)
    chapters = ChapterSerializer(many=True, required=False, read_only=True)
    id = serializers.HyperlinkedIdentityField(view_name='work-detail', read_only=True)
    word_count = serializers.IntegerField(read_only=True)
    audio_length = serializers.IntegerField(read_only=True)
    class Meta:
        model = Work
        fields = '__all__'

    def process_tags(self, work, validated_data, tags):
        required_tag_types = list(TagType.objects.filter(required=True))
        has_any_required = len(required_tag_types) > 0
        for item in tags:
            tag_id = item['text']
            tag_type = item['tag_type']
            if tag_type in required_tag_types:
                if tag_id is None or tag_id == '':
                    # todo: error
                    return None
                else:
                    required_tag_types.pop()
            tag, created = Tag.objects.get_or_create(text=tag_id, tag_type=tag_type)
            work.tags.add(tag)
        if has_any_required and len(required_tag_types) > 0:
            #todo: error
            return None
        work.save()
        return work

    def update(self, work, validated_data):
        work = self.process_tags(work, validated_data, validated_data.pop('tags'))
        Work.objects.filter(id=work.id).update(**validated_data)        
        return Work.objects.filter(id=work.id).first()

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        work = Work.objects.create(**validated_data)
        work = self.process_tags(work, validated_data, tags)   
        return work

    

class BookmarkSerializer(serializers.HyperlinkedModelSerializer):
    work = serializers.HyperlinkedRelatedField(view_name='work-detail', queryset=Work.objects.all())
    user = serializers.HyperlinkedRelatedField(view_name='user-detail', format='html', read_only=True)
    id = serializers.HyperlinkedIdentityField(view_name='bookmark-detail', read_only=True)
    tags = TagSerializer(many=True, required=False)
    class Meta:
        model = Bookmark
        fields = '__all__'
    def update(self, bookmark, validated_data):
        if 'tags' in validated_data:
            tags = validated_data.pop('tags')
            for item in tags:
                tag_id = item['text']
                tag_type = item['tag_type']
                tag, created = Tag.objects.get_or_create(text=tag_id, tag_type=tag_type)
                bookmark.tags.add(tag)
            bookmark.save()
        Bookmark.objects.filter(id=bookmark.id).update(**validated_data)        
        return Bookmark.objects.filter(id=bookmark.id).first()

    def create(self, validated_data):
        bookmark = Bookmark.objects.create(**validated_data)
        if 'tags' in validated_data:
            tags = validated_data.pop('tags')
            for item in tags:
                tag_id = item['text']
                tag_type = item['tag_type']
                tag, created = Tag.objects.get_or_create(text=tag_id, tag_type=tag_type)
                bookmark.tags.add(tag)
        bookmark.save()
        return bookmark


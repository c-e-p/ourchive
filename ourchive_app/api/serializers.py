from django.contrib.auth.models import User, Group
from rest_framework import serializers
from api.models import Work, Tag, Chapter, TagType, WorkType, Bookmark, Comment, Message, NotificationType, Notification

class UserSerializer(serializers.HyperlinkedModelSerializer):
    work_set = serializers.HyperlinkedRelatedField(many=True, view_name='work-detail', read_only=True)
    messages = serializers.HyperlinkedRelatedField(many=True, view_name='message-detail', read_only=True)
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
    tag_type = serializers.HyperlinkedRelatedField(view_name='tagtype-detail', queryset=NotificationType.objects.all())
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
    parent_comment = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all())
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
    comments = CommentSerializer(many=True)
    class Meta:
        model = Chapter
        fields = '__all__'


class WorkSerializer(serializers.HyperlinkedModelSerializer):
    tags = TagSerializer(many=True, required=False)
    user = serializers.HyperlinkedRelatedField(view_name='user-detail', format='html', read_only=True)
    chapters = ChapterSerializer(many=True)
    id = serializers.HyperlinkedIdentityField(view_name='work-detail', read_only=True)
    class Meta:
        model = Work
        fields = '__all__'

    def update(self, work, validated_data):
        if 'tags' in validated_data:
            tags = validated_data.pop('tags')
            for item in tags:
                tag_id = item['text']
                tag_type = item['tag_type']
                tag, created = Tag.objects.get_or_create(text=tag_id, tag_type=tag_type)
                work.tags.add(tag)
            work.save()
        Work.objects.update(**validated_data)        
        return work

    def create(self, validated_data):
        work = Work.objects.create(**validated_data)
        if 'tags' in validated_data:
            tags = validated_data.pop('tags')
            for item in tags:
                tag_id = item['text']
                tag_type = item['tag_type']
                tag, created = Tag.objects.get_or_create(text=tag_id, tag_type=tag_type)
                work.tags.add(tag)
        work.save()
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
        Bookmark.objects.update(**validated_data)        
        return bookmark

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


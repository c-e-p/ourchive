from django.db import models
import datetime
import uuid
from django.contrib.auth.models import User


class Work(models.Model):

    __tablename__ = 'works'

    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    work_summary = models.TextField(null=True, blank=True)
    work_notes = models.TextField(null=True, blank=True)
    is_complete = models.BooleanField(default=False)
    process_status = models.IntegerField(null=True)
    word_count = models.IntegerField(default=0)
    cover_url = models.CharField(max_length=600, null=True, blank=True)
    cover_alt_text = models.CharField(max_length=600, null=True, blank=True)
    epub_id = models.CharField(max_length=600, null=True, blank=True)
    zip_id = models.CharField(max_length=600, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    anon_comments_permitted = models.BooleanField(default=True)
    comments_permitted = models.BooleanField(default=True)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    work_type = models.ForeignKey('WorkType', on_delete=models.CASCADE,null=True)

    tags = models.ManyToManyField('Tag')

    def __repr__(self):
        return '<Work: {}>'.format(self.id)

class WorkType(models.Model):

    __tablename__ = 'work_types'

    type_name = models.CharField(max_length=200)

    def __repr__(self):
        return '<WorkType: {}>'.format(self.id)

class Chapter(models.Model):

    __tablename__ = 'chapters'

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=200)
    number = models.IntegerField(default=1)
    text = models.TextField(null=True)
    audio_url = models.CharField(max_length=600, null=True)
    audio_length = models.BigIntegerField(null=True)
    image_url = models.CharField(max_length=600, null=True)
    image_alt_text = models.CharField(max_length=600, null=True)
    image_format = models.CharField(max_length=100, null=True)
    image_size = models.CharField(max_length=100, null=True)
    summary = models.TextField(null=True)

    work = models.ForeignKey(
        'work',
        on_delete=models.CASCADE,
         related_name='chapters'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    def __repr__(self):
        return '<Chapter: {}>'.format(self.id)

class Comment(models.Model):

    __tablename__ = 'comments'

    text = models.TextField()

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    chapter = models.ForeignKey(
        'Chapter',
        on_delete=models.CASCADE,
        null=True,
    )

    bookmark = models.ForeignKey(
        'Bookmark',
        on_delete=models.CASCADE,
        null=True,
    )


    comments = models.ManyToManyField('self')

    def __repr__(self):
        return '<Comment: {}>'.format(self.id)

class Tag(models.Model):

    __tablename__ = 'tags'

    text = models.CharField(max_length=120)
    
    tag_type = models.ForeignKey(
        'TagType',
        on_delete=models.CASCADE,
    )

    def __repr__(self):
        return '<Tag: {}>'.format(self.id)

class TagType(models.Model):

    __tablename__ = 'tag_types'

    label = models.CharField(max_length=200)

    def __repr__(self):
        return '<TagType: {}>'.format(self.id)

class Bookmark(models.Model):

    __tablename__ = 'bookmarks'

    curator_title = models.CharField(max_length=200)
    rating = models.IntegerField()
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    anon_comments_permitted = models.BooleanField(default=False)
    comments_permitted = models.BooleanField(default=False)
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    is_private = models.BooleanField(default=False)

    work = models.ForeignKey(
        'Work',
        on_delete=models.CASCADE,
    )

    tags = models.ManyToManyField('Tag')


def __repr__(self):
    return '<Bookmark: {}>'.format(self.id)

class BookmarkLink(models.Model):

    __tablename__ = 'bookmark_links'

    link = models.CharField(max_length=200)
    text = models.CharField(max_length=200)


    bookmark = models.ForeignKey(
        'Bookmark',
        on_delete=models.CASCADE,
    )


    def __repr__(self):
        return '<BookmarkLink: {}>'.format(self.id)


class Message(models.Model):

    __tablename__ = 'messages'

    message_subject = models.CharField(max_length=200)
    message_content = models.TextField()
    message_read = models.BooleanField(default=False)

    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='messages_recieved',
    )

    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='messages_sent',
    )

    replies = models.ManyToManyField('self')

    def __repr__(self):
    	return '<Message: {}>'.format(self.id)

class Notification(models.Model):

    __tablename__ = 'notifications'

    content = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)
    route = models.CharField(max_length=200)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    notification_type = models.ForeignKey(
        'NotificationType',
        on_delete=models.CASCADE,
    )

class NotificationType(models.Model):
    __tablename__ = 'notification_types'

    type_label = models.CharField(max_length=200)
    send_email = models.BooleanField(default=False)

    def __init__(self, type_label, send_email):
        self.type_label = type_label
        self.send_email = send_email



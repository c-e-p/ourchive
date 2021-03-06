from django.db import models
import datetime
import uuid
from django.contrib.auth.models import User


class Work(models.Model):

    __tablename__ = 'works'

    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    summary = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    is_complete = models.BooleanField(default=False)
    process_status = models.IntegerField(null=True)
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

    def __str__(self):
        return self.title

class WorkType(models.Model):

    __tablename__ = 'work_types'

    type_name = models.CharField(max_length=200)

    def __repr__(self):
        return '<WorkType: {}>'.format(self.id)

    def __str__(self):
        return self.type_name

class Chapter(models.Model):

    __tablename__ = 'chapters'

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    number = models.IntegerField(default=1)
    text = models.TextField(null=True)
    notes = models.TextField(null=True, blank=True)
    word_count = models.IntegerField(default=0)
    audio_url = models.CharField(max_length=600, null=True, blank=True)
    audio_description = models.CharField(max_length=600, null=True, blank=True)
    audio_length = models.BigIntegerField(null=True, blank=True)
    image_url = models.CharField(max_length=600, null=True, blank=True)
    image_alt_text = models.CharField(max_length=600, null=True, blank=True)
    image_format = models.CharField(max_length=100, null=True, blank=True)
    image_size = models.CharField(max_length=100, null=True, blank=True)
    summary = models.TextField(null=True, blank=True)

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

    def __str__(self):
        return self.title
    class Meta:
        ordering = ['number']

class Comment(models.Model):

    __tablename__ = 'comments'

    text = models.TextField()

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    parent_comment = models.ForeignKey(
        'Comment',
        on_delete=models.CASCADE,
         related_name='replies',
         null=True,
         blank=True
    )

    chapter = models.ForeignKey(
        'Chapter',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='comments'
    )

    bookmark = models.ForeignKey(
        'Bookmark',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

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
    def __str__(self):
        return self.text

class TagType(models.Model):

    __tablename__ = 'tag_types'

    label = models.CharField(max_length=200)
    admin_administrated = models.BooleanField(default=False)
    required = models.BooleanField(default=False)

    def __repr__(self):
        return '<TagType: {}>'.format(self.id)

    def __str__(self):
        return self.label

class BookmarkCollection(models.Model):

    __tablename__ = 'bookmark_collection'

    title = models.CharField(max_length=200)
    is_complete = models.BooleanField(default=False)
    cover_url = models.CharField(max_length=600, null=True, blank=True)
    cover_alt_text = models.CharField(max_length=600, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    anon_comments_permitted = models.BooleanField(default=False)
    comments_permitted = models.BooleanField(default=False)
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    is_private = models.BooleanField(default=False)

    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title


    def __repr__(self):
        return '<BookmarkCollection: {}>'.format(self.id)

class Bookmark(models.Model):

    __tablename__ = 'bookmarks'

    title = models.CharField(max_length=200)
    rating = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    collection = models.ForeignKey(BookmarkCollection, on_delete=models.CASCADE, null=True, blank=True)
    
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

    def __str__(self):
        return self.title


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

    subject = models.CharField(max_length=200)
    content = models.TextField()
    read = models.BooleanField(default=False)

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

    def __str__(self):
        return self.subject

class Notification(models.Model):

    __tablename__ = 'notifications'

    content = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)

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

    def __repr__(self):
        return '<NotificationType: {}>'.format(self.id)

    def __str__(self):
        return self.type_label


class OurchiveSetting(models.Model):

    __tablename__ = 'ourchive_settings'

    
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=200)
    grouping = models.CharField(max_length=200)

    def __repr__(self):
        return '<OurchiveSettings: {}>'.format(self.id)

    def __str__(self):
        return self.name

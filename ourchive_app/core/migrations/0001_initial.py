# Generated by Django 5.0.2 on 2024-06-18 18:49

import django.contrib.auth.models
import django.db.models.deletion
import django.db.models.functions.text
import django.utils.timezone
import django_registration.validators
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminAnnouncement',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(default='', max_length=200)),
                ('content', models.TextField(blank=True, default='')),
                ('expires_on', models.DateTimeField(blank=True, null=True)),
                ('active', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('active', 'expires_on'),
            },
        ),
        migrations.CreateModel(
            name='AttributeValue',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('name', models.CharField(max_length=200)),
                ('display_name', models.CharField(max_length=200)),
                ('order', models.IntegerField(default=1)),
            ],
            options={
                'ordering': ('attribute_type__name', 'order', 'name'),
            },
        ),
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('title', models.CharField(blank=True, default='', max_length=200)),
                ('rating', models.IntegerField()),
                ('description', models.TextField(blank=True, null=True)),
                ('created_on', models.DateTimeField(blank=True, null=True)),
                ('updated_on', models.DateTimeField(blank=True, null=True)),
                ('system_created_on', models.DateTimeField(auto_now_add=True)),
                ('system_updated_on', models.DateTimeField(auto_now=True)),
                ('draft', models.BooleanField(default=False)),
                ('anon_comments_permitted', models.BooleanField(default=True)),
                ('comments_permitted', models.BooleanField(default=True)),
                ('comment_count', models.IntegerField(default=0)),
                ('public_notes', models.TextField(blank=True, null=True)),
                ('private_notes', models.TextField(blank=True, null=True)),
                ('is_private', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='BookmarkAttribute',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='BookmarkCollection',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('title', models.CharField(max_length=200)),
                ('is_complete', models.BooleanField(default=False)),
                ('header_url', models.CharField(blank=True, max_length=600, null=True)),
                ('header_alt_text', models.CharField(blank=True, max_length=600, null=True)),
                ('short_description', models.CharField(blank=True, max_length=300, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_on', models.DateTimeField(blank=True, null=True)),
                ('updated_on', models.DateTimeField(blank=True, null=True)),
                ('system_created_on', models.DateTimeField(auto_now_add=True)),
                ('system_updated_on', models.DateTimeField(auto_now=True)),
                ('draft', models.BooleanField(default=False)),
                ('anon_comments_permitted', models.BooleanField(default=True)),
                ('comments_permitted', models.BooleanField(default=True)),
                ('comment_count', models.IntegerField(default=0)),
                ('is_private', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('text', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='BookmarkLink',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('link', models.CharField(max_length=200)),
                ('text', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('created_on', models.DateTimeField(blank=True, null=True)),
                ('updated_on', models.DateTimeField(blank=True, null=True)),
                ('system_created_on', models.DateTimeField(auto_now_add=True)),
                ('system_updated_on', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('number', models.IntegerField(default=1)),
                ('text', models.TextField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('end_notes', models.TextField(blank=True, null=True)),
                ('word_count', models.IntegerField(default=0)),
                ('audio_url', models.CharField(blank=True, max_length=600, null=True)),
                ('audio_description', models.CharField(blank=True, max_length=600, null=True)),
                ('audio_length', models.BigIntegerField(blank=True, default=0, null=True)),
                ('video_url', models.CharField(blank=True, max_length=600, null=True)),
                ('video_description', models.CharField(blank=True, max_length=600, null=True)),
                ('video_length', models.BigIntegerField(blank=True, default=0, null=True)),
                ('image_url', models.CharField(blank=True, max_length=600, null=True)),
                ('image_alt_text', models.CharField(blank=True, max_length=600, null=True)),
                ('image_format', models.CharField(blank=True, max_length=100, null=True)),
                ('image_size', models.CharField(blank=True, max_length=100, null=True)),
                ('summary', models.TextField(blank=True, null=True)),
                ('draft', models.BooleanField(default=True)),
                ('comment_count', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['number'],
            },
        ),
        migrations.CreateModel(
            name='ChapterAttribute',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'ordering': ['attribute_value'],
            },
        ),
        migrations.CreateModel(
            name='ContentPage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('name', models.CharField(max_length=200)),
                ('value', models.TextField(blank=True, null=True)),
                ('order', models.IntegerField(default=1)),
                ('locked_to_users', models.BooleanField(default=False)),
                ('agree_on_signup', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('order', 'id'),
            },
        ),
        migrations.CreateModel(
            name='Fingergun',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('email', models.CharField(max_length=200)),
                ('invite_token', models.CharField(max_length=200)),
                ('token_expiration', models.DateTimeField(blank=True, null=True)),
                ('token_used', models.BooleanField(default=False)),
                ('register_link', models.CharField(max_length=200)),
                ('approved', models.BooleanField(default=False)),
                ('allow_upload', models.BooleanField(default=False)),
                ('join_reason', models.TextField(blank=True, max_length=400, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('subject', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('read', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(default='', max_length=200)),
                ('content', models.TextField(blank=True, default='')),
                ('read', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('read',),
            },
        ),
        migrations.CreateModel(
            name='NotificationType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('type_label', models.CharField(max_length=200)),
                ('send_email', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='OurchiveSetting',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('name', models.CharField(max_length=200)),
                ('value', models.CharField(max_length=200)),
                ('valtype', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('text', models.CharField(db_index=True, max_length=120)),
                ('display_text', models.CharField(default='', max_length=120)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('filterable', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('tag_type__sort_order', 'tag_type__label'),
            },
        ),
        migrations.CreateModel(
            name='TagType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=200)),
                ('type_name', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('admin_administrated', models.BooleanField(default=False)),
                ('required', models.BooleanField(default=False)),
                ('sort_order', models.IntegerField(default=1)),
                ('filterable', models.BooleanField(default=True)),
                ('show_in_aggregate', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('sort_order', 'label'),
            },
        ),
        migrations.CreateModel(
            name='UserAttribute',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'ordering': ['attribute_value'],
            },
        ),
        migrations.CreateModel(
            name='UserBlocks',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserCollection',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('approved', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'core_user_collections',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='UserReport',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('details', models.TextField(blank=True, null=True)),
                ('mod_notes', models.TextField(blank=True, null=True)),
                ('resolved', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['resolved', '-updated_on'],
            },
        ),
        migrations.CreateModel(
            name='UserReportReason',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('reason', models.CharField(max_length=200)),
            ],
            options={
                'ordering': ['reason'],
            },
        ),
        migrations.CreateModel(
            name='UserSubscription',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('subscribed_to_bookmark', models.BooleanField(default=False)),
                ('subscribed_to_collection', models.BooleanField(default=False)),
                ('subscribed_to_work', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-updated_on'],
            },
        ),
        migrations.CreateModel(
            name='UserWork',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('approved', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'core_user_works',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('title', models.CharField(max_length=200)),
                ('summary', models.TextField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('is_complete', models.BooleanField(default=False)),
                ('process_status', models.IntegerField(null=True)),
                ('cover_url', models.CharField(blank=True, max_length=600, null=True)),
                ('cover_alt_text', models.CharField(blank=True, max_length=600, null=True)),
                ('preferred_download_url', models.CharField(blank=True, max_length=600, null=True)),
                ('created_on', models.DateTimeField(blank=True, null=True)),
                ('updated_on', models.DateTimeField(blank=True, null=True)),
                ('system_created_on', models.DateTimeField(auto_now_add=True)),
                ('system_updated_on', models.DateTimeField(auto_now=True)),
                ('anon_comments_permitted', models.BooleanField(default=True)),
                ('comments_permitted', models.BooleanField(default=True)),
                ('word_count', models.IntegerField(default=0)),
                ('audio_length', models.IntegerField(default=0)),
                ('fingerguns', models.IntegerField(default=0)),
                ('draft', models.BooleanField(default=True)),
                ('comment_count', models.IntegerField(default=0)),
                ('preferred_download', models.CharField(blank=True, choices=[('EPUB', 'EPUB'), ('M4B', 'M4B'), ('ZIP', 'ZIP'), ('M4A', 'M4A'), ('MOBI', 'MOBI')], max_length=200, null=True)),
                ('epub_url', models.CharField(blank=True, max_length=600, null=True)),
                ('m4b_url', models.CharField(blank=True, max_length=600, null=True)),
                ('zip_url', models.CharField(blank=True, max_length=600, null=True)),
                ('external_id', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WorkAttribute',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='WorkType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('type_name', models.CharField(max_length=200)),
                ('sort_order', models.IntegerField(default=1)),
            ],
            options={
                'ordering': ['sort_order'],
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=150, unique=True, validators=[django_registration.validators.ReservedNameValidator()], verbose_name='Username')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('profile', models.TextField(blank=True, null=True)),
                ('icon', models.CharField(blank=True, max_length=600, null=True)),
                ('icon_alt_text', models.CharField(blank=True, max_length=600, null=True)),
                ('has_notifications', models.BooleanField(default=False)),
                ('default_content', models.TextField(blank=True, null=True)),
                ('can_upload_audio', models.BooleanField(default=False)),
                ('can_upload_images', models.BooleanField(default=False)),
                ('can_upload_export_files', models.BooleanField(default=False)),
                ('can_upload_video', models.BooleanField(default=False)),
                ('default_post_language', models.CharField(blank=True, max_length=10, null=True)),
                ('default_search_language', models.CharField(blank=True, max_length=10, null=True)),
                ('default_editor', models.CharField(blank=True, max_length=10, null=True)),
                ('display_username', models.CharField(blank=True, max_length=150, null=True)),
                ('cookies_accepted', models.BooleanField(default=False)),
                ('collapse_chapter_text', models.BooleanField(default=False)),
                ('collapse_chapter_audio', models.BooleanField(default=False)),
                ('collapse_chapter_image', models.BooleanField(default=False)),
                ('collapse_chapter_video', models.BooleanField(default=False)),
                ('copy_work_metadata', models.BooleanField(default=False)),
                ('chive_export_url', models.CharField(blank=True, max_length=200, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AttributeType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('name', models.CharField(max_length=200)),
                ('display_name', models.CharField(max_length=200)),
                ('allow_on_work', models.BooleanField(default=False)),
                ('allow_on_bookmark', models.BooleanField(default=False)),
                ('allow_on_chapter', models.BooleanField(default=False)),
                ('allow_on_user', models.BooleanField(default=False)),
                ('allow_multiselect', models.BooleanField(default=True)),
                ('allow_on_bookmark_collection', models.BooleanField(default=False)),
                ('sort_order', models.IntegerField(default=1)),
            ],
            options={
                'ordering': ['sort_order', 'name'],
                'indexes': [models.Index(fields=['name'], name='core_attribu_name_8fc968_idx')],
            },
        ),
        migrations.AddConstraint(
            model_name='attributetype',
            constraint=models.UniqueConstraint(models.OrderBy(django.db.models.functions.text.Lower('name'), descending=True), name='unique_attributetype_name'),
        ),
        migrations.AddField(
            model_name='attributevalue',
            name='attribute_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attribute_values', to='core.attributetype'),
        ),
        migrations.AddField(
            model_name='user',
            name='attributes',
            field=models.ManyToManyField(blank=True, to='core.attributevalue'),
        ),
        migrations.AddField(
            model_name='bookmark',
            name='attributes',
            field=models.ManyToManyField(to='core.attributevalue'),
        ),
        migrations.AddField(
            model_name='bookmark',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bookmarkattribute',
            name='attribute_value',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.attributevalue'),
        ),
        migrations.AddField(
            model_name='bookmarkattribute',
            name='bookmark',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.bookmark'),
        ),
        migrations.AddField(
            model_name='bookmarkcollection',
            name='attributes',
            field=models.ManyToManyField(to='core.attributevalue'),
        ),
        migrations.AddField(
            model_name='bookmarkcollection',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bookmark',
            name='collection',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bookmarks', to='core.bookmarkcollection'),
        ),
        migrations.CreateModel(
            name='BookmarkComment',
            fields=[
                ('comment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.comment')),
            ],
            bases=('core.comment',),
        ),
        migrations.CreateModel(
            name='ChapterComment',
            fields=[
                ('comment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.comment')),
            ],
            bases=('core.comment',),
        ),
        migrations.CreateModel(
            name='CollectionComment',
            fields=[
                ('comment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.comment')),
            ],
            bases=('core.comment',),
        ),
        migrations.AddField(
            model_name='comment',
            name='parent_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='replies', to='core.comment'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bookmarklink',
            name='bookmark',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.bookmark'),
        ),
        migrations.AddField(
            model_name='chapter',
            name='attributes',
            field=models.ManyToManyField(to='core.attributevalue'),
        ),
        migrations.AddField(
            model_name='chapter',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chapterattribute',
            name='attribute_value',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.attributevalue'),
        ),
        migrations.AddField(
            model_name='chapterattribute',
            name='chapter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.chapter'),
        ),
        migrations.AddField(
            model_name='fingergun',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='message',
            name='from_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages_sent', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='message',
            name='replies',
            field=models.ManyToManyField(to='core.message'),
        ),
        migrations.AddField(
            model_name='message',
            name='to_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages_recieved', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='notification',
            name='notification_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.notificationtype'),
        ),
        migrations.AddField(
            model_name='bookmarkcollection',
            name='tags',
            field=models.ManyToManyField(to='core.tag'),
        ),
        migrations.AddField(
            model_name='bookmark',
            name='tags',
            field=models.ManyToManyField(to='core.tag'),
        ),
        migrations.AddIndex(
            model_name='tagtype',
            index=models.Index(fields=['type_name'], name='core_tagtype_type_na_56cb9e_idx'),
        ),
        migrations.AddField(
            model_name='tag',
            name='tag_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.tagtype'),
        ),
        migrations.AddField(
            model_name='userattribute',
            name='attribute_value',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.attributevalue'),
        ),
        migrations.AddField(
            model_name='userattribute',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userblocks',
            name='blocked_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocked_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userblocks',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='usercollection',
            name='collection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.bookmarkcollection'),
        ),
        migrations.AddField(
            model_name='usercollection',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='collections',
            field=models.ManyToManyField(related_name='users', through='core.UserCollection', to='core.bookmarkcollection'),
        ),
        migrations.AddField(
            model_name='userreport',
            name='reported_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reported_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userreport',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='userreportreason',
            constraint=models.UniqueConstraint(fields=('reason',), name='unique reportreason'),
        ),
        migrations.AddField(
            model_name='userreport',
            name='reason',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.userreportreason'),
        ),
        migrations.AddField(
            model_name='usersubscription',
            name='subscribed_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribed_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='usersubscription',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userwork',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='work',
            name='attributes',
            field=models.ManyToManyField(to='core.attributevalue'),
        ),
        migrations.AddField(
            model_name='work',
            name='tags',
            field=models.ManyToManyField(to='core.tag'),
        ),
        migrations.AddField(
            model_name='work',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userwork',
            name='work',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.work'),
        ),
        migrations.AddField(
            model_name='fingergun',
            name='work',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.work'),
        ),
        migrations.AddField(
            model_name='chapter',
            name='work',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chapters', to='core.work'),
        ),
        migrations.AddField(
            model_name='bookmarkcollection',
            name='works',
            field=models.ManyToManyField(to='core.work'),
        ),
        migrations.AddField(
            model_name='bookmark',
            name='work',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.work'),
        ),
        migrations.AddField(
            model_name='user',
            name='works',
            field=models.ManyToManyField(related_name='users', through='core.UserWork', to='core.work'),
        ),
        migrations.AddField(
            model_name='workattribute',
            name='attribute_value',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.attributevalue'),
        ),
        migrations.AddField(
            model_name='workattribute',
            name='work',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.work'),
        ),
        migrations.AddField(
            model_name='work',
            name='work_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.worktype'),
        ),
        migrations.AddField(
            model_name='user',
            name='default_work_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.worktype'),
        ),
        migrations.AddIndex(
            model_name='attributevalue',
            index=models.Index(fields=['name'], name='core_attribu_name_0a819d_idx'),
        ),
        migrations.AddConstraint(
            model_name='attributevalue',
            constraint=models.UniqueConstraint(models.OrderBy(django.db.models.functions.text.Lower('name'), descending=True), name='unique_attributevalue_name'),
        ),
        migrations.AddField(
            model_name='bookmarkcomment',
            name='bookmark',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='core.bookmark'),
        ),
        migrations.AddField(
            model_name='chaptercomment',
            name='chapter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='core.chapter'),
        ),
        migrations.AddField(
            model_name='collectioncomment',
            name='collection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='core.bookmarkcollection'),
        ),
        migrations.AddIndex(
            model_name='tag',
            index=models.Index(fields=['text'], name='core_tag_text_e39765_idx'),
        ),
        migrations.AddConstraint(
            model_name='tag',
            constraint=models.UniqueConstraint(models.OrderBy(django.db.models.functions.text.Lower('text'), descending=True), models.F('tag_type_id'), name='unique_text_and_type'),
        ),
    ]

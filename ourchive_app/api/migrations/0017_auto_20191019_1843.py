# Generated by Django 2.2.6 on 2019-10-19 18:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_ourchivesetting'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookmark',
            old_name='curator_title',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='message_content',
            new_name='content',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='message_read',
            new_name='read',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='message_subject',
            new_name='subject',
        ),
    ]

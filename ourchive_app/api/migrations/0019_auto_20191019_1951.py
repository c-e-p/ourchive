# Generated by Django 2.2.6 on 2019-10-19 19:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_auto_20191019_1924'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='work',
            name='audio_length',
        ),
        migrations.RemoveField(
            model_name='work',
            name='chapter_count',
        ),
        migrations.RemoveField(
            model_name='work',
            name='word_count',
        ),
    ]

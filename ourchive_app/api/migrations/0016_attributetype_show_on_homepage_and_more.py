# Generated by Django 5.0.2 on 2024-05-06 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_language_alter_bookmark_work_bookmark_language_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='attributetype',
            name='show_on_homepage',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tagtype',
            name='show_on_homepage',
            field=models.BooleanField(default=False),
        ),
    ]

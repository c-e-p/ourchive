# Generated by Django 5.0.2 on 2024-02-24 17:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_bookmark_to_work'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCollection',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('approved', models.BooleanField(default=False)),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.bookmarkcollection')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'api_user_collections',
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='user',
            name='collections',
            field=models.ManyToManyField(related_name='users', through='api.UserCollection', to='api.bookmarkcollection'),
        ),
        migrations.CreateModel(
            name='UserWork',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('approved', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('work', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.work')),
            ],
            options={
                'db_table': 'api_user_works',
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='user',
            name='works',
            field=models.ManyToManyField(related_name='users', through='api.UserWork', to='api.work'),
        ),
    ]

# Generated by Django 5.0.2 on 2024-06-10 03:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0030_rename_users_anthology_owners'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useranthology',
            old_name='Anthology',
            new_name='anthology',
        ),
        migrations.AlterField(
            model_name='useranthology',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_anthologies', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='usercollection',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_collections', to=settings.AUTH_USER_MODEL),
        ),
    ]
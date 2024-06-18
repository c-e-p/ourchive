# Generated by Django 5.0.2 on 2024-06-12 03:01

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_create_new_anthology_series_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('label', models.CharField(max_length=200)),
            ],
            options={
                'ordering': ['label'],
            },
        ),
        migrations.AddConstraint(
            model_name='searchgroup',
            constraint=models.UniqueConstraint(fields=('label',), name='unique label'),
        ),
        migrations.AddField(
            model_name='attributetype',
            name='search_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.searchgroup'),
        ),
        migrations.AddField(
            model_name='tagtype',
            name='search_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.searchgroup'),
        ),
    ]

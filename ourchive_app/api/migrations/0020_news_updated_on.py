# Generated by Django 5.0.2 on 2024-05-09 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_rename_value_contentpage_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='updated_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
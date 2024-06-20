# Generated by Django 5.0.4 on 2024-06-20 19:03

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('project_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('project_name', models.CharField(max_length=255)),
                ('content_type', models.CharField(max_length=255)),
                ('budget', models.IntegerField()),
                ('description', models.TextField()),
                ('additional_details', models.TextField()),
                ('location_details', models.JSONField()),
                ('ai_suggestions', models.BooleanField()),
                ('status', models.CharField(default='INITIATED', max_length=255)),
            ],
        ),
    ]

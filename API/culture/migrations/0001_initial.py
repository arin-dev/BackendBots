# Generated by Django 5.0.4 on 2024-06-19 08:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Culture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=255)),
                ('details', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ProjectCulture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('culture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='culture.culture')),
            ],
        ),
    ]

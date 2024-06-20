# Generated by Django 5.0.4 on 2024-06-20 19:02

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CrewMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_pic', models.URLField(blank=True)),
                ('name', models.CharField(max_length=100)),
                ('userid', models.EmailField(max_length=254, unique=True)),
                ('crewType', models.CharField(max_length=50)),
                ('role', models.CharField(max_length=50)),
                ('services', models.JSONField()),
                ('tags', models.JSONField()),
                ('expertise', models.JSONField()),
                ('yoe', models.IntegerField()),
                ('minRatePerDay', models.DecimalField(decimal_places=2, max_digits=6)),
                ('maxRatePerDay', models.DecimalField(decimal_places=2, max_digits=6)),
                ('next_available_date', models.DateField(default=django.utils.timezone.now)),
                ('location', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='CrewRequirement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=50)),
                ('number_needed', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SelectedCrew',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preferred_because', models.TextField(default='Did not store the field')),
            ],
        ),
    ]

# Generated by Django 5.0.6 on 2024-06-13 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crew', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='crewmember',
            old_name='roleJobTitle',
            new_name='role',
        ),
    ]

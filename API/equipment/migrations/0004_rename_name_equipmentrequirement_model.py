# Generated by Django 5.0.6 on 2024-06-20 13:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0003_alter_equipmentrequirement_project_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='equipmentrequirement',
            old_name='name',
            new_name='model',
        ),
    ]
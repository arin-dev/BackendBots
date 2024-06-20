# Generated by Django 5.0.4 on 2024-06-20 19:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0001_initial'),
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipmentrequirement',
            name='project',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='equipment_requirements_set', to='project.project'),
        ),
        migrations.AddField(
            model_name='selectedequipments',
            name='equipment',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='equipment.equipment'),
        ),
        migrations.AddField(
            model_name='selectedequipments',
            name='equipment_requirements',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='equipment.equipmentrequirement'),
        ),
        migrations.AddField(
            model_name='selectedequipments',
            name='project',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='selected_equipment_set', to='project.project'),
        ),
    ]

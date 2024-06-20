# Generated by Django 5.0.4 on 2024-06-20 06:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crew', '0001_initial'),
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='crewrequirement',
            name='project',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='crew_requirements_set', to='project.project'),
        ),
        migrations.AddField(
            model_name='selectedcrew',
            name='crew_member',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='crew.crewmember'),
        ),
        migrations.AddField(
            model_name='selectedcrew',
            name='crew_requirements',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='selected_crews', to='crew.crewrequirement'),
        ),
        migrations.AddField(
            model_name='selectedcrew',
            name='project',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='selected_crews_set', to='project.project'),
        ),
    ]
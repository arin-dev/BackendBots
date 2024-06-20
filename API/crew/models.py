from django.db import models
from django.utils import timezone
import uuid

class CrewMember(models.Model):
    profile_pic = models.URLField(max_length=200, blank=True)
    name = models.CharField(max_length=100)
    userid = models.EmailField(unique=True)
    crewType = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    services = models.JSONField()
    tags = models.JSONField()
    expertise = models.JSONField()
    yoe = models.IntegerField()
    minRatePerDay = models.DecimalField(max_digits=6, decimal_places=2)
    maxRatePerDay = models.DecimalField(max_digits=6, decimal_places=2)
    next_available_date = models.DateField(default=timezone.now)
    location = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class CrewRequirement(models.Model):
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE, related_name='crew_requirements_set')
    role = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    number_needed = models.IntegerField()
    
    def __str__(self):
        return self.role

class SelectedCrew(models.Model):
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE, related_name='selected_crews_set')
    crew_member = models.ForeignKey('CrewMember', on_delete=models.CASCADE)
    crew_requirements = models.ForeignKey('CrewRequirement', on_delete=models.CASCADE, related_name='selected_crews')
    preferred_because = models.TextField(default="Did not store the field") #remove this after deleting previous data
    
    def __str__(self):
        return self.crew_member.name

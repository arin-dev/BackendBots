from django.db import models
from django.utils import timezone
import uuid

class CrewMember(models.Model):
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
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='crew_requirements_set')
    role = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    number_needed = models.IntegerField()
    
    def __str__(self):
        return self.role

class SelectedCrew(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='selected_crews_set')
    crew_member = models.ForeignKey('CrewMember', on_delete=models.CASCADE)
    crew_requirements = models.ForeignKey('CrewRequirement', on_delete=models.CASCADE)
    preferred_because = models.TextField(default="Did not store the field") #remove this after deleting previous data
    
    def __str__(self):
        return self.crew_member.name

class Project(models.Model):
    project_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project_name = models.CharField(max_length=255)
    content_type = models.CharField(max_length=255)
    budget = models.IntegerField()
    description = models.TextField()
    additional_details = models.TextField()
    locations = models.JSONField()
    ai_suggestions = models.BooleanField()
    crew_requirements = models.ManyToManyField(CrewRequirement, related_name='projects_set')
    selected_crews = models.ManyToManyField(SelectedCrew, related_name='projects_set')

    def delete(self, *args, **kwargs):
        self.crew_requirements.all().delete()
        self.selected_crews.all().delete()

        super().delete(*args, **kwargs)

    def __str__(self):
        return self.project_name
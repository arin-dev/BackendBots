from django.db import models
import uuid
# Create your models here.
class CrewMember(models.Model):
    name = models.CharField(max_length=100)
    userid = models.EmailField(unique=True)
    crewType = models.CharField(max_length=50)
    roleJobTitle = models.CharField(max_length=50)
    services = models.JSONField()
    tags = models.JSONField()
    expertise = models.JSONField()
    yoe = models.IntegerField()
    minRatePerDay = models.DecimalField(max_digits=6, decimal_places=2)
    maxRatePerDay = models.DecimalField(max_digits=6, decimal_places=2)
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
    
    def __str__(self):
        return self.crew_member.name

class Project(models.Model):
    project_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project_detail_from_customer = models.TextField()
    detailed_desc = models.TextField()
    crew_requirements = models.ManyToManyField(CrewRequirement, related_name='projects_set')
    selected_crews = models.ManyToManyField(SelectedCrew, related_name='projects_set')

    def __str__(self):
        return self.project_detail_from_customer
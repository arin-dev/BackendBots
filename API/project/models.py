import uuid
from django.db import models
from culture.models import ProjectCulture

class Project(models.Model):
    project_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project_name = models.CharField(max_length=255)
    content_type = models.CharField(max_length=255)
    budget = models.IntegerField()
    description = models.TextField()
    additional_details = models.TextField()
    location_details = models.JSONField()
    ai_suggestions = models.BooleanField()
    crew_requirements = models.ManyToManyField('crew.CrewRequirement', related_name='projects_set')
    selected_crews = models.ManyToManyField('crew.SelectedCrew', related_name='projects_set')
    equipment_requirements = models.ManyToManyField('equipment.EquipmentRequirement', related_name='projects_set_equipment1')
    selected_equipments = models.ManyToManyField('equipment.SelectedEquipments', related_name='projects_set_equipment2')
    project_cultures = models.ManyToManyField('culture.Culture', through='culture.ProjectCulture', related_name='projects_set')
    logistics = models.ManyToManyField('logistics.Logistics', related_name='projects_set')
    compliance_report = models.ManyToManyField('compliance.Compliance', related_name='projects_set')
    status = models.CharField(max_length=255, default='INITIATED')
    
    def delete(self, *args, **kwargs):
        self.crew_requirements.all().delete()
        self.selected_crews.all().delete()
        self.logistics.all().delete()
        self.compliance_report.all().delete()
        self.equipment_requirements.all().delete()
        self.selected_equipments.all().delete()
        ProjectCulture.objects.filter(project=self).delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.project_name

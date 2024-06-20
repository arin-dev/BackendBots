import uuid

from django.db import models
from crew.models import CrewRequirement, SelectedCrew
from equipment.models import EquipmentRequirement, SelectedEquipments
from django.apps import apps



# Create your models here.
class Project(models.Model):
    
    project_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project_name = models.CharField(max_length=255)
    content_type = models.CharField(max_length=255)
    budget = models.IntegerField()
    description = models.TextField()
    additional_details = models.TextField()
    locations = models.JSONField()
    ai_suggestions = models.BooleanField()
    crew_requirements = models.ManyToManyField('crew.CrewRequirement', related_name='projects_set')
    selected_crews = models.ManyToManyField('crew.SelectedCrew', related_name='projects_set')
    equipment_requirements = models.ManyToManyField('equipment.EquipmentRequirement', related_name='projects_set_equipment1')
    selected_equipments = models.ManyToManyField('equipment.SelectedEquipments', related_name='projects_set_equipment2')

    def delete(self, *args, **kwargs):
        self.crew_requirements.all().delete()
        self.selected_crews.all().delete()
        self.equipment_requirements.all().delete()
        self.selected_equipments.all().delete()

        super().delete(*args, **kwargs)

    def __str__(self):
        return self.project_name
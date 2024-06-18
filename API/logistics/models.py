from django.db import models

# Create your models here.
class Logistics(models.Model):
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE, related_name='logistics_set')
    flights_details = models.JSONField()
    hotel_details = models.JSONField()
    taxi_details = models.JSONField()

    

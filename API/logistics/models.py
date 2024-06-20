from django.db import models

class Logistics(models.Model):
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE, related_name='logistics_set')
    flights_details = models.JSONField()
    hotel_details = models.JSONField()
    taxi_details = models.JSONField()

    def __str__(self):
        return f"Logistics for {self.project}"

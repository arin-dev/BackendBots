from django.db import models

# Create your models here.
class Compliance(models.Model):
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE, related_name='compliance_details')
    locations = models.CharField(max_length=255)
    mode = models.CharField(max_length=255)
    crew_size = models.IntegerField()
    time_frame = models.CharField(max_length=255)
    landmarks = models.CharField(max_length=255, null=True, blank=True)
    special_equipment = models.CharField(max_length=255, null=True, blank=True)
    report = models.TextField()

    def __str__(self):
        return f"Compliance for {self.project}"
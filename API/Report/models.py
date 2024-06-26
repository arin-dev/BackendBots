from django.db import models

# Create your models here.
class EquipmentReport(models.Model):
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE, related_name='equipment_report_model')
    name = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=100)
    cost = models.CharField(max_length=50)
    size = models.CharField(max_length=50)
    sensitive = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
class CrewReport(models.Model):
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE, related_name='crew_report_model')
    name = models.CharField(max_length=50)
    userid = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    age = models.IntegerField()
    driving_licence = models.BooleanField()
    
    def __str__(self):
        return self.name
    
class CompleteReport(models.Model):
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE, related_name='complete_report_model')
    crew_report = models.ForeignKey(CrewReport, on_delete=models.CASCADE)
    equipment_report = models.ForeignKey(EquipmentReport, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'Complete Report for {self.project.name}'
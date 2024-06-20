from django.db import models

class Culture(models.Model):
    location = models.CharField(max_length=255)
    details = models.TextField()

    def __str__(self):
        return self.location

class ProjectCulture(models.Model):
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE, default=1)
    culture = models.ForeignKey('Culture', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.project} - {self.culture}"

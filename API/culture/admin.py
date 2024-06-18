from django.contrib import admin
from .models import Culture, ProjectCulture  # replace YourModel with the name of your model

admin.site.register(Culture)
admin.site.register(ProjectCulture)

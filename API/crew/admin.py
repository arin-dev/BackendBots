from django.contrib import admin
from .models import *  # replace YourModel with the name of your model

admin.site.register(CrewMember)
admin.site.register(SelectedCrew)
admin.site.register(CrewRequirement)
from rest_framework import serializers

from crew.serializers import CrewRequirementSerializer, SelectedCrewSerializer
from .models import Project

class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['project_id', 'project_name', 'description']
        depth = 1

class ProjectDetailsSerializer(serializers.ModelSerializer):
    crew_requirements_set = CrewRequirementSerializer(many=True, read_only=True)
    selected_crews_set = SelectedCrewSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        exclude = ['selected_crews', 'crew_requirements']
        depth = 1
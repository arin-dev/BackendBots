# culture/serializers.py

from rest_framework import serializers
from .models import Culture, ProjectCulture
from project.models import Project  # Import the Project model

class CultureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Culture
        fields = ['id', 'location', 'details']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['project_id', 'project_name', 'content_type', 'budget', 'description', 'additional_details', 'location_details', 'ai_suggestions']

class ProjectCultureSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    cultures = CultureSerializer(many=True, read_only=True)

    class Meta:
        model = ProjectCulture
        fields = ['id', 'project', 'cultures']

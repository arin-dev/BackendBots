from rest_framework import serializers

from .models import CrewMember, Project, CrewRequirement, SelectedCrew

class CrewMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrewMember
        exclude = ['next_available_date']
        depth = 1

class CrewRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrewRequirement
        fields = ['role', 'location', 'number_needed']
        depth = 1

class SelectedCrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectedCrew
        fields = ['crew_member', 'preferred_because']
        depth = 1

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
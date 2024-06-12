from rest_framework import serializers

from .models import CrewMember, Project, CrewRequirement, SelectedCrew

class CrewMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrewMember
        fields = ['name', 'userid', 'crewType', 'roleJobTitle', 'services', 'tags', 'expertise', 'yoe', 'minRatePerDay', 'maxRatePerDay', 'location']
        depth = 1

class CrewRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrewRequirement
        fields = ['role', 'location', 'number_needed']
        depth = 1

class SelectedCrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectedCrew
        fields = ['crew_member']
        depth = 1

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['project_id', 'project_detail_from_customer', 'detailed_desc']
        depth = 1
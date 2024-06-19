from rest_framework import serializers

from .models import CrewMember, CrewRequirement, SelectedCrew
from project.models import Project

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



########################## WILL USE PROPER NAMES IN FUTURE ##############################
class TryingCrewMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrewMember
        fields = ['id', 'profile_pic', 'name', 'userid', 'yoe', 'minRatePerDay', 'maxRatePerDay', 'location']
        depth = 1
class TryingSelectedCrewSerializer(serializers.ModelSerializer):
    crew_member = TryingCrewMemberSerializer(read_only=True)
    class Meta:
        model = SelectedCrew
        fields = ['crew_member', 'preferred_because']
        depth = 1

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        crew_member_representation = representation.pop('crew_member')
        for key in crew_member_representation:
            representation[key] = crew_member_representation[key]
        return representation

class TryingCrewRequirementSerializer(serializers.ModelSerializer):
    selected_crews = TryingSelectedCrewSerializer(many=True, read_only=True)

    class Meta:
        model = CrewRequirement
        fields = ['id', 'role', 'location', 'number_needed', 'selected_crews']

class TryingProjectSerializer(serializers.ModelSerializer):
    crew_requirements_set = TryingCrewRequirementSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['project_id', 'project_name', 'crew_requirements_set', ]
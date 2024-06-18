from rest_framework import serializers

from .models import CrewMember, CrewRequirement, SelectedCrew

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
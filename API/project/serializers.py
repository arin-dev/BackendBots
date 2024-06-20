from rest_framework import serializers

from .models import Project
from culture.serializers import CultureSerializer
from logistics.serializers import LogisticsSerializer
from crew.serializers import CrewRequirementSerializer, SelectedCrewSerializer
from compliance.serializers import ComplianceSerializer
from equipment.serializers import EquipmentRequirementSerializer, SelectedEquipmentsSerializer

class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['project_id', 'project_name', 'description', 'status']
        depth = 1

class ProjectDetailsSerializer(serializers.ModelSerializer):
    crew_requirements_set = CrewRequirementSerializer(many=True, read_only=True)
    selected_crews_set = SelectedCrewSerializer(many=True, read_only=True)
    culture_details = CultureSerializer(many=True, read_only=True)
    logistics_set = LogisticsSerializer(many=True, read_only=True)
    compliance_details = ComplianceSerializer(many=True, read_only=True)
    equipment_requirements_set = EquipmentRequirementSerializer(many=True, read_only=True)
    selected_equipment_set = SelectedEquipmentsSerializer(many=True, read_only=True)
    
    class Meta:
        model = Project
        exclude = ['selected_crews', 'crew_requirements', 'logistics', 'compliance_report']
        depth = 1
    
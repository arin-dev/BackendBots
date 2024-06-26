from rest_framework import serializers
from .models import *

class CrewReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrewReport
        fields = ['name', 'userid', 'age','gender','driving_licence']
      
class EquipmentReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentReport
        exclude = ['id', 'project']
        
class CompleteReportSerializer(serializers.ModelSerializer):
    equipment_report = EquipmentReportSerializer()
    crew_report = CrewReportSerializer()
    
    class Meta:
        model = CompleteReport
        fields = ['equipment_report', 'crew_report']
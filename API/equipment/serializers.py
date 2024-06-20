from rest_framework import serializers
from .models import Equipment, Provider, Availability, EquipmentRequirement, SelectedEquipments

class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ['name', 'contact_phone', 'contact_email', 'contact_address']

class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ['start_date', 'end_date', 'status']

class EquipmentSerializer(serializers.ModelSerializer):
    provider = ProviderSerializer(required=False)
    availability = AvailabilitySerializer(required=False)
    connectivity = serializers.ListField(child=serializers.CharField(), required=False)
    accessories = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = Equipment
        fields = '__all__'
        
class EquipmentRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentRequirement
        fields = ['name', 'number_needed', 'Specification_required','location']
        
class SelectedEquipmentsSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='equipment.name')
    model = serializers.CharField(source='equipment.model')
    brand = serializers.CharField(source='equipment.brand')
    number_needed = serializers.IntegerField(source='equipment_requirements.number_needed')
    location = serializers.CharField(source='equipment.location')
    Preferred_because = serializers.CharField(source='preferred_because')
    provider_email = serializers.EmailField(source='equipment.provider.email', required=False)
    
    class Meta:
        model = SelectedEquipments
        fields = ['name', 'model', 'brand', 'number_needed','location','Preferred_because', 'provider_email']
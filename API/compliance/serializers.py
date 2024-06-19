# culture/serializers.py

from .models import Compliance
from rest_framework import serializers

class ComplianceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compliance
        fields = '__all__'

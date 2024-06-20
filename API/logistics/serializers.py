# culture/serializers.py

from .models import Logistics
from rest_framework import serializers

class LogisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logistics
        fields = '__all__'

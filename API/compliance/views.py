from rest_framework import viewsets
from .models import Compliance
from .serializers import ComplianceSerializer

class ComplianceViewSet(viewsets.ModelViewSet):
    queryset = Compliance.objects.all()
    serializer_class = ComplianceSerializer
from rest_framework import generics
from .models import Logistics
from .serializers import LogisticsSerializer

class LogisticsListView(generics.ListAPIView):
    queryset = Logistics.objects.all()
    serializer_class = LogisticsSerializer
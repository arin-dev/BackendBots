# culture/views.py

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Culture, ProjectCulture
from .serializers import CultureSerializer, ProjectCultureSerializer, ProjectSerializer
from project.models import Project

class CultureListView(generics.ListAPIView):
    queryset = Culture.objects.all()
    serializer_class = CultureSerializer

@api_view(['GET'])
def project_culture_detail_view(request, project_id):
    project = Project.objects.get(project_id=project_id)
    project_culture = ProjectCulture.objects.filter(project=project)
    serializer = ProjectCultureSerializer(project_culture, many=True)
    return Response(serializer.data)

import uuid
import threading

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from crew.models import CrewMember
from Crew_Bot.CrewGraph import CrewGraph
from crew.models import CrewMember, CrewRequirement, SelectedCrew
from crew.serializers import CrewMemberSerializer, CrewRequirementSerializer, SelectedCrewSerializer

from .models import Project
from .serializers import ProjectsSerializer, ProjectDetailsSerializer

from .utils import *

# Create your views here.
@api_view(['POST'])
def create_project(request):
    
    project_state = get_form_data(request)

    new_project = Project(
    project_name=project_state["project_name"],
    content_type=project_state["content_type"],
    budget=project_state["budget"],
    description=project_state["description"],
    additional_details=project_state["additional_details"],
    locations=project_state["locations"],
    ai_suggestions=project_state["ai_suggestions"],)
    new_project.save()

    # task1 = threading.Thread(target=short_wait, args=())
    task2 = threading.Thread(target=complete_project_details, args=(project_state, new_project))
    
    # task1.start()
    task2.start()

    new_project_id = new_project.project_id
    return Response({"message": "Request successful", "project_id": new_project_id})


@api_view(['GET'])
def list_projects(request):
    projects = Project.objects.all()
    serializer = ProjectsSerializer(projects, many=True)
    return Response(serializer.data, status=200)

@api_view(['GET'])
def get_complete_project_details(request):
    project_id = request.GET.get('project_id')
    if project_id is None:
        return Response("Project id is required", status=400)
    project = Project.objects.get(project_id=uuid.UUID(project_id))
    serializer = ProjectDetailsSerializer(project)
    return Response(serializer.data, status=200)

@api_view(['DELETE'])
def delete_project(request):
    project_id = request.GET.get('project_id')
    try:
        project = Project.objects.get(project_id=project_id)
    except Project.DoesNotExist:
        return Response({'error': 'Project not found'}, status=404)

    project.delete()
    return Response({'message': 'Project deleted'}, status=200)
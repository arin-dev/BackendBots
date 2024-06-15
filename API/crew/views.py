import os
import uuid
# import json

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import CrewMember
from Crew_Bot.CrewGraph import CrewGraph
from crew.models import CrewMember, Project, CrewRequirement, SelectedCrew
from .serializers import CrewMemberSerializer, CrewRequirementSerializer, SelectedCrewSerializer, ProjectsSerializer, ProjectDetailsSerializer

from .APIFunctions import *


@api_view(['POST'])
def create_project(request):
    project_state = get_form_data(request)
    result = CrewGraph(State=State, state=project_state)

    new_project = Project(
    project_name=result["project_name"],
    content_type=result["content_type"],
    budget=result["budget"],
    description=result["description"],
    additional_details=result["additional_details"],
    locations=result["locations"],
    ai_suggestions=result["ai_suggestions"],)
    new_project.save()
    
    crew_req = result["crew_requirements"]
    createCrewRequirement(crew_req, new_project)

    selected_crews = result["selected_crews"]
    createSelectedCrews(selected_crews, new_project)
                
    new_project_id = new_project.project_id
    return Response({"message": "Request successful", "project_id": new_project_id})

    
@api_view(['GET'])
def crew_requirement(request):
    project_id = request.GET.get('project_id')
    if project_id is None:
        return Response("Project id is required", status=400)
    crew_requirement = CrewRequirement.objects.filter(project_id=project_id)
    serializer = CrewRequirementSerializer(crew_requirement, many=True)
    return Response(serializer.data, status=200)


@api_view(['GET'])
def selected_crew(request):
    project_id = request.GET.get('project_id')
    if project_id is None:
        return Response("Project id is required", status=400)
    selected_crew = SelectedCrew.objects.filter(project_id=project_id)
    serializer = SelectedCrewSerializer(selected_crew, many=True)
    return Response(serializer.data, status=200)


@api_view(['GET'])
def list_crew_memebers(request):
    users = CrewMember.objects.all()
    serializer = CrewMemberSerializer(users, many=True)
    return Response(serializer.data, status=200) 


@api_view(['GET'])
def crew_member(request):
    crew_id = request.GET.get('id')
    if crew_id is None:
        return Response("id is required", status=400)
    try:
        crew_member = CrewMember.objects.get(id=crew_id)
    except CrewMember.DoesNotExist:
        return Response("Crew member not found", status=404)
    serializer = CrewMemberSerializer(crew_member)
    return Response(serializer.data, status=200)


@api_view(['GET'])
def list_projects(request):
    projects = Project.objects.all()
    serializer = ProjectsSerializer(projects, many=True)
    return Response(serializer.data, status=200)


@api_view(['GET'])
def project_crew_details(request):
    project_id = request.GET.get('project_id')
    if project_id is None:
        return Response("Project id is required", status=400)
    project = Project.objects.get(project_id=uuid.UUID(project_id))
    serializer = ProjectDetailsSerializer(project)
    response = transform_crew_data(serializer.data)
    return Response(response, status=200)


@api_view(['GET'])
def complete_project_details(request):
    project_id = request.GET.get('project_id')
    if project_id is None:
        return Response("Project id is required", status=400)
    project = Project.objects.get(project_id=uuid.UUID(project_id))
    serializer = ProjectDetailsSerializer(project)
    return Response(serializer.data, status=200)


class CrewMemberCreateView(APIView):
    def post(self, request):
        serializer = CrewMemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_project(request):
    project_id = request.GET.get('project_id')
    try:
        project = Project.objects.get(project_id=project_id)
    except Project.DoesNotExist:
        return Response({'error': 'Project not found'}, status=404)

    project.delete()
    return Response({'message': 'Project deleted'}, status=200)

# @api_view(['POST'])
# def push_dummy_data(request):
#     print("Testing if dummy data present")

#     print("Starting pushing dummy data")
#     with open('crew/crewdata.json') as f:
#         data = json.load(f)

#     crew_members = []
#     for crew_member in data:
#         # Check if a CrewMember with the same userid already exists
#         if not CrewMember.objects.filter(userid=crew_member["userid"]).exists():
#             crew_members.append(CrewMember(
#                 name=crew_member["name"], 
#                 userid=crew_member["userid"], 
#                 crewType=crew_member["crewType"], 
#                 role=crew_member["roleJobTitle"], 
#                 services=','.join(crew_member["services"]), 
#                 tags=','.join(crew_member["tags"]), 
#                 expertise=','.join(crew_member["expertise"]), 
#                 yoe=crew_member["yoe"], 
#                 minRatePerDay=crew_member["minRatePerDay"], 
#                 maxRatePerDay=crew_member["maxRatePerDay"], 
#                 location=crew_member["location"]
#             ))
#     CrewMember.objects.bulk_create(crew_members)

#     return Response({"message": "Data pushed successfully"}, status=200)
import os, json
import uuid

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import CrewMember
from Crew_Bot.CrewGraph import CrewGraph
from .models import CrewMember, CrewRequirement, SelectedCrew
from .serializers import CrewMemberSerializer, CrewRequirementSerializer, SelectedCrewSerializer, TryingProjectSerializer

from project.models import Project
from project.serializers import ProjectsSerializer, ProjectDetailsSerializer

from .utils import *

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
def project_crew_details(request):
    project_id = request.GET.get('project_id')
    if project_id is None:
        return Response("Project id is required", status=400)
    proj = Project.objects.get(project_id=uuid.UUID(project_id))
    # serializer = ProjectDetailsSerializer(project)
    # response = transform_crew_data(serializer.data)
    # crew_req = CrewRequirement.objects.filter(project_id=uuid.UUID(project_id))
    serializer = TryingProjectSerializer(proj)
    # response = transform_crew_data(serializer.data)
    response = serializer.data
    return Response(response, status=200)


class CrewMemberCreateView(APIView):
    def post(self, request):
        serializer = CrewMemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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
 
####################### UPDATE DUMMY DATA
@api_view(['POST'])
def push_dummy_data(request):
    print("Testing if dummy data present")
    print(request)
    print("Starting pushing dummy data")
    with open('crew/crewdata_with_profilepic.json') as f:
        data = json.load(f)
    
    print(data[0])
    from django.db import transaction
    with transaction.atomic():
        for crew_member in data:
            # Check if a CrewMember with the same userid already exists
            obj, created = CrewMember.objects.update_or_create(
                userid=crew_member["userid"],
                defaults={
                    'name': crew_member["name"],
                    'crewType': crew_member["crewType"],
                    'role': crew_member["roleJobTitle"],
                    'services': ','.join(crew_member["services"]),
                    'tags': ','.join(crew_member["tags"]),
                    'expertise': ','.join(crew_member["expertise"]),
                    'yoe': crew_member["yoe"],
                    'minRatePerDay': crew_member["minRatePerDay"],
                    'maxRatePerDay': crew_member["maxRatePerDay"],
                    'location': crew_member["location"],
                    'profile_pic': crew_member["profilePic"]
                }
            )
            print(obj,created)
    print("Data Pushed Successfully")
    return Response({"message": "Data pushed successfully"}, status=200)
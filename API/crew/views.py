from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.
import os

from .serializers import CrewMemberSerializer, CrewRequirementSerializer, SelectedCrewSerializer, ProjectSerializer
from crew.models import CrewMember, Project, CrewRequirement, SelectedCrew

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

from Crew_Bot.CrewGraph import CrewGraph
from .models import CrewMember

from typing import TypedDict, List

@api_view(['POST'])
def create_project(request):
    project_detail = request.GET.get('project_detail')
    if project_detail is None:
        return Response("Project detail is required", status=400)
    # print("\n\nproject_detail", project_detail)

    class State(TypedDict):
        num_steps : int
        project_detail_from_customer : str
        detailed_desc : str
        roleJobTitles : List[str]
        crew_requirements : List[dict]
        queries : List[str]
        selected_crews : List[dict]

    result = CrewGraph(State=State, project_detail_from_customer=project_detail)

    # print("\n\nresult", result)

    new_project = Project(
    project_detail_from_customer=result["project_detail_from_customer"],
    detailed_desc=result["detailed_desc"],)
    new_project.save()
    
    crew_req = result["crew_requirements"]
    for crew in crew_req:
        new_crew = CrewRequirement(
            project=new_project,
            role=crew["roleJobTitle"], 
            number_needed=crew["number_needed"],
            location=crew["location"],
        )
        new_crew.save()

    selected_crews = result["selected_crews"]

    # print("\n\n\n ###########  \n\n\n")
    # print("\n\nselected_crews", type(selected_crews), selected_crews)
    for role_dict in selected_crews:
            for role, crews in role_dict.items():
                for crew in crews:
                    new_selected_crew = SelectedCrew(
                    project=new_project,
                    crew_member=CrewMember.objects.get(userid=crew["userid"]),
                    crew_requirements=CrewRequirement.objects.get(project=new_project, role=role, location=crew["location"]),
                    )
                    new_selected_crew.save()
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
def crew_member(request):
    project_id = request.GET.get('project_id')
    if project_id is None:
        return Response("Project id is required", status=400)
    crew_member = CrewMember.objects.filter(project_id=project_id)
    serializer = CrewMemberSerializer(crew_member, many=True)
    return Response(serializer.data, status=200)


class CrewMemberCreateView(APIView):
    def post(self, request):
        serializer = CrewMemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def push_dummy_data(request):
#     with open('crew/crewdata.json') as f:
#         data = json.load(f)

#     crew_members = []
#     for crew_member in data:
#         crew_members.append(CrewMember(
#             name=crew_member["name"], 
#             userid=crew_member["userid"], 
#             crewType=crew_member["crewType"], 
#             roleJobTitle=crew_member["roleJobTitle"], 
#             services=','.join(crew_member["services"]), 
#             tags=','.join(crew_member["tags"]), 
#             expertise=','.join(crew_member["expertise"]), 
#             yoe=crew_member["yoe"], 
#             minRatePerDay=crew_member["minRatePerDay"], 
#             maxRatePerDay=crew_member["maxRatePerDay"], 
#             location=crew_member["location"]
#         ))
#     CrewMember.objects.bulk_create(crew_members)

#     return Response("Data pushed successfully", status=200)
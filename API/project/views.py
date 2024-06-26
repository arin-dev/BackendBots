import uuid
import threading

from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Project
from .serializers import ProjectsSerializer, ProjectDetailsSerializer

from .utils import *

@api_view(['POST'])
def create_project(request):
    project_state, location_details = get_form_data(request)
    new_project = Project(
        project_name=project_state["project_name"],
        content_type=project_state["content_type"],
        budget=project_state["budget"],
        description=project_state["description"],
        additional_details=project_state["additional_details"],
        location_details=location_details,
        ai_suggestions=project_state["ai_suggestions"],
    )
    new_project.save()

    # Start threading tasks
    task2 = threading.Thread(target=complete_project_details, args=(project_state, new_project))
    task2_1 = threading.Thread(target=Crew_Equip_Report, args=(project_state, new_project))
    task3 = threading.Thread(target=complete_culture_details, args=(project_state["locations"], new_project))
    task4 = threading.Thread(target=complete_logistics_details, args=(location_details, new_project))
    task5 = threading.Thread(target=complete_compliance_reports, args=(project_state, location_details, new_project))
    task2.start()
    task2.join()
    task2_1.start()
    task2_1.join()
    task3.start()
    task4.start()
    task5.start()

    # Create a new thread that waits for all threads to complete and then updates the project status
    def update_project_status():
        task2.join()
        task3.join()
        task4.join()
        task5.join()
        new_project.status = "PENDING"
        new_project.save()

    update_thread = threading.Thread(target=update_project_status)
    update_thread.start()

    new_project_id = new_project.project_id
    return Response({"message": "Request successful", "project_id": new_project_id})



@api_view(['GET'])
def list_projects(request):
    if 'status' in request.GET:
        projects = Project.objects.filter(status=request.GET['status'])
    else:
        projects = Project.objects.all()
    serializer = ProjectsSerializer(projects, many=True)
    return Response(serializer.data, status=200)

@api_view(['POST'])
def mark_project_as_completed(request):
    project_id = request.GET.get('project_id')
    if project_id is None:
        return Response("Project id is required", status=400)
    project = Project.objects.get(project_id=uuid.UUID(project_id))
    project.status = "COMPLETED"
    project.save()
    return Response({"message": "Project marked as completed"}, status=200)



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

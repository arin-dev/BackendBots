from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
@api_view(['GET'])
def report(request):
    project_id = request.GET.get('project_id')
    if project_id is None:
        return Response("Project id is required", status=400)
    # selected_equipment = SelectedEquipments.objects.filter(project_id=project_id)
    # serializer = SelectedEquipmentsSerializer(selected_equipment, many=True)
    # return Response(serializer.data, status=200)
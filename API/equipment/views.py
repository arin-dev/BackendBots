import os, json
import uuid
import django
from django.shortcuts import render
from django.db import transaction
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Provider, Availability, Equipment, EquipmentRequirement, SelectedEquipments
from .serializers import EquipmentSerializer, EquipmentRequirementSerializer, SelectedEquipmentsSerializer

from project.models import Project
from project.serializers import ProjectsSerializer, ProjectDetailsSerializer

# Create your views here.

# ---------Pushing Equipment_Data.json into database ------

@api_view(['POST'])
def push_dummy_data(request):
    print("Testing if dummy data present")
    print(request)
    print("Starting pushing dummy data")
    with open('equipment/Equipment_Data.json') as f:
        data = json.load(f)
    
    # print(data[0])
    with transaction.atomic():
        for equip in data:
            mydict = {}
            # Check if a CrewMember with the same userid already exists
            for key, value in equip.items():
                if key=='type':
                    key='Type'
                mydict[key]=value
                # print(f"{key} : {value}.")
           
            print("This is my dict ",mydict ,"\n\n")
            obj, created = Equipment.objects.update_or_create(
                model=equip["model"],
                defaults=mydict
            )
            print(obj,created)
            
        # for provider in data:
        #     created = Provider.objects.update_or_create(
        #         name = provider["name"]
        #         # contact_phone = provider
        #         # contact_email = 
        #         # contact_address   =         
        #     )
        # for avaliable in data:
        #     created = Availability.objects.update_or_create(
        #         # name = provider["name"]
        #     )
    print("Data Pushed Successfully")
    return Response({"message": "Data pushed successfully"}, status=200)

@api_view(['GET'])
def equipment_requirement(request):
    project_id = request.GET.get('project_id')
    if project_id is None:
        return Response("Project id is required", status=400)
    equipment_requirement = EquipmentRequirement.objects.filter(project_id=project_id)
    serializer = EquipmentRequirementSerializer(equipment_requirement, many=True)
    return Response(serializer.data, status=200)


@api_view(['GET'])
def selected_equipment(request):
    project_id = request.GET.get('project_id')
    if project_id is None:
        return Response("Project id is required", status=400)
    selected_equipment = SelectedEquipments.objects.filter(project_id=project_id)
    serializer = SelectedEquipmentsSerializer(selected_equipment, many=True)
    return Response(serializer.data, status=200)


@api_view(['GET'])
def list_equipments(request):
    equipments = Equipment.objects.all()
    serializer = EquipmentSerializer(equipments, many=True)
    return Response(serializer.data, status=200) 




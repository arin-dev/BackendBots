from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *

# Create your views here.
@api_view(['GET'])
def crew_report(request):
    project_id = request.GET.get('project_id')
    if project_id is None:
        return Response("Project id is required", status=400)
    crewreport = CrewReport.objects.filter(project_id=project_id)
    serializer = CrewReportSerializer(crewreport, many=True)
    return Response(serializer.data, status=200)

@api_view(['GET'])
def equipment_report(request):
    project_id = request.GET.get('project_id')
    if project_id is None:
        return Response("Project id is required", status=400)
    equipreport = EquipmentReport.objects.filter(project_id=project_id)
    serializer = EquipmentReportSerializer(equipreport, many=True)
    return Response(serializer.data, status=200)

# @api_view(['GET'])
# def culture_report(request):
#     project_id = request.GET.get('project_id')
#     if project_id is None:
#         return Response("Project id is required", status=400)
#     culturereport = CultureReport.objects.filter(project_id=project_id)
#     serializer = CultureReportSerializer(culturereport, many=True)
#     return Response(serializer.data, status=200)


@api_view(['GET'])
def complete_report(request):
    project_id = request.GET.get('project_id')
    if project_id is None:
        return Response("Project id is required", status=400)
    completereport = CompleteReport.objects.filter(project_id=project_id)
    # print("\nInside View",completereport)
    serializer = CompleteReportSerializer(completereport, many=True)
    ans = serializer.data
    ans2 ={
        "crew_report":[],
        "equipment_report":[],
        "compliance_report":[],
        "logistic_report":[],
        "culture_report":[],
    }
    for i in ans:
        print(i,"\n")
        if "equipment_report" in i:
            if i["equipment_report"]!=None:
                ans2["equipment_report"].append(i["equipment_report"])
        if "crew_report" in i:
            if i["crew_report"]!=None:
                ans2["crew_report"].append(i["crew_report"])
                
    return Response(ans2, status=200)
    # return Response(serializer.data, status=200)
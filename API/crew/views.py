from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.

@api_view(['GET']) 
def index(request):
    print("Hello, world. You're at the polls index.")
    return Response("Hello, world. You're at the polls index.") 

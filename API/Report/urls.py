from . import views
from django.urls import path

urlpatterns = [ 
    path('crew_report/', views.crew_report, name='crew_report'),
    path('equipment_report/', views.equipment_report, name='equipment_report'),
    path('complete_report/', views.complete_report, name='complete_report'),
]
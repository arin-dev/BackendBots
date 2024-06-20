from . import views
from django.urls import path

urlpatterns = [ 
    path('push_dummy_data/', views.push_dummy_data, name='push_dummy_data'),
    path('equipments/', views.Equipment, name='equipments'),
    path('requiredEquipments/', views.equipment_requirement, name='requiredEquipments'),
    path('selectedEquipments/', views.selected_equipment, name='selectedEquipments')
]
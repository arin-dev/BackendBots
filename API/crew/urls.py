from django.urls import path, include
from . import views
from .views import CrewMemberCreateView

urlpatterns = [
    path('create_project/', views.create_project),
    path('addcrewmember/', CrewMemberCreateView.as_view(), name='crewmember-create'),
    path('crew_requirement/', views.crew_requirement, name='crew_requirement'),
    path('selected_crew/', views.selected_crew, name='selected_crew'),
    path('crew_member/', views.crew_member, name='crew_member'),
    # path('push_dummy_data/', views.push_dummy_data),
]

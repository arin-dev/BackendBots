from . import views
from django.urls import path

urlpatterns = [
    path('project-crew-details/', views.project_crew_details, name='project_crew_details'),
    path('view-crew-requirement/', views.crew_requirement, name='crew_requirement'),
    path('view-selected-crew/', views.selected_crew, name='selected_crew'),
    path('list-crew-members/', views.list_crew_memebers, name='list_crew_members'),
    path('view-crew-member/', views.crew_member, name='crew_member'),
    path('add-crew-member/', views.CrewMemberCreateView.as_view(), name='crewmember-create'),
    path('push_dummy_data/', views.push_dummy_data),
]

from . import views
from django.urls import path

urlpatterns = [
    path('list-projects/', views.list_projects, name='list_projects'),
    path('project-crew-details/', views.project_crew_details, name='project_crew_details'),
    path('complete-project-details/', views.complete_project_details, name='complete_project_details'),
    path('create-project/', views.create_project),
    path('view-crew-requirement/', views.crew_requirement, name='crew_requirement'),
    path('view-selected-crew/', views.selected_crew, name='selected_crew'),
    path('list-crew-members/', views.list_crew_memebers, name='list_crew_members'),
    path('view-crew-member/', views.crew_member, name='crew_member'),
    path('add-crew-member/', views.CrewMemberCreateView.as_view(), name='crewmember-create'),
    path('delete-project/', views.delete_project, name='project-delete'),
    # path('push_dummy_data/', views.push_dummy_data),
]

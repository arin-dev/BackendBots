from . import views
from django.urls import path

urlpatterns = [
    path('list-projects/', views.list_projects, name='list_projects'),
    path('complete-project-details/', views.get_complete_project_details, name='complete_project_details'),
    path('create-project/', views.create_project),
    path('delete-project/', views.delete_project, name='project-delete'),
]
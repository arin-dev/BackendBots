# culture/urls.py

from django.urls import path
from .views import CultureListView, project_culture_detail_view

urlpatterns = [
    path('list-cultures/', CultureListView.as_view(), name='culture-list'),
    path('project-cultures/<uuid:project_id>/', project_culture_detail_view, name='project-culture-detail'),
]

from django.urls import path
from .views import LogisticsListView

app_name = 'logistics'
urlpatterns = [
    path('list-project-logistics/<uuid:project_id>/', LogisticsListView.as_view(), name='logistics-list'),
]
from django.urls import path
from .views import ComplianceViewSet

urlpatterns = [
    path('compliance/', ComplianceViewSet.as_view({'get': 'list', 'post': 'create'}), name='compliance-list-create'),
    path('compliance/<uuid:pk>/', ComplianceViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='compliance-detail'),
]
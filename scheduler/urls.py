# scheduler/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'indexes', views.IndexViewSet)
router.register(r'team-members', views.TeamMemberViewSet)
router.register(r'jobs', views.JobViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('assign-job/<int:job_id>/', views.assign_job, name='assign-job'),
]
# scheduler/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'indexes', views.IndexViewSet)
router.register(r'team-members', views.TeamMemberViewSet)
router.register(r'jobs', views.JobViewSet)
router.register(r'companies', views.CompanyViewSet)
router.register(r'time-slots', views.TimeSlotViewSet)
router.register(r'task-groups', views.TaskGroupViewSet)
router.register(r'tasks', views.TaskViewSet)
router.register(r'task-signoffs', views.TaskSignOffViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('assign-job/<int:job_id>/', views.assign_job, name='assign-job'),
    path('task-history/', views.get_task_history, name='task-history'),
]
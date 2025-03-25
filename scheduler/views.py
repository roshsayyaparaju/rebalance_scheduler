# scheduler/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from datetime import datetime, date
from django.db.models import Q
from .models import (
    Index, TeamMember, Job, 
    Company, TimeSlot, TaskGroup, Task, TaskSignOff
)
from .serializers import (
    IndexSerializer, TeamMemberSerializer, JobSerializer,
    CompanySerializer, TimeSlotSerializer, TaskGroupSerializer, 
    TaskSerializer, TaskSignOffSerializer, CompanyTasksSerializer
)

class IndexViewSet(viewsets.ModelViewSet):
    queryset = Index.objects.all()
    serializer_class = IndexSerializer

class TeamMemberViewSet(viewsets.ModelViewSet):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    
    def get_queryset(self):
        """Allow filtering by date range and index"""
        queryset = Job.objects.all()
        
        # Filter by date range if provided
        start = self.request.query_params.get('start')
        end = self.request.query_params.get('end')
        
        if start:
            queryset = queryset.filter(start_time__gte=start)
        if end:
            queryset = queryset.filter(end_time__lte=end)
            
        # Filter by index if provided
        index_id = self.request.query_params.get('index_id')
        if index_id:
            queryset = queryset.filter(index_id=index_id)
            
        return queryset

@api_view(['PUT'])
def assign_job(request, job_id):
    """API endpoint to assign a job to a team member"""
    try:
        job = Job.objects.get(pk=job_id)
        member_id = request.data.get('team_member_id')
        
        if member_id:
            team_member = TeamMember.objects.get(pk=member_id)
            job.assigned_to = team_member
        else:
            # If no member_id is provided, unassign the job
            job.assigned_to = None
            
        job.save()
        return Response(JobSerializer(job).data)
        
    except (Job.DoesNotExist, TeamMember.DoesNotExist):
        return Response({"error": "Job or Team Member not found"}, status=404)

# New ViewSets for task models

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    
    @action(detail=False, methods=['get'])
    def with_tasks(self, request):
        """Return companies with their task groups and tasks."""
        # Get time slot filter if provided
        time_slot_id = request.query_params.get('time_slot')
        # Get today's date for checking sign-offs
        today_str = request.query_params.get('date')
        if today_str:
            try:
                today = datetime.strptime(today_str, '%Y-%m-%d').date()
            except ValueError:
                today = date.today()
        else:
            today = date.today()
        
        # Get all companies
        companies = Company.objects.all().order_by('name')
        
        # Create context for the serializer
        context = {
            'time_slot_id': time_slot_id,
            'today': today
        }
        
        # Serialize the companies with their tasks
        serializer = CompanyTasksSerializer(
            companies, 
            many=True, 
            context=context
        )
        
        # Filter out companies with no task groups
        result_data = []
        for company_data in serializer.data:
            # Only include companies that have task groups
            if company_data['task_groups'] and len(company_data['task_groups']) > 0:
                result_data.append(company_data)
        
        return Response(result_data)
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    
    @action(detail=False, methods=['get'])
    def with_tasks(self, request):
        """Return companies with their task groups and tasks."""
        # Get time slot filter if provided
        time_slot_id = request.query_params.get('time_slot')
        # Get today's date for checking sign-offs
        today_str = request.query_params.get('date')
        if today_str:
            try:
                today = datetime.strptime(today_str, '%Y-%m-%d').date()
            except ValueError:
                today = date.today()
        else:
            today = date.today()
            
        companies = Company.objects.all()
        serializer = CompanyTasksSerializer(
            companies, 
            many=True, 
            context={
                'time_slot_id': time_slot_id,
                'today': today
            }
        )
        return Response(serializer.data)

class TimeSlotViewSet(viewsets.ModelViewSet):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer

class TaskGroupViewSet(viewsets.ModelViewSet):
    queryset = TaskGroup.objects.all()
    serializer_class = TaskGroupSerializer
    
    def get_queryset(self):
        """Allow filtering by company and time slot"""
        queryset = TaskGroup.objects.all()
        
        company_id = self.request.query_params.get('company')
        time_slot_id = self.request.query_params.get('time_slot')
        
        if company_id:
            queryset = queryset.filter(company_id=company_id)
        if time_slot_id:
            queryset = queryset.filter(time_slot_id=time_slot_id)
            
        return queryset

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskSignOffViewSet(viewsets.ModelViewSet):
    queryset = TaskSignOff.objects.all()
    serializer_class = TaskSignOffSerializer
    
    def get_queryset(self):
        """Allow filtering by task group, team member, and date"""
        queryset = TaskSignOff.objects.all()
        
        task_group_id = self.request.query_params.get('task_group')
        team_member_id = self.request.query_params.get('team_member')
        date_str = self.request.query_params.get('date')
        
        if task_group_id:
            queryset = queryset.filter(task_group_id=task_group_id)
        if team_member_id:
            queryset = queryset.filter(team_member_id=team_member_id)
        if date_str:
            try:
                completed_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                queryset = queryset.filter(completed_date=completed_date)
            except ValueError:
                pass
            
        return queryset
    
    @action(detail=False, methods=['post'])
    def sign_off(self, request):
        """Sign off on a task group for today's date."""
        task_group_id = request.data.get('task_group_id')
        team_member_id = request.data.get('team_member_id')
        notes = request.data.get('notes', '')
        completed_date_str = request.data.get('completed_date')
        
        # Default to today if no date provided
        if completed_date_str:
            try:
                completed_date = datetime.strptime(completed_date_str, '%Y-%m-%d').date()
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD."},
                               status=status.HTTP_400_BAD_REQUEST)
        else:
            completed_date = date.today()
            
        try:
            task_group = TaskGroup.objects.get(pk=task_group_id)
            team_member = TeamMember.objects.get(pk=team_member_id)
            
            # Check if already signed off for this date
            existing = TaskSignOff.objects.filter(
                task_group=task_group,
                team_member=team_member,
                completed_date=completed_date
            ).first()
            
            if existing:
                # Update existing sign-off
                existing.notes = notes
                existing.save()
                serializer = TaskSignOffSerializer(existing)
                return Response(serializer.data)
            else:
                # Create new sign-off
                sign_off = TaskSignOff.objects.create(
                    task_group=task_group,
                    team_member=team_member,
                    completed_date=completed_date,
                    notes=notes
                )
                serializer = TaskSignOffSerializer(sign_off)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except TaskGroup.DoesNotExist:
            return Response({"error": "Task group not found"}, status=status.HTTP_404_NOT_FOUND)
        except TeamMember.DoesNotExist:
            return Response({"error": "Team member not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_task_history(request):
    """Get recent task sign-off history."""
    days = request.query_params.get('days', 7)
    try:
        days = int(days)
    except ValueError:
        days = 7
        
    # Get recent sign-offs
    recent_signoffs = TaskSignOff.objects.all().order_by('-sign_off_date')[:days * 10]  # Fetch more than needed for filtering
    
    serializer = TaskSignOffSerializer(recent_signoffs, many=True)
    return Response(serializer.data)
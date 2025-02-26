# scheduler/views.py
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Index, TeamMember, Job
from .serializers import IndexSerializer, TeamMemberSerializer, JobSerializer

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
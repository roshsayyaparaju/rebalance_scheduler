# scheduler/serializers.py
from rest_framework import serializers
from .models import (
    Index, TeamMember, Job, 
    Company, TimeSlot, TaskGroup, Task, TaskSignOff
)

class IndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Index
        fields = '__all__'

class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = '__all__'

class JobSerializer(serializers.ModelSerializer):
    index_name = serializers.CharField(source='index.name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.name', read_only=True)
    
    class Meta:
        model = Job
        fields = [
            'id', 'index', 'index_name', 'title', 'start_time', 
            'end_time', 'assigned_to', 'assigned_to_name', 
            'color', 'notes'
        ]

# New serializers for task models

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'description', 'order']

class TaskGroupSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    company_name = serializers.CharField(source='company.name', read_only=True)
    time_slot_name = serializers.CharField(source='time_slot.name', read_only=True)
    
    class Meta:
        model = TaskGroup
        fields = ['id', 'name', 'company', 'company_name', 'time_slot', 
                  'time_slot_name', 'dallas_time', 'tasks']

class TaskSignOffSerializer(serializers.ModelSerializer):
    task_group_name = serializers.CharField(source='task_group.name', read_only=True)
    team_member_name = serializers.CharField(source='team_member.name', read_only=True)
    company_name = serializers.CharField(source='task_group.company.name', read_only=True)
    time_slot_name = serializers.CharField(source='task_group.time_slot.name', read_only=True)
    
    class Meta:
        model = TaskSignOff
        fields = ['id', 'task_group', 'task_group_name', 'team_member', 'team_member_name',
                  'sign_off_date', 'completed_date', 'notes', 'company_name', 'time_slot_name']
        
# Nested serializers for dashboard views

class TaskGroupWithSignoffsSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    company_name = serializers.CharField(source='company.name', read_only=True)
    time_slot_name = serializers.CharField(source='time_slot.name', read_only=True)
    latest_signoff = serializers.SerializerMethodField()
    
    class Meta:
        model = TaskGroup
        fields = ['id', 'name', 'company', 'company_name', 'time_slot', 
                  'time_slot_name', 'dallas_time', 'tasks', 'latest_signoff']
    
    def get_latest_signoff(self, obj):
        # Get today's date for context
        today = self.context.get('today')
        if today:
            signoff = obj.signoffs.filter(completed_date=today).first()
            if signoff:
                return {
                    'id': signoff.id,
                    'team_member_name': signoff.team_member.name,
                    'sign_off_date': signoff.sign_off_date,
                }
        return None

class CompanyTasksSerializer(serializers.ModelSerializer):
    task_groups = serializers.SerializerMethodField()
    
    class Meta:
        model = Company
        fields = ['id', 'name', 'description', 'task_groups']
    
    def get_task_groups(self, obj):
        # Get time slot as query parameter
        time_slot_id = self.context.get('time_slot_id')
        today = self.context.get('today')
        
        # Filter task groups by time slot if provided
        queryset = obj.task_groups.all()
        if time_slot_id:
            queryset = queryset.filter(time_slot_id=time_slot_id)
            
        serializer = TaskGroupWithSignoffsSerializer(
            queryset, 
            many=True, 
            context={'today': today}
        )
        return serializer.data
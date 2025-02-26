# scheduler/serializers.py
from rest_framework import serializers
from .models import Index, TeamMember, Job

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
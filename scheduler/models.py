# scheduler/models.py
from django.db import models
from django.contrib.auth.models import User

class Index(models.Model):
    """Model representing an index that needs to be calculated or maintained."""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class TeamMember(models.Model):
    """Model representing a team member."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.name

class Job(models.Model):
    """Model representing a scheduled job for an index."""
    index = models.ForeignKey(Index, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    assigned_to = models.ForeignKey(
        TeamMember, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='assigned_jobs'
    )
    color = models.CharField(max_length=20, default='#3174ad')  # For calendar display
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.index.name} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"
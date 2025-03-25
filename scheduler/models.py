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

# New models for the runbook tasks

class Company(models.Model):
    """Model representing a company for which tasks are performed."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name_plural = "Companies"

class TimeSlot(models.Model):
    """Model representing a time slot (Morning, Afternoon 1, etc.)."""
    name = models.CharField(max_length=50, unique=True)
    order = models.IntegerField(default=0)  # For sorting time slots in correct order
    
    def __str__(self):
        return self.name
        
    class Meta:
        ordering = ['order']

class TaskGroup(models.Model):
    """Model representing a group of related tasks."""
    name = models.CharField(max_length=200)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='task_groups')
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    dallas_time = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return f"{self.company.name} - {self.name} ({self.time_slot.name})"
    
    class Meta:
        unique_together = ('name', 'company', 'time_slot')

class Task(models.Model):
    """Model representing an individual task within a task group."""
    task_group = models.ForeignKey(TaskGroup, on_delete=models.CASCADE, related_name='tasks')
    description = models.CharField(max_length=500)
    order = models.IntegerField(default=0)  # For preserving the order of tasks
    
    def __str__(self):
        return self.description
        
    class Meta:
        ordering = ['order']

class TaskSignOff(models.Model):
    """Model for tracking when task groups are signed off by team members."""
    task_group = models.ForeignKey(TaskGroup, on_delete=models.CASCADE, related_name='signoffs')
    team_member = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name='signoffs')
    sign_off_date = models.DateTimeField(auto_now_add=True)
    completed_date = models.DateField()  # The date for which tasks were completed
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.task_group} - Signed by {self.team_member.name} on {self.sign_off_date.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        unique_together = ('task_group', 'team_member', 'completed_date')
        ordering = ['-sign_off_date']
# scheduler/admin.py
from django.contrib import admin
from .models import (
    Index, TeamMember, Job, 
    Company, TimeSlot, TaskGroup, Task, TaskSignOff
)

@admin.register(Index)
class IndexAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('index', 'title', 'start_time', 'end_time', 'assigned_to')
    list_filter = ('index', 'assigned_to', 'start_time')
    search_fields = ('title', 'index__name', 'assigned_to__name')
    date_hierarchy = 'start_time'

# Admin classes for new models

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)
    ordering = ('order',)

class TaskInline(admin.TabularInline):
    model = Task
    extra = 1
    ordering = ('order',)

@admin.register(TaskGroup)
class TaskGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'time_slot', 'dallas_time')
    list_filter = ('company', 'time_slot')
    search_fields = ('name', 'company__name')
    inlines = [TaskInline]

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('description', 'task_group', 'order')
    list_filter = ('task_group__company', 'task_group__time_slot')
    search_fields = ('description', 'task_group__name')
    ordering = ('task_group', 'order')

@admin.register(TaskSignOff)
class TaskSignOffAdmin(admin.ModelAdmin):
    list_display = ('task_group', 'team_member', 'sign_off_date', 'completed_date')
    list_filter = ('task_group__company', 'team_member', 'completed_date')
    search_fields = ('task_group__name', 'team_member__name', 'notes')
    date_hierarchy = 'sign_off_date'
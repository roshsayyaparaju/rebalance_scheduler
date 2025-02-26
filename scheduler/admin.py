# scheduler/admin.py
from django.contrib import admin
from .models import Index, TeamMember, Job

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
# this_week_data.py - place this file in the project root directory (same level as manage.py)
import os
import django
from datetime import datetime, timedelta
import random

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User
from scheduler.models import Index, TeamMember, Job

def create_this_week_data():
    # Check if data already exists
    if Job.objects.count() > 0:
        print("Jobs already exist. Clearing existing jobs...")
        Job.objects.all().delete()
    
    # Make sure indexes and team members exist
    if Index.objects.count() == 0 or TeamMember.objects.count() == 0:
        create_base_data()
    
    # Get all indexes and members
    all_indexes = list(Index.objects.all())
    all_members = list(TeamMember.objects.all())
    
    # Define colors for different indexes
    colors = ['#3174ad', '#ff6b6b', '#5cb85c', '#f0ad4e', '#9467bd']
    
    # Calculate this week's date range
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    
    job_count = 0
    
    # Create jobs for each day of this week
    for day in range(7):  # Monday to Sunday
        current_date = start_of_week + timedelta(days=day)
        
        # Day name for readable output
        day_name = current_date.strftime('%A')
        
        # Morning index calculation (9 AM)
        morning_index = random.choice(all_indexes)
        morning_start = current_date + timedelta(hours=9)
        morning_end = morning_start + timedelta(hours=2)
        
        # Create the morning job
        Job.objects.create(
            index=morning_index,
            title=f"{morning_index.name} Morning Update",
            start_time=morning_start,
            end_time=morning_end,
            assigned_to=random.choice(all_members) if random.random() > 0.3 else None,
            color=colors[all_indexes.index(morning_index) % len(colors)],
            notes=f"{day_name} morning {morning_index.name} calculation"
        )
        job_count += 1
        
        # Afternoon index calculation (2 PM)
        afternoon_index = random.choice([idx for idx in all_indexes if idx != morning_index])
        afternoon_start = current_date + timedelta(hours=14)
        afternoon_end = afternoon_start + timedelta(hours=2)
        
        # Create the afternoon job
        Job.objects.create(
            index=afternoon_index,
            title=f"{afternoon_index.name} Afternoon Review",
            start_time=afternoon_start,
            end_time=afternoon_end,
            assigned_to=random.choice(all_members) if random.random() > 0.3 else None,
            color=colors[all_indexes.index(afternoon_index) % len(colors)],
            notes=f"{day_name} afternoon {afternoon_index.name} review"
        )
        job_count += 1
        
        # Add an extra job on Wednesday (team meeting)
        if day == 2:  # Wednesday
            meeting_start = current_date + timedelta(hours=11)
            meeting_end = meeting_start + timedelta(hours=1)
            
            Job.objects.create(
                index=all_indexes[0],  # Use first index
                title="Team Coordination Meeting",
                start_time=meeting_start,
                end_time=meeting_end,
                assigned_to=None,  # All team members attend
                color="#8a2be2",  # Different color for meetings
                notes="Weekly team coordination meeting"
            )
            job_count += 1
    
    print(f"Created {job_count} jobs for this week (from {start_of_week.strftime('%Y-%m-%d')} to {(start_of_week + timedelta(days=6)).strftime('%Y-%m-%d')})")

def create_base_data():
    # Create admin user if not exists
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')
        print("Created admin user")
    
    # Create indexes
    indexes = [
        {"name": "Market Index", "description": "Weekly market performance index calculation"},
        {"name": "Customer Satisfaction", "description": "Monthly customer satisfaction index"},
        {"name": "Product Quality", "description": "Weekly product quality metrics"},
        {"name": "Supply Chain", "description": "Bi-weekly supply chain efficiency index"},
        {"name": "Employee Engagement", "description": "Quarterly employee engagement metrics"}
    ]
    
    for index_data in indexes:
        Index.objects.get_or_create(
            name=index_data["name"],
            defaults={"description": index_data["description"]}
        )
    
    # Create team members
    team_members = [
        {"name": "John Doe", "email": "john@example.com"},
        {"name": "Jane Smith", "email": "jane@example.com"},
        {"name": "Michael Johnson", "email": "michael@example.com"},
        {"name": "Sarah Williams", "email": "sarah@example.com"},
        {"name": "Robert Brown", "email": "robert@example.com"}
    ]
    
    for member_data in team_members:
        TeamMember.objects.get_or_create(
            email=member_data["email"],
            defaults={"name": member_data["name"]}
        )
    
    print(f"Created {len(indexes)} indexes and {len(team_members)} team members")

if __name__ == "__main__":
    create_this_week_data()
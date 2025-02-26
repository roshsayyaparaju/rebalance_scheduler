# load_sample_data.py - place this file in the project root directory (same level as manage.py)
import os
import django
from datetime import datetime, timedelta
import random

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User
from scheduler.models import Index, TeamMember, Job

def create_sample_data():
    # Create superuser for admin access
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
    
    # Get created objects
    all_indexes = list(Index.objects.all())
    all_members = list(TeamMember.objects.all())
    
    # Define colors for different indexes
    colors = ['#3174ad', '#ff6b6b', '#5cb85c', '#f0ad4e', '#9467bd']
    
    # Create jobs for the next 30 days
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    job_count = 0
    
    # Delete existing jobs to avoid duplication when running script multiple times
    Job.objects.all().delete()
    
    for day in range(30):
        current_date = today + timedelta(days=day)
        
        # Weekly indexes on Mondays
        if current_date.weekday() == 0:  # Monday
            for i, index in enumerate([all_indexes[0], all_indexes[2]]):
                start = current_date + timedelta(hours=9 + i*2)
                end = start + timedelta(hours=2)
                
                Job.objects.create(
                    index=index,
                    title=f"{index.name} Calculation",
                    start_time=start,
                    end_time=end,
                    assigned_to=random.choice(all_members) if random.random() > 0.3 else None,
                    color=colors[i % len(colors)],
                    notes=f"Regular weekly calculation for {index.name}"
                )
                job_count += 1
        
        # Bi-weekly supply chain index (every other Thursday)
        if current_date.weekday() == 3 and (day // 7) % 2 == 0:  # Thursday, every other week
            start = current_date + timedelta(hours=13)
            end = start + timedelta(hours=3)
            
            Job.objects.create(
                index=all_indexes[3],
                title=f"{all_indexes[3].name} Analysis",
                start_time=start,
                end_time=end,
                assigned_to=random.choice(all_members) if random.random() > 0.3 else None,
                color=colors[3 % len(colors)],
                notes=f"Bi-weekly analysis for {all_indexes[3].name}"
            )
            job_count += 1
        
        # Monthly customer satisfaction index (1st of month)
        if current_date.day == 1:
            start = current_date + timedelta(hours=10)
            end = start + timedelta(hours=4)
            
            Job.objects.create(
                index=all_indexes[1],
                title=f"Monthly {all_indexes[1].name} Review",
                start_time=start,
                end_time=end,
                assigned_to=random.choice(all_members) if random.random() > 0.3 else None,
                color=colors[1 % len(colors)],
                notes=f"Monthly review for {all_indexes[1].name}"
            )
            job_count += 1
        
        # Quarterly employee engagement (first Monday of quarter)
        if current_date.day <= 7 and current_date.weekday() == 0 and current_date.month in [1, 4, 7, 10]:
            start = current_date + timedelta(hours=14)
            end = start + timedelta(hours=3)
            
            Job.objects.create(
                index=all_indexes[4],
                title=f"Quarterly {all_indexes[4].name}",
                start_time=start,
                end_time=end,
                assigned_to=random.choice(all_members) if random.random() > 0.3 else None,
                color=colors[4 % len(colors)],
                notes=f"Quarterly analysis for {all_indexes[4].name}"
            )
            job_count += 1
    
    print(f"Created {len(indexes)} indexes, {len(team_members)} team members, and {job_count} jobs")

if __name__ == "__main__":
    create_sample_data()
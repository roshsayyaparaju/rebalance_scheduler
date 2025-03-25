# import_tasks.py - improved version
import os
import django
import pandas as pd
import numpy as np
from datetime import datetime

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from scheduler.models import Company, TimeSlot, TaskGroup, Task

def import_tasks_from_excel():
    """Import task data from the Runbook.xlsx file with improved hierarchy handling."""
    try:
        print("Starting task import from Runbook.xlsx...")
        
        # Clear existing data first
        print("Clearing existing task data...")
        Task.objects.all().delete()
        TaskGroup.objects.all().delete()
        
        # Read Excel file
        excel_file = 'Runbook.xlsx'
        df = pd.read_excel(excel_file, sheet_name='Runbook')
        
        print("Excel columns:", df.columns.tolist())
        
        # First, create the time slots
        time_slots = {
            'Morning': 1,
            'Afternoon 1': 2,
            'Afternoon 2': 3,
            'T3': 4,  # Special time slot found in the data
        }
        
        for name, order in time_slots.items():
            TimeSlot.objects.get_or_create(name=name, defaults={'order': order})
        
        # Get all time slots from database
        time_slots_db = {ts.name: ts for ts in TimeSlot.objects.all()}
        
        # Identify column names
        company_col = 'Customer'
        time_slot_col = 'Unnamed: 1'  # This is the second column with time of day
        task_col = 'Task'
        time_col = 'Dallas Time'
        
        print(f"Using columns: Company='{company_col}', TimeSlot='{time_slot_col}', Task='{task_col}', Time='{time_col}'")
        
        # Initial cleanup - replace NaN values with empty strings
        df = df.fillna('')
        
        # Process the data
        task_groups_created = 0
        tasks_created = 0
        
        # Group rows by company and time slot
        current_company = None
        current_time_slot = None
        current_task_group = None
        is_main_task = False
        
        for i, row in df.iterrows():
            company_name = str(row[company_col]).strip()
            time_slot_name = str(row[time_slot_col]).strip()
            task_desc = str(row[task_col]).strip()
            dallas_time = row[time_col] if pd.notna(row[time_col]) else None
            
            # Skip rows without task description
            if not task_desc:
                continue
                
            # Update current company if provided
            if company_name:
                current_company = company_name
                is_main_task = True  # New company always starts a main task
            
            # Update current time slot if provided and valid
            if time_slot_name and time_slot_name in time_slots_db:
                current_time_slot = time_slot_name
                is_main_task = True  # New time slot always starts a main task
            
            # Skip if no valid company or time slot context
            if not current_company or not current_time_slot:
                continue
            
            # Get or create the company
            company_obj, _ = Company.objects.get_or_create(name=current_company)
            time_slot_obj = time_slots_db[current_time_slot]
            
            # Format dallas_time if needed
            formatted_dallas_time = None
            if dallas_time is not None:
                if isinstance(dallas_time, (int, float)):
                    # Convert Excel time (decimal) to HH:MM
                    hours = int(dallas_time * 24)
                    minutes = int((dallas_time * 24 * 60) % 60)
                    formatted_dallas_time = f"{hours:02d}:{minutes:02d}"
                elif isinstance(dallas_time, str):
                    formatted_dallas_time = dallas_time
            
            # If this is a main task, create a new task group
            if is_main_task or current_task_group is None:
                task_group, created = TaskGroup.objects.get_or_create(
                    company=company_obj,
                    time_slot=time_slot_obj,
                    name=task_desc,
                    defaults={'dallas_time': formatted_dallas_time}
                )
                current_task_group = task_group
                
                if created:
                    task_groups_created += 1
                    
                # Don't add the main task as a subtask (to avoid duplication)
                is_main_task = False  # Reset for next rows
                
            else:
                # This is a subtask, add it to the current task group
                task_count = Task.objects.filter(task_group=current_task_group).count()
                task, created = Task.objects.get_or_create(
                    task_group=current_task_group,
                    description=task_desc,
                    defaults={'order': task_count}
                )
                
                if created:
                    tasks_created += 1
            
            # Check if next row indicates a new main task
            if i < len(df) - 1:
                next_row = df.iloc[i+1]
                next_company = str(next_row[company_col]).strip()
                next_time_slot = str(next_row[time_slot_col]).strip()
                
                if next_company or next_time_slot:
                    is_main_task = True  # Next row starts a new main task
        
        # Print summary
        print(f"Import completed successfully.")
        print(f"Companies: {Company.objects.count()}")
        print(f"Time slots: {TimeSlot.objects.count()}")
        print(f"Created {task_groups_created} task groups")
        print(f"Created {tasks_created} subtasks")
        
    except Exception as e:
        print(f"Error importing tasks: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import_tasks_from_excel()
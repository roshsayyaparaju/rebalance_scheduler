# Job Scheduler Application

A team job scheduler application built with Django (backend) and React (frontend). The application allows teams to manage indexes that need to be calculated/maintained on specific dates and assign team members to these jobs.

## Features

- Calendar view showing scheduled jobs with month/week/day views
- Job creation and management
- Team member assignment
- Index management
- Color-coded job visualization

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup

1. Clone the repository and navigate to the project directory:

   ```bash
   git clone <repository-url>
   cd job_scheduler
   ```

2. Create and activate a virtual environment:

   ```bash
   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate

   # On Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Run database migrations:

   ```bash
   python manage.py makemigrations scheduler
   python manage.py migrate
   ```

5. (Optional) Load sample data:

   ```bash
   # For general sample data over the next 30 days
   python load_sample_data.py

   # Or for data specifically for the current week
   python this_week_data.py
   ```

6. Start the Django development server:
   ```bash
   python manage.py runserver
   ```
   The backend will be running at http://localhost:8000/

### Frontend Setup

1. Open a new terminal window, navigate to the frontend directory:

   ```bash
   cd frontend
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Start the React development server:
   ```bash
   npm start
   ```
   The frontend will be running at http://localhost:3000/

## Usage

### Accessing the Application

- **Main Application**: http://localhost:3000/
- **Django Admin Panel**: http://localhost:8000/admin/
  - Username: admin
  - Password: adminpassword (if using sample data)

### Creating Jobs

1. Click on "Add New Job" button in the calendar view
2. Fill in the job details:
   - Title
   - Select an index
   - Set start and end times
   - Assign to a team member (optional)
   - Add notes (optional)
   - Choose a color
3. Click "Create Job"

### Assigning Team Members

1. Click on a job in the calendar
2. Select a team member from the dropdown
3. Click "Save Assignment"

### Managing Team Members and Indexes

Use the respective tabs in the navigation bar to add, edit, or delete team members and indexes.

## Project Structure

```
job_scheduler/
├── backend/              # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── scheduler/            # Django app for job scheduling
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── ...
├── frontend/             # React frontend application
│   ├── src/
│   │   ├── components/   # React components
│   │   └── ...
│   └── ...
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
├── load_sample_data.py   # Script to load sample data
└── this_week_data.py     # Script to load data for current week
```

## Creating requirements.txt

If you make changes to the backend and need to update the requirements.txt file:

```bash
# Activate your virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Generate the requirements.txt file
pip freeze > requirements.txt
```

## Development Notes

- The backend uses Django REST Framework to provide a RESTful API
- CORS is enabled in development mode for all origins (restrict this in production)
- The frontend uses react-big-calendar for the calendar view
- Sample data scripts can be modified to create custom job patterns

## Troubleshooting

### Backend Issues

- **Database migration errors**: Delete the db.sqlite3 file and migration files in scheduler/migrations/ (except **init**.py), then run migrations again.
- **ModuleNotFoundError**: Make sure you're running commands from the project root and the virtual environment is activated.

### Frontend Issues

- **Module not found errors**: Make sure all dependencies are installed with `npm install`.
- **API connection errors**: Verify the backend server is running and accessible.

## Production Deployment

For production deployment:

1. Set `DEBUG = False` in backend/settings.py
2. Configure a proper database (PostgreSQL recommended)
3. Set up proper CORS settings in backend/settings.py
4. Build the React app with `npm run build` and serve it with a web server
5. Configure a WSGI server (like Gunicorn) for Django
6. Set up a reverse proxy (like Nginx) in front of everything

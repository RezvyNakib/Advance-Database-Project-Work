# Student Exchange Program Management System

A web-based Student Exchange Program Management System built with Python Flask and SQLite.

## Features

### 3 Separate Interfaces:
1. **Student Panel** - Register, Login, Apply to exchange programs
2. **Coordinator Panel** - Login, View applications, Approve/Reject
3. **University Panel** - Login, Manage coordinators, Manage programs, View all applications

## Demo Credentials

| Role | Username | Password |
|------|----------|----------|
| Student | nakib | nakib123 |
| Coordinator | fan_coord | fan123 |
| University | aiub_uni | aiub123 |

## Tech Stack

- **Backend:** Python Flask
- **Frontend:** HTML, CSS
- **Database:** SQLite

## How to Run Locally

```bash
# Clone the repository
git clone https://github.com/RezvyNakib/Advance-Database-Project-Work.git

# Navigate to project folder
cd Advance-Database-Project-Work

# Install requirements
pip install -r requirements.txt

# Run the application
python app.py

# Open browser
http://localhost:5000
```

## How to Deploy Online (Render.com)

1. Go to [render.com](https://render.com) and create free account
2. Click **New** → **Web Service**
3. Connect your GitHub repository: `https://github.com/RezvyNakib/Advance-Database-Project-Work`
4. Settings:
   - **Name:** student-exchange-system
   - **Runtime:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. Click **Create Web Service**
6. Wait 2-3 minutes for deployment
7. Get your free link: `https://student-exchange-system.onrender.com`

## Project Structure

```
student_exchange_system/
├── app.py              # Main Flask application
├── db_config.py        # Database configuration
├── requirements.txt    # Python dependencies
├── render.yaml         # Render deployment config
├── static/
│   └── style.css       # CSS styling
└── templates/
    ├── landing.html         # Homepage
    ├── student_login.html   # Student login
    ├── student_register.html # Student registration
    ├── student_dashboard.html # Student dashboard
    ├── coordinator_login.html # Coordinator login
    ├── coordinator_register.html # Coordinator registration
    ├── coordinator_dashboard.html # Coordinator dashboard
    ├── university_login.html # University login
    ├── university_register.html # University registration
    ├── university_dashboard.html # University dashboard
    └── database_viewer.html # Database viewer
```

## Group Members

| Name | ID | Contribution |
|------|-----|-------------|
| Md Rezvine Enjoy Nakib | 23-50573-1 | 25% |
| MST Nusrat Jahan Nijhum | 23-51211-1 | 25% |
| Md Mahay Alam Hasib | 23-53246-3 | 25% |
| Sani Alam | 22-48445-3 | 25% |

**Course:** Advanced Database Management System (ADBMS)
**Section:** A
**Group:** 7
**Summer:** 2025-2026
**Teacher:** JUENA AHMED NOSHIN

<<<<<<< HEAD
# Abuyog Community College - Health & Medical Record System

A full-stack Flask web application featuring Role-Based Access Control (RBAC) and a *Mobile Legends: Bang Bang* inspired UI design theme.

## Features
- **Role-Based Access Control (RBAC)**: Supports `Super Admin`, `Medical Expert`, and `Student`.
- **Super Admin**: User management (Create, Edit, Deactivate, Role Assignment), System Audit Logs, Health Metrics Analytics.
- **Medical Expert**: Manage Student Medical Records, Review Appointments/Health Requests, Issue Medical Clearances.
- **Student**: View personal medical history, submit health/appointment requests, update personal profile.
- **Security**: Password hashing using Werkzeug, Session-based authentication via Flask-Login, Role protection decorators.

---

## Folder Structure

```
abuyog_cc_health_system/
│
├── app.py                  # Application factory and initialization
├── models.py               # Database models (User, Role, MedicalRecord, HealthRequest, AuditLog)
├── decorators.py           # Custom RBAC protection decorators
├── requirements.txt        # Python dependencies
├── README.md               # Setup and usage guide
│
├── routes/
│   ├── __init__.py
│   ├── auth.py             # Login, Logout, Profile routes
│   ├── admin.py            # Super Admin user management & audit logs
│   ├── medical.py          # Medical Expert records & approvals
│   └── student.py          # Student health requests & personal records
│
├── static/
│   ├── css/
│   │   └── style.css       # MLBB Theme Stylesheet (Dark, Gold, Glowing UI)
│   └── js/
│       └── main.js        # Dynamic UI scripts and helper interactions
│
└── templates/
    ├── base.html           # Base layout template
    ├── login.html          # MLBB Cyber-themed Login page
    ├── dashboard.html      # Main dynamic dashboard template
    ├── admin_users.html    # User management panel
    ├── medical_records.html# Medical records management
    └── health_request.html # Student health request submission form
```

---

## Step-by-Step Setup and Execution Guide

### Prerequisites
- Python 3.8 or higher installed on your system.

### 1. Create a Virtual Environment
Navigate to the project root folder in your terminal/command prompt and run:

**On Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
Start the Flask development server:
```bash
python app.py
```

The database (`abuyog_health.db`) will be automatically created and populated with default seed data on first launch!

### 4. Access the Web Application
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## Default Login Credentials (Seeded Automatically)

| Role | Username | Password |
| :--- | :--- | :--- |
| **Super Admin** | `admin` | `admin123` |
| **Medical Expert** | `doc_smith` | `doc123` |
| **Student** | `student1` | `student123` |

---

## How RBAC Logic Works & Scalability

### 1. Role Model & User Association
Roles are stored in the database (`Role` table) and associated with Users through a Many-to-Many or Foreign Key relation (`role_id` on `User`).

### 2. Modern Custom Decorator Protection (`decorators.py`)
Custom decorators inspect the current logged-in user's role before executing any route function:

```python
from functools import wraps
from flask import abort
from flask_login import current_user

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return abort(401)
            if current_user.role.name not in roles:
                return abort(403) # Forbidden
            return f(*args, **kwargs)
        return decorated_function
    return decorator
```

### 3. Adding a New Role in the Future
To add a new role (e.g., `Faculty` or `Department Head`):
1. **Database Insertion**: Add the new role name into the `Role` table during database setup or via Super Admin panel:
   ```python
   new_role = Role(name='Faculty', description='ACC Faculty Member')
   db.session.add(new_role)
   db.session.commit()
   ```
2. **Create Routes**: Create a new blueprint in `routes/faculty.py` or protect existing endpoints using the decorator:
   ```python
   @faculty_bp.route('/faculty/dashboard')
   @login_required
   @role_required('Faculty', 'Super Admin')
   def faculty_dashboard():
       return render_template('faculty_dashboard.html')
   ```
3. **Template Navigation**: Use standard Jinja condition checks to render role-specific sidebar navigation items:
   ```jinja2
   {% if current_user.role.name == 'Faculty' %}
       <a href="{{ url_for('faculty.faculty_dashboard') }}">Faculty Hub</a>
   {% endif %}
   ```
=======
# ACC_Consultation_System
 ABUYOG COMMUNITY COLLEGE CONSULTATION SYSTEM
>>>>>>> bb83b4bc02c5c24066afea3fd0948fe6730d7275

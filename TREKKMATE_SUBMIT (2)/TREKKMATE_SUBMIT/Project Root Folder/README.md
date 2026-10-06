
# ⛰️ TREKKMATE

**A Trek Management System**

## Project Details

- **Project Name:** TREKKMATE
- **Roll No:** 24F3000141
- **Name:** Nishant Girhepunje

## Technologies Used

- **Backend:** Python 3, Flask 3.0.0
- **Frontend:** HTML5, Bootstrap 5.3.0, Custom CSS
- **Database:** SQLite
- **Templating:** Jinja2 (Flask default)
  
## How to Run

### Step 1: Install Requirements

```bash
pip install flask
```

### Step 2: Run the Application

```bash
python app.py
```

### Step 3: Open in Browser

```
http://127.0.0.1:5000
```

### Step 4: Seed the Database (Optional)

```bash
python seed.py
```

This creates sample data for testing.

---

## Features

### Admin Dashboard
- View all stats (treks, staff, users, bookings)
- Manage treks (add, edit, delete, assign staff)
- Manage staff (approve, blacklist, delete)
- Manage users (blacklist, activate, delete)
- View all bookings
- Search functionality

### Staff Dashboard
- View assigned treks
- Update trek details
- Manage trek slots and status
- View participants

### User Dashboard
- Browse available treks
- Filter treks by difficulty and location
- Book treks
- View booking history
- Edit profile

---

## Project Structure

```
TREKKMATE/
├── app.py                  # Main application file
├── database.py             # Database setup and queries
├── seed.py                 # Sample data seeder
├── requirements.txt        # Python packages
├── README.md               # This file
├── static/
│   └── css/
│       └── style.css       # Custom styles
├── templates/
│   ├── base.html           # Base template
│   ├── home.html           # Landing page
│   ├── login.html          # Login page
│   ├── register.html       # Registration page
│   ├── admin/              # Admin templates
│   ├── staff/              # Staff templates
│   └── user/               # User templates
```

---

## Sample Login Credentials

After running `python seed.py`:

| Role   | Username | Password |
|--------|----------|----------|
| Admin  | admin    | admin123 |
| Staff  | rahul_guide | rahul123 |
| User   | rishabh  | rishabh123 |


=======
# TREKKMATE - Trekking Management Application

**Name:** Nishant Girhepunje
**Roll No:** 24F3000141

## About

TREKKMATE is a web application for managing trekking activities. It allows Admin, Trek Staff, and Users (Trekkers) to interact with the system based on their roles. The application handles trek creation, booking, staff management, and maintains complete trekking history.

## Technologies Used

- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, Bootstrap 5, Jinja2 templating
- **Database:** SQLite (created programmatically)

## How to Run

```bash
cd "Project Root Folder"
pip install flask
python app.py
```

Then open browser and go to: http://127.0.0.1:5000

## Default Admin Login

| Username | Password |
|----------|----------|
| admin    | admin123 |

## Features

### Admin
- Dashboard with stats (total treks, users, staff, bookings)
- Add, edit, delete treks
- Approve staff registration
- Blacklist/activate staff and users
- Assign staff to treks
- Search treks, users, and staff
- View all bookings

### Trek Staff
- View assigned treks
- Update available slots
- Update trek status (Open/Closed/Completed)
- View registered participants

### User (Trekker)
- Browse and filter treks by difficulty and location
- Book treks
- Cancel bookings
- View booking status and trek history
- Edit profile

## Project Structure

```
Project Root Folder/
├── app.py              # Main Flask application with all routes
├── database.py         # Database connection and table creation
├── static/css/style.css
└── templates/
    ├── base.html       # Base template with navbar
    ├── home.html       # Landing page
    ├── login.html      # Login form
    ├── register.html   # Registration form
    ├── admin/          # Admin templates
    │   ├── dashboard.html
    │   ├── treks.html
    │   ├── add_trek.html
    │   ├── edit_trek.html
    │   ├── assign_staff.html
    │   ├── staff.html
    │   ├── users.html
    │   ├── bookings.html
    │   └── search.html
    ├── staff/          # Staff templates
    │   ├── dashboard.html
    │   └── trek_detail.html
    └── user/           # User templates
        ├── dashboard.html
        ├── treks.html
        ├── profile.html
        └── history.html
```

## Database Tables

### users
| Field | Type | Description |
|-------|------|-------------|
| id | INTEGER | Primary key, auto increment |
| username | TEXT | Unique username |
| password | TEXT | User password |
| full_name | TEXT | Full name |
| email | TEXT | Email address |
| phone | TEXT | Phone number |
| role | TEXT | admin / staff / user |
| status | TEXT | active / pending / blacklisted |
| created_at | TEXT | Registration timestamp |

### treks
| Field | Type | Description |
|-------|------|-------------|
| id | INTEGER | Primary key, auto increment |
| name | TEXT | Trek name |
| location | TEXT | Trek location |
| difficulty | TEXT | Easy / Moderate / Hard |
| duration | INTEGER | Duration in days |
| total_slots | INTEGER | Total available slots |
| available_slots | INTEGER | Current available slots |
| staff_id | INTEGER | Foreign key to users |
| status | TEXT | Pending / Open / Closed / Completed |
| start_date | TEXT | Trek start date |
| end_date | TEXT | Trek end date |
| description | TEXT | Trek description |
| price | REAL | Trek price in Rs. |
| created_at | TEXT | Creation timestamp |

### bookings
| Field | Type | Description |
|-------|------|-------------|
| id | INTEGER | Primary key, auto increment |
| user_id | INTEGER | Foreign key to users |
| trek_id | INTEGER | Foreign key to treks |
| booking_date | TEXT | Booking timestamp |
| status | TEXT | Booked / Cancelled / Completed |
>>>>>>> 830b3c25dba837d39268c020bd5e5c70991a237e

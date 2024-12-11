# Hive Activity Management System

## Overview
Hive Activity Management System is a Django-based web application designed to facilitate project and activity management. It allows users to collaborate, track progress, and manage tasks effectively. The system features role-based access control with multiple user groups to ensure secure and streamlined operations.

### Key Features
- **User Authentication and Role-Based Access Control:** Users are assigned roles (e.g. Viewer, Team Member, Project Manager, Staff Admin, Super Admin) with varying levels of permissions.
- **Activity Management:** Create, track, and manage tasks and activities.
- **Project Organization:** Group activities into projects with collaborative features.
- **Team Collaboration:** Leave notes on activities to communicate with team members.
- **Data Export:** Export project data in CSV and Excel formats.
- **Profile Management:** Customize user profiles and permissions.
- **Unregistered User Access:** Basic task management functionality for unregistered users, with data persistence limited to the session.

## Prerequisites
- **Python 3.x**
- **Django 4.x**
- **PostgreSQL**

## Installation

### Step 1: Clone or Download the Repository
```bash
git clone <your-repository-url>
cd <project-directory>
```

### Step 2: Create and Activate a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Create a `.env` file in the root directory and add the required environment variables as per the secret key provided earlier.

### Step 5: Run Migrations
```bash
python manage.py migrate
```

### Step 6: Create Test Users
For testing purposes, you can create test users for each role:
```bash
python manage.py create_testing_users
```
This will create the following users (password for all: `123admin123`):
- Viewer: `viewer@test.com`
- Project Manager: `pm@test.com`
- Team Member: `team@test.com`
- Staff Admin: `staff@test.com`
- Super Admin: `super@test.com`

## Usage

### Step 1: Start the Development Server
```bash
python manage.py runserver
```

### Step 2: Access the Application
Open your browser and navigate to: [http://localhost:8000](http://localhost:8000)

## User Roles

### 1. **Unregistered Users**
- Can create a basic list of activities.
- Activities can be exported but are not saved beyond the session.

### 2. **Viewer**
- View-only access to information shared by their team.

### 3. **Team Member**
- Default role for newly registered users.
- Can create and manage activities and notes.
- Can request a role change.

### 4. **Project Manager**
- Has the same scope as team members in addition to:
- Can create projects and add/remove team members to them.

### 4. **Staff Admin**
- Can approve role changes for Team Members.
- CRUD permissions for models visible to application users.
- Can only perform administrative tasks through the admin panel.
- `is_staff = True`

### 5. **Super Admin**
- Full access to all features both on the application and admin side.
- Can manage user roles and permissions, including Staff Admin assignments.
- Superusers must manually assign themselves to the Super Admin group via the admin panel if created through the superuser command.

## Group Setup
To set up user groups and permissions, you can:
1. Use the signal that creates groups after migrations (`post_migrate`).
2. Apply the migration file: `0009_20241204_create_groups.py`.
3. Load the fixture: `groups_permissions.json`.

## Notes
1. **Superusers:**
   - Upon creation, superusers must be assigned to the Super Admin group manually via the admin panel or by running the `command fix_user_groups`.
   - Ensure at least one Staff Admin user is created, as some functionalities are exclusive to them.

2. **Export Functionality:**
   - Both registered and unregistered users can export their data in CSV and Excel formats.

3. **Security:**
   - Critical administrative actions are restricted to the admin panel to ensure data integrity and prevent accidental deletions.


## Contributions
Feel free to contribute! Fork the repository, make your changes, and submit a pull request.

---
Thank you for using Hive Activity Management System!


# Team Task Manager

A collaborative task management web application built using **Python, Flask, SQLite, HTML, and CSS**.  
The application allows users to create projects, manage tasks, assign members, and track task progress through a simple dashboard system.

---

## Features

### Authentication System
- User Registration
- User Login
- Logout Functionality
- Session Management
- Protected Routes

---

### Project Management
- Create Projects
- View Project Dashboard
- Project-based Access Control
- Admin Ownership System

---

### Task Management (CRUD)
- Create Tasks
- View Tasks
- Update Task Status
- Delete Tasks

---

### Task Status Workflow
- To Do
- In Progress
- Done

---

### Dashboard Analytics
- Total Tasks Count
- Tasks By Status
- Shared Project Visibility

---

### Member Collaboration System
- Add Members To Projects
- Shared Project Access
- Role-Based Permissions
- Admin-Only Controls

---

## Tech Stack

### Backend
- Python
- Flask
- SQLite

### Frontend
- HTML
- CSS
- Jinja Templates

---

## Database Tables

### users
Stores user account information.

### projects
Stores project details and admin ownership.

### tasks
Stores task information related to projects.

### project_members
Stores project-member relationships.

---

## Project Structure

```text
Team Task Manager/
│
├── app.py
├── database.db
├── requirements.txt
├── Procfile
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── create_project.html
│   ├── project.html
│   ├── create_task.html
│   └── add_member.html
│
├── static/
│   └── style.css
```

---

## How To Run Locally

### 1. Clone Repository

```bash
git clone <your-github-repo-link>
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Run Application

```bash
python app.py
```

---

### 4. Open In Browser

```text
http://127.0.0.1:5000
```

---

## Deployment

The application is deployed using **Railway**.

---

## Future Improvements

- Task Assignment To Specific Members
- File Attachments
- Notifications
- Due Date Reminders
- Better UI/UX
- Email Invitations
- Activity Logs

---

## Learning Outcomes

This project helped in understanding:
- Flask Routing
- CRUD Operations
- Session Management
- Authentication & Authorization
- SQL Queries
- Joins & Relationships
- Many-to-Many Database Design
- Dynamic Rendering Using Jinja
- Full Stack Web Development Basics

---

## Author

Shivansh Parmar

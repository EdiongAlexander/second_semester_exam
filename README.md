#### Project Title:
# EduTrack Lite API

## Description:
This system allows users to register for courses, track course completion, and manage course information. It supports CRUD operations and enforces simple validation and relationships between the entities.

## Entities:
1. User
id: Unique identifier
name: Full name
email: Email address
is_active: Boolean (default: True)

2. Course
id: Unique identifier
title: Name of the course
description: Brief description
is_open: Whether the course is open for enrollment (default: True)

3. Enrollment
id: Unique identifier
user_id: ID of the enrolling user
course_id: ID of the course
enrolled_date: Date of enrollment
completed: Boolean to indicate if the course was completed (default: False)

## API Endpoints
### 👤 User Endpoints
- CRUD users
- Deactivate user
- 
## 🗓️ Course Endpoints
- CRUD courses:
- Close enrollment: 
- View all users enrolled in a particular course
  
### 📝 Enrollment Endpoints
- Enroll a user in a course:
- Only active users can enroll
- Course must be open
- User cannot enroll twice in the same course
- Mark course completion:
- View enrollments for a user:
- View all enrollments:
  
## ⚙️ Technical Requirements
- Use Pydantic models for validation
- Store data in in-memory lists or dictionaries
- Follow modular structure:
  main.py
  schemas/
  routes/
  services/
- Return appropriate HTTP status codes
- Write test for your endpoints

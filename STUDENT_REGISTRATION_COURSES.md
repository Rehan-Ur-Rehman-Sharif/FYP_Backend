# Student Registration with Course Enrollment - Example

## Overview
This document demonstrates the new course enrollment feature during student registration.

## API Endpoint
```
POST /api/auth/register/student/
```

## Example 1: Registration without courses (backward compatible)
```bash
curl -X POST http://localhost:8000/api/auth/register/student/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "password": "SecurePassword123!",
    "password2": "SecurePassword123!",
    "student_name": "John Doe",
    "rfid": "RFID123456",
    "year": 1,
    "dept": "CS",
    "section": "A"
  }'
```

**Response:**
```json
{
    "message": "Student registered successfully",
    "student_id": 1,
    "email": "john.doe@example.com",
    "student_name": "John Doe",
    "enrolled_courses": []
}
```

## Example 2: Registration with course enrollment
```bash
curl -X POST http://localhost:8000/api/auth/register/student/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "jane.smith@example.com",
    "password": "SecurePassword123!",
    "password2": "SecurePassword123!",
    "student_name": "Jane Smith",
    "rfid": "RFID789012",
    "year": 2,
    "dept": "CS",
    "section": "B",
    "courses": [1, 2, 3]
  }'
```

**Response:**
```json
{
    "message": "Student registered successfully",
    "student_id": 2,
    "email": "jane.smith@example.com",
    "student_name": "Jane Smith",
    "enrolled_courses": [
        {
            "course_id": 1,
            "course_name": "Data Structures",
            "teacher_id": 5,
            "teacher_name": "Dr. Smith"
        },
        {
            "course_id": 2,
            "course_name": "Algorithms",
            "teacher_id": 6,
            "teacher_name": "Dr. Johnson"
        },
        {
            "course_id": 3,
            "course_name": "Database Systems",
            "teacher_id": 7,
            "teacher_name": "Dr. Williams"
        }
    ]
}
```

## Example 3: Validation - Invalid course IDs
```bash
curl -X POST http://localhost:8000/api/auth/register/student/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "bob.jones@example.com",
    "password": "SecurePassword123!",
    "password2": "SecurePassword123!",
    "student_name": "Bob Jones",
    "rfid": "RFID345678",
    "year": 1,
    "dept": "IT",
    "section": "A",
    "courses": [999, 1000]
  }'
```

**Response (400 Bad Request):**
```json
{
    "courses": [
        "The following course IDs do not exist: [999, 1000]"
    ]
}
```

## How It Works

1. **Course Validation**: The system validates that all provided course IDs exist in the Course table before creating the student record.

2. **Teacher Assignment**: For each course, the system looks up the TaughtCourse table to find which teacher teaches that course for the specific year and section of the student.

3. **StudentCourse Creation**: If a teacher is found, a StudentCourse entry is created linking the student to the course with the assigned teacher. The `classes_attended` field is initialized as empty and will be populated as the student attends classes.

4. **Atomic Transaction**: If any course ID is invalid, the entire registration is rejected - no student record or course enrollments are created.

## Prerequisites

Before enrolling students in courses, ensure:
1. Courses exist in the Course table
2. Teachers are assigned to teach those courses via TaughtCourse entries
3. TaughtCourse entries match the student's year and section

## Database Structure

### Course Table
- course_id (Primary Key)
- course_name
- course_code

### TaughtCourse Table
- course (Foreign Key to Course)
- teacher (Foreign Key to Teacher)
- year (e.g., 1, 2, 3, 4)
- section (e.g., A, B, C)
- classes_taken

### StudentCourse Table (Created automatically)
- student (Foreign Key to Student)
- course (Foreign Key to Course)
- teacher (Foreign Key to Teacher)
- classes_attended

## Notes

- The `courses` field is optional - existing registration flows without courses will continue to work
- Only courses with assigned teachers (via TaughtCourse) for the student's year/section will be enrolled
- The system uses bulk operations for efficient database performance
- All validations happen before any database writes (atomic transaction)

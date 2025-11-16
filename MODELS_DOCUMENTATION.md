# Student Attendance Management System - Models Documentation

This document describes the database models implemented for the Student Attendance Management System.

## Overview

The system is designed to track student attendance across multiple courses, manage teachers and their course assignments, and provide administrative capabilities for system management.

## Models

### Department
Represents academic departments within the institution.

**Fields:**
- `name` (CharField): Full department name (unique)
- `code` (CharField): Short department code, e.g., "CS", "EE" (unique)

**Purpose:** Organizes courses and students by academic department.

---

### Course
Represents courses offered by the institution.

**Fields:**
- `course_code` (CharField): Unique course identifier, e.g., "CS101"
- `course_name` (CharField): Full course name
- `department` (ForeignKey): Department offering this course
- `credit_hours` (PositiveIntegerField): Number of credit hours (default: 3)

**Purpose:** Defines the catalog of courses available in each department.

---

### Student
Represents students enrolled in the institution.

**Fields:**
- `roll_number` (CharField): Unique student identifier
- `name` (CharField): Student's full name
- `department` (ForeignKey): Student's department
- `section` (CharField): Class section, e.g., "A", "B"

**Methods:**
- `get_overall_attendance()`: Calculates overall attendance percentage as the average of all enrolled courses

**Purpose:** Maintains student records and tracks their overall attendance.

---

### Teacher
Represents teaching staff.

**Fields:**
- `roll_number` (CharField): Unique teacher identifier
- `name` (CharField): Teacher's full name
- `user` (OneToOneField, optional): Link to Django User for authentication

**Purpose:** Maintains teacher records. Teachers can be assigned to teach course offerings.

---

### CourseOffering
Represents a specific instance of a course being taught in a semester.

**Fields:**
- `course` (ForeignKey): The course being offered
- `teacher` (ForeignKey): Teacher assigned to this offering
- `semester` (CharField): Semester identifier, e.g., "Fall 2024"
- `section` (CharField): Section identifier, e.g., "A"
- `is_active` (BooleanField): Whether this offering is currently active

**Constraints:**
- Unique together: course + semester + section

**Purpose:** Links courses with teachers for a specific semester and section. This allows the same course to be taught by different teachers in different sections or semesters.

---

### CourseEnrollment
Represents a student's enrollment in a specific course offering.

**Fields:**
- `student` (ForeignKey): Enrolled student
- `course_offering` (ForeignKey): The course offering
- `enrollment_date` (DateField): Date of enrollment

**Methods:**
- `get_attendance_percentage()`: Calculates attendance percentage for this specific course

**Constraints:**
- Unique together: student + course_offering

**Purpose:** Tracks which students are enrolled in which course offerings and calculates per-course attendance.

---

### AttendanceRecord
Represents individual attendance records for each class session.

**Fields:**
- `enrollment` (ForeignKey): The course enrollment this record belongs to
- `date` (DateField): Date of the class
- `is_present` (BooleanField): Whether student was present
- `remarks` (TextField, optional): Additional notes, e.g., "late", "excused"

**Constraints:**
- Unique together: enrollment + date

**Purpose:** Records daily attendance for each student in each course. Multiple records per enrollment create a complete attendance history.

---

### Management
Represents system administrators and management personnel.

**Fields:**
- `roll_number` (CharField): Unique management identifier
- `name` (CharField): Full name
- `designation` (CharField): Job title/position
- `user` (OneToOneField, optional): Link to Django User for authentication
- `can_modify_students` (BooleanField): Permission to modify student records
- `can_modify_teachers` (BooleanField): Permission to modify teacher records
- `can_modify_courses` (BooleanField): Permission to modify course records

**Purpose:** Defines system administrators with granular permissions for modifying different types of records.

---

## Relationships

```
Department
├── courses (Course) - One-to-Many
└── students (Student) - One-to-Many

Course
├── department (Department) - Many-to-One
└── offerings (CourseOffering) - One-to-Many

Teacher
└── course_offerings (CourseOffering) - One-to-Many

CourseOffering
├── course (Course) - Many-to-One
├── teacher (Teacher) - Many-to-One
└── enrollments (CourseEnrollment) - One-to-Many

Student
├── department (Department) - Many-to-One
└── enrollments (CourseEnrollment) - One-to-Many

CourseEnrollment
├── student (Student) - Many-to-One
├── course_offering (CourseOffering) - Many-to-One
└── attendance_records (AttendanceRecord) - One-to-Many

AttendanceRecord
└── enrollment (CourseEnrollment) - Many-to-One
```

## Usage Examples

### Calculate Student Overall Attendance
```python
student = Student.objects.get(roll_number="2024-CS-001")
overall_attendance = student.get_overall_attendance()
print(f"{student.name}'s overall attendance: {overall_attendance:.2f}%")
```

### Calculate Course-Specific Attendance
```python
enrollment = CourseEnrollment.objects.get(student=student, course_offering=offering)
course_attendance = enrollment.get_attendance_percentage()
print(f"Attendance in {enrollment.course_offering.course.course_code}: {course_attendance:.2f}%")
```

### Record Attendance
```python
from datetime import date
from core.models import AttendanceRecord

# Mark student as present
AttendanceRecord.objects.create(
    enrollment=enrollment,
    date=date.today(),
    is_present=True
)
```

## Design Considerations

1. **Flexibility**: The CourseOffering model allows the same course to be taught multiple times with different teachers, sections, and semesters.

2. **Data Integrity**: Unique constraints prevent duplicate enrollments and attendance records.

3. **Scalability**: The design can handle multiple departments, courses, students, and teachers without performance issues.

4. **Extensibility**: Additional fields can be easily added to any model to accommodate future requirements.

5. **Permissions**: Management model includes granular permissions for different types of modifications.

6. **Authentication**: Optional User links allow integration with Django's authentication system.

## Testing

The implementation includes comprehensive tests covering:
- Model creation and string representation
- Attendance percentage calculations
- Overall attendance calculation across multiple courses
- Foreign key relationships
- Unique constraints

Run tests with:
```bash
python manage.py test core --settings=FYP_Backend.test_settings
```

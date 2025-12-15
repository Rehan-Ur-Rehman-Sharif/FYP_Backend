# Bulk Student Enrollment API Documentation

This document describes the APIs for enrolling students in courses, both in bulk and individually.

## Overview

The system provides two main endpoints:
1. **Bulk Enrollment**: Enroll multiple students in a course based on filters (year, section, dept) or specific student IDs
2. **Single Student Enrollment**: Enroll a single student in a course

Both endpoints require management user authentication.

## Authentication

All endpoints require authentication using JWT tokens. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

## Endpoints

### 1. Bulk Enrollment

Enroll multiple students in a course based on filters or specific student IDs.

**Endpoint:** `POST /student-courses/bulk_enroll/`

**Permissions:** Management users only

#### Request Body

##### Option 1: Filter by Year, Section, and/or Department

```json
{
  "course_id": 1,
  "year": 2024,
  "section": "B",
  "dept": "CS"  // optional
}
```

##### Option 2: Specific Student IDs

```json
{
  "course_id": 1,
  "student_ids": [1, 2, 3, 4, 5]
}
```

#### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| course_id | integer | Yes | ID of the course to enroll students in |
| year | integer | Conditional* | Filter students by year (e.g., 2024) |
| section | string | Conditional* | Filter students by section (e.g., "A", "B", "C") |
| dept | string | Conditional* | Filter students by department (e.g., "CS", "IT") |
| student_ids | array of integers | Conditional* | Specific list of student IDs to enroll |

*Note: You must provide either filter criteria (year/section/dept) OR student_ids. If student_ids is provided, it takes precedence over filters.

#### Success Response

**Code:** `200 OK`

**Content Example:**

```json
{
  "message": "Bulk enrollment completed",
  "course_name": "Network Information Security",
  "enrolled_count": 15,
  "skipped_count": 2,
  "total_students_found": 17,
  "skipped_students": [
    {
      "student_id": 123,
      "student_name": "John Doe",
      "reason": "Already enrolled in this course"
    },
    {
      "student_id": 124,
      "student_name": "Jane Smith",
      "reason": "No teacher assigned for course Network Information Security in year 2024 section B"
    }
  ]
}
```

#### Error Responses

**No students found:**
```json
{
  "error": "No students found matching the criteria"
}
```
**Code:** `404 NOT FOUND`

**Invalid course:**
```json
{
  "course_id": ["Course with id 9999 does not exist"]
}
```
**Code:** `400 BAD REQUEST`

**Missing filters:**
```json
{
  "non_field_errors": ["Must provide either filter criteria (year, section, dept) or specific student_ids"]
}
```
**Code:** `400 BAD REQUEST`

**Non-management user:**
```json
{
  "error": "Only management users can perform bulk enrollment"
}
```
**Code:** `403 FORBIDDEN`

#### Example Usage

**Example 1: Enroll all students of year 2024 Section B in Network Information Security course**

```bash
curl -X POST https://your-domain.com/student-courses/bulk_enroll/ \
  -H "Authorization: Bearer <your-jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "course_id": 1,
    "year": 2024,
    "section": "B"
  }'
```

**Example 2: Enroll specific students in a course**

```bash
curl -X POST https://your-domain.com/student-courses/bulk_enroll/ \
  -H "Authorization: Bearer <your-jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "course_id": 1,
    "student_ids": [101, 102, 103, 104, 105]
  }'
```

**Example 3: Enroll all CS students of year 2024 Section B**

```bash
curl -X POST https://your-domain.com/student-courses/bulk_enroll/ \
  -H "Authorization: Bearer <your-jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "course_id": 1,
    "year": 2024,
    "section": "B",
    "dept": "CS"
  }'
```

### 2. Single Student Enrollment

Enroll a single student in a course.

**Endpoint:** `POST /students/{student_id}/enroll_course/`

**Permissions:** Management users only

#### URL Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| student_id | integer | Yes | ID of the student to enroll |

#### Request Body

```json
{
  "course_id": 1
}
```

#### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| course_id | integer | Yes | ID of the course to enroll the student in |

#### Success Response

**Code:** `201 CREATED`

**Content Example:**

```json
{
  "message": "Student enrolled successfully",
  "student_id": 123,
  "student_name": "John Doe",
  "course_id": 1,
  "course_name": "Network Information Security",
  "teacher_id": 5,
  "teacher_name": "Dr. Jane Smith"
}
```

#### Error Responses

**Student already enrolled:**
```json
{
  "error": "Student is already enrolled in this course"
}
```
**Code:** `400 BAD REQUEST`

**No teacher assigned:**
```json
{
  "error": "No teacher assigned for course Network Information Security in year 2024 section B"
}
```
**Code:** `400 BAD REQUEST`

**Invalid course:**
```json
{
  "course_id": ["Course with id 9999 does not exist"]
}
```
**Code:** `400 BAD REQUEST`

**Student not found:**
```json
{
  "error": "Student not found"
}
```
**Code:** `404 NOT FOUND`

**Non-management user:**
```json
{
  "error": "Only management users can enroll students"
}
```
**Code:** `403 FORBIDDEN`

#### Example Usage

**Enroll student with ID 123 in Network Information Security course**

```bash
curl -X POST https://your-domain.com/students/123/enroll_course/ \
  -H "Authorization: Bearer <your-jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "course_id": 1
  }'
```

## Business Logic

### Teacher Assignment

When enrolling students in a course, the system automatically assigns the appropriate teacher based on:
1. The course being enrolled
2. The student's year
3. The student's section

The system looks for a `TaughtCourse` entry that matches all three criteria. If no matching teacher is found, the enrollment is skipped (for bulk) or fails (for single enrollment).

### Duplicate Enrollment Prevention

The system checks if a student is already enrolled in a course before creating a new enrollment. If the student is already enrolled, the system:
- For bulk enrollment: Skips that student and includes them in the `skipped_students` list
- For single enrollment: Returns an error

### Classes Attended

When a student is newly enrolled in a course, the `classes_attended` field is initialized as an empty string. This field is updated when the student marks attendance through the RFID/QR code system.

## Important Notes

1. **Management Authorization Required**: Only users with a Management profile can perform student enrollments. Regular users (students/teachers) will receive a 403 Forbidden error.

2. **Course Must Exist**: The course_id must reference an existing course in the system. Invalid course IDs will result in a 400 Bad Request error.

3. **Teacher Assignment Required**: For successful enrollment, there must be a TaughtCourse entry for the specified course, year, and section. Without this, the system cannot determine which teacher to assign to the student.

4. **Idempotent Operations**: Both bulk and single enrollment operations are designed to be idempotent. Re-running the same enrollment request will not create duplicate entries.

5. **Bulk Enrollment Filters**: When using filters for bulk enrollment, you can combine year, section, and department filters to narrow down the student selection. At least one filter must be provided if not using student_ids.

## Use Cases

### Use Case 1: Semester Course Assignment
**Scenario:** At the start of a semester, assign all students of year 2024 Section B to the course "CT-486 Network Information Security"

**Solution:** Use bulk enrollment with year and section filters
```json
{
  "course_id": 1,
  "year": 2024,
  "section": "B"
}
```

### Use Case 2: Department-Specific Course
**Scenario:** Assign a specialized course only to CS students in a particular section

**Solution:** Use bulk enrollment with year, section, and department filters
```json
{
  "course_id": 5,
  "year": 2024,
  "section": "A",
  "dept": "CS"
}
```

### Use Case 3: Late Registration
**Scenario:** A student joins the class late and needs to be enrolled individually

**Solution:** Use single student enrollment
```json
{
  "course_id": 1
}
```

### Use Case 4: Special Group Assignment
**Scenario:** Assign a specific group of students (honors students, athletes, etc.) to a course

**Solution:** Use bulk enrollment with student_ids
```json
{
  "course_id": 3,
  "student_ids": [101, 105, 112, 118, 125]
}
```

## Testing

The implementation includes comprehensive test coverage for both bulk and single enrollment features:

### Bulk Enrollment Tests
- Test enrollment by year and section
- Test enrollment by specific student IDs
- Test enrollment with department filter
- Test handling of already enrolled students
- Test handling of courses without assigned teachers
- Test validation of invalid course IDs
- Test authorization for non-management users

### Single Student Enrollment Tests
- Test successful individual enrollment
- Test handling of already enrolled students
- Test handling of courses without assigned teachers
- Test validation of invalid course IDs
- Test validation of invalid student IDs
- Test authorization for non-management users

To run the tests:
```bash
python manage.py test core.tests.BulkEnrollStudentsTestCase
python manage.py test core.tests.SingleStudentEnrollTestCase
```

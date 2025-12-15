# Teacher Profile and Course Update API Documentation

This document describes the new API endpoints that allow teachers to update their profile information and manage their taught courses.

## Overview

The system now provides three new API endpoints for teachers:
1. **Update Profile** - Teachers can update their own profile information
2. **Get My Courses** - Teachers can retrieve their taught courses
3. **Update Taught Course** - Teachers can update their own course assignments

## API Endpoints

### 1. Update Teacher Profile

**Endpoint:** `POST /api/teachers/update_profile/` or `PATCH /api/teachers/update_profile/`

**Authentication:** Required (Teacher)

**Description:** Allows authenticated teachers to update their own profile information including name, email, and teacher code.

**Request Body:**
```json
{
  "teacher_name": "Updated Teacher Name",
  "email": "newemail@example.com",
  "teacher_code": "TC123"
}
```

**Notes:**
- All fields are optional, but at least one must be provided
- Email and teacher_code must be unique across all teachers
- Updating email also updates the associated User account

**Success Response (200 OK):**
```json
{
  "message": "Profile updated successfully",
  "teacher": {
    "teacher_id": 1,
    "teacher_name": "Updated Teacher Name",
    "teacher_code": "TC123",
    "email": "newemail@example.com",
    "rfid": "RFID001"
  }
}
```

**Error Responses:**
- `400 Bad Request` - No fields provided or validation error
- `403 Forbidden` - User is not a teacher
- `404 Not Found` - Teacher profile not found for user

**Example Usage:**
```bash
curl -X POST http://localhost:8000/api/teachers/update_profile/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "teacher_name": "Dr. John Smith",
    "teacher_code": "TS001"
  }'
```

---

### 2. Get My Courses

**Endpoint:** `GET /api/teachers/my_courses/`

**Authentication:** Required (Teacher)

**Description:** Retrieves all courses taught by the authenticated teacher.

**Request Body:** None (GET request)

**Success Response (200 OK):**
```json
{
  "teacher_id": 1,
  "teacher_name": "Dr. John Smith",
  "courses": [
    {
      "id": 1,
      "course": 5,
      "teacher": 1,
      "course_name": "Mathematics 101",
      "teacher_name": "Dr. John Smith",
      "classes_taken": "Room 101, Room 102",
      "section": "A",
      "year": 1
    },
    {
      "id": 2,
      "course": 8,
      "teacher": 1,
      "course_name": "Physics 201",
      "teacher_name": "Dr. John Smith",
      "classes_taken": "Lab 5",
      "section": "B",
      "year": 2
    }
  ]
}
```

**Error Responses:**
- `403 Forbidden` - User is not a teacher
- `404 Not Found` - Teacher profile not found for user

**Example Usage:**
```bash
curl -X GET http://localhost:8000/api/teachers/my_courses/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

### 3. Update Taught Course (Teacher)

**Endpoint:** `POST /api/taught-courses/{id}/teacher-update/` or `PATCH /api/taught-courses/{id}/teacher-update/`

**Authentication:** Required (Teacher)

**Description:** Allows teachers to update their own taught course information. Teachers can only update section, year, and classes_taken fields for courses they teach.

**URL Parameters:**
- `id` - The ID of the TaughtCourse to update

**Request Body:**
```json
{
  "section": "C",
  "year": 3,
  "classes_taken": "Room 201, Lab 3, Room 202"
}
```

**Notes:**
- All fields are optional, but at least one must be provided
- Teachers can only update courses assigned to them
- Teachers cannot change the course or teacher assignment (only management can do that)

**Success Response (200 OK):**
```json
{
  "message": "TaughtCourse updated successfully",
  "taught_course": {
    "id": 1,
    "course": 5,
    "teacher": 1,
    "course_name": "Mathematics 101",
    "teacher_name": "Dr. John Smith",
    "classes_taken": "Room 201, Lab 3, Room 202",
    "section": "C",
    "year": 3
  }
}
```

**Error Responses:**
- `400 Bad Request` - No fields provided
- `403 Forbidden` - User is not a teacher or trying to update another teacher's course
- `404 Not Found` - TaughtCourse not found

**Example Usage:**
```bash
curl -X POST http://localhost:8000/api/taught-courses/1/teacher-update/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "section": "D",
    "year": 2,
    "classes_taken": "Room 305"
  }'
```

---

## UI Integration

The teacher dashboard (`/dashboard/teacher/`) now includes:

### Profile Edit Modal
- Click "Edit Profile" button to open a modal
- Update teacher name, email, and teacher code
- Changes are saved via the `update_profile` API endpoint
- Display updates immediately after successful save

### Course Edit Forms
- Each course card has an "Edit Course Info" button
- Click to reveal an inline edit form
- Update section, year, and classes taken
- Changes are saved via the `teacher-update` API endpoint
- Page reloads after successful update

### Visual Feedback
- Modal dialogs for profile editing
- Inline forms for course editing
- Success/error alerts for all operations
- Maintains maroon color scheme (#800020, #A0324B, #FA8072)

---

## Security & Authorization

### Authentication
All endpoints require JWT authentication. Include the JWT token in the Authorization header:
```
Authorization: Bearer YOUR_JWT_TOKEN
```

### Authorization Rules
1. **Profile Update**: Only the authenticated teacher can update their own profile
2. **Get Courses**: Teachers can only see their own courses
3. **Course Update**: Teachers can only update courses assigned to them

### Validation
- Email uniqueness is enforced across all teachers
- Teacher code uniqueness is enforced across all teachers
- Year must be a valid integer
- Section is a string field (typically A, B, C, etc.)

---

## Differences from Management Endpoints

### Management Update (`/api/taught-courses/{id}/management-update/`)
- Can update course, teacher, year, and section
- Can reassign courses to different teachers
- Can change the course being taught
- Requires management user authentication

### Teacher Update (`/api/taught-courses/{id}/teacher-update/`)
- Can only update year, section, and classes_taken
- Cannot change course or teacher assignment
- Can only update own courses
- Requires teacher user authentication

---

## Error Handling

All endpoints follow consistent error response patterns:

**400 Bad Request:**
```json
{
  "error": "At least one field must be provided"
}
```

**403 Forbidden:**
```json
{
  "error": "Only teachers can perform this action"
}
```

**404 Not Found:**
```json
{
  "error": "Teacher profile not found for this user"
}
```

---

## Testing

Comprehensive test suites have been added:

### TeacherUpdateProfileTestCase
- Tests for updating name, email, and teacher code
- Tests for duplicate validation
- Tests for authorization checks
- Tests for multiple field updates

### TeacherMyCoursesTestCase
- Tests for retrieving teacher's courses

### TaughtCourseTeacherUpdateTestCase
- Tests for updating course information
- Tests for authorization (only own courses)
- Tests for validation and error handling

Run tests with:
```bash
python manage.py test core.tests.TeacherUpdateProfileTestCase
python manage.py test core.tests.TeacherMyCoursesTestCase
python manage.py test core.tests.TaughtCourseTeacherUpdateTestCase
```

---

## Related Documentation
- [Management TaughtCourse Update API](MANAGEMENT_TAUGHTCOURSE_UPDATE_API.md)
- [Student Course Management API](STUDENT_COURSE_MANAGEMENT_API.md)
- [Bulk Student Enrollment API](BULK_STUDENT_ENROLLMENT_API.md)

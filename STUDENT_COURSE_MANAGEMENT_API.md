# Student Course Management API - Bulk Operations

This document describes the complete API for managing student course enrollments and updates in bulk.

## Overview

The system provides comprehensive endpoints for both **creating** and **updating** student course enrollments:

### Creation (Enrollment)
1. **Bulk Enrollment**: Enroll multiple students in a course (creates new StudentCourse records)
2. **Single Student Enrollment**: Enroll a single student in a course

### Updates (Modification)
3. **Bulk Update**: Update existing student course enrollments in bulk
4. **Single Course Update**: Update individual StudentCourse record (standard REST API)

All endpoints require management user authentication.

## Authentication

All endpoints require authentication using JWT tokens. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

---

## PART 1: Enrollment APIs (Creating New Enrollments)

### 1. Bulk Enrollment

**Creates new** StudentCourse enrollments for multiple students.

**Endpoint:** `POST /student-courses/bulk_enroll/`

**Permissions:** Management users only

#### Request Body Options

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

#### Success Response

**Code:** `200 OK`

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
    }
  ]
}
```

#### Example Usage

```bash
# Enroll all students of year 2024 Section B in CT-486
curl -X POST https://your-domain.com/student-courses/bulk_enroll/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "course_id": 1,
    "year": 2024,
    "section": "B"
  }'
```

### 2. Single Student Enrollment

**Creates a new** enrollment for one student.

**Endpoint:** `POST /students/{student_id}/enroll_course/`

**Permissions:** Management users only

#### Request Body

```json
{
  "course_id": 1
}
```

#### Success Response

**Code:** `201 CREATED`

```json
{
  "message": "Student enrolled successfully",
  "student_id": 123,
  "student_name": "John Doe",
  "course_id": 1,
  "course_name": "Network Information Security",
  "teacher_id": 5,
  "teacher_name": "Dr. Smith"
}
```

---

## PART 2: Update APIs (Modifying Existing Enrollments)

### 3. Bulk Update (NEW)

**Updates existing** StudentCourse enrollments for multiple students.

**Endpoint:** `PUT /student-courses/bulk_update/` or `PATCH /student-courses/bulk_update/`

**Permissions:** Management users only

#### Request Body

You must provide:
1. **Filter criteria** (to select which records to update): year, section, dept, current_course_id, OR student_ids
2. **Update fields** (what to change): new_course_id, new_teacher_id, and/or classes_attended

```json
{
  // FILTERS (select records) - at least one required
  "year": 2024,
  "section": "B",
  "dept": "CS",                    // optional
  "current_course_id": 1,          // optional - filter by current course
  "student_ids": [1, 2, 3],        // optional - overrides other filters
  
  // UPDATES (modify fields) - at least one required
  "new_course_id": 2,              // optional - change to different course
  "new_teacher_id": 5,             // optional - reassign to different teacher
  "classes_attended": "2024-01-01, 2024-01-08"  // optional - update attendance
}
```

#### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| **Filters (at least one required)** |
| year | integer | Conditional | Filter by student year |
| section | string | Conditional | Filter by student section |
| dept | string | Conditional | Filter by student department |
| current_course_id | integer | Conditional | Filter by current enrolled course |
| student_ids | array | Conditional | Specific student IDs (overrides other filters) |
| **Update Fields (at least one required)** |
| new_course_id | integer | Conditional | New course ID to assign |
| new_teacher_id | integer | Conditional | New teacher ID to assign |
| classes_attended | string | Conditional | Update attendance record |

#### Success Response

**Code:** `200 OK`

```json
{
  "message": "Bulk update completed",
  "updated_count": 15,
  "total_records_found": 15,
  "updated_fields": ["course_id", "teacher_id"],
  "sample_updated_records": [
    {
      "student_id": 101,
      "student_name": "John Doe",
      "course_id": 2,
      "course_name": "Network Security",
      "teacher_id": 5,
      "teacher_name": "Dr. Smith"
    }
  ],
  "note": "Showing 10 of 15 updated records"
}
```

#### Error Responses

**No records found:**
```json
{
  "error": "No student course enrollments found matching the criteria"
}
```
**Code:** `404 NOT FOUND`

**Missing filters:**
```json
{
  "non_field_errors": ["Must provide either filter criteria (year, section, dept, current_course_id) or specific student_ids"]
}
```
**Code:** `400 BAD REQUEST`

**Missing update fields:**
```json
{
  "non_field_errors": ["Must provide at least one field to update (new_course_id, new_teacher_id, classes_attended)"]
}
```
**Code:** `400 BAD REQUEST`

#### Example Usage

**Example 1: Change all year 2024 Section B students from CS-301 to CT-486**

```bash
curl -X PUT https://your-domain.com/student-courses/bulk_update/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "year": 2024,
    "section": "B",
    "current_course_id": 1,
    "new_course_id": 2
  }'
```

**Example 2: Reassign teacher for all students in a specific course**

```bash
curl -X PUT https://your-domain.com/student-courses/bulk_update/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "current_course_id": 1,
    "new_teacher_id": 5
  }'
```

**Example 3: Update multiple fields for specific students**

```bash
curl -X PUT https://your-domain.com/student-courses/bulk_update/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "student_ids": [101, 102, 103],
    "new_course_id": 2,
    "new_teacher_id": 5,
    "classes_attended": "2024-01-01, 2024-01-08, 2024-01-15"
  }'
```

**Example 4: Update attendance for all students in a year/section**

```bash
curl -X PATCH https://your-domain.com/student-courses/bulk_update/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "year": 2024,
    "section": "B",
    "classes_attended": "2024-01-01, 2024-01-08"
  }'
```

### 4. Single Course Update

**Updates a single** StudentCourse enrollment record (standard REST API).

**Endpoint:** `PUT /student-courses/{id}/` or `PATCH /student-courses/{id}/`

**Permissions:** Authenticated users

#### Request Body

```json
{
  "student": 123,
  "course": 2,
  "teacher": 5,
  "classes_attended": "2024-01-01, 2024-01-08"
}
```

For PATCH, include only fields to update:

```json
{
  "teacher": 5
}
```

#### Success Response

**Code:** `200 OK`

Returns the updated StudentCourse object with all fields.

---

## Use Cases

### Enrollment Use Cases

1. **Semester Start** - Bulk enroll all students in required courses
2. **Late Registration** - Individually enroll students who join late
3. **Section Assignment** - Enroll specific sections in elective courses

### Update Use Cases

1. **Course Change** - Move all students from one course to another
   ```json
   {
     "year": 2024,
     "section": "B",
     "current_course_id": 1,
     "new_course_id": 2
   }
   ```

2. **Teacher Reassignment** - Change instructor for a course
   ```json
   {
     "current_course_id": 1,
     "new_teacher_id": 5
   }
   ```

3. **Department-Wide Updates** - Modify courses for entire department
   ```json
   {
     "dept": "CS",
     "year": 2024,
     "new_course_id": 3
   }
   ```

4. **Attendance Correction** - Update attendance records in bulk
   ```json
   {
     "year": 2024,
     "section": "B",
     "current_course_id": 1,
     "classes_attended": "corrected dates"
   }
   ```

5. **Selective Updates** - Update specific students only
   ```json
   {
     "student_ids": [101, 102, 103],
     "new_teacher_id": 5
   }
   ```

---

## Comparison: Enrollment vs Update

| Feature | Bulk Enrollment | Bulk Update |
|---------|----------------|-------------|
| **HTTP Method** | POST | PUT/PATCH |
| **Endpoint** | `/student-courses/bulk_enroll/` | `/student-courses/bulk_update/` |
| **Purpose** | Create new enrollments | Modify existing enrollments |
| **Required** | course_id + filters | filters + update fields |
| **Creates Records** | Yes | No |
| **Modifies Records** | No | Yes |
| **Skips Existing** | Yes (prevents duplicates) | N/A (updates all matching) |
| **Teacher Assignment** | Automatic via TaughtCourse | Manual specification |

---

## Business Rules

### For Enrollment (Create)
1. Teacher is automatically assigned via TaughtCourse lookup
2. Duplicate enrollments are prevented (atomic with get_or_create)
3. Requires TaughtCourse entry for student's year/section
4. Skips students without matching teacher assignments

### For Update (Modify)
1. Only updates existing StudentCourse records
2. Does not create new records if none match
3. All matching records are updated
4. No automatic teacher assignment - must specify if changing
5. Can update any combination of: course, teacher, attendance

---

## Important Notes

⚠️ **Enrollment vs Update**: 
- Use **enrollment** to add students to courses (creates new records)
- Use **update** to modify existing course assignments (changes existing records)

⚠️ **Management Access**: Only users with Management profile can use bulk operations

⚠️ **Filters Required**: Bulk update requires at least one filter AND at least one update field

⚠️ **No Rollback**: Bulk updates modify all matching records immediately. There is no automatic rollback.

⚠️ **Teacher Assignment**: 
- Enrollment: Teacher assigned automatically based on TaughtCourse
- Update: Must explicitly specify new_teacher_id if changing teacher

---

## Testing

Run the comprehensive test suites:

```bash
# Test bulk enrollment (16 tests)
python manage.py test core.tests.BulkEnrollStudentsTestCase

# Test single enrollment (5 tests)
python manage.py test core.tests.SingleStudentEnrollTestCase

# Test bulk update (13 tests)
python manage.py test core.tests.BulkUpdateStudentCoursesTestCase
```

---

## Support

For issues or questions:
1. Check this documentation for usage examples
2. Review test cases for implementation examples
3. Verify error messages for specific issues
4. Ensure proper management authentication

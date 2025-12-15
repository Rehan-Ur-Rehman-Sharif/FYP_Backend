# Quick Reference: Student Course Operations

## Summary

This implementation provides **complete CRUD operations** for student course management:

### CREATE (Enrollment)
- **Bulk**: `POST /student-courses/bulk_enroll/` - Enroll multiple students
- **Single**: `POST /students/{id}/enroll_course/` - Enroll one student

### UPDATE (Modification) 
- **Bulk**: `PUT/PATCH /student-courses/bulk_update/` - Update multiple enrollments
- **Single**: `PUT/PATCH /student-courses/{id}/` - Update one enrollment

### READ
- `GET /student-courses/` - List all enrollments (with filters)
- `GET /student-courses/{id}/` - Get one enrollment

### DELETE
- `DELETE /student-courses/{id}/` - Delete one enrollment

---

## Key Differences

| Operation | Enrollment | Update |
|-----------|-----------|--------|
| **Purpose** | Create new records | Modify existing records |
| **HTTP Method** | POST | PUT/PATCH |
| **Creates records?** | Yes | No |
| **Modifies records?** | No | Yes |
| **Auto teacher assignment?** | Yes (via TaughtCourse) | No (must specify) |
| **Prevents duplicates?** | Yes | N/A |

---

## Common Use Cases

### 1. Semester Start - Enroll all students
```bash
POST /student-courses/bulk_enroll/
{
  "course_id": 1,
  "year": 2024,
  "section": "B"
}
```

### 2. Course Change - Switch students to different course
```bash
PUT /student-courses/bulk_update/
{
  "year": 2024,
  "section": "B",
  "current_course_id": 1,
  "new_course_id": 2
}
```

### 3. Teacher Reassignment - Change instructor
```bash
PUT /student-courses/bulk_update/
{
  "current_course_id": 1,
  "new_teacher_id": 5
}
```

### 4. Late Registration - Add one student
```bash
POST /students/123/enroll_course/
{
  "course_id": 1
}
```

### 5. Individual Course Update - Change one student's enrollment
```bash
PATCH /student-courses/456/
{
  "teacher": 5,
  "classes_attended": "2024-01-01, 2024-01-08"
}
```

---

## Authorization

All operations require:
- **Authentication**: Valid JWT token
- **Bulk operations**: Management user role
- **Single operations**: Authenticated user (varies by endpoint)

---

## Complete Documentation

See `STUDENT_COURSE_MANAGEMENT_API.md` for:
- Detailed API specifications
- All request/response formats
- Error handling
- Complete examples
- Business rules
- Testing instructions

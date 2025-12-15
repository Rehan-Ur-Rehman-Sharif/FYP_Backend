# Quick Reference: Student Course Enrollment APIs

## Purpose
This implementation adds two new APIs for enrolling students in courses:
1. **Bulk Enrollment** - Enroll multiple students at once
2. **Single Enrollment** - Enroll one student at a time

## Quick Start

### 1. Bulk Enrollment Example
**Scenario:** Assign all students of year 2024 Section B to CT-486

```bash
curl -X POST http://your-domain/student-courses/bulk_enroll/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "course_id": 1,
    "year": 2024,
    "section": "B"
  }'
```

**Response:**
```json
{
  "message": "Bulk enrollment completed",
  "course_name": "Network Information Security",
  "enrolled_count": 15,
  "skipped_count": 2,
  "total_students_found": 17,
  "skipped_students": [...]
}
```

### 2. Single Student Enrollment Example
**Scenario:** Enroll student ID 123 in a course

```bash
curl -X POST http://your-domain/students/123/enroll_course/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "course_id": 1
  }'
```

**Response:**
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

## Key Features

✅ **Management Only** - Both APIs require management authentication
✅ **Auto-Teacher Assignment** - Automatically assigns teachers based on TaughtCourse entries
✅ **Smart Filtering** - Filter by year, section, dept, or use specific student IDs
✅ **Duplicate Prevention** - Won't create duplicate enrollments
✅ **Detailed Feedback** - Reports enrolled/skipped students with reasons

## Requirements

1. **Authentication**: Management user JWT token required
2. **Prerequisites**: 
   - Course must exist
   - TaughtCourse entry must exist for student's year/section
   - Student must not already be enrolled

## Filter Options (Bulk Enrollment)

You can use any combination:

### By Year and Section
```json
{
  "course_id": 1,
  "year": 2024,
  "section": "B"
}
```

### By Department
```json
{
  "course_id": 1,
  "year": 2024,
  "section": "B",
  "dept": "CS"
}
```

### By Specific Student IDs
```json
{
  "course_id": 1,
  "student_ids": [101, 102, 103, 104, 105]
}
```

## Common Use Cases

1. **Semester Start** - Bulk enroll all students in required courses
2. **Section Assignment** - Enroll specific sections in elective courses
3. **Late Registration** - Add individual students who join late
4. **Special Groups** - Enroll honors students, athletes, etc. using student IDs

## Testing

Run the comprehensive test suite:
```bash
# Test bulk enrollment
python manage.py test core.tests.BulkEnrollStudentsTestCase

# Test single enrollment
python manage.py test core.tests.SingleStudentEnrollTestCase
```

## Documentation

📄 **Full API Documentation**: `BULK_STUDENT_ENROLLMENT_API.md`
📄 **Implementation Details**: `IMPLEMENTATION_SUMMARY.md`

## Support

For issues or questions:
1. Check the full API documentation
2. Review test cases for usage examples
3. Check error messages for specific issues

## Important Notes

⚠️ **Teacher Assignment**: Enrollment only works if a TaughtCourse entry exists for the course, year, and section combination.

⚠️ **Management Access**: Regular users (students/teachers) cannot use these endpoints.

⚠️ **Validation**: Course IDs must exist in the system.

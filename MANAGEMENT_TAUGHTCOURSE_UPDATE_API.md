# Management TaughtCourse Update API

This document describes the new management endpoint for updating TaughtCourse entries.

## Overview

The Management TaughtCourse Update API allows management users to update specific fields of TaughtCourse entries, including:
- Year
- Section
- Course

This endpoint is restricted to management users only and provides a controlled way to update teacher-course assignments.

## Endpoint

**URL**: `/taught-courses/{id}/management-update/`

**Methods**: `POST`, `PATCH`

**Authentication**: Required (JWT or Session)

**Permission**: Management users only

## Request Format

### Headers
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

### Body Parameters

At least one of the following fields must be provided:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| year | integer | No | The academic year (e.g., 1, 2, 3, 4) |
| section | string | No | The section identifier (e.g., 'A', 'B', 'C') |
| course | integer | No | The course ID to assign |

## Examples

### Update Year Only

**Request:**
```bash
POST /taught-courses/1/management-update/
Content-Type: application/json
Authorization: Bearer <jwt_token>

{
  "year": 3
}
```

**Response:**
```json
{
  "message": "TaughtCourse updated successfully by management",
  "taught_course": {
    "id": 1,
    "course": 5,
    "teacher": 2,
    "course_name": "Data Structures",
    "teacher_name": "Dr. Smith",
    "classes_taken": "Room 101, Room 102",
    "section": "A",
    "year": 3
  }
}
```

### Update Section Only

**Request:**
```bash
POST /taught-courses/1/management-update/
Content-Type: application/json
Authorization: Bearer <jwt_token>

{
  "section": "B"
}
```

**Response:**
```json
{
  "message": "TaughtCourse updated successfully by management",
  "taught_course": {
    "id": 1,
    "course": 5,
    "teacher": 2,
    "course_name": "Data Structures",
    "teacher_name": "Dr. Smith",
    "classes_taken": "Room 101, Room 102",
    "section": "B",
    "year": 3
  }
}
```

### Update Course Only

**Request:**
```bash
POST /taught-courses/1/management-update/
Content-Type: application/json
Authorization: Bearer <jwt_token>

{
  "course": 7
}
```

**Response:**
```json
{
  "message": "TaughtCourse updated successfully by management",
  "taught_course": {
    "id": 1,
    "course": 7,
    "teacher": 2,
    "course_name": "Algorithms",
    "teacher_name": "Dr. Smith",
    "classes_taken": "Room 101, Room 102",
    "section": "B",
    "year": 3
  }
}
```

### Update Multiple Fields

**Request:**
```bash
POST /taught-courses/1/management-update/
Content-Type: application/json
Authorization: Bearer <jwt_token>

{
  "year": 4,
  "section": "C",
  "course": 10
}
```

**Response:**
```json
{
  "message": "TaughtCourse updated successfully by management",
  "taught_course": {
    "id": 1,
    "course": 10,
    "teacher": 2,
    "course_name": "Machine Learning",
    "teacher_name": "Dr. Smith",
    "classes_taken": "Room 101, Room 102",
    "section": "C",
    "year": 4
  }
}
```

### Using PATCH Method

The endpoint also supports the PATCH method:

**Request:**
```bash
PATCH /taught-courses/1/management-update/
Content-Type: application/json
Authorization: Bearer <jwt_token>

{
  "year": 2
}
```

## Error Responses

### 400 Bad Request - No Fields Provided

**Response:**
```json
{
  "error": "At least one of year, section, or course must be provided"
}
```

### 401 Unauthorized - Not Authenticated

**Response:**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden - Not a Management User

**Response:**
```json
{
  "error": "Only management users can perform this action"
}
```

### 404 Not Found - Invalid TaughtCourse ID

**Response:**
```json
{
  "error": "TaughtCourse not found"
}
```

### 404 Not Found - Invalid Course ID

**Response:**
```json
{
  "error": "Course with id 99999 not found"
}
```

## Use Cases

1. **Academic Restructuring**: When academic years or sections need to be reorganized, management can update teacher assignments accordingly.

2. **Course Reassignment**: If a teacher needs to teach a different course in the same time slot, management can update the course assignment.

3. **Section Changes**: When section groupings change, management can update which section a teacher is assigned to teach.

4. **Bulk Updates**: Management can programmatically update multiple TaughtCourse entries for administrative changes.

## Notes

- Only management users can access this endpoint
- The teacher and classes_taken fields cannot be modified through this endpoint
- Regular CRUD operations are still available through standard PUT/PATCH endpoints for authenticated users
- This endpoint provides additional validation and is specifically designed for management-level updates
- The endpoint preserves all other fields that are not being updated

## Related Endpoints

- `GET /taught-courses/` - List all taught courses
- `POST /taught-courses/` - Create a new taught course
- `GET /taught-courses/{id}/` - Get details of a specific taught course
- `PUT /taught-courses/{id}/` - Update a taught course (general users)
- `PATCH /taught-courses/{id}/` - Partial update a taught course (general users)
- `DELETE /taught-courses/{id}/` - Delete a taught course

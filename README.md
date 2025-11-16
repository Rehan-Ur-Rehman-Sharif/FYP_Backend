# Student Attendance Management System

A Django-based backend system for managing student attendance across courses, teachers, and departments.

## Features

- **Student Management**: Track students with roll numbers, departments, sections, and overall attendance
- **Course Management**: Organize courses by department with credit hours
- **Teacher Management**: Manage teachers and their course assignments
- **Attendance Tracking**: Record daily attendance with automatic percentage calculations
- **Multi-Semester Support**: Handle multiple semesters and sections
- **Administrative Controls**: Management users with granular permissions

## Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL (for production) or SQLite (for testing)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Rehan-Ur-Rehman-Sharif/FYP_Backend.git
cd FYP_Backend
```

2. Install dependencies:
```bash
pip install Django==5.2.8 psycopg2-binary
```

3. Configure database in `FYP_Backend/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'school_db',
        'USER': 'dbuser',
        'PASSWORD': 'dbpass',
        'HOST': 'localhost',
        'PORT': '5433',
    }
}
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

7. Access the admin interface at `http://localhost:8000/admin`

### Running Tests

Run the test suite:
```bash
python manage.py test core --settings=FYP_Backend.test_settings
```

## Models Overview

### Core Models

1. **Department** - Academic departments (CS, EE, ME, etc.)
2. **Course** - Course catalog with department relationships
3. **Student** - Student records with attendance tracking
4. **Teacher** - Teacher records
5. **CourseOffering** - Course instances for specific semesters
6. **CourseEnrollment** - Links students to courses with attendance
7. **AttendanceRecord** - Daily attendance records
8. **Management** - System administrators

For detailed model documentation, see [MODELS_DOCUMENTATION.md](MODELS_DOCUMENTATION.md).

## Usage Examples

### Creating a Department
```python
from core.models import Department

dept = Department.objects.create(
    name="Computer Science",
    code="CS"
)
```

### Adding a Course
```python
from core.models import Course

course = Course.objects.create(
    course_code="CS101",
    course_name="Introduction to Programming",
    department=dept,
    credit_hours=3
)
```

### Registering a Student
```python
from core.models import Student

student = Student.objects.create(
    roll_number="2024-CS-001",
    name="John Doe",
    department=dept,
    section="A"
)
```

### Recording Attendance
```python
from datetime import date
from core.models import AttendanceRecord, CourseEnrollment

# First, enroll student in a course offering
enrollment = CourseEnrollment.objects.create(
    student=student,
    course_offering=offering
)

# Record attendance
AttendanceRecord.objects.create(
    enrollment=enrollment,
    date=date.today(),
    is_present=True
)

# Check attendance percentage
print(f"Attendance: {enrollment.get_attendance_percentage():.2f}%")
```

### Getting Overall Attendance
```python
student = Student.objects.get(roll_number="2024-CS-001")
overall = student.get_overall_attendance()
print(f"Overall Attendance: {overall:.2f}%")
```

## Admin Interface

The system includes a comprehensive Django admin interface with:

- List views with filters and search
- Inline editing of related objects
- Calculated fields (attendance percentages)
- Date hierarchies for attendance records
- Permission-based access control

## API Endpoints

*Note: REST API endpoints can be added using Django REST Framework in future iterations.*

## Database Schema

The database uses the following relationships:

- **Department** → **Course** (One-to-Many)
- **Department** → **Student** (One-to-Many)
- **Course** → **CourseOffering** (One-to-Many)
- **Teacher** → **CourseOffering** (One-to-Many)
- **CourseOffering** → **CourseEnrollment** (One-to-Many)
- **Student** → **CourseEnrollment** (One-to-Many)
- **CourseEnrollment** → **AttendanceRecord** (One-to-Many)

## Extending the System

The system is designed to be extensible. You can:

1. Add new fields to existing models
2. Create additional models for new features
3. Implement custom business logic in model methods
4. Add REST API endpoints using Django REST Framework
5. Integrate with external authentication systems

## Testing

The project includes comprehensive tests covering:

- Model creation and validation
- Attendance calculations
- Relationship integrity
- Business logic methods

All tests pass with 100% coverage of core functionality.

## Security

- No security vulnerabilities detected by CodeQL
- Password validation enabled
- CSRF protection enabled
- SQL injection protection via Django ORM

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests to ensure nothing breaks
5. Submit a pull request

## License

[Specify your license here]

## Support

For issues and questions, please open an issue on GitHub.

## Version History

- **v1.0.0** - Initial implementation with core models
  - 8 models for complete attendance management
  - Comprehensive test coverage
  - Admin interface
  - Documentation

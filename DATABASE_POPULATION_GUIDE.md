# Database Population Guide

This guide provides SQL commands to populate the PostgreSQL database for the FYP_Backend project.

## Database Configuration

Based on `settings.py`, the PostgreSQL database configuration is:
- **Database Name**: `school_db`
- **User**: `dbuser`
- **Password**: `dbpass`
- **Host**: `localhost`
- **Port**: `5433`

## How to Use

### Method 1: Execute the Complete SQL File

```bash
psql -h localhost -p 5433 -U dbuser -d school_db -f populate_database.sql
```

### Method 2: Connect to PostgreSQL and Copy-Paste Commands

1. Connect to the database:
```bash
psql -h localhost -p 5433 -U dbuser -d school_db
```

2. Copy and paste the sections from `populate_database.sql` in order

### Method 3: Execute Specific Sections

You can execute specific sections separately:

**Delete existing data:**
```bash
psql -h localhost -p 5433 -U dbuser -d school_db -c "DELETE FROM core_attendancerecord; DELETE FROM core_attendancesession; DELETE FROM core_updateattendancerequest; DELETE FROM core_studentcourse; DELETE FROM core_taughtcourse; DELETE FROM core_student; DELETE FROM core_teacher; DELETE FROM core_management; DELETE FROM core_course; DELETE FROM core_class; DELETE FROM auth_user;"
```

## Data Summary

The SQL script will create:

### Students (5 total)
1. **Ahmed Khan** - Year 3, CS, Section A (4 courses)
2. **Fatima Ali** - Year 3, CS, Section A (4 courses)
3. **Hassan Malik** - Year 3, CS, Section B (3 courses)
4. **Ayesha Raza** - Year 2, IT, Section A (2 courses)
5. **Usman Sheikh** - Year 3, CS, Section A (4 courses)

### Teachers (6 total)
1. **Dr. Sarah Ahmed** - Teaches Database Systems (Section A) and Software Engineering (Section B)
2. **Prof. Muhammad Hussain** - Teaches Data Structures (Sections A & B)
3. **Dr. Zainab Farooq** - Teaches Operating Systems (Year 3) and Computer Networks (Year 2)
4. **Prof. Ali Haider** - Teaches Artificial Intelligence
5. **Dr. Mariam Nasir** - Teaches Web Development
6. **Prof. Imran Siddiqui** - Teaches Mobile Application Development

### Courses (8 total)
1. Database Systems
2. Data Structures and Algorithms
3. Operating Systems
4. Computer Networks
5. Software Engineering
6. Artificial Intelligence
7. Web Development
8. Mobile Application Development

### Management (2 total)
1. **Dean Rashid** - Dean
2. **HOD Kamran** - Head of Department

### Relationships
- **9 TaughtCourse entries** - Teacher-Course assignments with section and year
- **17 StudentCourse entries** - Student enrollments in courses

## Login Credentials

All users have the same password: `password123`

### Student Usernames
- `student1` - Ahmed Khan
- `student2` - Fatima Ali
- `student3` - Hassan Malik
- `student4` - Ayesha Raza
- `student5` - Usman Sheikh

### Teacher Usernames
- `teacher1` - Dr. Sarah Ahmed
- `teacher2` - Prof. Muhammad Hussain
- `teacher3` - Dr. Zainab Farooq
- `teacher4` - Prof. Ali Haider
- `teacher5` - Dr. Mariam Nasir
- `teacher6` - Prof. Imran Siddiqui

### Management Usernames
- `management1` - Dean Rashid
- `management2` - HOD Kamran

## Verification

After running the script, you can verify the data:

```sql
-- Check counts
SELECT COUNT(*) as student_count FROM core_student;      -- Should be 5
SELECT COUNT(*) as teacher_count FROM core_teacher;      -- Should be 6
SELECT COUNT(*) as course_count FROM core_course;        -- Should be 8
SELECT COUNT(*) as management_count FROM core_management; -- Should be 2
SELECT COUNT(*) as taught_count FROM core_taughtcourse;  -- Should be 9
SELECT COUNT(*) as enrolled_count FROM core_studentcourse; -- Should be 17
SELECT COUNT(*) as user_count FROM auth_user;            -- Should be 13
```

## Course Enrollments by Student

| Student | Courses |
|---------|---------|
| Ahmed Khan | Database Systems, Data Structures, Operating Systems, AI |
| Fatima Ali | Database Systems, Data Structures, AI, Mobile App Dev |
| Hassan Malik | Data Structures, Software Engineering, Mobile App Dev |
| Ayesha Raza | Computer Networks, Web Development |
| Usman Sheikh | Database Systems, Data Structures, Operating Systems, AI |

## Notes

- All RFID tags are in format `RFID-STD-00X` for students and `RFID-TCH-00X` for teachers
- Email addresses follow the pattern: `firstname.lastname@university.edu`
- User passwords are hashed using Django's PBKDF2-SHA256 algorithm
- All accounts are active and ready for login
- Teachers have `is_staff=True` to access admin panel
- Management users have `is_superuser=True` for full system access
- The script resets all sequence counters to ensure proper auto-increment behavior

## Troubleshooting

### If you get "relation does not exist" errors:
Run Django migrations first:
```bash
python manage.py makemigrations
python manage.py migrate
```

### If you get "sequence does not exist" errors:
The sequences are created by Django migrations. Make sure migrations are run before executing this script.

### To generate a proper password hash for Django:
```python
from django.contrib.auth.hashers import make_password
password = make_password('your_password_here')
print(password)
```

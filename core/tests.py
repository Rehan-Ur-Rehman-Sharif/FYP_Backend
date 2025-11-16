from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date, timedelta
from .models import (
    Department, Course, Student, Teacher,
    CourseOffering, CourseEnrollment, AttendanceRecord, Management
)


class DepartmentModelTest(TestCase):
    def test_create_department(self):
        dept = Department.objects.create(name="Computer Science", code="CS")
        self.assertEqual(str(dept), "CS - Computer Science")
        self.assertEqual(dept.code, "CS")


class CourseModelTest(TestCase):
    def setUp(self):
        self.dept = Department.objects.create(name="Computer Science", code="CS")
    
    def test_create_course(self):
        course = Course.objects.create(
            course_code="CS101",
            course_name="Introduction to Programming",
            department=self.dept,
            credit_hours=3
        )
        self.assertEqual(str(course), "CS101 - Introduction to Programming")
        self.assertEqual(course.department, self.dept)


class StudentModelTest(TestCase):
    def setUp(self):
        self.dept = Department.objects.create(name="Computer Science", code="CS")
    
    def test_create_student(self):
        student = Student.objects.create(
            roll_number="2024-CS-001",
            name="John Doe",
            department=self.dept,
            section="A"
        )
        self.assertEqual(str(student), "2024-CS-001 - John Doe")
        self.assertEqual(student.department, self.dept)
    
    def test_student_overall_attendance_empty(self):
        student = Student.objects.create(
            roll_number="2024-CS-001",
            name="John Doe",
            department=self.dept,
            section="A"
        )
        self.assertEqual(student.get_overall_attendance(), 0.0)


class TeacherModelTest(TestCase):
    def test_create_teacher(self):
        teacher = Teacher.objects.create(
            roll_number="T-001",
            name="Dr. Smith"
        )
        self.assertEqual(str(teacher), "T-001 - Dr. Smith")


class CourseOfferingModelTest(TestCase):
    def setUp(self):
        self.dept = Department.objects.create(name="Computer Science", code="CS")
        self.course = Course.objects.create(
            course_code="CS101",
            course_name="Introduction to Programming",
            department=self.dept
        )
        self.teacher = Teacher.objects.create(roll_number="T-001", name="Dr. Smith")
    
    def test_create_course_offering(self):
        offering = CourseOffering.objects.create(
            course=self.course,
            teacher=self.teacher,
            semester="Fall 2024",
            section="A"
        )
        self.assertTrue(offering.is_active)
        self.assertIn("CS101", str(offering))


class CourseEnrollmentModelTest(TestCase):
    def setUp(self):
        self.dept = Department.objects.create(name="Computer Science", code="CS")
        self.course = Course.objects.create(
            course_code="CS101",
            course_name="Introduction to Programming",
            department=self.dept
        )
        self.teacher = Teacher.objects.create(roll_number="T-001", name="Dr. Smith")
        self.student = Student.objects.create(
            roll_number="2024-CS-001",
            name="John Doe",
            department=self.dept,
            section="A"
        )
        self.offering = CourseOffering.objects.create(
            course=self.course,
            teacher=self.teacher,
            semester="Fall 2024",
            section="A"
        )
    
    def test_create_enrollment(self):
        enrollment = CourseEnrollment.objects.create(
            student=self.student,
            course_offering=self.offering
        )
        self.assertIn("John Doe", str(enrollment))
        self.assertIn("CS101", str(enrollment))
    
    def test_enrollment_attendance_percentage_no_records(self):
        enrollment = CourseEnrollment.objects.create(
            student=self.student,
            course_offering=self.offering
        )
        self.assertEqual(enrollment.get_attendance_percentage(), 0.0)
    
    def test_enrollment_attendance_percentage_with_records(self):
        enrollment = CourseEnrollment.objects.create(
            student=self.student,
            course_offering=self.offering
        )
        
        # Create attendance records
        AttendanceRecord.objects.create(enrollment=enrollment, date=date.today(), is_present=True)
        AttendanceRecord.objects.create(enrollment=enrollment, date=date.today() - timedelta(days=1), is_present=True)
        AttendanceRecord.objects.create(enrollment=enrollment, date=date.today() - timedelta(days=2), is_present=False)
        
        # 2 present out of 3 = 66.67%
        self.assertAlmostEqual(enrollment.get_attendance_percentage(), 66.67, places=1)


class AttendanceRecordModelTest(TestCase):
    def setUp(self):
        dept = Department.objects.create(name="Computer Science", code="CS")
        course = Course.objects.create(
            course_code="CS101",
            course_name="Introduction to Programming",
            department=dept
        )
        teacher = Teacher.objects.create(roll_number="T-001", name="Dr. Smith")
        student = Student.objects.create(
            roll_number="2024-CS-001",
            name="John Doe",
            department=dept,
            section="A"
        )
        offering = CourseOffering.objects.create(
            course=course,
            teacher=teacher,
            semester="Fall 2024",
            section="A"
        )
        self.enrollment = CourseEnrollment.objects.create(
            student=student,
            course_offering=offering
        )
    
    def test_create_attendance_record(self):
        record = AttendanceRecord.objects.create(
            enrollment=self.enrollment,
            date=date.today(),
            is_present=True,
            remarks="On time"
        )
        self.assertTrue(record.is_present)
        self.assertIn("Present", str(record))


class ManagementModelTest(TestCase):
    def test_create_management(self):
        mgmt = Management.objects.create(
            roll_number="M-001",
            name="Admin User",
            designation="System Administrator"
        )
        self.assertEqual(str(mgmt), "M-001 - Admin User (System Administrator)")
        self.assertTrue(mgmt.can_modify_students)
        self.assertTrue(mgmt.can_modify_teachers)


class AttendanceCalculationTest(TestCase):
    def setUp(self):
        dept = Department.objects.create(name="Computer Science", code="CS")
        
        # Create two courses
        self.course1 = Course.objects.create(
            course_code="CS101",
            course_name="Programming",
            department=dept
        )
        self.course2 = Course.objects.create(
            course_code="CS102",
            course_name="Data Structures",
            department=dept
        )
        
        teacher = Teacher.objects.create(roll_number="T-001", name="Dr. Smith")
        
        self.student = Student.objects.create(
            roll_number="2024-CS-001",
            name="John Doe",
            department=dept,
            section="A"
        )
        
        # Create offerings
        self.offering1 = CourseOffering.objects.create(
            course=self.course1,
            teacher=teacher,
            semester="Fall 2024",
            section="A"
        )
        self.offering2 = CourseOffering.objects.create(
            course=self.course2,
            teacher=teacher,
            semester="Fall 2024",
            section="A"
        )
    
    def test_overall_attendance_calculation(self):
        # Enroll student in both courses
        enrollment1 = CourseEnrollment.objects.create(
            student=self.student,
            course_offering=self.offering1
        )
        enrollment2 = CourseEnrollment.objects.create(
            student=self.student,
            course_offering=self.offering2
        )
        
        # Course 1: 100% attendance (2 present out of 2)
        AttendanceRecord.objects.create(enrollment=enrollment1, date=date.today(), is_present=True)
        AttendanceRecord.objects.create(enrollment=enrollment1, date=date.today() - timedelta(days=1), is_present=True)
        
        # Course 2: 50% attendance (1 present out of 2)
        AttendanceRecord.objects.create(enrollment=enrollment2, date=date.today(), is_present=True)
        AttendanceRecord.objects.create(enrollment=enrollment2, date=date.today() - timedelta(days=1), is_present=False)
        
        # Overall should be average: (100 + 50) / 2 = 75%
        self.assertAlmostEqual(self.student.get_overall_attendance(), 75.0, places=1)

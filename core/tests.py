from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import (
    Student, Teacher, Management, Course, Class, TaughtCourse, StudentCourse,
    UpdateAttendanceRequest, AttendanceSession, AttendanceRecord
)


class StudentRegistrationTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('student-register')
        self.valid_data = {
            'email': 'student@test.com',
            'password': 'TestPass123!',
            'password2': 'TestPass123!',
            'student_name': 'Test Student',
            'rfid': 'RFID001',
            'year': 1,
            'dept': 'CS',
            'section': 'A'
        }

    def test_student_registration_success(self):
        """Test successful student registration"""
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('student_id', response.data)
        self.assertEqual(response.data['email'], 'student@test.com')
        
        # Verify user and student were created
        self.assertTrue(User.objects.filter(email='student@test.com').exists())
        self.assertTrue(Student.objects.filter(email='student@test.com').exists())

    def test_student_registration_password_mismatch(self):
        """Test registration fails when passwords don't match"""
        data = self.valid_data.copy()
        data['password2'] = 'DifferentPass123!'
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_student_registration_duplicate_email(self):
        """Test registration fails with duplicate email"""
        self.client.post(self.url, self.valid_data, format='json')
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_student_registration_with_valid_courses(self):
        """Test student registration with valid course codes"""
        # Create courses
        course1 = Course.objects.create(course_name='Math 101', course_code='MATH101')
        course2 = Course.objects.create(course_name='Physics 101', course_code='PHYS101')
        
        # Create a teacher
        teacher = Teacher.objects.create(
            teacher_name='Test Teacher',
            email='teacher@test.com',
            rfid='RFID_TEACHER'
        )
        
        # Create TaughtCourse entries
        TaughtCourse.objects.create(
            course=course1,
            teacher=teacher,
            year=1,
            section='A',
            classes_taken=''
        )
        TaughtCourse.objects.create(
            course=course2,
            teacher=teacher,
            year=1,
            section='A',
            classes_taken=''
        )
        
        # Register student with courses
        data = self.valid_data.copy()
        data['courses'] = ['MATH101', 'PHYS101']
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('enrolled_courses', response.data)
        self.assertEqual(len(response.data['enrolled_courses']), 2)
        
        # Verify StudentCourse entries were created
        student = Student.objects.get(email='student@test.com')
        student_courses = StudentCourse.objects.filter(student=student)
        self.assertEqual(student_courses.count(), 2)
        
        # Verify the courses are correctly assigned
        course_codes = set(sc.course.course_code for sc in student_courses)
        self.assertEqual(course_codes, {'MATH101', 'PHYS101'})
        
        # Verify teachers are assigned
        for sc in student_courses:
            self.assertEqual(sc.teacher, teacher)
    
    def test_student_registration_with_invalid_course_codes(self):
        """Test student registration fails with invalid course codes"""
        data = self.valid_data.copy()
        data['courses'] = ['INVALID101', 'NOTEXIST202']  # Non-existent course codes
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('courses', response.data)
        
        # Verify student was not created
        self.assertFalse(Student.objects.filter(email='student@test.com').exists())
    
    def test_student_registration_with_mixed_valid_invalid_courses(self):
        """Test student registration fails when some course codes are invalid"""
        # Create one valid course
        course1 = Course.objects.create(course_name='Math 101', course_code='MATH101')
        
        data = self.valid_data.copy()
        data['courses'] = ['MATH101', 'INVALID999']  # One valid, one invalid
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('courses', response.data)
        
        # Verify student was not created
        self.assertFalse(Student.objects.filter(email='student@test.com').exists())
    
    def test_student_registration_with_empty_courses_list(self):
        """Test student registration succeeds with empty courses list"""
        data = self.valid_data.copy()
        data['courses'] = []
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('enrolled_courses', response.data)
        self.assertEqual(len(response.data['enrolled_courses']), 0)
        
        # Verify student was created
        student = Student.objects.get(email='student@test.com')
        self.assertEqual(StudentCourse.objects.filter(student=student).count(), 0)
    
    def test_student_registration_without_courses_field(self):
        """Test student registration succeeds without courses field"""
        # Don't include courses field at all
        response = self.client.post(self.url, self.valid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('enrolled_courses', response.data)
        self.assertEqual(len(response.data['enrolled_courses']), 0)
    
    def test_student_registration_course_without_taught_course(self):
        """Test student registration when course exists but no TaughtCourse for that year/section"""
        # Create a course
        course = Course.objects.create(course_name='Math 101', course_code='MATH101')
        
        # Don't create any TaughtCourse entry
        
        data = self.valid_data.copy()
        data['courses'] = ['MATH101']
        response = self.client.post(self.url, data, format='json')
        
        # Registration should succeed
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # But no StudentCourse should be created (since no teacher is assigned)
        student = Student.objects.get(email='student@test.com')
        self.assertEqual(StudentCourse.objects.filter(student=student).count(), 0)
        self.assertEqual(len(response.data['enrolled_courses']), 0)


class StudentLoginTestCase(APITestCase):
    def setUp(self):
        self.register_url = reverse('student-register')
        self.login_url = reverse('student-login')
        self.credentials = {
            'email': 'student@test.com',
            'password': 'TestPass123!',
            'password2': 'TestPass123!',
            'student_name': 'Test Student',
            'rfid': 'RFID001',
            'year': 1,
            'dept': 'CS',
            'section': 'A'
        }
        # Register a student
        self.client.post(self.register_url, self.credentials, format='json')

    def test_student_login_success(self):
        """Test successful student login"""
        response = self.client.post(self.login_url, {
            'email': 'student@test.com',
            'password': 'TestPass123!'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['user_type'], 'student')

    def test_student_login_invalid_password(self):
        """Test login fails with invalid password"""
        response = self.client.post(self.login_url, {
            'email': 'student@test.com',
            'password': 'WrongPassword123!'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_student_login_nonexistent_user(self):
        """Test login fails with nonexistent user"""
        response = self.client.post(self.login_url, {
            'email': 'nonexistent@test.com',
            'password': 'TestPass123!'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TeacherRegistrationTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('teacher-register')
        self.valid_data = {
            'email': 'teacher@test.com',
            'password': 'TestPass123!',
            'password2': 'TestPass123!',
            'teacher_name': 'Test Teacher',
            'rfid': 'RFID002'
        }

    def test_teacher_registration_success(self):
        """Test successful teacher registration"""
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('teacher_id', response.data)
        self.assertEqual(response.data['email'], 'teacher@test.com')
        
        # Verify user and teacher were created
        self.assertTrue(User.objects.filter(email='teacher@test.com').exists())
        self.assertTrue(Teacher.objects.filter(email='teacher@test.com').exists())


class TeacherLoginTestCase(APITestCase):
    def setUp(self):
        self.register_url = reverse('teacher-register')
        self.login_url = reverse('teacher-login')
        self.credentials = {
            'email': 'teacher@test.com',
            'password': 'TestPass123!',
            'password2': 'TestPass123!',
            'teacher_name': 'Test Teacher',
            'rfid': 'RFID002'
        }
        # Register a teacher
        self.client.post(self.register_url, self.credentials, format='json')

    def test_teacher_login_success(self):
        """Test successful teacher login"""
        response = self.client.post(self.login_url, {
            'email': 'teacher@test.com',
            'password': 'TestPass123!'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['user_type'], 'teacher')


class ManagementRegistrationTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('management-register')
        self.valid_data = {
            'email': 'management@test.com',
            'password': 'TestPass123!',
            'password2': 'TestPass123!',
            'Management_name': 'Test Management'
        }

    def test_management_registration_success(self):
        """Test successful management registration"""
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('management_id', response.data)
        self.assertEqual(response.data['email'], 'management@test.com')
        
        # Verify user and management were created
        self.assertTrue(User.objects.filter(email='management@test.com').exists())
        self.assertTrue(Management.objects.filter(email='management@test.com').exists())


class ManagementLoginTestCase(APITestCase):
    def setUp(self):
        self.register_url = reverse('management-register')
        self.login_url = reverse('management-login')
        self.credentials = {
            'email': 'management@test.com',
            'password': 'TestPass123!',
            'password2': 'TestPass123!',
            'Management_name': 'Test Management'
        }
        # Register a management user
        self.client.post(self.register_url, self.credentials, format='json')

    def test_management_login_success(self):
        """Test successful management login"""
        response = self.client.post(self.login_url, {
            'email': 'management@test.com',
            'password': 'TestPass123!'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['user_type'], 'management')


class UserTypeSeparationTestCase(APITestCase):
    """Test that users can only login through their correct user type endpoint"""
    
    def test_student_cannot_login_as_teacher(self):
        """Test that a student cannot login through teacher endpoint"""
        # Register a student
        student_register_url = reverse('student-register')
        student_data = {
            'email': 'student@test.com',
            'password': 'TestPass123!',
            'password2': 'TestPass123!',
            'student_name': 'Test Student',
            'rfid': 'RFID001',
            'year': 1,
            'dept': 'CS',
            'section': 'A'
        }
        self.client.post(student_register_url, student_data, format='json')
        
        # Try to login as teacher
        teacher_login_url = reverse('teacher-login')
        response = self.client.post(teacher_login_url, {
            'email': 'student@test.com',
            'password': 'TestPass123!'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# ============ CRUD Tests for Models ============

class AuthenticatedAPITestCase(APITestCase):
    """Base class for authenticated API tests"""
    
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(
            username='testuser@test.com',
            email='testuser@test.com',
            password='TestPass123!'
        )
        self.client.force_authenticate(user=self.user)


class StudentCRUDTestCase(AuthenticatedAPITestCase):
    """Test CRUD operations for Student model"""
    
    def setUp(self):
        super().setUp()
        # Create a student for testing
        self.student = Student.objects.create(
            student_name='Test Student',
            email='student@test.com',
            rfid='RFID001',
            year=1,
            dept='CS',
            section='A'
        )
        self.list_url = reverse('student-list')
        self.detail_url = reverse('student-detail', args=[self.student.student_id])
    
    def test_list_students(self):
        """Test listing all students"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_retrieve_student(self):
        """Test retrieving a single student"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['student_name'], 'Test Student')
    
    def test_update_student(self):
        """Test updating a student"""
        data = {'student_name': 'Updated Student', 'email': 'updated@test.com', 'rfid': 'RFID001', 'year': 2, 'dept': 'IT', 'section': 'B'}
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['student_name'], 'Updated Student')
    
    def test_partial_update_student(self):
        """Test partially updating a student"""
        data = {'student_name': 'Partially Updated'}
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['student_name'], 'Partially Updated')
    
    def test_delete_student(self):
        """Test deleting a student"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Student.objects.filter(student_id=self.student.student_id).exists())
    
    def test_filter_students_by_year(self):
        """Test filtering students by year"""
        Student.objects.create(student_name='Year 2 Student', email='year2@test.com', rfid='RFID002', year=2, dept='CS', section='A')
        response = self.client.get(self.list_url, {'year': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['year'], 1)


class TeacherCRUDTestCase(AuthenticatedAPITestCase):
    """Test CRUD operations for Teacher model"""
    
    def setUp(self):
        super().setUp()
        self.teacher = Teacher.objects.create(
            teacher_name='Test Teacher',
            email='teacher@test.com',
            rfid='RFID001'
        )
        self.list_url = reverse('teacher-list')
        self.detail_url = reverse('teacher-detail', args=[self.teacher.teacher_id])
    
    def test_list_teachers(self):
        """Test listing all teachers"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_retrieve_teacher(self):
        """Test retrieving a single teacher"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['teacher_name'], 'Test Teacher')
    
    def test_update_teacher(self):
        """Test updating a teacher"""
        data = {'teacher_name': 'Updated Teacher', 'email': 'updated@test.com', 'rfid': 'RFID001'}
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['teacher_name'], 'Updated Teacher')
    
    def test_delete_teacher(self):
        """Test deleting a teacher"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ManagementCRUDTestCase(AuthenticatedAPITestCase):
    """Test CRUD operations for Management model"""
    
    def setUp(self):
        super().setUp()
        self.management = Management.objects.create(
            Management_name='Test Management',
            email='management@test.com'
        )
        self.list_url = reverse('management-list')
        self.detail_url = reverse('management-detail', args=[self.management.Management_id])
    
    def test_list_management(self):
        """Test listing all management users"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_retrieve_management(self):
        """Test retrieving a single management user"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Management_name'], 'Test Management')
    
    def test_update_management(self):
        """Test updating a management user"""
        data = {'Management_name': 'Updated Management', 'email': 'updated@test.com'}
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Management_name'], 'Updated Management')
    
    def test_delete_management(self):
        """Test deleting a management user"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CourseCRUDTestCase(AuthenticatedAPITestCase):
    """Test CRUD operations for Course model"""
    
    def setUp(self):
        super().setUp()
        self.course = Course.objects.create(course_name='Test Course')
        self.list_url = reverse('course-list')
        self.detail_url = reverse('course-detail', args=[self.course.course_id])
    
    def test_list_courses(self):
        """Test listing all courses"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_course(self):
        """Test creating a course"""
        data = {'course_name': 'New Course'}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['course_name'], 'New Course')
    
    def test_retrieve_course(self):
        """Test retrieving a single course"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['course_name'], 'Test Course')
    
    def test_update_course(self):
        """Test updating a course"""
        data = {'course_name': 'Updated Course'}
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['course_name'], 'Updated Course')
    
    def test_delete_course(self):
        """Test deleting a course"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ClassCRUDTestCase(AuthenticatedAPITestCase):
    """Test CRUD operations for Class model"""
    
    def setUp(self):
        super().setUp()
        self.classroom = Class.objects.create(scanner_id='SCANNER001')
        self.list_url = reverse('class-list')
        self.detail_url = reverse('class-detail', args=[self.classroom.classroom_id])
    
    def test_list_classes(self):
        """Test listing all classes"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_class(self):
        """Test creating a class"""
        data = {'scanner_id': 'SCANNER002'}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['scanner_id'], 'SCANNER002')
    
    def test_retrieve_class(self):
        """Test retrieving a single class"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['scanner_id'], 'SCANNER001')
    
    def test_update_class(self):
        """Test updating a class"""
        data = {'scanner_id': 'UPDATED_SCANNER'}
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['scanner_id'], 'UPDATED_SCANNER')
    
    def test_delete_class(self):
        """Test deleting a class"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TaughtCourseCRUDTestCase(AuthenticatedAPITestCase):
    """Test CRUD operations for TaughtCourse model"""
    
    def setUp(self):
        super().setUp()
        self.course = Course.objects.create(course_name='Test Course')
        self.teacher = Teacher.objects.create(teacher_name='Test Teacher', email='teacher@test.com', rfid='RFID001')
        self.taught_course = TaughtCourse.objects.create(
            course=self.course,
            teacher=self.teacher,
            classes_taken='Class A, Class B'
        )
        self.list_url = reverse('taughtcourse-list')
        self.detail_url = reverse('taughtcourse-detail', args=[self.taught_course.id])
    
    def test_list_taught_courses(self):
        """Test listing all taught courses"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_taught_course(self):
        """Test creating a taught course"""
        new_teacher = Teacher.objects.create(teacher_name='New Teacher', email='new@test.com', rfid='RFID002')
        data = {'course': self.course.course_id, 'teacher': new_teacher.teacher_id, 'classes_taken': 'Class C'}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_retrieve_taught_course(self):
        """Test retrieving a single taught course"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['course_name'], 'Test Course')
        self.assertEqual(response.data['teacher_name'], 'Test Teacher')
    
    def test_update_taught_course(self):
        """Test updating a taught course"""
        data = {'course': self.course.course_id, 'teacher': self.teacher.teacher_id, 'classes_taken': 'Class D, Class E'}
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['classes_taken'], 'Class D, Class E')
    
    def test_delete_taught_course(self):
        """Test deleting a taught course"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_filter_by_teacher(self):
        """Test filtering taught courses by teacher"""
        response = self.client.get(self.list_url, {'teacher': self.teacher.teacher_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class StudentCourseCRUDTestCase(AuthenticatedAPITestCase):
    """Test CRUD operations for StudentCourse model"""
    
    def setUp(self):
        super().setUp()
        self.student = Student.objects.create(student_name='Test Student', email='student@test.com', rfid='RFID001', year=1, dept='CS', section='A')
        self.course = Course.objects.create(course_name='Test Course')
        self.teacher = Teacher.objects.create(teacher_name='Test Teacher', email='teacher@test.com', rfid='RFID002')
        self.student_course = StudentCourse.objects.create(
            student=self.student,
            course=self.course,
            teacher=self.teacher,
            classes_attended='Class A'
        )
        self.list_url = reverse('studentcourse-list')
        self.detail_url = reverse('studentcourse-detail', args=[self.student_course.id])
    
    def test_list_student_courses(self):
        """Test listing all student courses"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_student_course(self):
        """Test creating a student course"""
        new_student = Student.objects.create(student_name='New Student', email='new@test.com', rfid='RFID003', year=2, dept='IT', section='B')
        data = {'student': new_student.student_id, 'course': self.course.course_id, 'teacher': self.teacher.teacher_id, 'classes_attended': 'Class B'}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_retrieve_student_course(self):
        """Test retrieving a single student course"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['student_name'], 'Test Student')
        self.assertEqual(response.data['course_name'], 'Test Course')
        self.assertEqual(response.data['teacher_name'], 'Test Teacher')
    
    def test_update_student_course(self):
        """Test updating a student course"""
        data = {'student': self.student.student_id, 'course': self.course.course_id, 'teacher': self.teacher.teacher_id, 'classes_attended': 'Class A, Class B'}
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['classes_attended'], 'Class A, Class B')
    
    def test_delete_student_course(self):
        """Test deleting a student course"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_filter_by_student(self):
        """Test filtering student courses by student"""
        response = self.client.get(self.list_url, {'student': self.student.student_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class UnauthenticatedAccessTestCase(APITestCase):
    """Test that CRUD endpoints require authentication"""
    
    def test_unauthenticated_access_denied(self):
        """Test that unauthenticated users cannot access CRUD endpoints"""
        endpoints = [
            reverse('student-list'),
            reverse('teacher-list'),
            reverse('management-list'),
            reverse('course-list'),
            reverse('class-list'),
            reverse('taughtcourse-list'),
            reverse('studentcourse-list'),
            reverse('updateattendancerequest-list'),
        ]
        for url in endpoints:
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UpdateAttendanceRequestCRUDTestCase(AuthenticatedAPITestCase):
    """Test CRUD operations for UpdateAttendanceRequest model"""
    
    def setUp(self):
        super().setUp()
        # Create required related objects
        self.teacher = Teacher.objects.create(
            teacher_name='Test Teacher',
            email='teacher@test.com',
            rfid='RFID001'
        )
        self.student = Student.objects.create(
            student_name='Test Student',
            email='student@test.com',
            rfid='RFID002',
            year=1,
            dept='CS',
            section='A'
        )
        self.course = Course.objects.create(course_name='Test Course')
        
        # Create an update attendance request
        self.attendance_request = UpdateAttendanceRequest.objects.create(
            teacher=self.teacher,
            student=self.student,
            course=self.course,
            classes_to_add='Class A, Class B',
            reason='Student was marked absent by mistake'
        )
        
        self.list_url = reverse('updateattendancerequest-list')
        self.detail_url = reverse('updateattendancerequest-detail', args=[self.attendance_request.id])
    
    def test_list_update_attendance_requests(self):
        """Test listing all update attendance requests"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_update_attendance_request(self):
        """Test creating an update attendance request"""
        new_student = Student.objects.create(
            student_name='New Student',
            email='new@test.com',
            rfid='RFID003',
            year=2,
            dept='IT',
            section='B'
        )
        data = {
            'teacher': self.teacher.teacher_id,
            'student': new_student.student_id,
            'course': self.course.course_id,
            'classes_to_add': 'Class C',
            'reason': 'Late arrival registered'
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['classes_to_add'], 'Class C')
        self.assertEqual(response.data['status'], 'pending')
    
    def test_retrieve_update_attendance_request(self):
        """Test retrieving a single update attendance request"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['teacher_name'], 'Test Teacher')
        self.assertEqual(response.data['student_name'], 'Test Student')
        self.assertEqual(response.data['course_name'], 'Test Course')
        self.assertEqual(response.data['status'], 'pending')
    
    def test_update_attendance_request(self):
        """Test updating an update attendance request"""
        data = {
            'teacher': self.teacher.teacher_id,
            'student': self.student.student_id,
            'course': self.course.course_id,
            'classes_to_add': 'Class D, Class E',
            'reason': 'Updated reason'
        }
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['classes_to_add'], 'Class D, Class E')
        self.assertEqual(response.data['reason'], 'Updated reason')
    
    def test_delete_update_attendance_request(self):
        """Test deleting an update attendance request"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(UpdateAttendanceRequest.objects.filter(id=self.attendance_request.id).exists())
    
    def test_filter_by_status(self):
        """Test filtering update attendance requests by status"""
        response = self.client.get(self.list_url, {'status': 'pending'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
        response = self.client.get(self.list_url, {'status': 'approved'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
    
    def test_filter_by_teacher(self):
        """Test filtering update attendance requests by teacher"""
        response = self.client.get(self.list_url, {'teacher': self.teacher.teacher_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class UpdateAttendanceRequestApproveRejectTestCase(APITestCase):
    """Test approve and reject functionality for UpdateAttendanceRequest"""
    
    def setUp(self):
        # Create management user for approving/rejecting
        self.management_user = User.objects.create_user(
            username='management@test.com',
            email='management@test.com',
            password='TestPass123!'
        )
        self.management = Management.objects.create(
            user=self.management_user,
            email='management@test.com',
            Management_name='Test Management'
        )
        
        # Create regular user (non-management)
        self.regular_user = User.objects.create_user(
            username='regular@test.com',
            email='regular@test.com',
            password='TestPass123!'
        )
        
        # Create required related objects
        self.teacher = Teacher.objects.create(
            teacher_name='Test Teacher',
            email='teacher@test.com',
            rfid='RFID001'
        )
        self.student = Student.objects.create(
            student_name='Test Student',
            email='student@test.com',
            rfid='RFID002',
            year=1,
            dept='CS',
            section='A'
        )
        self.course = Course.objects.create(course_name='Test Course')
        
        # Create an update attendance request
        self.attendance_request = UpdateAttendanceRequest.objects.create(
            teacher=self.teacher,
            student=self.student,
            course=self.course,
            classes_to_add='Class A, Class B',
            reason='Student was marked absent by mistake'
        )
        
        self.approve_url = reverse('updateattendancerequest-approve', args=[self.attendance_request.id])
        self.reject_url = reverse('updateattendancerequest-reject', args=[self.attendance_request.id])
    
    def test_approve_request_by_management(self):
        """Test that management can approve attendance requests"""
        self.client.force_authenticate(user=self.management_user)
        response = self.client.post(self.approve_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['request']['status'], 'approved')
        
        # Verify StudentCourse was created/updated
        student_course = StudentCourse.objects.get(
            student=self.student,
            course=self.course,
            teacher=self.teacher
        )
        self.assertEqual(student_course.classes_attended, 'Class A, Class B')
        
        # Verify the request was updated
        self.attendance_request.refresh_from_db()
        self.assertEqual(self.attendance_request.status, 'approved')
        self.assertEqual(self.attendance_request.processed_by, self.management)
        self.assertIsNotNone(self.attendance_request.processed_at)
    
    def test_approve_request_updates_existing_attendance(self):
        """Test that approving a request updates existing attendance"""
        # Create existing StudentCourse
        student_course = StudentCourse.objects.create(
            student=self.student,
            course=self.course,
            teacher=self.teacher,
            classes_attended='Class X'
        )
        
        self.client.force_authenticate(user=self.management_user)
        response = self.client.post(self.approve_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify attendance was appended
        student_course.refresh_from_db()
        self.assertEqual(student_course.classes_attended, 'Class X, Class A, Class B')
    
    def test_reject_request_by_management(self):
        """Test that management can reject attendance requests"""
        self.client.force_authenticate(user=self.management_user)
        response = self.client.post(self.reject_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['request']['status'], 'rejected')
        
        # Verify no StudentCourse was created
        self.assertFalse(StudentCourse.objects.filter(
            student=self.student,
            course=self.course,
            teacher=self.teacher
        ).exists())
        
        # Verify the request was updated
        self.attendance_request.refresh_from_db()
        self.assertEqual(self.attendance_request.status, 'rejected')
        self.assertEqual(self.attendance_request.processed_by, self.management)
        self.assertIsNotNone(self.attendance_request.processed_at)
    
    def test_non_management_cannot_approve(self):
        """Test that non-management users cannot approve requests"""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.post(self.approve_url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Verify request was not changed
        self.attendance_request.refresh_from_db()
        self.assertEqual(self.attendance_request.status, 'pending')
    
    def test_non_management_cannot_reject(self):
        """Test that non-management users cannot reject requests"""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.post(self.reject_url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Verify request was not changed
        self.attendance_request.refresh_from_db()
        self.assertEqual(self.attendance_request.status, 'pending')
    
    def test_cannot_approve_already_processed_request(self):
        """Test that already processed requests cannot be approved again"""
        # First approve the request
        self.client.force_authenticate(user=self.management_user)
        self.client.post(self.approve_url)
        
        # Try to approve again
        response = self.client.post(self.approve_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('already been approved', response.data['error'])
    
    def test_cannot_reject_already_processed_request(self):
        """Test that already processed requests cannot be rejected"""
        # First reject the request
        self.client.force_authenticate(user=self.management_user)
        self.client.post(self.reject_url)
        
        # Try to reject again
        response = self.client.post(self.reject_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('already been rejected', response.data['error'])
    
    def test_unauthenticated_cannot_approve(self):
        """Test that unauthenticated users cannot approve requests"""
        response = self.client.post(self.approve_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_unauthenticated_cannot_reject(self):
        """Test that unauthenticated users cannot reject requests"""
        response = self.client.post(self.reject_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# ============ Attendance Session Tests ============

class AttendanceSessionTestCase(APITestCase):
    """Test attendance session functionality"""
    
    def setUp(self):
        # Create authenticated user
        self.user = User.objects.create_user(
            username='teacher@test.com',
            email='teacher@test.com',
            password='TestPass123!'
        )
        self.teacher = Teacher.objects.create(
            user=self.user,
            teacher_name='Test Teacher',
            email='teacher@test.com',
            rfid='RFID001'
        )
        self.course = Course.objects.create(course_name='Test Course')
        
        self.client.force_authenticate(user=self.user)
        
        self.session_url = reverse('attendancesession-list')
    
    def test_create_attendance_session(self):
        """Test creating/starting an attendance session"""
        data = {
            'teacher': self.teacher.teacher_id,
            'course': self.course.course_id,
            'section': 'A',
            'year': 1
        }
        response = self.client.post(self.session_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['session']['status'], 'active')
        self.assertIn('qr_code_token', response.data['session'])
        self.assertIsNotNone(response.data['session']['qr_code_token'])
    
    def test_list_attendance_sessions(self):
        """Test listing attendance sessions"""
        AttendanceSession.objects.create(
            teacher=self.teacher,
            course=self.course,
            section='A',
            year=1,
            qr_code_token='test_token_1'
        )
        
        response = self.client.get(self.session_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_stop_attendance_session(self):
        """Test stopping an active attendance session"""
        session = AttendanceSession.objects.create(
            teacher=self.teacher,
            course=self.course,
            section='A',
            year=1,
            qr_code_token='test_token_1',
            status='active'
        )
        
        stop_url = reverse('attendancesession-stop', args=[session.id])
        response = self.client.post(stop_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['session']['status'], 'stopped')
        self.assertIsNotNone(response.data['session']['stopped_at'])
    
    def test_cannot_stop_already_stopped_session(self):
        """Test that already stopped sessions cannot be stopped again"""
        session = AttendanceSession.objects.create(
            teacher=self.teacher,
            course=self.course,
            section='A',
            year=1,
            qr_code_token='test_token_1',
            status='stopped'
        )
        
        stop_url = reverse('attendancesession-stop', args=[session.id])
        response = self.client.post(stop_url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_get_qr_code(self):
        """Test getting QR code for an active session"""
        session = AttendanceSession.objects.create(
            teacher=self.teacher,
            course=self.course,
            section='A',
            year=1,
            qr_code_token='test_token_1',
            status='active'
        )
        
        qr_url = reverse('attendancesession-qr', args=[session.id])
        response = self.client.get(qr_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('qr_code', response.data)
        self.assertIn('qr_token', response.data)
        self.assertIn('data:image/png;base64,', response.data['qr_code'])
    
    def test_cannot_get_qr_for_stopped_session(self):
        """Test that QR code cannot be generated for stopped sessions"""
        session = AttendanceSession.objects.create(
            teacher=self.teacher,
            course=self.course,
            section='A',
            year=1,
            qr_code_token='test_token_1',
            status='stopped'
        )
        
        qr_url = reverse('attendancesession-qr', args=[session.id])
        response = self.client.get(qr_url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_filter_sessions_by_teacher(self):
        """Test filtering sessions by teacher"""
        other_teacher = Teacher.objects.create(
            teacher_name='Other Teacher',
            email='other@test.com',
            rfid='RFID002'
        )
        
        AttendanceSession.objects.create(
            teacher=self.teacher,
            course=self.course,
            section='A',
            year=1,
            qr_code_token='test_token_1'
        )
        
        AttendanceSession.objects.create(
            teacher=other_teacher,
            course=self.course,
            section='B',
            year=2,
            qr_code_token='test_token_2'
        )
        
        response = self.client.get(self.session_url, {'teacher': self.teacher.teacher_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['teacher'], self.teacher.teacher_id)


class RFIDScanTestCase(APITestCase):
    """Test RFID scanning functionality"""
    
    def setUp(self):
        self.teacher = Teacher.objects.create(
            teacher_name='Test Teacher',
            email='teacher@test.com',
            rfid='RFID001'
        )
        self.course = Course.objects.create(course_name='Test Course')
        self.student = Student.objects.create(
            student_name='Test Student',
            email='student@test.com',
            rfid='RFID_STUDENT_1',
            year=1,
            dept='CS',
            section='A'
        )
        self.session = AttendanceSession.objects.create(
            teacher=self.teacher,
            course=self.course,
            section='A',
            year=1,
            qr_code_token='test_token_1',
            status='active'
        )
        
        self.rfid_scan_url = reverse('rfid-scan')
    
    def test_rfid_scan_success(self):
        """Test successful RFID scan"""
        data = {
            'rfid': 'RFID_STUDENT_1',
            'session_id': self.session.id
        }
        response = self.client.post(self.rfid_scan_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['rfid_scanned'])
        self.assertFalse(response.data['qr_scanned'])
        self.assertFalse(response.data['is_present'])
        self.assertTrue(response.data['needs_qr'])
        
        # Verify record was created
        record = AttendanceRecord.objects.get(session=self.session, student=self.student)
        self.assertTrue(record.rfid_scanned)
        self.assertFalse(record.qr_scanned)
        self.assertFalse(record.is_present)
    
    def test_rfid_scan_invalid_student(self):
        """Test RFID scan with invalid student RFID"""
        data = {
            'rfid': 'INVALID_RFID',
            'session_id': self.session.id
        }
        response = self.client.post(self.rfid_scan_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_rfid_scan_inactive_session(self):
        """Test RFID scan on inactive session"""
        self.session.status = 'stopped'
        self.session.save()
        
        data = {
            'rfid': 'RFID_STUDENT_1',
            'session_id': self.session.id
        }
        response = self.client.post(self.rfid_scan_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_rfid_scan_wrong_section(self):
        """Test RFID scan with student from different section"""
        self.student.section = 'B'
        self.student.save()
        
        data = {
            'rfid': 'RFID_STUDENT_1',
            'session_id': self.session.id
        }
        response = self.client.post(self.rfid_scan_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class QRScanTestCase(APITestCase):
    """Test QR code scanning functionality"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='student@test.com',
            email='student@test.com',
            password='TestPass123!'
        )
        self.teacher = Teacher.objects.create(
            teacher_name='Test Teacher',
            email='teacher@test.com',
            rfid='RFID001'
        )
        self.course = Course.objects.create(course_name='Test Course')
        self.student = Student.objects.create(
            user=self.user,
            student_name='Test Student',
            email='student@test.com',
            rfid='RFID_STUDENT_1',
            year=1,
            dept='CS',
            section='A'
        )
        self.session = AttendanceSession.objects.create(
            teacher=self.teacher,
            course=self.course,
            section='A',
            year=1,
            qr_code_token='test_token_1',
            status='active'
        )
        
        self.client.force_authenticate(user=self.user)
        self.qr_scan_url = reverse('qr-scan')
    
    def test_qr_scan_success(self):
        """Test successful QR scan"""
        data = {
            'qr_token': 'test_token_1',
            'student_id': self.student.student_id
        }
        response = self.client.post(self.qr_scan_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['rfid_scanned'])
        self.assertTrue(response.data['qr_scanned'])
        self.assertFalse(response.data['is_present'])
        self.assertTrue(response.data['needs_rfid'])
        
        # Verify record was created
        record = AttendanceRecord.objects.get(session=self.session, student=self.student)
        self.assertFalse(record.rfid_scanned)
        self.assertTrue(record.qr_scanned)
        self.assertFalse(record.is_present)
    
    def test_qr_scan_invalid_token(self):
        """Test QR scan with invalid token"""
        data = {
            'qr_token': 'invalid_token',
            'student_id': self.student.student_id
        }
        response = self.client.post(self.qr_scan_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_qr_scan_inactive_session(self):
        """Test QR scan on inactive session"""
        self.session.status = 'stopped'
        self.session.save()
        
        data = {
            'qr_token': 'test_token_1',
            'student_id': self.student.student_id
        }
        response = self.client.post(self.qr_scan_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TwoFactorAttendanceTestCase(APITestCase):
    """Test 2FA attendance (RFID + QR)"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='student@test.com',
            email='student@test.com',
            password='TestPass123!'
        )
        self.teacher = Teacher.objects.create(
            teacher_name='Test Teacher',
            email='teacher@test.com',
            rfid='RFID001'
        )
        self.course = Course.objects.create(course_name='Test Course')
        self.student = Student.objects.create(
            user=self.user,
            student_name='Test Student',
            email='student@test.com',
            rfid='RFID_STUDENT_1',
            year=1,
            dept='CS',
            section='A'
        )
        self.session = AttendanceSession.objects.create(
            teacher=self.teacher,
            course=self.course,
            section='A',
            year=1,
            qr_code_token='test_token_1',
            status='active'
        )
        
        self.client.force_authenticate(user=self.user)
        self.rfid_scan_url = reverse('rfid-scan')
        self.qr_scan_url = reverse('qr-scan')
    
    def test_both_scans_marks_present(self):
        """Test that both RFID and QR scans mark student as present"""
        # First scan RFID
        rfid_data = {
            'rfid': 'RFID_STUDENT_1',
            'session_id': self.session.id
        }
        rfid_response = self.client.post(self.rfid_scan_url, rfid_data, format='json')
        self.assertEqual(rfid_response.status_code, status.HTTP_200_OK)
        self.assertFalse(rfid_response.data['is_present'])
        
        # Then scan QR
        qr_data = {
            'qr_token': 'test_token_1',
            'student_id': self.student.student_id
        }
        qr_response = self.client.post(self.qr_scan_url, qr_data, format='json')
        self.assertEqual(qr_response.status_code, status.HTTP_200_OK)
        self.assertTrue(qr_response.data['is_present'])
        
        # Verify record shows present
        record = AttendanceRecord.objects.get(session=self.session, student=self.student)
        self.assertTrue(record.rfid_scanned)
        self.assertTrue(record.qr_scanned)
        self.assertTrue(record.is_present)
        self.assertIsNotNone(record.marked_present_at)
        
        # Verify StudentCourse was updated
        student_course = StudentCourse.objects.get(
            student=self.student,
            course=self.course,
            teacher=self.teacher
        )
        self.assertIsNotNone(student_course.classes_attended)
        self.assertIn(self.session.started_at.strftime('%Y-%m-%d'), student_course.classes_attended)
    
    def test_qr_then_rfid_marks_present(self):
        """Test that scanning QR first then RFID also marks present"""
        # First scan QR
        qr_data = {
            'qr_token': 'test_token_1',
            'student_id': self.student.student_id
        }
        qr_response = self.client.post(self.qr_scan_url, qr_data, format='json')
        self.assertEqual(qr_response.status_code, status.HTTP_200_OK)
        self.assertFalse(qr_response.data['is_present'])
        
        # Then scan RFID
        rfid_data = {
            'rfid': 'RFID_STUDENT_1',
            'session_id': self.session.id
        }
        rfid_response = self.client.post(self.rfid_scan_url, rfid_data, format='json')
        self.assertEqual(rfid_response.status_code, status.HTTP_200_OK)
        self.assertTrue(rfid_response.data['is_present'])
        
        # Verify record shows present
        record = AttendanceRecord.objects.get(session=self.session, student=self.student)
        self.assertTrue(record.is_present)
    
    def test_only_rfid_does_not_mark_present(self):
        """Test that only RFID scan does not mark student as present"""
        rfid_data = {
            'rfid': 'RFID_STUDENT_1',
            'session_id': self.session.id
        }
        response = self.client.post(self.rfid_scan_url, rfid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['is_present'])
        
        # Verify no StudentCourse was created
        self.assertFalse(StudentCourse.objects.filter(
            student=self.student,
            course=self.course,
            teacher=self.teacher
        ).exists())
    
    def test_only_qr_does_not_mark_present(self):
        """Test that only QR scan does not mark student as present"""
        qr_data = {
            'qr_token': 'test_token_1',
            'student_id': self.student.student_id
        }
        response = self.client.post(self.qr_scan_url, qr_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['is_present'])
        
        # Verify no StudentCourse was created
        self.assertFalse(StudentCourse.objects.filter(
            student=self.student,
            course=self.course,
            teacher=self.teacher
        ).exists())
    
    def test_neither_scan_no_attendance(self):
        """Test that no scans means no attendance record"""
        # Verify no record exists
        self.assertFalse(AttendanceRecord.objects.filter(
            session=self.session,
            student=self.student
        ).exists())


class AttendanceSessionStatisticsTestCase(APITestCase):
    """Test attendance statistics endpoint"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='teacher@test.com',
            email='teacher@test.com',
            password='TestPass123!'
        )
        self.teacher = Teacher.objects.create(
            user=self.user,
            teacher_name='Test Teacher',
            email='teacher@test.com',
            rfid='RFID001'
        )
        self.course = Course.objects.create(course_name='Test Course')
        self.session = AttendanceSession.objects.create(
            teacher=self.teacher,
            course=self.course,
            section='A',
            year=1,
            qr_code_token='test_token_1',
            status='active'
        )
        
        # Create students
        self.student1 = Student.objects.create(
            student_name='Student 1',
            email='student1@test.com',
            rfid='RFID_1',
            year=1, dept='CS', section='A'
        )
        self.student2 = Student.objects.create(
            student_name='Student 2',
            email='student2@test.com',
            rfid='RFID_2',
            year=1, dept='CS', section='A'
        )
        self.student3 = Student.objects.create(
            student_name='Student 3',
            email='student3@test.com',
            rfid='RFID_3',
            year=1, dept='CS', section='A'
        )
        
        self.client.force_authenticate(user=self.user)
    
    def test_attendance_statistics(self):
        """Test getting attendance statistics for a session"""
        # Create different attendance scenarios
        # Student 1: Both RFID and QR (present)
        AttendanceRecord.objects.create(
            session=self.session,
            student=self.student1,
            rfid_scanned=True,
            qr_scanned=True,
            is_present=True
        )
        
        # Student 2: Only RFID (not present)
        AttendanceRecord.objects.create(
            session=self.session,
            student=self.student2,
            rfid_scanned=True,
            qr_scanned=False,
            is_present=False
        )
        
        # Student 3: Only QR (not present)
        AttendanceRecord.objects.create(
            session=self.session,
            student=self.student3,
            rfid_scanned=False,
            qr_scanned=True,
            is_present=False
        )
        
        attendance_url = reverse('attendancesession-attendance', args=[self.session.id])
        response = self.client.get(attendance_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['statistics']['total_students'], 3)
        self.assertEqual(response.data['statistics']['present'], 1)
        self.assertEqual(response.data['statistics']['absent'], 2)
        self.assertEqual(response.data['statistics']['rfid_only'], 1)
        self.assertEqual(response.data['statistics']['qr_only'], 1)


class TaughtCourseManagementUpdateTestCase(APITestCase):
    """Test management update functionality for TaughtCourse"""
    
    def setUp(self):
        # Create management user
        self.management_user = User.objects.create_user(
            username='management@test.com',
            email='management@test.com',
            password='TestPass123!'
        )
        self.management = Management.objects.create(
            user=self.management_user,
            email='management@test.com',
            Management_name='Test Management'
        )
        
        # Create regular user (non-management)
        self.regular_user = User.objects.create_user(
            username='regular@test.com',
            email='regular@test.com',
            password='TestPass123!'
        )
        
        # Create test data
        self.teacher = Teacher.objects.create(
            teacher_name='Test Teacher',
            email='teacher@test.com',
            rfid='RFID001'
        )
        self.course1 = Course.objects.create(course_name='Course 1', course_code='CS101')
        self.course2 = Course.objects.create(course_name='Course 2', course_code='CS102')
        
        self.taught_course = TaughtCourse.objects.create(
            course=self.course1,
            teacher=self.teacher,
            classes_taken='Class A',
            section='A',
            year=1
        )
        
        self.update_url = reverse('taughtcourse-management-update', args=[self.taught_course.id])
    
    def test_management_can_update_year(self):
        """Test that management can update year field"""
        self.client.force_authenticate(user=self.management_user)
        response = self.client.post(self.update_url, {'year': 2}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['taught_course']['year'], 2)
        self.assertEqual(response.data['message'], 'TaughtCourse updated successfully by management')
        
        # Verify database was updated
        self.taught_course.refresh_from_db()
        self.assertEqual(self.taught_course.year, 2)
    
    def test_management_can_update_section(self):
        """Test that management can update section field"""
        self.client.force_authenticate(user=self.management_user)
        response = self.client.post(self.update_url, {'section': 'B'}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['taught_course']['section'], 'B')
        
        # Verify database was updated
        self.taught_course.refresh_from_db()
        self.assertEqual(self.taught_course.section, 'B')
    
    def test_management_can_update_course(self):
        """Test that management can update course field"""
        self.client.force_authenticate(user=self.management_user)
        response = self.client.post(self.update_url, {'course': self.course2.course_id}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['taught_course']['course'], self.course2.course_id)
        
        # Verify database was updated
        self.taught_course.refresh_from_db()
        self.assertEqual(self.taught_course.course, self.course2)
    
    def test_management_can_update_multiple_fields(self):
        """Test that management can update multiple fields at once"""
        self.client.force_authenticate(user=self.management_user)
        data = {
            'year': 3,
            'section': 'C',
            'course': self.course2.course_id
        }
        response = self.client.post(self.update_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['taught_course']['year'], 3)
        self.assertEqual(response.data['taught_course']['section'], 'C')
        self.assertEqual(response.data['taught_course']['course'], self.course2.course_id)
        
        # Verify database was updated
        self.taught_course.refresh_from_db()
        self.assertEqual(self.taught_course.year, 3)
        self.assertEqual(self.taught_course.section, 'C')
        self.assertEqual(self.taught_course.course, self.course2)
    
    def test_management_update_with_patch_method(self):
        """Test that management can use PATCH method for updates"""
        self.client.force_authenticate(user=self.management_user)
        response = self.client.patch(self.update_url, {'year': 4}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['taught_course']['year'], 4)
    
    def test_non_management_cannot_update(self):
        """Test that non-management users cannot use this endpoint"""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.post(self.update_url, {'year': 2}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('Only management users', response.data['error'])
        
        # Verify database was not updated
        self.taught_course.refresh_from_db()
        self.assertEqual(self.taught_course.year, 1)
    
    def test_unauthenticated_user_cannot_update(self):
        """Test that unauthenticated users cannot use this endpoint"""
        response = self.client.post(self.update_url, {'year': 2}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_with_no_fields_returns_error(self):
        """Test that providing no fields returns an error"""
        self.client.force_authenticate(user=self.management_user)
        response = self.client.post(self.update_url, {}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('At least one of', response.data['error'])
    
    def test_update_with_invalid_course_id(self):
        """Test that providing invalid course_id returns an error"""
        self.client.force_authenticate(user=self.management_user)
        response = self.client.post(self.update_url, {'course': 99999}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('Course with id 99999 not found', response.data['error'])
    
    def test_update_with_invalid_course_id_prevents_partial_update(self):
        """Test that invalid course_id prevents any updates (year/section not updated)"""
        self.client.force_authenticate(user=self.management_user)
        data = {
            'year': 4,
            'section': 'D',
            'course': 99999  # Invalid course ID
        }
        response = self.client.post(self.update_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        # Verify that year and section were NOT updated
        self.taught_course.refresh_from_db()
        self.assertEqual(self.taught_course.year, 1)  # Original value
        self.assertEqual(self.taught_course.section, 'A')  # Original value
    
    def test_update_nonexistent_taught_course(self):
        """Test that updating a nonexistent TaughtCourse returns 404"""
        self.client.force_authenticate(user=self.management_user)
        nonexistent_url = reverse('taughtcourse-management-update', args=[99999])
        response = self.client.post(nonexistent_url, {'year': 2}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_preserves_other_fields(self):
        """Test that updating one field doesn't affect other fields"""
        self.client.force_authenticate(user=self.management_user)
        response = self.client.post(self.update_url, {'year': 2}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify other fields are unchanged
        self.taught_course.refresh_from_db()
        self.assertEqual(self.taught_course.section, 'A')
        self.assertEqual(self.taught_course.course, self.course1)
        self.assertEqual(self.taught_course.teacher, self.teacher)
        self.assertEqual(self.taught_course.classes_taken, 'Class A')


class BulkEnrollStudentsTestCase(APITestCase):
    """Test cases for bulk enrollment of students in courses"""
    
    def setUp(self):
        # Create management user
        self.management_user = User.objects.create_user(
            username='management@test.com',
            email='management@test.com',
            password='TestPass123!'
        )
        self.management = Management.objects.create(
            user=self.management_user,
            email='management@test.com',
            Management_name='Test Management'
        )
        
        # Create a teacher
        self.teacher = Teacher.objects.create(
            teacher_name='Test Teacher',
            email='teacher@test.com',
            rfid='RFID_TEACHER'
        )
        
        # Create courses
        self.course1 = Course.objects.create(
            course_name='Network Information Security',
            course_code='CT-486'
        )
        self.course2 = Course.objects.create(
            course_name='Database Systems',
            course_code='CS-301'
        )
        
        # Create students with different years and sections
        self.student1 = Student.objects.create(
            student_name='Student 1',
            email='student1@test.com',
            rfid='RFID001',
            year=2024,
            dept='CS',
            section='B'
        )
        self.student2 = Student.objects.create(
            student_name='Student 2',
            email='student2@test.com',
            rfid='RFID002',
            year=2024,
            dept='CS',
            section='B'
        )
        self.student3 = Student.objects.create(
            student_name='Student 3',
            email='student3@test.com',
            rfid='RFID003',
            year=2024,
            dept='CS',
            section='A'
        )
        self.student4 = Student.objects.create(
            student_name='Student 4',
            email='student4@test.com',
            rfid='RFID004',
            year=2023,
            dept='IT',
            section='B'
        )
        
        # Create TaughtCourse entries
        self.taught_course1 = TaughtCourse.objects.create(
            course=self.course1,
            teacher=self.teacher,
            year=2024,
            section='B',
            classes_taken=''
        )
        self.taught_course2 = TaughtCourse.objects.create(
            course=self.course2,
            teacher=self.teacher,
            year=2024,
            section='A',
            classes_taken=''
        )
        
        # Login as management
        self.client.force_authenticate(user=self.management_user)
    
    def test_bulk_enroll_by_year_section(self):
        """Test bulk enrollment of students by year and section"""
        url = reverse('studentcourse-bulk-enroll')
        data = {
            'course_id': self.course1.course_id,
            'year': 2024,
            'section': 'B'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['enrolled_count'], 2)
        self.assertEqual(response.data['skipped_count'], 0)
        
        # Verify StudentCourse entries were created
        self.assertTrue(StudentCourse.objects.filter(student=self.student1, course=self.course1).exists())
        self.assertTrue(StudentCourse.objects.filter(student=self.student2, course=self.course1).exists())
        self.assertFalse(StudentCourse.objects.filter(student=self.student3, course=self.course1).exists())
    
    def test_bulk_enroll_by_specific_student_ids(self):
        """Test bulk enrollment of specific students by IDs"""
        url = reverse('studentcourse-bulk-enroll')
        data = {
            'course_id': self.course1.course_id,
            'student_ids': [self.student1.student_id, self.student2.student_id]
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['enrolled_count'], 2)
        
        # Verify StudentCourse entries were created
        self.assertTrue(StudentCourse.objects.filter(student=self.student1, course=self.course1).exists())
        self.assertTrue(StudentCourse.objects.filter(student=self.student2, course=self.course1).exists())
    
    def test_bulk_enroll_with_dept_filter(self):
        """Test bulk enrollment with department filter"""
        url = reverse('studentcourse-bulk-enroll')
        data = {
            'course_id': self.course1.course_id,
            'year': 2024,
            'section': 'B',
            'dept': 'CS'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['enrolled_count'], 2)
    
    def test_bulk_enroll_already_enrolled_students(self):
        """Test bulk enrollment skips already enrolled students"""
        # Pre-enroll student1
        StudentCourse.objects.create(
            student=self.student1,
            course=self.course1,
            teacher=self.teacher,
            classes_attended=''
        )
        
        url = reverse('studentcourse-bulk-enroll')
        data = {
            'course_id': self.course1.course_id,
            'year': 2024,
            'section': 'B'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['enrolled_count'], 1)  # Only student2 enrolled
        self.assertEqual(response.data['skipped_count'], 1)  # student1 skipped
    
    def test_bulk_enroll_no_teacher_assigned(self):
        """Test bulk enrollment when no teacher is assigned for the course"""
        url = reverse('studentcourse-bulk-enroll')
        data = {
            'course_id': self.course1.course_id,
            'year': 2023,  # No TaughtCourse for year 2023
            'section': 'B'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['enrolled_count'], 0)
        self.assertEqual(response.data['skipped_count'], 1)
        self.assertIn('No teacher assigned', response.data['skipped_students'][0]['reason'])
    
    def test_bulk_enroll_no_students_found(self):
        """Test bulk enrollment when no students match the criteria"""
        url = reverse('studentcourse-bulk-enroll')
        data = {
            'course_id': self.course1.course_id,
            'year': 2025,  # No students in year 2025
            'section': 'Z'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('No students found', response.data['error'])
    
    def test_bulk_enroll_invalid_course(self):
        """Test bulk enrollment with invalid course ID"""
        url = reverse('studentcourse-bulk-enroll')
        data = {
            'course_id': 9999,  # Non-existent course
            'year': 2024,
            'section': 'B'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('course_id', response.data)
    
    def test_bulk_enroll_missing_filters(self):
        """Test bulk enrollment fails when no filters are provided"""
        url = reverse('studentcourse-bulk-enroll')
        data = {
            'course_id': self.course1.course_id
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_bulk_enroll_non_management_user(self):
        """Test bulk enrollment fails for non-management users"""
        # Create and authenticate as a student
        student_user = User.objects.create_user(
            username='student@test.com',
            email='student@test.com',
            password='TestPass123!'
        )
        self.client.force_authenticate(user=student_user)
        
        url = reverse('studentcourse-bulk-enroll')
        data = {
            'course_id': self.course1.course_id,
            'year': 2024,
            'section': 'B'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SingleStudentEnrollTestCase(APITestCase):
    """Test cases for single student enrollment in courses"""
    
    def setUp(self):
        # Create management user
        self.management_user = User.objects.create_user(
            username='management@test.com',
            email='management@test.com',
            password='TestPass123!'
        )
        self.management = Management.objects.create(
            user=self.management_user,
            email='management@test.com',
            Management_name='Test Management'
        )
        
        # Create a teacher
        self.teacher = Teacher.objects.create(
            teacher_name='Test Teacher',
            email='teacher@test.com',
            rfid='RFID_TEACHER'
        )
        
        # Create a course
        self.course = Course.objects.create(
            course_name='Network Information Security',
            course_code='CT-486'
        )
        
        # Create a student
        self.student = Student.objects.create(
            student_name='Test Student',
            email='student@test.com',
            rfid='RFID001',
            year=2024,
            dept='CS',
            section='B'
        )
        
        # Create TaughtCourse entry
        self.taught_course = TaughtCourse.objects.create(
            course=self.course,
            teacher=self.teacher,
            year=2024,
            section='B',
            classes_taken=''
        )
        
        # Login as management
        self.client.force_authenticate(user=self.management_user)
    
    def test_single_student_enroll_success(self):
        """Test successful single student enrollment"""
        url = reverse('student-enroll-course', kwargs={'pk': self.student.student_id})
        data = {
            'course_id': self.course.course_id
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('Student enrolled successfully', response.data['message'])
        self.assertEqual(response.data['student_id'], self.student.student_id)
        self.assertEqual(response.data['course_id'], self.course.course_id)
        
        # Verify StudentCourse entry was created
        self.assertTrue(StudentCourse.objects.filter(
            student=self.student,
            course=self.course,
            teacher=self.teacher
        ).exists())
    
    def test_single_student_enroll_already_enrolled(self):
        """Test enrollment fails when student is already enrolled"""
        # Pre-enroll student
        StudentCourse.objects.create(
            student=self.student,
            course=self.course,
            teacher=self.teacher,
            classes_attended=''
        )
        
        url = reverse('student-enroll-course', kwargs={'pk': self.student.student_id})
        data = {
            'course_id': self.course.course_id
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('already enrolled', response.data['error'])
    
    def test_single_student_enroll_no_teacher_assigned(self):
        """Test enrollment fails when no teacher is assigned"""
        # Create a course without TaughtCourse
        course2 = Course.objects.create(
            course_name='Data Structures',
            course_code='CS-201'
        )
        
        url = reverse('student-enroll-course', kwargs={'pk': self.student.student_id})
        data = {
            'course_id': course2.course_id
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('No teacher assigned', response.data['error'])
    
    def test_single_student_enroll_invalid_course(self):
        """Test enrollment fails with invalid course ID"""
        url = reverse('student-enroll-course', kwargs={'pk': self.student.student_id})
        data = {
            'course_id': 9999  # Non-existent course
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_single_student_enroll_invalid_student(self):
        """Test enrollment fails with invalid student ID"""
        url = reverse('student-enroll-course', kwargs={'pk': 9999})
        data = {
            'course_id': self.course.course_id
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_single_student_enroll_non_management_user(self):
        """Test enrollment fails for non-management users"""
        # Create and authenticate as a teacher
        teacher_user = User.objects.create_user(
            username='teacher2@test.com',
            email='teacher2@test.com',
            password='TestPass123!'
        )
        self.client.force_authenticate(user=teacher_user)
        
        url = reverse('student-enroll-course', kwargs={'pk': self.student.student_id})
        data = {
            'course_id': self.course.course_id
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class BulkUpdateStudentCoursesTestCase(APITestCase):
    """Test cases for bulk update of student course enrollments"""
    
    def setUp(self):
        # Create management user
        self.management_user = User.objects.create_user(
            username='management@test.com',
            email='management@test.com',
            password='TestPass123!'
        )
        self.management = Management.objects.create(
            user=self.management_user,
            email='management@test.com',
            Management_name='Test Management'
        )
        
        # Create teachers
        self.teacher1 = Teacher.objects.create(
            teacher_name='Teacher 1',
            email='teacher1@test.com',
            rfid='RFID_TEACHER1'
        )
        self.teacher2 = Teacher.objects.create(
            teacher_name='Teacher 2',
            email='teacher2@test.com',
            rfid='RFID_TEACHER2'
        )
        
        # Create courses
        self.course1 = Course.objects.create(
            course_name='Database Systems',
            course_code='CS-301'
        )
        self.course2 = Course.objects.create(
            course_name='Network Security',
            course_code='CT-486'
        )
        
        # Create students
        self.student1 = Student.objects.create(
            student_name='Student 1',
            email='student1@test.com',
            rfid='RFID001',
            year=2024,
            dept='CS',
            section='B'
        )
        self.student2 = Student.objects.create(
            student_name='Student 2',
            email='student2@test.com',
            rfid='RFID002',
            year=2024,
            dept='CS',
            section='B'
        )
        self.student3 = Student.objects.create(
            student_name='Student 3',
            email='student3@test.com',
            rfid='RFID003',
            year=2024,
            dept='IT',
            section='A'
        )
        
        # Create existing StudentCourse enrollments
        self.sc1 = StudentCourse.objects.create(
            student=self.student1,
            course=self.course1,
            teacher=self.teacher1,
            classes_attended='2024-01-01, 2024-01-08'
        )
        self.sc2 = StudentCourse.objects.create(
            student=self.student2,
            course=self.course1,
            teacher=self.teacher1,
            classes_attended='2024-01-01'
        )
        self.sc3 = StudentCourse.objects.create(
            student=self.student3,
            course=self.course2,
            teacher=self.teacher2,
            classes_attended=''
        )
        
        # Login as management
        self.client.force_authenticate(user=self.management_user)
    
    def test_bulk_update_change_course(self):
        """Test bulk update to change course for students"""
        url = reverse('studentcourse-bulk-update')
        data = {
            'year': 2024,
            'section': 'B',
            'dept': 'CS',
            'current_course_id': self.course1.course_id,
            'new_course_id': self.course2.course_id
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['updated_count'], 2)
        
        # Verify updates
        self.sc1.refresh_from_db()
        self.sc2.refresh_from_db()
        self.assertEqual(self.sc1.course, self.course2)
        self.assertEqual(self.sc2.course, self.course2)
    
    def test_bulk_update_change_teacher(self):
        """Test bulk update to change teacher for students"""
        url = reverse('studentcourse-bulk-update')
        data = {
            'year': 2024,
            'section': 'B',
            'new_teacher_id': self.teacher2.teacher_id
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['updated_count'], 2)
        
        # Verify updates
        self.sc1.refresh_from_db()
        self.sc2.refresh_from_db()
        self.assertEqual(self.sc1.teacher, self.teacher2)
        self.assertEqual(self.sc2.teacher, self.teacher2)
    
    def test_bulk_update_change_attendance(self):
        """Test bulk update to modify classes_attended"""
        url = reverse('studentcourse-bulk-update')
        data = {
            'year': 2024,
            'section': 'B',
            'classes_attended': '2024-01-01, 2024-01-08, 2024-01-15'
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['updated_count'], 2)
        
        # Verify updates
        self.sc1.refresh_from_db()
        self.sc2.refresh_from_db()
        self.assertEqual(self.sc1.classes_attended, '2024-01-01, 2024-01-08, 2024-01-15')
        self.assertEqual(self.sc2.classes_attended, '2024-01-01, 2024-01-08, 2024-01-15')
    
    def test_bulk_update_multiple_fields(self):
        """Test bulk update changing multiple fields at once"""
        url = reverse('studentcourse-bulk-update')
        data = {
            'year': 2024,
            'section': 'B',
            'new_course_id': self.course2.course_id,
            'new_teacher_id': self.teacher2.teacher_id,
            'classes_attended': 'Updated'
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['updated_count'], 2)
        
        # Verify updates
        self.sc1.refresh_from_db()
        self.assertEqual(self.sc1.course, self.course2)
        self.assertEqual(self.sc1.teacher, self.teacher2)
        self.assertEqual(self.sc1.classes_attended, 'Updated')
    
    def test_bulk_update_by_student_ids(self):
        """Test bulk update using specific student IDs"""
        url = reverse('studentcourse-bulk-update')
        data = {
            'student_ids': [self.student1.student_id, self.student2.student_id],
            'new_teacher_id': self.teacher2.teacher_id
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['updated_count'], 2)
    
    def test_bulk_update_with_course_filter(self):
        """Test bulk update filtered by current course"""
        url = reverse('studentcourse-bulk-update')
        data = {
            'current_course_id': self.course1.course_id,
            'new_teacher_id': self.teacher2.teacher_id
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['updated_count'], 2)
        
        # Verify only course1 enrollments were updated
        self.sc1.refresh_from_db()
        self.sc2.refresh_from_db()
        self.sc3.refresh_from_db()
        self.assertEqual(self.sc1.teacher, self.teacher2)
        self.assertEqual(self.sc2.teacher, self.teacher2)
        # sc3 is enrolled in course2, so should NOT be affected (remains teacher2 from original setup)
        self.assertEqual(self.sc3.teacher, self.teacher2)
    
    def test_bulk_update_no_records_found(self):
        """Test bulk update when no records match criteria"""
        url = reverse('studentcourse-bulk-update')
        data = {
            'year': 2025,  # No students in year 2025
            'section': 'Z',
            'new_teacher_id': self.teacher2.teacher_id
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('No student course enrollments found', response.data['error'])
    
    def test_bulk_update_invalid_course(self):
        """Test bulk update with invalid course ID"""
        url = reverse('studentcourse-bulk-update')
        data = {
            'year': 2024,
            'section': 'B',
            'new_course_id': 9999  # Non-existent course
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('new_course_id', response.data)
    
    def test_bulk_update_invalid_teacher(self):
        """Test bulk update with invalid teacher ID"""
        url = reverse('studentcourse-bulk-update')
        data = {
            'year': 2024,
            'section': 'B',
            'new_teacher_id': 9999  # Non-existent teacher
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('new_teacher_id', response.data)
    
    def test_bulk_update_missing_filters_and_student_ids(self):
        """Test bulk update fails when no filters provided"""
        url = reverse('studentcourse-bulk-update')
        data = {
            'new_teacher_id': self.teacher2.teacher_id
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_bulk_update_missing_update_fields(self):
        """Test bulk update fails when no update fields provided"""
        url = reverse('studentcourse-bulk-update')
        data = {
            'year': 2024,
            'section': 'B'
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_bulk_update_non_management_user(self):
        """Test bulk update fails for non-management users"""
        # Create and authenticate as a student
        student_user = User.objects.create_user(
            username='student@test.com',
            email='student@test.com',
            password='TestPass123!'
        )
        self.client.force_authenticate(user=student_user)
        
        url = reverse('studentcourse-bulk-update')
        data = {
            'year': 2024,
            'section': 'B',
            'new_teacher_id': self.teacher2.teacher_id
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)




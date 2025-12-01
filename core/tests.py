from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Student, Teacher, Management, Course, Class, TaughtCourse, StudentCourse


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
        ]
        for url in endpoints:
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


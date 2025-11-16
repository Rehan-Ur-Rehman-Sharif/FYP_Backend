from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Student, Teacher, Management


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


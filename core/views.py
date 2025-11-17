from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    StudentRegistrationSerializer,
    TeacherRegistrationSerializer,
    ManagementRegistrationSerializer,
    LoginSerializer
)
from .models import Student, Teacher, Management, StudentCourse, TaughtCourse


class StudentRegistrationView(generics.CreateAPIView):
    """
    API endpoint for student registration
    """
    serializer_class = StudentRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            student = serializer.save()
            return Response({
                'message': 'Student registered successfully',
                'student_id': student.student_id,
                'email': student.email,
                'student_name': student.student_name
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherRegistrationView(generics.CreateAPIView):
    """
    API endpoint for teacher registration
    """
    serializer_class = TeacherRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            teacher = serializer.save()
            return Response({
                'message': 'Teacher registered successfully',
                'teacher_id': teacher.teacher_id,
                'email': teacher.email,
                'teacher_name': teacher.teacher_name
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ManagementRegistrationView(generics.CreateAPIView):
    """
    API endpoint for management registration
    """
    serializer_class = ManagementRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            management = serializer.save()
            return Response({
                'message': 'Management registered successfully',
                'management_id': management.Management_id,
                'email': management.email,
                'management_name': management.Management_name
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentLoginView(APIView):
    """
    API endpoint for student login
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            # Authenticate user
            user = authenticate(username=email, password=password)
            
            if user is not None:
                # Check if user has a student profile
                try:
                    student = Student.objects.get(user=user)
                    # Generate JWT tokens
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'message': 'Login successful',
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'user_type': 'student',
                        'student_id': student.student_id,
                        'student_name': student.student_name,
                        'email': student.email
                    }, status=status.HTTP_200_OK)
                except Student.DoesNotExist:
                    return Response({
                        'error': 'Student profile not found for this user'
                    }, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({
                    'error': 'Invalid email or password'
                }, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherLoginView(APIView):
    """
    API endpoint for teacher login
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            # Authenticate user
            user = authenticate(username=email, password=password)
            
            if user is not None:
                # Check if user has a teacher profile
                try:
                    teacher = Teacher.objects.get(user=user)
                    # Generate JWT tokens
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'message': 'Login successful',
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'user_type': 'teacher',
                        'teacher_id': teacher.teacher_id,
                        'teacher_name': teacher.teacher_name,
                        'email': teacher.email
                    }, status=status.HTTP_200_OK)
                except Teacher.DoesNotExist:
                    return Response({
                        'error': 'Teacher profile not found for this user'
                    }, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({
                    'error': 'Invalid email or password'
                }, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ManagementLoginView(APIView):
    """
    API endpoint for management login
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            # Authenticate user
            user = authenticate(username=email, password=password)
            
            if user is not None:
                # Check if user has a management profile
                try:
                    management = Management.objects.get(user=user)
                    # Generate JWT tokens
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'message': 'Login successful',
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'user_type': 'management',
                        'management_id': management.Management_id,
                        'management_name': management.Management_name,
                        'email': management.email
                    }, status=status.HTTP_200_OK)
                except Management.DoesNotExist:
                    return Response({
                        'error': 'Management profile not found for this user'
                    }, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({
                    'error': 'Invalid email or password'
                }, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Template-based views for login and register pages

def student_login_page(request):
    """
    Django template view for student login
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            try:
                student = Student.objects.get(user=user)
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('student-dashboard')
            except Student.DoesNotExist:
                messages.error(request, 'Student profile not found for this user')
        else:
            messages.error(request, 'Invalid email or password')
    
    return render(request, 'core/student_login.html')


def teacher_login_page(request):
    """
    Django template view for teacher login
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            try:
                teacher = Teacher.objects.get(user=user)
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('teacher-dashboard')
            except Teacher.DoesNotExist:
                messages.error(request, 'Teacher profile not found for this user')
        else:
            messages.error(request, 'Invalid email or password')
    
    return render(request, 'core/teacher_login.html')


def management_login_page(request):
    """
    Django template view for management login
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            try:
                management = Management.objects.get(user=user)
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('management-dashboard')
            except Management.DoesNotExist:
                messages.error(request, 'Management profile not found for this user')
        else:
            messages.error(request, 'Invalid email or password')
    
    return render(request, 'core/management_login.html')


def student_register_page(request):
    """
    Django template view for student registration
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        student_name = request.POST.get('student_name')
        rfid = request.POST.get('rfid')
        year = request.POST.get('year')
        dept = request.POST.get('dept')
        section = request.POST.get('section')
        
        errors = []
        
        # Validation
        if password != password2:
            errors.append("Passwords don't match")
        
        if User.objects.filter(email=email).exists():
            errors.append("Email already exists")
        
        try:
            validate_password(password)
        except ValidationError as e:
            errors.extend(e.messages)
        
        if not errors:
            try:
                # Create user
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password
                )
                
                # Create student
                student = Student.objects.create(
                    user=user,
                    email=email,
                    student_name=student_name,
                    rfid=rfid,
                    year=int(year),
                    dept=dept,
                    section=section
                )
                
                messages.success(request, 'Registration successful! Please login.')
                return redirect('student-login-page')
            except Exception as e:
                errors.append(str(e))
        
        return render(request, 'core/student_register.html', {'errors': errors})
    
    return render(request, 'core/student_register.html')


def teacher_register_page(request):
    """
    Django template view for teacher registration
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        teacher_name = request.POST.get('teacher_name')
        rfid = request.POST.get('rfid')
        
        errors = []
        
        # Validation
        if password != password2:
            errors.append("Passwords don't match")
        
        if User.objects.filter(email=email).exists():
            errors.append("Email already exists")
        
        try:
            validate_password(password)
        except ValidationError as e:
            errors.extend(e.messages)
        
        if not errors:
            try:
                # Create user
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password
                )
                
                # Create teacher
                teacher = Teacher.objects.create(
                    user=user,
                    email=email,
                    teacher_name=teacher_name,
                    rfid=rfid
                )
                
                messages.success(request, 'Registration successful! Please login.')
                return redirect('teacher-login-page')
            except Exception as e:
                errors.append(str(e))
        
        return render(request, 'core/teacher_register.html', {'errors': errors})
    
    return render(request, 'core/teacher_register.html')


def management_register_page(request):
    """
    Django template view for management registration
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        management_name = request.POST.get('Management_name')
        
        errors = []
        
        # Validation
        if password != password2:
            errors.append("Passwords don't match")
        
        if User.objects.filter(email=email).exists():
            errors.append("Email already exists")
        
        try:
            validate_password(password)
        except ValidationError as e:
            errors.extend(e.messages)
        
        if not errors:
            try:
                # Create user
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password
                )
                
                # Create management
                management = Management.objects.create(
                    user=user,
                    email=email,
                    Management_name=management_name
                )
                
                messages.success(request, 'Registration successful! Please login.')
                return redirect('management-login-page')
            except Exception as e:
                errors.append(str(e))
        
        return render(request, 'core/management_register.html', {'errors': errors})
    
    return render(request, 'core/management_register.html')


@login_required
def student_dashboard(request):
    """
    Dashboard view for students with attendance information
    """
    try:
        student = Student.objects.get(user=request.user)
        
        # Get course-wise attendance
        student_courses = StudentCourse.objects.filter(student=student).select_related('course', 'teacher')
        
        course_attendance = []
        for sc in student_courses:
            # Calculate attendance percentage for this course
            taught_course = TaughtCourse.objects.filter(
                course=sc.course, 
                teacher=sc.teacher
            ).first()
            
            if taught_course:
                # Parse classes attended and classes taken
                classes_attended = len(sc.classes_attended.split(',')) if sc.classes_attended else 0
                classes_taken = len(taught_course.classes_taken.split(',')) if taught_course.classes_taken else 0
                
                attendance_percentage = (classes_attended / classes_taken * 100) if classes_taken > 0 else 0
            else:
                attendance_percentage = 0
            
            course_attendance.append({
                'course_name': sc.course.course_name,
                'teacher_name': sc.teacher.teacher_name,
                'attendance': round(attendance_percentage, 1)
            })
        
        context = {
            'student_name': student.student_name,
            'student_id': student.student_id,
            'overall_attendance': round(student.overall_attendance, 1),
            'total_courses': len(course_attendance),
            'course_attendance': course_attendance,
        }
        
        return render(request, 'core/student_dashboard.html', context)
    except Student.DoesNotExist:
        messages.error(request, 'Student profile not found')
        return redirect('student-login-page')


@login_required
def teacher_dashboard(request):
    """
    Dashboard view for teachers
    """
    try:
        teacher = Teacher.objects.get(user=request.user)
        
        # Get courses taught by this teacher
        taught_courses = TaughtCourse.objects.filter(teacher=teacher).select_related('course')
        
        courses = []
        for tc in taught_courses:
            courses.append({
                'course_name': tc.course.course_name,
                'classes_taken': tc.classes_taken if tc.classes_taken else 'None'
            })
        
        context = {
            'teacher_name': teacher.teacher_name,
            'teacher_id': teacher.teacher_id,
            'email': teacher.email,
            'total_courses': len(courses),
            'courses': courses,
        }
        
        return render(request, 'core/teacher_dashboard.html', context)
    except Teacher.DoesNotExist:
        messages.error(request, 'Teacher profile not found')
        return redirect('teacher-login-page')


@login_required
def management_dashboard(request):
    """
    Dashboard view for management
    """
    try:
        management = Management.objects.get(user=request.user)
        
        context = {
            'management_name': management.Management_name,
            'management_id': management.Management_id,
            'email': management.email,
        }
        
        return render(request, 'core/management_dashboard.html', context)
    except Management.DoesNotExist:
        messages.error(request, 'Management profile not found')
        return redirect('management-login-page')


def logout_page(request):
    """
    Logout view
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('student-login-page')



from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    StudentRegistrationSerializer,
    TeacherRegistrationSerializer,
    ManagementRegistrationSerializer,
    LoginSerializer
)
from .models import Student, Teacher, Management


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


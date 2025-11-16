from django.urls import path
from .views import (
    StudentRegistrationView,
    TeacherRegistrationView,
    ManagementRegistrationView,
    StudentLoginView,
    TeacherLoginView,
    ManagementLoginView
)

urlpatterns = [
    # Registration endpoints
    path('auth/register/student/', StudentRegistrationView.as_view(), name='student-register'),
    path('auth/register/teacher/', TeacherRegistrationView.as_view(), name='teacher-register'),
    path('auth/register/management/', ManagementRegistrationView.as_view(), name='management-register'),
    
    # Login endpoints
    path('auth/login/student/', StudentLoginView.as_view(), name='student-login'),
    path('auth/login/teacher/', TeacherLoginView.as_view(), name='teacher-login'),
    path('auth/login/management/', ManagementLoginView.as_view(), name='management-login'),
]

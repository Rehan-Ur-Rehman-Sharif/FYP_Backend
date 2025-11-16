from django.urls import path
from .views import (
    StudentRegistrationView,
    TeacherRegistrationView,
    ManagementRegistrationView,
    StudentLoginView,
    TeacherLoginView,
    ManagementLoginView,
    student_login_page,
    teacher_login_page,
    management_login_page,
    student_register_page,
    teacher_register_page,
    management_register_page,
    student_dashboard,
    teacher_dashboard,
    management_dashboard,
    logout_page
)

urlpatterns = [
    # API Registration endpoints
    path('auth/register/student/', StudentRegistrationView.as_view(), name='student-register'),
    path('auth/register/teacher/', TeacherRegistrationView.as_view(), name='teacher-register'),
    path('auth/register/management/', ManagementRegistrationView.as_view(), name='management-register'),
    
    # API Login endpoints
    path('auth/login/student/', StudentLoginView.as_view(), name='student-login'),
    path('auth/login/teacher/', TeacherLoginView.as_view(), name='teacher-login'),
    path('auth/login/management/', ManagementLoginView.as_view(), name='management-login'),
    
    # Template-based login pages
    path('login/student/', student_login_page, name='student-login-page'),
    path('login/teacher/', teacher_login_page, name='teacher-login-page'),
    path('login/management/', management_login_page, name='management-login-page'),
    
    # Template-based register pages
    path('register/student/', student_register_page, name='student-register-page'),
    path('register/teacher/', teacher_register_page, name='teacher-register-page'),
    path('register/management/', management_register_page, name='management-register-page'),
    
    # Dashboard pages
    path('dashboard/student/', student_dashboard, name='student-dashboard'),
    path('dashboard/teacher/', teacher_dashboard, name='teacher-dashboard'),
    path('dashboard/management/', management_dashboard, name='management-dashboard'),
    
    # Logout
    path('logout/', logout_page, name='logout-page'),
]

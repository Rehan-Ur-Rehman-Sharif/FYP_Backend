from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.

class Department(models.Model):
    """Represents academic departments in the institution"""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True, help_text="Department code (e.g., CS, EE, ME)")
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    class Meta:
        ordering = ['code']


class Course(models.Model):
    """Represents courses that can be taught"""
    course_code = models.CharField(max_length=20, unique=True)
    course_name = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    credit_hours = models.PositiveIntegerField(default=3)
    
    def __str__(self):
        return f"{self.course_code} - {self.course_name}"
    
    class Meta:
        ordering = ['course_code']


class Student(models.Model):
    """Represents students in the system"""
    roll_number = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='students')
    section = models.CharField(max_length=10, help_text="Section (e.g., A, B, C)")
    
    def __str__(self):
        return f"{self.roll_number} - {self.name}"
    
    def get_overall_attendance(self):
        """Calculate overall attendance as average of all course attendances"""
        enrollments = self.enrollments.all()
        if not enrollments:
            return 0.0
        
        total_attendance = sum(enrollment.get_attendance_percentage() for enrollment in enrollments)
        return total_attendance / len(enrollments)
    
    class Meta:
        ordering = ['roll_number']


class Teacher(models.Model):
    """Represents teachers in the system"""
    roll_number = models.CharField(max_length=50, unique=True, help_text="Teacher ID/Roll Number")
    name = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='teacher_profile')
    
    def __str__(self):
        return f"{self.roll_number} - {self.name}"
    
    class Meta:
        ordering = ['roll_number']


class CourseOffering(models.Model):
    """Represents a course offering in a specific semester by a teacher"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='offerings')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='course_offerings')
    semester = models.CharField(max_length=20, help_text="Semester (e.g., Fall 2024, Spring 2025)")
    section = models.CharField(max_length=10, help_text="Section (e.g., A, B, C)")
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.course.course_code} - {self.section} ({self.semester}) - {self.teacher.name}"
    
    class Meta:
        ordering = ['-semester', 'course__course_code']
        unique_together = ['course', 'semester', 'section']


class CourseEnrollment(models.Model):
    """Represents a student's enrollment in a course offering"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course_offering = models.ForeignKey(CourseOffering, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.name} - {self.course_offering.course.course_code}"
    
    def get_attendance_percentage(self):
        """Calculate attendance percentage for this course"""
        total_classes = self.attendance_records.count()
        if total_classes == 0:
            return 0.0
        
        attended_classes = self.attendance_records.filter(is_present=True).count()
        return (attended_classes / total_classes) * 100
    
    class Meta:
        ordering = ['student__roll_number', 'course_offering__course__course_code']
        unique_together = ['student', 'course_offering']


class AttendanceRecord(models.Model):
    """Represents individual attendance records for students"""
    enrollment = models.ForeignKey(CourseEnrollment, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    is_present = models.BooleanField(default=False)
    remarks = models.TextField(blank=True, null=True, help_text="Optional remarks (e.g., late, excused)")
    
    def __str__(self):
        status = "Present" if self.is_present else "Absent"
        return f"{self.enrollment.student.name} - {self.enrollment.course_offering.course.course_code} - {self.date} - {status}"
    
    class Meta:
        ordering = ['-date', 'enrollment__student__roll_number']
        unique_together = ['enrollment', 'date']


class Management(models.Model):
    """Represents management/admin personnel with system authority"""
    roll_number = models.CharField(max_length=50, unique=True, help_text="Management ID/Roll Number")
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=100, help_text="Job title/designation")
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='management_profile')
    can_modify_students = models.BooleanField(default=True)
    can_modify_teachers = models.BooleanField(default=True)
    can_modify_courses = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.roll_number} - {self.name} ({self.designation})"
    
    class Meta:
        verbose_name_plural = "Management"
        ordering = ['roll_number']
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Class(models.Model):
    classroom_id = models.AutoField(primary_key=True)
    scanner_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"Classroom {self.classroom_id}"


class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='student_profile')
    student_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=True, blank=True)
    # image = models.ImageField(upload_to='student_images/', null=True, blank=True)  # for CV
    rfid = models.CharField(max_length=100, unique=True)
    overall_attendance = models.FloatField(default=0.0)  # percentage
    year = models.IntegerField()  # e.g., 1, 2, 3, 4
    dept = models.CharField(max_length=100)  # e.g., CS, IT
    section = models.CharField(max_length=10)  # e.g., A, B, C

    def __str__(self):
        return self.student_name

class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=200)

    def __str__(self):
        return self.course_name

class Teacher(models.Model):
    teacher_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='teacher_profile')
    teacher_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=True, blank=True)
    # image = models.ImageField(upload_to='teacher_images/', null=True, blank=True)
    rfid = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.teacher_name

class Management(models.Model):
    Management_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='management_profile')
    Management_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.Management_name

class TaughtCourse(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='taught_courses')
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, related_name='taught_courses')
    classes_taken = models.CharField(max_length=255)  # e.g., "Class A, Class B"

    def __str__(self):
        return f"{self.teacher} teaches {self.course}"

class StudentCourse(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='student_courses')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='student_courses')
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, related_name='student_courses')
    classes_attended = models.CharField(max_length=255, blank=True)  # e.g., "Class A, Class B"

    def __str__(self):
        return f"{self.student} - {self.course} - {self.teacher}"

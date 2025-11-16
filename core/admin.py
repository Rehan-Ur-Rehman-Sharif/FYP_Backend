from django.contrib import admin
from .models import (
    Department, Course, Student, Teacher, 
    CourseOffering, CourseEnrollment, AttendanceRecord, Management
)

# Register your models here.

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('name', 'code')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'course_name', 'department', 'credit_hours')
    list_filter = ('department',)
    search_fields = ('course_code', 'course_name')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_number', 'name', 'department', 'section')
    list_filter = ('department', 'section')
    search_fields = ('roll_number', 'name')


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('roll_number', 'name', 'user')
    search_fields = ('roll_number', 'name')


@admin.register(CourseOffering)
class CourseOfferingAdmin(admin.ModelAdmin):
    list_display = ('course', 'teacher', 'semester', 'section', 'is_active')
    list_filter = ('semester', 'is_active', 'course__department')
    search_fields = ('course__course_code', 'course__course_name', 'teacher__name')


@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course_offering', 'enrollment_date', 'get_attendance_display')
    list_filter = ('course_offering__semester', 'course_offering__course__department')
    search_fields = ('student__roll_number', 'student__name', 'course_offering__course__course_code')
    
    def get_attendance_display(self, obj):
        return f"{obj.get_attendance_percentage():.2f}%"
    get_attendance_display.short_description = 'Attendance %'


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'date', 'is_present', 'remarks')
    list_filter = ('date', 'is_present', 'enrollment__course_offering__semester')
    search_fields = ('enrollment__student__name', 'enrollment__student__roll_number')
    date_hierarchy = 'date'


@admin.register(Management)
class ManagementAdmin(admin.ModelAdmin):
    list_display = ('roll_number', 'name', 'designation', 'user', 'can_modify_students', 'can_modify_teachers')
    list_filter = ('can_modify_students', 'can_modify_teachers', 'can_modify_courses')
    search_fields = ('roll_number', 'name', 'designation')
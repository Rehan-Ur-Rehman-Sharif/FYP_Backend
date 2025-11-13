from django.contrib import admin
from .models import Class, Student

# Register your models here.
@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('class_id', 'class_name')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'name', 'class_fk')
    list_filter = ('class_fk',)
    search_fields = ('name',)
from django.db import models

# Create your models here.
class Class(models.Model):
    class_id = models.AutoField(primary_key=True)
    class_name = models.CharField(max_length=200)

    def __str__(self):
        return self.class_name

class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    class_fk = models.ForeignKey(Class, on_delete=models.CASCADE, db_column='class_id', related_name='students')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
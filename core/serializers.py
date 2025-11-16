from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Student, Teacher, Management


class StudentRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = Student
        fields = ('email', 'password', 'password2', 'student_name', 'rfid', 'year', 'dept', 'section')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Email already exists."})
        
        return attrs

    def create(self, validated_data):
        # Remove password2 as it's not needed for User creation
        validated_data.pop('password2')
        
        # Create User instance
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        # Create Student instance
        student = Student.objects.create(
            user=user,
            email=validated_data['email'],
            student_name=validated_data['student_name'],
            rfid=validated_data['rfid'],
            year=validated_data['year'],
            dept=validated_data['dept'],
            section=validated_data['section']
        )
        
        return student


class TeacherRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = Teacher
        fields = ('email', 'password', 'password2', 'teacher_name', 'rfid')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Email already exists."})
        
        return attrs

    def create(self, validated_data):
        # Remove password2 as it's not needed for User creation
        validated_data.pop('password2')
        
        # Create User instance
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        # Create Teacher instance
        teacher = Teacher.objects.create(
            user=user,
            email=validated_data['email'],
            teacher_name=validated_data['teacher_name'],
            rfid=validated_data['rfid']
        )
        
        return teacher


class ManagementRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = Management
        fields = ('email', 'password', 'password2', 'Management_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Email already exists."})
        
        return attrs

    def create(self, validated_data):
        # Remove password2 as it's not needed for User creation
        validated_data.pop('password2')
        
        # Create User instance
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        # Create Management instance
        management = Management.objects.create(
            user=user,
            email=validated_data['email'],
            Management_name=validated_data['Management_name']
        )
        
        return management


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

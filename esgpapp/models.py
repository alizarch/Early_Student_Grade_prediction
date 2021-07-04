from django.db import models
from django.conf import settings
from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone


class Users(AbstractBaseUser):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50,unique=True)
    phone_number = models.CharField(max_length=13)
    date_of_birth = models.DateField()
    faculty_or_student = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    status= models.IntegerField(default = 1)
    created_at= models.DateTimeField(default=datetime.now())
    updated_at= models.DateTimeField(default=datetime.now())
    last_login = models.DateTimeField(('last login'), blank=True, null=True)

    USERNAME_FIELD = 'email'
    
    def __str__(self):
        return self.name

class CSV_Content(models.Model):

    student_id = models.CharField(("student_id"), blank=True, null=True , max_length=50 )
    student_name = models.CharField(("student_name"), blank=True, null=True , max_length=50 )
    total_quizes = models.IntegerField()
    given_quizes = models.IntegerField()
    total_marks_of_quizes = models.IntegerField()
    obtain_marks_in_quizes = models.IntegerField()
    total_assignments = models.IntegerField()
    given_assignments = models.IntegerField()
    total_marks_of_assignments = models.IntegerField()
    obtain_marks_in_assignments = models.IntegerField()
    total_classes = models.IntegerField()
    taken_classes = models.IntegerField()
    last_month_grade = models.FloatField()
    predicted_grads = models.FloatField(("predicted_grads"), blank=True, null=True)
    remedial_plan = models.TextField(("remedial_plan"), blank=True, null=True)
    grades = models.CharField(max_length=50, default='')
    status = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=datetime.now())
    updated_at = models.DateTimeField(default=datetime.now())


    def __str__(self):
        return self.student_name


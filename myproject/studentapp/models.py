from django.db import models
from django.db.models.fields import CharField, EmailField
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser



# Create your models here.
class Teacher(models.Model):
    teacher_name = CharField(max_length=200, null=False, blank=False)
    role=CharField(max_length=200, default="teacher")
    subject = CharField(max_length=200,null=False, blank=False)
    email=EmailField(null=False, blank=False)
    password=CharField(max_length=200,null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return "<id={}, teacher_name={}>".format(self.id,self.teacher_name)




class ClassRoom(models.Model):
    class_name = CharField(max_length=200, null=False, unique=True)
    teacher = models.ManyToManyField(Teacher, null=True, blank=True)    
    
    def __str__(self):
        return "<id={}, class_name={}>".format(self.id,self.class_name)




class Student(models.Model):
    student_name = CharField(max_length=200, null=False)
    role=CharField(max_length=200, default="student", null=True, blank=True)
    email=EmailField(null=False, blank=False)
    password = CharField(max_length=200,null=False)
    classroom = models.ManyToManyField(ClassRoom,null=True, blank=True)    
    
    def __str__(self):
        return "<id={}, student_name={}>".format(self.id,self.student_name)

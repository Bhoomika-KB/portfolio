from django.contrib import admin
from .models import Teacher,ClassRoom,Student

# Register your models here.
admin.site.register(Teacher)
admin.site.register(ClassRoom)
admin.site.register(Student)
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=64)
    major = models.CharField(max_length=128)
    course = models.ForeignKey(to='Course',to_field='id')

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=256)
    student_count = models.IntegerField(default=0)
    def __str__(self):
        return self.name

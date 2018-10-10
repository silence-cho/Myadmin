#coding:utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=64, verbose_name='书籍名称')
    price = models.IntegerField(default=0, verbose_name='价格')
    publish = models.ForeignKey(to='Publish', to_field='id',verbose_name='出版社')
    author = models.ManyToManyField(to='Author', verbose_name='作者')

    def __str__(self):
        return self.title

class Author(models.Model):
    name = models.CharField(max_length=64)
    age = models.IntegerField(default=0,null=True)

    def __str__(self):
        return self.name

class Publish(models.Model):
    name = models.CharField(max_length=256)
    address = models.CharField(max_length=256)

    def __str__(self):
        return self.name
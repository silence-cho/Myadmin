# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-09-30 14:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_auto_20180930_2210'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='author',
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-16 08:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StuAdmin1', '0004_auto_20180814_1827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stuinfo',
            name='Stu_Class_1',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='大类班级'),
        ),
        migrations.AlterField(
            model_name='stuinfo',
            name='Stu_Class_2',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='专业班级'),
        ),
    ]

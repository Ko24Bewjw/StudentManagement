# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-14 10:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StuAdmin1', '0003_auto_20180814_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stuinfo',
            name='Stu_Sex',
            field=models.CharField(blank=True, choices=[('男', '男'), ('女', '女')], default='男', max_length=4, null=True, verbose_name='性  别'),
        ),
    ]

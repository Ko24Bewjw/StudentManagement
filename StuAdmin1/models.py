from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth.models import AbstractUser

from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime


class User(models.Model):
    '''用户表'''

    gender = (

        ('male', '男'),

        ('female', '女'),

    )

    name = models.CharField(max_length=128, unique=True)

    password = models.CharField(max_length=256)

    email = models.EmailField(unique=True)

    sex = models.CharField(max_length=32, choices=gender, default='男')

    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['c_time']

        verbose_name = '用户'

        verbose_name_plural = '用户'


class Stuinfo(models.Model):
    #user = models.OneToOneField(User,on_delete=models.CASCADE)
    Stu_ID=models.CharField(u"学号",max_length=12,primary_key=True,help_text=u'学号不能为空')
    Stu_Name = models.CharField(u"姓名",max_length=20)
    Stu_Password=models.CharField(u"密码",max_length=20,help_text=u'密码不能为空',default='123456',blank=True,null=True)
    sex_type = ((u'男',u'男'),(u'女',u'女'))
    Stu_Sex = models.CharField(u"性  别",choices=sex_type,default=u'男',max_length=4,blank=True,null=True)
    Stu_BirthDate= models.DateTimeField(u'出生日期',max_length=64,blank=True,null=True)
    Stu_Class_1= models.CharField(u'大类班级',max_length=20,blank=True, null=True)
    Stu_Class_2=models.CharField(u'专业班级',max_length=20,blank=True, null=True)
    Stu_Address=models.CharField(u'家庭地址',max_length=200,blank=True, null=True)
    Stu_Telephone=models.CharField(u'电话号码',max_length=11,blank=True, null=True)
    Stu_Hostel=models.CharField(u'宿  舍',max_length=100,blank=True, null=True,help_text=u'(9-201)')
    Stu_Image=models.ImageField(upload_to='image/%Y/%m/%d/')


    class META:
        ordering = [' Stu_ID']
        verbose_name =u'学生信息'
        verbose_name_plural = verbose_name



    def __unicode__(self):
        #return self.name

        return self.Stu_Name





class Class(models.Model):
    Class_ID=models.CharField(max_length=12,primary_key=True)
    Class_Name = models.CharField(max_length=20)
    Class_Institute=models.ForeignKey('Institute',on_delete=models.CASCADE,blank=True, null=True)

    class META:
        ordering = ['Class_Name']
        verbose_name =u'班级'

    def __unicode__(self):
        return self.Class_Name

    def __str__(self):
        return self.Class_Name


class Institute(models.Model):
    Institute_ID=models.CharField(max_length=12,primary_key=True)
    Institute_Name = models.CharField(max_length=20)

    class META:
        ordering = ['Institute_Name']
        verbose_name =u'学院'

    def __unicode__(self):
        return self.Institute_Name

    def __str__(self):
        return self.Institute_Name


class Teacher(models.Model):
    Teacher_ID=models.CharField(max_length=12,primary_key=True)                  #工号
    Teacher_Name = models.CharField(max_length=20)                               #姓名
    Teacher_Password=models.CharField(max_length=20,default='123456')             #密码
    Teacher_Telephone=models.CharField(max_length=11,blank=True, null=True)     #电话
    Teacher_Office=models.CharField(max_length=20,blank=True, null=True)        #办公室
    Teacher_Office_tel=models.CharField(max_length=20,blank=True, null=True)    #办公室电话
    Teacher_QQ=models.CharField(max_length=20,blank=True, null=True)            #qq
    Teacher_Email=models.CharField(max_length=20,blank=True, null=True)            #Email
    Teacher_Role=models.CharField(max_length=20,blank=True, null=True)          #院长;团支书;辅导员;教师

    class META:
        ordering = ['Teacher_Name']
        verbose_name =u'教师'

    def __unicode__(self):
        return self.Teacher_Name

    def __str__(self):
        return self.Teacher_Name


#班级管理表

class Admin_Class(models.Model):
    If_Large_class_type = ((u'是',u'是'),(u'否',u'否'))
    Admin_Teacher_ID=models.ForeignKey('Teacher',on_delete=models.CASCADE,blank=False, null=False,verbose_name =u'教师ID')  #教师
    Admin_Class=models.ForeignKey('Class',on_delete=models.CASCADE,blank=False, null=False,verbose_name =u'班级ID')         # 教师管理的班级
    Admin_Start_Time=models.DateTimeField(u'开始时间',max_length=64,blank=True,null=True,help_text="格式yyyy-mm-dd")
    Admin_End_Time=models.DateTimeField(u'结束时间',max_length=64,blank=True,null=True,help_text="格式yyyy-mm-dd")
    If_Large_class=models.CharField(u'是否大类班',choices= If_Large_class_type,max_length=1)         #是否是大类,默认为 0
    Admin_Class_Remarks=models.CharField(u'备注',max_length=500)         #备注


    class META:
        ordering = ['TAdmin_Class']
        verbose_name =u'班级管理'

    def __unicode__(self):
        return self.Admin_Teacher_ID

    def __str__(self):
        return self.Admin_Teacher_ID


from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth.models import AbstractUser

from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    Stu_ID=models.CharField(u"学号",max_length=12,primary_key=True,help_text=u'学号不能为空')
    Stu_Name = models.CharField(u"姓名",max_length=20)
    sex_type = ((u'男',u'男'),(u'女',u'女'))
    Stu_Sex = models.CharField(u"性别",choices=sex_type,default=u'男',max_length=4)


    Stu_BirthDate= models.DateTimeField(u'出生日期',max_length=64,blank=True,null=True,help_text="格式yyyy-mm-dd")
    Stu_Class= models.ForeignKey('Class',on_delete=models.CASCADE,verbose_name =u'班级',blank=True, null=True)

    Stu_Address=models.CharField(u'家庭地址',max_length=200,blank=True, null=True)
    Stu_Telephone=models.CharField(u'电话号码',max_length=11,blank=True, null=True)
    #Stu_Image=models.ImageField(upload_to='image/%Y/%m/%d/')

    class META:
        ordering = [' Stu_ID']
        verbose_name =u'学生信息'
        verbose_name_plural = verbose_name



    def __unicode__(self):
        #return self.name

        return self.Stu_Name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


def update_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    user.profile.bio = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit...'
    user.save()

class Class(models.Model):
    Class_ID=models.CharField(max_length=12,primary_key=True)
    Class_Name = models.CharField(max_length=20)
    Class_Year= models.CharField(max_length=4) #班级所属年级
    Class_Institute=models.ForeignKey('Institute',on_delete=models.CASCADE,blank=True, null=True)
    Class_Instructor=models.ForeignKey('Teacher',on_delete=models.CASCADE,blank=True, null=True)

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
    Teacher_ID=models.CharField(max_length=12,primary_key=True)
    Teacher_Name = models.CharField(max_length=20)

    class META:
        ordering = ['Teacher_Name']
        verbose_name =u'教师'

    def __unicode__(self):
        return self.Teacher_Name

    def __str__(self):
        return self.Teacher_Name





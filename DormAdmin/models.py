from django.db import models

# Create your models here.
#宿舍表
class Dorm(models.Model):
    Dorm_ID=models.CharField(u"宿舍ID",max_length=100,primary_key=True,help_text=u'宿舍号不能为空')
    Building_Num = models.CharField(u'楼号', max_length=100, blank=True, null=True)
    Floor_Num = models.CharField(u'层号', max_length=10, blank=True, null=True)
    Room_Num = models.CharField(u'房间号', max_length=10, blank=True, null=True)
    Dorm_Capacity = models.IntegerField(u'宿舍容量',default=4)
    Actual_Num = models.IntegerField(u'实住人数',default=0)
    sex_type = ((u'男', u'男'), (u'女', u'女'))
    Sex = models.CharField(u"性  别", choices=sex_type, default=u'男', max_length=4, blank=True, null=True)

#当前学生宿舍信息表
class CurrentDormInfo(models.Model):
    Stu_ID = models.ForeignKey('StuAdmin1.Stuinfo', on_delete=models.CASCADE, blank=False, null=False, verbose_name=u'原宿舍ID')
    Building_Num = models.CharField(u'现楼号', max_length=10, blank=True, null=True)
    Floor_Num = models.CharField(u'现层号', max_length=10, blank=True, null=True)
    Room_Num = models.CharField(u'现房间号', max_length=10, blank=True, null=True)
    Bed = models.CharField(u'现床位号', max_length=10, blank=True, null=True)

#宿舍调整表
class DormAdjust(models.Model):
    Adjust_ID = models.IntegerField(u'调整ID', default=1,help_text=u'调整宿舍号不能为空')
    Stu_ID = models.ForeignKey('StuAdmin1.Stuinfo', on_delete=models.CASCADE, blank=False, null=False,verbose_name=u'原宿舍ID')
    Adjust_Time = models.DateTimeField(u'调整时间', max_length=64, blank=True, null=True)
    Original_Dorm_ID = models.CharField(u'原宿舍ID', max_length=100, blank=True, null=True)
    Original_Building_Num = models.CharField(u'原楼号', max_length=10, blank=True, null=True)
    Original_Floor_Num = models.CharField(u'原层号', max_length=10, blank=True, null=True)
    Original_Room_Num = models.CharField(u'原房间号', max_length=10, blank=True, null=True)
    Original_Bed = models.CharField(u'原床位号', max_length=10, blank=True, null=True)
    Extra = models.CharField(u'调整备注说明', max_length=1000, blank=True, null=True)
    # 接下来设置联合主键
    class Meta:
        unique_together = ("Adjust_ID", "Stu_ID")

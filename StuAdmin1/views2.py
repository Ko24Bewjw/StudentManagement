# coding:utf-8
import pdb
import time

from django.http import HttpResponse
from django.shortcuts import render,render_to_response

from StuAdmin1.Form import StuForm,TeacherForm
from StuAdmin1.models import Stuinfo,Class,Teacher,Admin_Class
from django.db import models
from django.shortcuts import render
from django.shortcuts import HttpResponse
# Create your views here.
def index(request):
    return render(request,"index1.html")

def base(request):
    return render(request,"base.html")


def StuAdd(request):
    curtime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    if request.method == "POST":
            Stu_ID1=request.POST.get('Stu_ID','55555')
            Stu_Name1=request.POST.get('Stu_Name','123')
            Stu_Password1=request.POST.get('Stu_Password','888')
            Stu_Sex1=request.POST.get('Stu_Sex','')
            Stu_BirthDate1=request.POST.get('Stu_BirthDate','2018-01-01')
            Stu_Class11=request.POST.get('Stu_Class_1','')
            Stu_Class21=request.POST.get('Stu_Class_2','')
            Stu_Address1=request.POST.get('Stu_Address','')
            Stu_Telephone1=request.POST.get('Stu_Telephone','')
            Stu_Hostel1=request.POST.get('Stu_Hostel','')
            try:
                 Stuinfo.objects.create(Stu_ID= Stu_ID1,Stu_Name=Stu_Name1,Stu_Password=Stu_Password1,Stu_Sex=Stu_Sex1,Stu_BirthDate=Stu_BirthDate1,Stu_Class_1_id=Stu_Class11,\
                                    Stu_Class_2_id=Stu_Class21,  Stu_Telephone=Stu_Telephone1,Stu_Address=Stu_Address1,Stu_Hostel=Stu_Hostel1)
                #user = User(username=username,password=password,email=email)

            #NewStudent.save()
            #pdb.set_trace()
                 state = 'success'
            except:

               state = 'notsuccess'

            content = {
             'user': Stu_Name1,
             'active_menu': 'add_stu',
             'state': state,}


            #return HttpResponse("Add Success",Stu_ID1)
            classadmin=ClassAdmin()
            classlist=classadmin.FindClass()
            return render(request, 'StuAdd2.html',content,{'ClassList':classlist})



    else:
        form = StuForm()
        classadmin=ClassAdmin()
        classlist=classadmin.FindClass()
        return render(request, 'StuAdd2.html', {'form_info': form,'ClassList':classlist})


def StuShow(request):

    return render(request, 'stushow.html')

def StuAdd1(request):
    if request.method == 'POST':
        '''
        form = StuForm(request.POST)
        if form.is_valid():
            exam_info = form.save()
            exam_info.save()
            return HttpResponse('Thank you')
        '''
    else:
        form = StuForm()
        classadmin=ClassAdmin()
        classlist=classadmin.FindClass()

    return render(request, 'StuAdd2.html', {'form_info': form,'ClassList':classlist})



def test(request):
     classadmin=ClassAdmin()
     classlist=classadmin.FindClass()
     return render(request, 'test3.html',{'ClassList':classlist})


def studata(request):
     user_list = Stuinfo.objects.all()
     import json
     #return HttpResponse(json.dumps(user_list))
     return HttpResponse(json.dumps(list(user_list)), content_type='application/json')


class  StuAdmin():

    def StuFindAll(self,classid="all"):
         if classid=="all":
            stuallist=models.Stuinfo.objects.all().order_by("Stu_ID")  #检索所有学生
         else:
           stuallist=models.Stuinfo.objects.get(Stu_Class_2='classid')
         return stuallist

    def StuFindById(self,stu_id):
         stuone=models.Stuinfo.objects.get(Stu_ID=stu_id)
         return stuone

    def GetpostData(request):
            postdatastup={}   #提交数据
            postdatastup['Stu_ID']=request.POST.get('Stu_ID1','55555')
            postdatastup['Stu_Name']=request.POST.get('Stu_Name1','123')
            postdatastup['Stu_Password']=request.POST.get('Stu_Password','888')
            postdatastup['Stu_Sex']=request.POST.get('Stu_Sex','')
            postdatastup['Stu_BirthDate']=request.POST.get('Stu_BirthDate','2018-01-01')
            postdatastup['Stu_Class1']=request.POST.get('Stu_Class_1','')
            postdatastup['Stu_Class2']=request.POST.get('Stu_Class_2','')
            postdatastup['Stu_Address']=request.POST.get('Stu_Address','')
            postdatastup['Stu_Telephone']=request.POST.get('Stu_Telephone','')
            postdatastup['Stu_Hostel']=request.POST.get('Stu_Hostel','')
            return postdatastup


    def UpdataStu(self,stu_id,postdata):   # postdate 为接收到的更新信息（字典存放）
        currentstu=Stuinfo.objects.get(Stu_Id=stu_id)
        currentstu.Stu_ID=postdata['Stu_ID']
        currentstu.Stu_Password=postdata['Stu_Name']
        currentstu.Stu_Name= postdata['Stu_Name']
        currentstu.Stu_Password= postdata['Stu_Password']
        currentstu.Stu_Sex= postdata['Stu_Sex']
        currentstu.Stu_Class1=postdata['Stu_Class1']
        currentstu.Stu_Class2=postdata['Stu_Class2']
        currentstu.Stu_Address= postdata['Stu_Address']
        currentstu.Stu_Telephone=postdata['Stu_Telephone']
        currentstu.Stu_Hostel=postdata['Stu_Hostel']
        currentstu.save()




class ClassAdmin():

  def FindClass(self):

      classlist= Class.objects.all().order_by("Class_ID").reverse() #班级名称
      return classlist

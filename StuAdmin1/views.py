# coding:utf-8
import pdb
import time
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render,render_to_response
from django.shortcuts import render, redirect

from . import models

from .forms import UserForm

from .forms import RegisterForm
from StuAdmin1.Form import StuForm
from StuAdmin1.models import Stuinfo, Class,Teacher,Admin_Class,Institute,User
from django.db import models
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.core import serializers
import json
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

from django.utils.encoding import force_text
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
import os



upload_file_name=""
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))

# 放置上传的图片
UPLOADFILES = os.path.join(PROJECT_DIR, 'upfile')
# Create your views here.
def index(request):
    return render(request, "nenglong.html")

def base(request):
    return render(request, "base.html")



'''def DormAssign(request):
    classadmin=ClassAdmin()
    classlist=classadmin.FindClass()
    return render(request, "student/DormAssign.html", {'ClassList': classlist})
def Dormadjust(request):
    return render(request, "student/DormAdjust.html")'''

def tabletest(request):
    classadmin=ClassAdmin()
    classlist=classadmin.FindClass()
    #data = Stuinfo.objects.all()
    search_class='全部'
    search_name=""
    search_id=""
    if request.method == "POST":
          search_class=request.POST.get('Stu_Class_2',"全部")
          search_name=request.POST.get('txt_search_name',"")
          search_id=request.POST.get('txt_search_stuid',"")

    stuobj=StuAdmin(search_class,search_name,search_id)

    stu_obj=stuobj.StuFindAll(request)

    return render(request, 'tabletest.html', {'ClassList':classlist,'stulist':stu_obj})

def StuManage(request):

    classadmin=ClassAdmin()
    classlist=classadmin.FindClass()
    return render(request, "student/stuadmin.html", {'ClassList':classlist})

def getstudata(request):  #得到学生的信息
    data_set = []
    targets = Stuinfo.objects.all()
    offset = request.GET.get('offset')
    limit = request.GET.get('limit')
    sort = request.GET.get('sort')
    order = request.GET.get('order')
    search_class=request.GET.get('search_class',"全部")
    search_name=request.GET.get('search_name',"")
    search_stuid=request.GET.get('search_stuid',"")
    search=request.GET.get('search',"")  #自带搜素框

    if  search_name!="":
        StuQuerySet= targets = Stuinfo.objects.all().filter(Stu_Name=search_name)
    elif search_stuid!="":
        StuQuerySet= targets = Stuinfo.objects.all().filter(Stu_ID=search_stuid)
    elif search_class!="全部":
       StuQuerySet= targets = Stuinfo.objects.all().filter( Stu_Class_2=search_class)
    else:
       StuQuerySet= targets = Stuinfo.objects.all()
    if search!="":
        StuQuerySet=Stuinfo.objects.filter(Q(Stu_Name__contains=search) | Q(Stu_ID__contains=search))



    length = len(StuQuerySet)
    targets =StuQuerySet
    if not offset or not limit:
        targets =StuQuerySet
        if sort:
            sort = sort if order == 'asc' else '-'+sort
            targets = StuQuerySet.order_by(sort)
    else:
        offset = int(offset)
        limit = int(limit)
        if sort:
            sort = sort if order == 'asc' else '-' + sort
            targets = StuQuerySet.order_by(sort)[offset:offset+limit]
        else:
            targets =StuQuerySet[offset:offset+limit]
    for stuone in targets:
        #str={"Stu_ID":stuone.Stu_ID,"Stu_Name":stuone.Stu_Name}

        '''
        hrefstr='<a class="btn btn-success" id="btndetail" href="/studetail/?stuid='+str(stuone.Stu_ID)+  '"><i class="icon-zoom-in"></i></a>'
        hrefstr+='<a class="btn btn-info" id="btnedit" href="/stuedit/?stuid='+stuone.Stu_ID+  '"><i class="icon-edit "></i></a>'
        hrefstr+='<a class="btn btn-danger" id="btndel" href="/studel?stuid='+stuone.Stu_ID+  '"><i class="icon-trash"></i></a>'
        data_set.append({"Stu_ID":stuone.Stu_ID,"Stu_Name":stuone.Stu_Name,"Stu_Sex":stuone.Stu_Sex,"Stu_Class2":str(stuone.Stu_Class_2),"action":hrefstr})

        hrefstr='<a class="btn btn-success" id="btndetail" href="#" onclick="modal_show(this)"><i class="icon-zoom-in"></i></a>'
        hrefstr+='<a class="btn btn-info" id="btnedit" href="#" onclick="modal_edit(this)"><i class="icon-edit "></i></a>'
        hrefstr+='<a class="btn btn-danger" id="btndel" href="#" onclick="modal_del(this)"><i class="icon-trash"></i></a>'
        '''
        calss1=stuone.Stu_Class_1
        if calss1==None:
          calss1=""
        calss2=stuone.Stu_Class_2
        if calss2==None:
          calss2=""
        data_set.append({"Stu_ID":stuone.Stu_ID,"Stu_Name":stuone.Stu_Name,"Stu_Sex":stuone.Stu_Sex,"Stu_Class_1":str(calss1),"Stu_Telephone":str(stuone.Stu_Telephone),"Stu_Class_2":str(calss2),"Stu_Hostel":stuone.Stu_Hostel})

    return HttpResponse(json.dumps({'total':length,'rows':data_set}),content_type='application/json')





def StuAdd(request):
    curtime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

    if request.method == "POST":
            Stu_ID1=request.POST.get('Stu_ID','55555')
            Stu_Name1=request.POST.get('Stu_Name','123')
            Stu_Password1=request.POST.get('Stu_Password','123456')
            if Stu_Password1=="":
                Stu_Password1="123456"
            Stu_Sex1=request.POST.get('Stu_Sex','')
            Stu_BirthDate1=request.POST.get('Stu_BirthDate','2018-01-01')
            Stu_Class11=request.POST.get('Stu_Class_1','')
            Stu_Class21=request.POST.get('Stu_Class_2','')
            Stu_Address1=request.POST.get('Stu_Address','')
            Stu_Telephone1=request.POST.get('Stu_Telephone','')
            Stu_Hostel1=request.POST.get('Stu_Hostel','')
            try:
                 Stuinfo.objects.create(Stu_ID= Stu_ID1,Stu_Name=Stu_Name1,Stu_Password=Stu_Password1,Stu_Sex=Stu_Sex1,Stu_BirthDate=Stu_BirthDate1,Stu_Class_1=Stu_Class11,\
                                    Stu_Class_2=Stu_Class21,  Stu_Telephone=Stu_Telephone1,Stu_Address=Stu_Address1,Stu_Hostel=Stu_Hostel1)
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

            #return HttpResponse("Add Success")
            return render(request, 'student/StuEdit.html', content)

    else:
        form = StuForm()
        classadmin=ClassAdmin()
        classlist=classadmin.FindClass()

        return render(request, 'StuAdd2.html', {'form_info': form,'ClassList':classlist})



def StudentEdit(request):
     Stu_ID2='123456'
     stuone=Stuinfo.objects.get(Stu_ID= Stu_ID2)
     classadmin=ClassAdmin()
     classlist=classadmin.FindClass()
     return render(request, 'student/StuEdit.html',{'stuone':stuone,'ClassList':classlist})


def StuEditdata(request):
             curtime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
             Stu_ID1="123456"
             try:

               stuoneone=Stuinfo.objects.get(Stu_ID=Stu_ID1)
               stuoneone.Stu_Name=request.POST.get('Stu_Name','')
               stuoneone.Stu_Password=request.POST.get('Stu_Password','123456')
               stuoneone.Stu_Sex=request.POST.get('Stu_Sex','')
               stuoneone.Stu_BirthDate=request.POST.get('Stu_BirthDate','')
               stuoneone.Stu_Class_1=request.POST.get('Stu_Class_1','')
               stuoneone.Stu_Class_2=request.POST.get('Stu_Class_2','')
               stuoneone.Stu_Address=request.POST.get('Stu_Address','')
               stuoneone.Stu_Telephone=request.POST.get('Stu_Telephone','')
               stuoneone.Stu_Hostel=request.POST.get('Stu_Hostel','')
               stuoneone.save()

               state = 'success'
             except:

               state = 'notsuccess'

             data1={
                     'data': state}

            #return HttpResponse("Add Success")
             return HttpResponse(json.dumps(data1))



def StuAddajax(request):

            Stu_ID1=request.POST.get('Stu_ID','55555')
            Stu_Name1=request.POST.get('Stu_Name','123')
            Stu_Password1=request.POST.get('Stu_Password','123456')
            if Stu_Password1=="" :
               Stu_Password1="123456"
            Stu_Sex1=request.POST.get('Stu_Sex','')
            Stu_BirthDate1=request.POST.get('Stu_BirthDate','2018-01-01')
            Stu_Class11=request.POST.get('Stu_Class_1','')
            Stu_Class21=request.POST.get('Stu_Class_2','')
            Stu_Address1=request.POST.get('Stu_Address','')
            Stu_Telephone1=request.POST.get('Stu_Telephone','')
            Stu_Hostel1=request.POST.get('Stu_Hostel','')
            try:
                 Stuinfo.objects.create(Stu_ID= Stu_ID1,Stu_Name=Stu_Name1,Stu_Password=Stu_Password1,Stu_Sex=Stu_Sex1,Stu_BirthDate=Stu_BirthDate1,Stu_Class_1=Stu_Class11,\
                                    Stu_Class_2=Stu_Class21,  Stu_Telephone=Stu_Telephone1,Stu_Address=Stu_Address1,Stu_Hostel=Stu_Hostel1)
                #user = User(username=username,password=password,email=email)

            #NewStudent.save()
            #pdb.set_trace()
                 state = 'success'
            except:

              state = 'notsuccess'

            data1 ={
             'data': state}

            #return HttpResponse("Add Success")
            return HttpResponse(json.dumps(data1))


def StuEdit(request):
       Stu_ID=request.GET.get('stuid','')
       return render(request, 'stuedit.html',{"stuid":Stu_ID})



# 显示学生详细信息

def Stu_Detail(request):
        stuid=request.GET.get('stu_id',"123456")
        stuone=Stuinfo.objects.get(Stu_ID=stuid)
        stu_BirthDate=stuone.Stu_BirthDate.strftime('%Y-%m-%d')
        data={"Stu_ID":stuone.Stu_ID,"Stu_Name":stuone.Stu_Name,"Stu_Sex":stuone.Stu_Sex, "Stu_BirthDate":stu_BirthDate,"Stu_Class_1":str(stuone.Stu_Class_1),"Stu_Class2":str(stuone.Stu_Class_2),"Stu_Address":stuone.Stu_Address,\
             "Stu_Telephone":stuone.Stu_Telephone,"Stu_Hostel":stuone.Stu_Hostel}

        #ensure_ascii=False 解决汉字显示问题
        return HttpResponse(json.dumps(data,ensure_ascii=False), content_type="application/json; charset=utf-8")

def Stu_Del(request):
        stuid=request.GET.get('stu_id',"123456")

        stuone=Stuinfo.objects.get(Stu_ID=stuid)
        stuone.delete()
        data1 ={'data': 'success'}

        #ensure_ascii=False 解决汉字显示问题
        return HttpResponse(json.dumps(data1,ensure_ascii=False), content_type="application/json; charset=utf-8")




def UpLoadStuFile(request):
    if request.method == "POST":
        file_obj = request.FILES.getlist('input-file')

        '''
        _n = "%d" % (time.time() * 1000)
        _f = time.strftime("%Y%m%d", time.localtime())
        '''
        for file in file_obj :
            upload_file_name ="stuinfo_import.xlsx"

            path_file = os.path.join( UPLOADFILES, upload_file_name)
            f = open(path_file , 'wb')
            for chunk in file.chunks():
                f.write(chunk)
            f.close()

        data1 ={
             "success": True,
            "fileName":upload_file_name}

            #return HttpResponse("Add Success")
        return HttpResponse(json.dumps(data1))


def down_template(request):
     return render(request, "学生模板.xlsx")



def import_excel(file_excel= os.path.join( UPLOADFILES, "stuinfo_import.xlsx"),col_name_index=0, by_name=u'Sheet1'):


    import  xlrd
    import uuid
    import datetime
    """
        根据名称获取Excel表格中的数据
        参数: file_excel：Excel文件路径
             col_name_index：表头列名所在行的所以
             by_name：Sheet1名称
    """
    filepath= os.path.join( UPLOADFILES, "stuinfo_import.xlsx")
    data = xlrd.open_workbook(filepath)
    table = data.sheet_by_name(by_name)
    n_rows = table.nrows      # 行数
    ncole = table.ncols       #列数
    errorrowcount=0
    for row_num in range(1, n_rows):
        row = table.row_values(row_num)
        rowValues = table.row_values(row_num)  #一行的数据
        stu_id1=str(int(rowValues[0]))
        stutemp =Stuinfo.objects.filter(Stu_ID =stu_id1)
        status="success"
        stu_Name=rowValues[1]
        stu_Password='123456'
        stu_Sex=str(rowValues[2])
        stu_BirthDate=str(rowValues[3])

        if stu_BirthDate=="":
            stu_BirthDate=None
        stu_Class_1=str(rowValues[4])

        stu_Class_2=str(rowValues[5])

        stu_Address=str(rowValues[6])
        stu_Telephone=str(int(rowValues[7]))
        stu_Hostel=str(rowValues[8])

        if not stutemp.exists():   #空值
            try:
                 Stuinfo.objects.create(Stu_ID=stu_id1,Stu_Name=stu_Name,Stu_Password='123456',Stu_Sex=stu_Sex,Stu_BirthDate=stu_BirthDate,Stu_Telephone=stu_Telephone,Stu_Hostel= stu_Hostel,Stu_Class_1=stu_Class_1,Stu_Class_2=stu_Class_2)
            except:
                errorrowcount+=1
                status="error"
                continue
        else:
            try:
                stutemp.Stu_Name=stu_Name
                stutemp.Stu_Sex=stu_Sex
                stutemp.Stu_BirthDate=stu_BirthDate
                stutemp.Stu_Class_1=stu_Class_1
                stutemp.Stu_Class_2=stu_Class_2
                stutemp.Stu_Telephone=stu_Telephone
                stutemp.Stu_Address=stu_Address
                stutemp.Stu_Hostel= stu_Hostel
                stutemp.save()
            except:
                errorrowcount+=1
                status="error"
                continue
    data1={"status":status,"errorcount":str(errorrowcount)}
    return HttpResponse(json.dumps(data1))


class StuAdmin():

    def __init__(self,search_class='',search_name='',search_id=''):
     self.search_class=search_class
     self.search_name=search_name
     self.search_id=search_id


    def StuFindAll(self,request):

        self.stuall=Stuinfo.objects.all()

        if self.search_class!="全部" :

             self.stuall1 = self.stuall.filter(Stu_Class_2=self.search_class)
        else:
            self.stuall1 = self.stuall

        if (self.search_name!=""):
            self.stuall1=self.stuall.filter(Stu_Name=self.search_name)
        if (self.search_id!=""):

            self.stuall1=self.stuall.filter(Stu_ID=self.search_id)



        paginator=Paginator(self.stuall1,2)        #每页显示2
        page=request.GET.get('page')        #前段请求的页,比如点击'下一页',该页以变量'page'表示
        try:
              self.stu_obj=paginator.page(page)      #获取前端请求的页数
        except PageNotAnInteger:
               self.stu_obj=paginator.page(1)        #如果前端输入的不是数字,就返回第一页
        except EmptyPage:
                self.stu_obj=paginator.page(paginator.num_pages)   #如果前端请求的页码超出范围,则显示最后一页.获取总页数,返回最后一页.比如共10页,则返回第10页.

        return self.stu_obj
            #return render(request,'tabletest.html',{'stulist':stu_obj})

class ClassAdmin():

  def FindClass(self):

      classlist=Class.objects.all().order_by("Class_ID").reverse() #班级名称
      return classlist

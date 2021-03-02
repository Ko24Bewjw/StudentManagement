from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect

from . import models

# coding:utf-8
import pdb
import time
import random
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render,render_to_response

from StuAdmin1.Form import StuForm
from StuAdmin1.models import Stuinfo, Class,Teacher,Admin_Class,Institute
from DormAdmin.models import Dorm,DormAdjust,CurrentDormInfo
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
def dormassign(request):
    pass

    return render(request, 'student/DormAssign.html')
def dormadjust(request):
    pass

    return render(request, 'student/DormAdjust.html')

def dormupdate(request):
    pass

    return render(request, 'student/DormUpdate.html')
def distribute_dorm(self):
    #男生，女生人数（学院，专业，班级）
    College_Boy_num=Stuinfo.objects.filter(Stu_Sex='男').count()
    College_Girl_num=Stuinfo.objects.filter(Stu_Sex='女').count()
    Major_Boy_num = Stuinfo.objects.filter(Stu_Sex='男').count()
    Major_Girl_num = Stuinfo.objects.filter(Stu_Sex='女').count()
    Classes_Boy_num = Stuinfo.objects.filter(Stu_Sex='男').count()
    Classes_Girl_num = Stuinfo.objects.filter(Stu_Sex='女').count()

    #可分配宿舍：宿舍楼   楼层   空宿舍  半空宿舍（容量-实住人数）
    #信息条数
    All_num = Dorm.objects.count()
    Boy_Building_array,Girl_Building_array = [],[]
    Boy_Floor_array,Girl_Floor_array = [],[]
    #男生，女生可分配宿舍
    Boy_Room_array,Girl_Room_array = [],[]
    # 男生，女生可分配全空，半空宿舍
    Boy_Room_All_Empty_array, Boy_Room_Half_Empty_array = [], []
    Girl_Room_All_Empty_array, Girl_Room_Half_Empty_array = [], []
    # 男生，女生全空、半空的宿舍数
    All_Empty_Boy_DormNum = 0
    Half_Empty_Boy_DormNum = 0
    All_Empty_Girl_DormNum = 0
    Half_Empty_Girl_DormNum = 0
    # 全空、半空的宿舍容纳的男生，女生数
    All_Empty_Boy_Num = 0
    Half_Empty_Boy_Num = 0
    All_Empty_Girl_Num = 0
    Half_Empty_Girl_Num = 0

    #初始化
    # Dorm_data = Dorm.objects.all()[0].Dorm_ID
    # Boy_Building_array.append(Dorm_data.split('-')[0])
    # Boy_Room_array.append(Dorm_data.split('-')[1:][0])
    # Boy_Floor_array.append(Boy_Room_array[0][0])
    for num in range(0, All_num):
        Dorm_data = Dorm.objects.all()[num].Dorm_ID

        #把Dorm_ID中楼号，宿舍号，层数都读取出来
        Building1=Dorm_data.split('-')[0]
        Room1 = Dorm_data.split('-')[1:][0]
        Floor1=Room1[0][0]

        #把Dorm_ID拆开，把Building_Num,Floor_Num,Room_Num存到数据库中
        stutemp = Dorm.objects.filter(Dorm_ID=Dorm_data)
        if stutemp.exists():  # 如果宿舍ID存在，更新Building_Num,Floor_Num,Room_Num
            try:
                Dorm.objects.filter(Dorm_ID=Dorm_data).update(Building_Num=Building1,Room_Num=Room1,Floor_Num=Floor1)
            except:
                continue
        else:
            try:
                stutemp.Building_Num = Building1
                stutemp.Room_Num = Room1
                stutemp.Floor_Num = Floor1
                stutemp.save()
            except:
                continue

        #统计有空床位的宿色
        #该宿舍的性别
        Buliding_Sex = Dorm.objects.all()[num].Sex
        #有空床位的宿舍
        Bed_Num=Dorm.objects.all()[num].Dorm_Capacity-Dorm.objects.all()[num].Actual_Num

        if Bed_Num>0:
            if Buliding_Sex=='男' and Dorm.objects.all()[num].Actual_Num>0:
                Boy_Room_array.append(Dorm_data)
                Boy_Room_Half_Empty_array.append(Dorm_data)
                Half_Empty_Boy_Num=Half_Empty_Boy_Num+Bed_Num
                Half_Empty_Boy_DormNum = Half_Empty_Boy_DormNum+1
            elif Buliding_Sex=='男' and Dorm.objects.all()[num].Actual_Num==0:
                Boy_Room_array.append(Dorm_data)
                Boy_Room_All_Empty_array.append(Dorm_data)
                All_Empty_Boy_Num =All_Empty_Boy_Num+Bed_Num
                All_Empty_Boy_DormNum = All_Empty_Boy_DormNum+1
            elif Buliding_Sex == '女' and Dorm.objects.all()[num].Actual_Num > 0:
                Girl_Room_array.append(Dorm_data)
                Girl_Room_Half_Empty_array.append(Dorm_data)
                Half_Empty_Girl_Num=Half_Empty_Girl_Num+Bed_Num
                Half_Empty_Girl_DormNum = Half_Empty_Girl_DormNum+1
            elif Buliding_Sex=='女' and Dorm.objects.all()[num].Actual_Num==0:
                Girl_Room_array.append(Dorm_data)
                Girl_Room_All_Empty_array.append(Dorm_data)
                All_Empty_Girl_Num=All_Empty_Girl_Num+Bed_Num
                All_Empty_Girl_DormNum = All_Empty_Girl_DormNum+1

        # if Building1 not in Boy_Building_array and Buliding_Sex=='男':
        #     Boy_Building_array.append(Building1)
        # elif Building1 not in Girl_Building_array and Buliding_Sex=='女':
        #     Girl_Building_array.append(Building1)
        # if Floor1 not in Boy_Floor_array and Buliding_Sex=='男':
        #     Boy_Floor_array.append(Floor1)
        #     Boy_Room_array.append(Room1)
        # elif Floor1 not in Girl_Floor_array and Buliding_Sex=='女':
        #     Girl_Floor_array.append(Floor1)
        #     Girl_Room_array.append(Room1)


        # if Building1 not in Boy_Building_array and Buliding_Sex=='男':
        #     Boy_Building_array.append(Building1)
        # elif Building1 not in Boy_Building_array and Buliding_Sex=='女':
        #     Girl_Building_array.append(Building1)
        # if Floor1 not in Floor_array and Building1 not in Building_array:
        #     Floor_array.append(Floor1)
        # if Room1 not in Boy_Room_array and Building1 not in Boy_Building_array:
        #     Boy_Room_array.append(Room1)

    # Boy_Room_array = Boy_Room_All_Empty_array
    # Boy_Room_array.extend(Boy_Room_Half_Empty_array)
    # Girl_Room_array = Girl_Room_All_Empty_array
    # Girl_Room_array.extend(Girl_Room_Half_Empty_array)
    if College_Boy_num<=All_Empty_Boy_Num+Half_Empty_Boy_Num and College_Girl_num<=All_Empty_Girl_Num+Half_Empty_Girl_Num:
        Stu_num = Stuinfo.objects.count()
        print(Stu_num)
        #存放每个班级的男生，女生数（列表内存放字典，包含三个键：班级，男生，女生人数）
        classes=[]
        #存放各个班男生，女生的详细学生信息，用于后边选取各种算法分配宿舍(eg:按学号随机分配)
        Boy_Info=[]
        Girl_Info=[]
        Classes_Num=0   #Classes_Num+1是分宿舍时班级的个数，Classes_Num是Boy_Info，Girl_Info的数组第i项
        #Flag作为标志，判断该班级是否在classes这个列表中
        Flag=False
        # Flag作为标志，分别判断该班级是否在Boy_Info,Girl_Info这个列表中
        Flag_Boy = False
        Flag_Girl = False
        # classes.append({'班级': '信1601-3', '男生人数': 0, '女生人数': 0})
        classes.append({'班级': Stuinfo.objects.all()[0].Stu_Class_1, '男生人数': 0, '女生人数': 0})
        #分宿舍同一班级学生尽量在一起，得到每一个班级的男生人数，女生人数,得到每一个班级的男生信息，女生信息
        for num in range(0, Stu_num):
            Stu_data = Stuinfo.objects.all()[num]
            banji=Stu_data.Stu_Class_1
            sex=Stu_data.Stu_Sex
            Man_num=0
            Girl_num=0
            for item in classes:
                # print(classes)
                if banji == item['班级']:
                    #找到该班级在列表中的索引（即第几项匹配）
                    # dict2=item
                    # Classes_Num=classes.index(item)
                    # print(Classes_Num)
                    Flag=True
                    break
            if(Flag):
                if sex == '男':
                    item['男生人数'] = item['男生人数'] + 1
                    # print(Boy_Info)
                    # Boy_Info.append([])
                    # print(Boy_Info)
                    # Boy_Info[Classes_Num].append(Stuinfo.objects.all()[num])
                    # print(Boy_Info)
                elif sex == '女':
                    item['女生人数'] = item['女生人数'] + 1
                    # if Girl_Info[Classes_Num]:
                    #     Girl_Info.append([])
                    # Girl_Info[Classes_Num].append(Stuinfo.objects.all()[num])
                    # print(Girl_Info)
                Flag=False
            else:
                if sex == '男':
                    classes.append({'班级': banji, '男生人数': 1, '女生人数': 0})
                    # for item in classes:
                    #     if banji == item['班级']:
                    #         # 找到该班级在列表中的索引（即第几项匹配）
                    #         # dict2=item
                    #         Classes_Num = classes.index(item)
                    #         Boy_Info.append([])
                    #         Boy_Info[Classes_Num].append(Stuinfo.objects.all()[num])
                elif sex == '女':
                    classes.append({'班级': banji, '男生人数': 0, '女生人数': 1})
                    # for item in classes:
                    #     if banji == item['班级']:
                    #         # 找到该班级在列表中的索引（即第几项匹配）
                    #         # dict2=item
                    #         Classes_Num = classes.index(item)
                    #         Girl_Info.append([])
                    #         Girl_Info[Classes_Num].append(Stuinfo.objects.all()[num])

        #得到每个班级男生信息
        i = len(classes)
        j = 0

        while j < i:
            Boy_Info.append([])
            Girl_Info.append([])
            Boy_Info[j].append(list(Stuinfo.objects.filter(Stu_Class_1=(classes[j]['班级']),Stu_Sex='男').values('Stu_ID')))
            Girl_Info[j].append(list(Stuinfo.objects.filter(Stu_Class_1=(classes[j]['班级']), Stu_Sex='女').values('Stu_ID')))
            # Boy_Info_List=list(Boy_Info)
            j = j + 1
        # 按学号随机给学生分配宿舍（步骤（1），（2），（3））
        Boy_ID_random=[]      #男生学号随机列表
        Girl_ID_random = []   #女生学号随机列表
        i = len(classes)
        j = 0
        #（1）得到每个班男生，女生的学号
        while j < i:
            k1 = len(Boy_Info[j][0])
            k2 = len(Girl_Info[j][0])
            m=0
            Boy_ID_random.append([])
            Girl_ID_random.append([])
            while m<k1:
                Boy_ID_random[j].append(Boy_Info[j][0][m]['Stu_ID'])
                m=m+1
            m=0
            while m<k2:
                Girl_ID_random[j].append(Girl_Info[j][0][m]['Stu_ID'])
                m = m + 1
            j=j+1
        print(Boy_ID_random)
        print(Girl_ID_random)
        #（2）把每个班男生，女生学号随机排列
        i = len(classes)
        j = 0
        while j < i:
            # index = [i for i in range(len(Boy_ID_random[j]))]
            random.shuffle(Boy_ID_random[j])
            random.shuffle(Girl_ID_random[j])
            j=j+1
        print(Boy_ID_random)
        print(Girl_ID_random)

        # （3）正式分配算法
        i = len(classes)
        j = 0
        Boy_Num=0
        Girl_Num=0
        while j < i:
            Boy_Num=Boy_Num+len(Boy_Info[j])
            Girl_Num=Girl_Num+len(Girl_Info[j])
            j=j+1
        j = 0
        while j < i:
            k1=len(Boy_ID_random[j])
            k2 = len(Girl_ID_random[j])
            m=0
            n=0
            #给男生分配
            while m < k1:
                stutemp = Stuinfo.objects.filter(Stu_ID=Boy_ID_random[j][m])
                dormtemp=Dorm.objects.filter(Dorm_ID=Boy_Room_array[n])
                Actual_Num2=list(dormtemp.values('Actual_Num'))[0]['Actual_Num']
                Dorm_Capacity2=list(dormtemp.values('Dorm_Capacity'))[0]['Dorm_Capacity']
                if Actual_Num2==Dorm_Capacity2:
                    n=n+1
                    dormtemp = Dorm.objects.filter(Dorm_ID=Boy_Room_array[n])
                    Actual_Num2 = list(dormtemp.values('Actual_Num'))[0]['Actual_Num']
                print(Actual_Num2)
                print(Dorm_Capacity2)
                if stutemp.exists():  # 如果宿舍ID存在，更新Building_Num,Floor_Num,Room_Num
                    try:
                        if stutemp.filter(Stu_Sex='男'):
                            stutemp.update(Stu_Hostel=Boy_Room_array[n])
                            Actual_Num2=Actual_Num2+1
                            dormtemp.update(Actual_Num=Actual_Num2)
                        m = m + 1
                    except:
                        continue
                else:
                    try:
                        print("错误")
                    except:
                        continue
            j = j + 1

        # 给女生分配
        j = 0
        while j < i:
            k2 = len(Girl_ID_random[j])
            # 给女生分配
            m2 = 0
            n2 = 0
            while m2 < k2:
                stutemp2 = Stuinfo.objects.filter(Stu_ID=Girl_ID_random[j][m2])
                dormtemp2 = Dorm.objects.filter(Dorm_ID=Girl_Room_array[n2])
                Actual_Num2 = list(dormtemp2.values('Actual_Num'))[0]['Actual_Num']
                Dorm_Capacity2 = list(dormtemp2.values('Dorm_Capacity'))[0]['Dorm_Capacity']
                if Actual_Num2 == Dorm_Capacity2:
                    n2 = n2 + 1
                    dormtemp2 = Dorm.objects.filter(Dorm_ID=Girl_Room_array[n2])
                    Actual_Num2 = list(dormtemp2.values('Actual_Num'))[0]['Actual_Num']
                print(Actual_Num2)
                print(Dorm_Capacity2)
                if stutemp2.exists():  # 如果宿舍ID存在，更新Building_Num,Floor_Num,Room_Num
                    try:
                        if stutemp2.filter(Stu_Sex='女'):
                            stutemp2.update(Stu_Hostel=Girl_Room_array[n2])
                            Actual_Num2 = Actual_Num2 + 1
                            dormtemp2.update(Actual_Num=Actual_Num2)
                        m2 = m2 + 1
                    except:
                        continue
                else:
                    try:
                        print("错误")
                    except:
                        continue
            j=j+1
        # Boy_Room_All_Empty_array, Boy_Room_Half_Empty_array = [], []
        # Girl_Room_All_Empty_array, Girl_Room_Half_Empty_array = [], []
        print(Boy_Info)
        print(Girl_Info)
        # print(Boy_Info[0][0][0]['Stu_ID'])
        # print(Girl_Info[0])
        # index = [i for i in range(len(Boy_Info[0]))]
        # random.shuffle(index)
        #
        # print(Boy_Info)
        #按学号随机给学生分配宿舍
        i=0
        print("可以分配")
        # i=len(classes)
        print(i)
        j=0
        while j<i:
            print(classes[j])
            j=j+1
    else:
        print("不可以分配！")
    # print(Boy_Building_array)
    # print(Girl_Building_array)
    # print(Boy_Floor_array)
    # print(Girl_Floor_array)
    print('各班男女生人数')
    print(Boy_Room_array)
    print(Girl_Room_array)
    print(Boy_Room_All_Empty_array)
    print(Boy_Room_Half_Empty_array)
    print(Girl_Room_All_Empty_array)
    print(Girl_Room_Half_Empty_array)
    print('各班男女生详细信息')

    print('宿舍空床位数')
    print(All_Empty_Boy_Num)
    print(Half_Empty_Boy_Num)
    print(All_Empty_Girl_Num)
    print(Half_Empty_Girl_Num)
    print('空/半空宿舍数')
    print(All_Empty_Boy_DormNum)
    print(Half_Empty_Boy_DormNum)
    print(All_Empty_Girl_DormNum)
    print(Half_Empty_Girl_DormNum)
    print(College_Boy_num)
    print(College_Girl_num)


    data1 = {'data': 'success'}
    return HttpResponse(json.dumps(data1))



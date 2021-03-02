"""StudentMangement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.conf.urls import url

from StuAdmin1 import views
from django.urls import path, include
from django.conf.urls import url, include   #导入了include函数

from DormAdmin import views2

urlpatterns = [

    url('admin/', admin.site.urls),
    url(r'^base/', views.base, name="base"),
    url(r'^StudentEdit/', views.StudentEdit, name="StudentEdit"),
    url(r'^StuEditdata/', views.StuEditdata, name="StuEditdata"),
    url(r'^tabletest/', views.tabletest, name="tabletest"),
    url(r'^getstudata/', views.getstudata, name="getstudata"),
    url(r'^StuManage/', views.StuManage, name="StuManage"),
    url(r'^studetail/', views.Stu_Detail, name="Stu_Detail"),
    url(r'^StuAdd/', views.StuAdd, name="StuAdd"),
    url(r'^StuAddajax/$', views.StuAddajax, name="StuAddajax"),
    url(r'^Stu_Del/$', views.Stu_Del, name="Stu_Del"),
    url(r'^upstufile/$', views.UpLoadStuFile, name="upstufile"),
    url(r'^down_template/$', views.down_template, name="down_template"),
    url(r'^import_excel/$', views.import_excel, name="import_excel"),
    url(r'^',  include('DormAdmin.urls', namespace="DormAssign")),
    url(r'^', include('login.urls', namespace="login")),
    url(r'^captcha', include('captcha.urls')),  # 增加这一行
    # url(r'^password_reset', include('password_reset.urls')),  # 增加这一行

    #分配宿舍
    url(r'^distribute_dorm/$',views2.distribute_dorm, name="distribute_dorm"),

]
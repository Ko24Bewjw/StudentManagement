from django.conf.urls import url
from DormAdmin import views2
app_name = '[DormAssign]'
urlpatterns = [

    url(r'^dormassign/', views2.dormassign, name="dormassign"),
    url(r'^dormadjust/', views2.dormadjust, name="dormadjust"),
    url(r'^dormupdate/', views2.dormupdate, name="dormupdate"),

    # #分配宿舍
    # url(r'^distribute_dorm/$',views.distribute_dorm, name="distribute_dorm"),
]
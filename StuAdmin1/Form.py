# coding:utf-8
from django.http import HttpResponse
from django.shortcuts import render,render_to_response
from StuAdmin1.models import  Class,Stuinfo,Teacher,Institute,Admin_Class
from django import forms
import pdb
import time
from django.forms import ModelForm
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.admin import widgets

from django.contrib.auth.models import User
from django.forms import widgets as Fwidgets

from StuAdmin1.models import Stuinfo
class StuForm(forms.ModelForm):
    class Meta:
        model =Stuinfo
        fields ="__all__"







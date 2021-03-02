from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from StuAdmin1.models import Stuinfo
from django.contrib.auth.models import User
from StuAdmin1.models import Class,Institute,Teacher

import bootstrap3_datetime
from django.contrib import admin


admin.site.register(Stuinfo)
admin.site.register(Class)
admin.site.register(Institute)
admin.site.register(Teacher)


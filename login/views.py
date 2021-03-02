# login/views.py

from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from . import forms
import hashlib
import datetime
from django.conf import settings


# Create your views here.




def index(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    return render(request, 'login/index.html')
def login(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/index/')
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            try:
                user = models.User.objects.get(name=username)
            except:
                message = '用户不存在！'
                return render(request, 'login/login.html', locals())
            if user.password == hash_code(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/StuManage/')
            else:
                message = '密码不正确！'
                return render(request, 'login/login.html', locals())
        else:
            return render(request, 'login/login.html', locals())
    login_form = forms.UserForm()
    return render(request, 'login/login.html', locals())

def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')

            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已经存在'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已经被注册了！'
                    return render(request, 'login/register.html', locals())

                new_user = models.User()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()

                message = '注册成功，自动跳转至登录界面'
                return render(request, 'login/confirm.html', locals())
        else:
            return render(request, 'login/register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())

def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/login/")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/login/")
def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()

def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user,)
    return code

def send_email(email, code):

    from django.core.mail import EmailMultiAlternatives

    subject = '来自www.liujiangblog.com的注册确认邮件'

    text_content = '''感谢注册127.0.0.1:8080/confirm，这里是刘江的博客和教程站点，专注于Python、Django和机器学习技术的分享！\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''
                    <p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>http://127.0.0.1:8080</a>，\
                    这里是刘江的博客和教程站点，专注于Python、Django和机器学习技术的分享！</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求!'
        return render(request, 'login/confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'login/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
        return render(request, 'login/confirm.html', locals())

def pwd_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        pwdconfirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求!'
        return render(request, 'login/login.html', locals())

    c_time = pwdconfirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        pwdconfirm.user.delete()
        message = '您的邮件已经过期！请重新确认!'
        return render(request, 'login/resetpwd.html', locals())
    else:
        pwdconfirm.user.has_confirmed = True
        pwdconfirm.user.save()
        pwdconfirm.delete()
        message = '感谢确认，请前往新页面设置新的密码！'
        return render(request, 'login/pwd_confirm_done.html', locals())

def resetpwd_send(email, code):

    from django.core.mail import EmailMultiAlternatives

    subject = '来自信息学院网站的重置密码界面'

    text_content = '''这里是信息学院站点，专注于用信息技术改变未来！
                       如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''
                       <p>感谢注册<a href="http://{}/setpwd/?code={}" target=blank>http://127.0.0.1:8080</a>，\
                       这里是信息学院的官网，专注于培养用信息技术造福世界的一批优秀学者</p>
                       <p>请点击站点链接完成密码修改！</p>
                       <p>此链接有效期为{}天！</p>
                       '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def resetpwd(request):

    if request.method == 'POST':
        reset_form = forms.ResetForm(request.POST)
        message = '请检查填写的内容！'
        if reset_form.is_valid():
            email = reset_form.cleaned_data.get('email')
            try:
                user = models.User.objects.get(email=email)
            except:
                message = '用户不存在！'
                return render(request, 'login/resetpwd.html', locals())

            code = make_confirm_string(user)
            resetpwd_send(email, code)
            message = '请前往邮箱进行确认！'
            return render(request, 'login/resetpwdconfirm.html', locals())

        else:
            return render(request, 'login/resetpwd.html', locals())

    reset_form = forms.ResetForm()
    return render(request, 'login/resetpwd.html', locals())


def resetpwddone(request):

    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/index/')
    if request.method == 'POST':
        pwd_form = forms.PwdForm(request.POST)
        message = '请检查填写的内容！'
        if pwd_form.is_valid():
            username = pwd_form.cleaned_data.get('username')
            password1 = pwd_form.cleaned_data.get('password1')
            password2 = pwd_form.cleaned_data.get('password2')
            try:
                user = models.User.objects.get(name=username)
            except:
                message = '用户不存在！'
                return render(request, 'login/login.html', locals())
            models.User.objects.filter(name=username).update(password=hash_code(password1))
            message='修改成功，正在跳转到登录界面！ '
            return render(request, 'login/confirm.html')
        else:
            return render(request, 'login/resetpwd_done.html', locals())
    pwd_form = forms.PwdForm()
    return render(request, 'login/resetpwd_done.html', locals())

def pwd_confirm_done(request):

    code = request.GET.get('code', None)
    message = ''
    try:
        pwd_done_confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求!'
        return render(request, 'login/confirm.html', locals())

    c_time = pwd_done_confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        pwd_done_confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'login/confirm.html', locals())
    else:
        pwd_done_confirm.user.has_confirmed = True
        pwd_done_confirm.user.save()
        pwd_done_confirm.delete()
        message = '感谢确认，！'
        return render(request, 'login/pwd_confirm_done.html', locals())



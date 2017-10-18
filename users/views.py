from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic.base import View

# Create your views here.
from users.models import UserProfile, EmailVerifyRecord, UserMessage
from utils.email_send import send_register_email
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class RegisterView(View):  # 注册
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            if UserProfile.objects.filter(email=user_name):  # 判断用户是否存在
                return render(request, 'register.html', {'register_form': register_form, 'msg': '用户已经存在'})

            pass_word = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False  # 数据库中is_active 默认是False 没有激活,当变为True时为激活
            user_profile.password = make_password(pass_word)  # 密码加密
            user_profile.save()

            # 写入欢迎注册消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = '欢迎注册慕学在线网'
            user_message.save()

            send_register_email(user_name, 'register')
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'register_form': register_form})


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        # print(all_records)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                if user.is_active == False:
                    user.is_active = True
                    user.save()
                else:
                    return render(request, 'active_fail.html', {"msg": "这个链接已激活过!"})
        else:
            return render(request, 'active_fail.html', {"msg": "激活失败,链接错误!"})
        # return render(request, 'login.html')
        return HttpResponse("激活成功")


class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {"msg": ""})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get("username", "")
            password = request.POST.get("password", "")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_active:
                    return render(request, "index.html")
                else:
                    return render(request, "login.html", {"msg": "用户未激活"})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误"})
        else:
            return render(request, "login.html", {"msg": "", "login_form": login_form})


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_register_email(email, 'forget')
            # return render(request, 'send_success.html')
            return HttpResponse("密码重置链接发送成功")
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})
        else:
            return render(request, 'active_fail.html', {"msg": "重置密码链接无效"})
        return render(request, 'login.html')


class ModifyPwdView(View):
    """
    修改用户密码
    """

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'email': email, 'msg': '密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)  # 密码加密
            user.save()

            return render(request, 'login.html')
        else:
            email = request.POST.get('email', '')
            print(email)
            return render(request, 'password_reset.html', {'email': email, 'modify_form': modify_form})


class LogoutView(View):
    """
    用户登录
    """

    def get(self, request):
        logout(request)
        from django.core.urlresolvers import reverse  #
        return HttpResponseRedirect(reverse('index'))

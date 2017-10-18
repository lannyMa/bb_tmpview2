#!/usr/bin/env python
# coding=utf-8
from captcha.fields import CaptchaField
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True,min_length=5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True,min_length=5)
    captcha = CaptchaField(error_messages={"invalid":"验证码错误"})
    # captcha = CaptchaField()


class ForgetForm(forms.Form):   #忘记密码
    email = forms.CharField(required=True)
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


class ModifyPwdForm(forms.Form):   #重置密码
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)

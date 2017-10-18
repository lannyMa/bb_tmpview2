from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class UserProfile(AbstractUser):
    image = models.ImageField(max_length=100, upload_to="image/%Y/%m", default="image/default.png", verbose_name="头像")
    nick_name = models.CharField(max_length=50, default="", verbose_name="昵称")
    gender = models.CharField(max_length=10, choices=(("male", "男"), ("female", "女")), verbose_name="性别")
    birthday = models.DateField(verbose_name="生日", null=True, blank=True)
    address = models.CharField(max_length=100, default="", verbose_name="地址")
    mobile = models.CharField(max_length=11, default="", verbose_name="手机")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u'验证码')
    email = models.EmailField(max_length=50, verbose_name=u'邮箱')
    send_type = models.CharField(verbose_name=u'验证码类型',
                                 choices=(('register', u'注册'), ('forget', u'找回密码'), ('update_email', u'修改邮箱')),
                                 max_length=30)
    send_time = models.DateTimeField(verbose_name=u'发送时间', default=datetime.now)

    class Meta:
        verbose_name = u'邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.code, self.email)


class UserMessage(models.Model):
    user = models.IntegerField(default=0, verbose_name=u'接受用户')
    message = models.CharField(max_length=500, verbose_name=u'消息内容')
    has_read = models.BooleanField(default=False, verbose_name=u'是否已读')  # 布尔类型
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'用户消息'
        verbose_name_plural = verbose_name

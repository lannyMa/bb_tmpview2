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

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import AbstractBaseUser
from django.db.models import Max
from django.utils import timezone
from datetime import datetime

# Create your models here.



class UserProfile(AbstractUser):
    petname = models.CharField(max_length=20, )
    avator = models.ImageField(upload_to="pets/%Y/%m", default="pets/cmu.png", verbose_name="avatar")
    petage = models.IntegerField(null=True, blank=True)
    petbio = models.CharField(max_length=420, default=" ", null=True, blank=True)


class FoodSet(models.Model):
    amount  = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='amount')
    time = models.CharField(max_length=10)
    add_time = models.DateTimeField(auto_now=True)
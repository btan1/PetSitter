# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin


from .models import UserProfile,FoodSet
# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    pass


class FoodSetAdmin(admin.ModelAdmin):
    pass




admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(FoodSet, FoodSetAdmin)



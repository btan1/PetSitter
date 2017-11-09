# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin


from .models import *
# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    pass


class FoodSetAdmin(admin.ModelAdmin):
    pass


class ClipsAdmin(admin.ModelAdmin):
    pass

class PostAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(FoodSet, FoodSetAdmin)
admin.site.register(Clips, ClipsAdmin)
admin.site.register(Post, PostAdmin)




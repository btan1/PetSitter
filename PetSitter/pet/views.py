# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.http import  HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.db import transaction


from form import *
from models import *

# Create your views here.

@method_decorator(login_required, name='dispatch')
class IndexView(View):
    def get(self, request):
        return render(request, "index.html", {})


class RegisterView(View):

    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse("index"))
        return render(request, "register.html", {})

    def post(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse("globalstream"))
        registerForm = RegisterForm(request.POST)
        if registerForm.is_valid():
            username = registerForm.cleaned_data['email']
            first_name = registerForm.cleaned_data['first_name']
            last_name = registerForm.cleaned_data['last_name']
            password = registerForm.cleaned_data['password']
            email = registerForm.cleaned_data['email']
            userProfile = UserProfile()
            userProfile.username = username
            userProfile.first_name = first_name
            userProfile.last_name = last_name
            userProfile.password = make_password(password)
            userProfile.email = email
            userProfile.save()
            return render(request, 'login.html',{})
        else:
            return render(request, 'register.html', {"form":registerForm})




class LoginView(View):

    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse("index"))
        return render(request, "login.html", {
            "user":request.user,
        })

    def post(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse("index"))
        loginForm = LoginForm(request.POST)
        if loginForm.is_valid():
            username = loginForm.cleaned_data['email']
            password = loginForm.cleaned_data['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse("index"))

        else:
            return render(request, "login.html", {"loginForm": loginForm})


class LogoutView(View):
    def get(self,request):
        logout(request)
        return HttpResponseRedirect(reverse("login"))


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self,request):
        return render(request, 'profile.html', {
            "user": request.user,
        })

    def post(self, request):
        form = profileForm(request.POST)
        if form.is_valid():
            petname = form.cleaned_data['petname']
            petage = form.cleaned_data['petage']
            petbio = form.cleaned_data['petbio']
            user = request.user
            user.petname = petname
            user.petage = petage
            user.petbio = petbio
            user.save()
            return render(request, 'profile.html', {
                "user": request.user,
            })
        else:
            return render(request, 'profile.html', {"form":form})


@method_decorator(login_required, name='dispatch')
class UploadAvatorView(View):
    @transaction.atomic
    def post(self, request):
        avatorform = AvatorUploadForm(request.POST, request.FILES)
        user = request.user
        if avatorform.is_valid():
            avator = avatorform.cleaned_data['avator']
            request.user.avator = avator
            request.user.save()
            url = reverse("profile")
            return HttpResponseRedirect(url)
        else:

            return render(request, "profile.html", {
                "user": user,
                "form": avatorform,
            })


class FoodSetView(View):

    def get(self, request):
        return render(request, "food.html", {})

    def post(self, request):
        form = FoodSetForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            time = form.cleaned_data['time']
            foodset = FoodSet()
            foodset.amount = amount
            foodset.time = time
            foodset.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, 'food.html', {"form":form})













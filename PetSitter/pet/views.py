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
from django.views.decorators.csrf import csrf_exempt


from form import *
from models import *

import socket
# Create your views here.

@method_decorator(login_required, name='dispatch')
class IndexView(View):
    def get(self, request):
        user = request.user
        foodset = user.foodset_set.all()
        if Clips.objects.filter(user=user):
            photo = Clips.objects.filter(user=user)
        else:
            photo = None



        return render(request, "index.html", {
            "foodset":foodset,
            "photo":photo,
        })


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
            foodset.user = request.user
            foodset.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, 'food.html', {"form":form})

class SocketView(View):
    def get(self, request, flag):
        sock = socket.socket()
        port = 8080
        sock.connect(('192.168.137.243',port))

        if flag == "0":
            sock.send('0')
        else:
            sock.send('1')

        return render(request, 'camera.html', {})


class CameraView(View):
    def get(self, request):
        return render(request, 'camera.html', {})


class FoodChangeView(View):

    def get(self, request, id):

        if FoodSet.objects.filter(id=id):
            foodset = FoodSet.objects.get(id=id)
        else:
            foodset = None
        return render(request, "foodchange.html", {
            "foodset":foodset,
        })

    def post(self, request, id):
        form = FoodSetForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            time = form.cleaned_data['time']
            foodset = FoodSet.objects.get(id=id)
            foodset.amount = amount
            foodset.time = time
            foodset.user = request.user
            foodset.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, 'food.html', {"form":form})


@csrf_exempt
def uploadClips(request):
    if request.method == 'POST':

        #clipsform = ClipsUploadForm(request.POST, request.FILES)
        if request.META.has_key('HTTP_X_FORWARDED_FOR'):
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']

        user = UserProfile.objects.get(ipaddress=ip)
        clips = Clips(user=user, photos=request.FILES.get('media'))
        clips.save()


        return HttpResponseRedirect(reverse("index"))


class ClipView(View):
    def get(self,request):
        user = request.user
        all_clips = Clips.objects.all().filter(user = user)


        return render(request, 'clips.html', {
            "all_clips":all_clips
        })



class ShareView(View):
    def get(self, request):
        user = request.user
        all_clips = Clips.objects.all().filter(user=user)
        posts = Post.objects.all().order_by("-add_time")

        return render(request, 'share.html',{
            "all_clips": all_clips,
            "posts":posts,

        })

class PostShareView(View):
    def post(self, request):
        photo_path = request.POST.get("photo_path","")
        post = request.POST.get("post", "")
        if  photo_path and  post:
            newpost = Post(user=request.user, photo_path=photo_path, post=post);
            newpost.save()
            return HttpResponseRedirect(reverse('shareview'))
        else:
            return HttpResponseRedirect(reverse('shareview'))














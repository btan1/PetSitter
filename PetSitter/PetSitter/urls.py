"""PetSitter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from PetSitter.settings import MEDIA_ROOT
from django.views.static import serve
from pet.views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', login_required(IndexView.as_view()), name="index"),
    url(r'^register/$', RegisterView.as_view(), name="register"),
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^logout/', LogoutView.as_view(), name="logout"),
    url(r'^media/(?P<path>.*)/$', serve, {"document_root": MEDIA_ROOT}, name="media"),
    url(r'^profile/$', login_required(ProfileView.as_view()), name="profile"),
    url(r'^uploadavator/', login_required(UploadAvatorView.as_view()), name="uploadavator"),
    url(r'^foodset/', login_required(FoodSetView.as_view()), name="foodset"),
    url(r'^socket/', login_required(SocketView.as_view()), name="socket"),

]

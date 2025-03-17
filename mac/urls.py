"""
URL configuration for mac project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.shortcuts import HttpResponse,render
from django.conf import settings
from django.conf.urls.static import static
from . import views
def home(request):
    return HttpResponse("Welcome to home page")
urlpatterns = [
    path('admin/', admin.site.urls),
    path("signup", views.handleSignUp, name="handleSignUp"),
    path("login", views.handleLogin, name="handleLogin"),
    path("logout", views.handleLogout, name="handleLogout"),
    path('shop/', include('shop.urls')),
    path('blog/', include('blog.urls')),
    path("",views.index,name='home'),    
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


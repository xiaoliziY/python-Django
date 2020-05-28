"""LastProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from SuperApp import views #需要先导入对应的APP文件
urlpatterns = [
    #path('admin/', admin.site.urls),
    #path(r'index/',views.index),
    path('to_login/', views.to_login),
    path('register/', views.register),
    path('delUser/', views.delUser),
    path('editUser/',views.editUser),
    path('login/',views.login),
    path('selMsg/',views.selMsg),
    path('delMovie/',views.delMovie),
    path('toRegister/',views.toRegister),
    path('select/',views.select),
    path('showData/',views.showData),
    path('toIndex/', views.toIndex),
    path('tieba/', views.tieba),
    path('spiderMovies/', views.spiderMovies),
]


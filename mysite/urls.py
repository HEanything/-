"""
URL configuration for mysite project.

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
from django.urls import path
from app01 import views

urlpatterns = [
    path("", views.login,name='login'),
    path("login/",views.login,name='login'),
    path('index/', views.index, name='index'),
    path('student_index', views.student_index, name='student_index'),  # 学生仪表板
    path('logout/', views.logout, name='logout'),
    path('my_announcements/', views.my_announcements, name='my_announcements'),
    path('my_courses/', views.my_courses, name='my_courses'),
    path('my_scores/', views.my_scores, name='my_scores'),
    path('manage_courses/', views.manage_courses, name='manage_courses'),
    path('announcements/', views.announcements, name='announcements'),
    path('add_course/', views.add_course, name='add_course'),
    path('add_announcement/', views.add_announcement, name='add_announcement'),
    path('teacher_scores/', views.teacher_scores, name='teacher_scores')




]

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
    # 登录页面
    path('login/', views.login_view, name='login'),  # 登录页面路径
    path('', views.login_view, name='login'),
    # 教师和学生仪表板
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),  # 教师仪表板路径
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),  # 学生仪表板路径

    # 注销
    path('logout/', views.logout_view, name='logout'),  # 注销路径

    path('manage_courses/', views.manage_courses, name='manage_courses'),
    path('announcements/', views.announcements, name='announcements'),
    path('edit_announcement/<int:announcement_id>/', views.edit_announcement, name='edit_announcement'),
    path('delete_announcement/<int:announcement_id>/', views.delete_announcement, name='delete_announcement'),
    path('add_announcement/', views.add_announcement, name='add_announcement'),
    path('teacher_score/', views.manage_student_scores, name='manage_student_score'),

    path('my_announcements/', views.my_announcements, name='my_announcements'),
    path('my_courses/', views.my_courses, name='my_courses'),
    path('my_scores/', views.my_scores, name='my_scores'),







]

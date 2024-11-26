import psycopg2
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Course, Announcement, StudentScore

def login(request):
    # 处理登录请求
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # 尝试连接数据库并验证用户名和密码
        try:
            conn = psycopg2.connect(
                dbname="Stu_Score_Manage",
                user="postgres",  # 使用管理员用户连接数据库
                password="123",   # 使用管理员密码连接数据库
                host="localhost",
                port="5432"
            )
            cur = conn.cursor()

            # 查询用户信息
            cur.execute("SELECT * FROM Users WHERE user_name = %s", (username,))
            user = cur.fetchone()

            # 检查用户是否存在
            if user:
                stored_password = user[2]  # 假设密码在表中的第二列

                # 比较数据库中存储的密码和用户输入的密码
                if stored_password == password:
                    # 登录成功，将用户信息保存到会话中
                    request.session['user_id'] = user[0]  # 存储用户ID
                    request.session['username'] = username
                    request.session['role'] = user[5]  # 存储角色（学生或教师）

                    # 根据角色重定向到不同页面
                    if user[5] == 'teacher':  # 如果是教师
                        return redirect('/index')  # 教师仪表板页面
                    else:  # 如果是学生
                        return redirect('/student_index')  # 学生仪表板页面

                else:
                    # 密码错误
                    messages.error(request, '密码错误，请重新输入')
            else:
                # 用户名不存在
                messages.error(request, '用户名不存在，请重新输入')

            # 关闭数据库连接
            cur.close()
            conn.close()

        except psycopg2.OperationalError as e:
            # 数据库连接错误
            messages.error(request, '无法连接到数据库，请稍后再试')
        except Exception as e:
            # 其他错误
            messages.error(request, f'发生错误: {e}')

    return render(request, 'login.html')




def index(req):
    return render(req,'index.html')

def student_index(request):
    # 这里可以添加一些逻辑来获取学生的成绩、课程等信息
    return render(request, 'student_index.html')
def logout(request):
    # 清除会话中的用户信息
    request.session.flush()  # 清空会话数据
    return redirect('/login')  # 重定向到登录页面

# 教师管理课程
def manage_courses(request):

    return render(request, 'manager_course.html')

# 添加课程
def add_course(request):

    return render(request, 'add_course.html')

# 教师查看公告
def announcements(request):

    return render(request, 'announcement.html')

# 学生查看已注册课程
def my_courses(request):

    return render(request, 'my_courses.html')

# 学生查看成绩
def my_scores(request):

    return render(request, 'my_scores.html')

def my_announcements(request):
    # 假设学生公告是对所有学生可见的

    return render(request, 'my_announcements.html')
def add_announcement(request):
    return render(request, 'add_announcement.html')
def teacher_scores(request):
    return render(request, 'teacher_scores.html')

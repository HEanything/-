import psycopg2
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from django.db import connection

from app01.models import Course


# 数据库连接函数
def connect_db():
    try:
        conn = psycopg2.connect(
            database="stu_score",
            user="postgres",
            password="123",
            host="localhost",
            port="5432"
        )
    except Exception as e:
        print("Connect DB error:", e)
        return None
    return conn
# 提交数据库语句并断开数据库连接
def close_db_connection(conn):
    conn.commit()
    conn.close()

# 登录视图函数
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        is_teacher = 'is_teacher' in request.POST  # 检查是否选择了教师登录

        # 连接数据库
        conn = connect_db()
        if conn is None:
            messages.error(request, '无法连接到数据库，请稍后再试')
            return render(request, 'login.html')

        try:
            cur = conn.cursor()

            if is_teacher:
                # 查询教师表
                cur.execute("SELECT * FROM Teachers WHERE teacher_id = %s", (username,))
                user = cur.fetchone()

                if user and user[2] == password:  # 假设密码是用户表的第3列
                    # 登录成功，保存用户信息到会话
                    request.session['user_id'] = user[0]
                    request.session['username'] = user[1]  # 假设教师姓名在第二列
                    request.session['role'] = 'teacher'

                    # 重定向到教师仪表板
                    return redirect('teacher_dashboard')
                else:
                    messages.error(request, '用户名或密码错误')

            else:
                # 查询学生表
                cur.execute("SELECT * FROM Students WHERE student_id = %s", (username,))
                user = cur.fetchone()

                if user and user[2] == password:  # 假设密码是用户表的第3列
                    # 登录成功，保存用户信息到会话
                    request.session['user_id'] = user[0]
                    request.session['username'] = user[1]  # 假设学生姓名在第二列
                    request.session['role'] = 'student'

                    # 重定向到学生仪表板
                    return redirect('student_dashboard')
                else:
                    messages.error(request, '用户名或密码错误')

        except Exception as e:
            messages.error(request, f"发生错误: {e}")
        finally:
            cur.close()
            conn.close()

    return render(request, 'login.html')




def teacher_dashboard(req):
    return render(req,'index.html')

def student_dashboard(request):
    # 这里可以添加一些逻辑来获取学生的成绩、课程等信息
    return render(request, 'student_index.html')
def logout_view(request):
    # 清除会话中的用户信息
    request.session.flush()  # 清空会话数据
    return redirect('/login')  # 重定向到登录页面


# 课程管理视图
# 课程管理视图
def manage_courses(request):
    # 检查用户角色是否为教师
    if request.session.get('role') != 'teacher':
        messages.error(request, "请先登录")
        return redirect('/login')

    teacher_id = request.session.get('user_id')

    # 连接到数据库
    conn = connect_db()
    if conn is None:
        messages.error(request, "无法连接到数据库，请稍后再试")
        return redirect('/login')

    try:
        # 获取教师教授的所有课程
        cur = conn.cursor()
        cur.execute("""
            SELECT id, course_name, usual_score_ratio, attendance_score_ratio, final_score_ratio
            FROM Courses
            WHERE teacher_id = %s
        """, (teacher_id,))
        courses = cur.fetchall()  # 获取所有课程信息

        if request.method == 'POST':
            # 遍历所有提交的课程成绩占比数据
            for course in courses:
                course_id = course[0]
                usual_weight = request.POST.get(f'usual_weight_{course_id}')
                attendance_weight = request.POST.get(f'attendance_weight_{course_id}')
                final_weight = request.POST.get(f'final_weight_{course_id}')

                try:
                    # 更新课程的成绩占比
                    usual_weight = float(usual_weight) if usual_weight else None
                    attendance_weight = float(attendance_weight) if attendance_weight else None
                    final_weight = float(final_weight) if final_weight else None

                    # 执行更新
                    cur.execute("""
                        UPDATE Courses
                        SET usual_score_ratio = %s, attendance_score_ratio = %s, final_score_ratio = %s
                        WHERE id = %s
                    """, (usual_weight, attendance_weight, final_weight, course_id))

                    conn.commit()  # 提交事务
                    messages.success(request, f'课程 {course[1]} 更新成功')  # course[1] 是课程名称
                except ValueError:
                    messages.error(request, '请输入有效的成绩占比')

            # 更新数据库后，重新查询最新的课程数据
            cur.execute("""
                SELECT id, course_name, usual_score_ratio, attendance_score_ratio, final_score_ratio
                FROM Courses
                WHERE teacher_id = %s
            """, (teacher_id,))
            courses = cur.fetchall()  # 重新获取所有课程信息

        # 将课程数据传递到模板中
        return render(request, 'manager_course.html', {'courses': courses})

    except Exception as e:
        messages.error(request, f"发生错误: {e}")
        return redirect('/login')

    finally:
        if conn:
            close_db_connection(conn)



# 教师查看公告
# 查看公告视图函数
def announcements(request):
    # 检查用户角色是否为教师
    if request.session.get('role') != 'teacher':
        messages.error(request, "请先登录")
        return redirect('/login')

    # 获取教师ID
    teacher_id = request.session.get('user_id')

    # 连接到数据库
    conn = connect_db()
    if conn is None:
        messages.error(request, "无法连接到数据库，请稍后再试")
        return redirect('/login')

    try:
        cur = conn.cursor()

        # 获取该教师发布的所有公告
        cur.execute("""
            SELECT id, title, publish_date
            FROM Announcements
            WHERE teacher_id = %s
            ORDER BY publish_date DESC
        """, (teacher_id,))

        announcements = cur.fetchall()  # 获取公告列表

        # 将公告数据传递到模板
        return render(request, 'announcement.html', {'announcements': announcements})

    except Exception as e:
        messages.error(request, f"发生错误: {e}")
        return redirect('/login')

    finally:
        if conn:
            close_db_connection(conn)

# 发布公告视图
def add_announcement(request):
    # 检查用户角色是否为教师
    if request.session.get('role') != 'teacher':
        messages.error(request, "请先登录")
        return redirect('/login')

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        if not title or not content:
            messages.error(request, "标题和内容不能为空")
            return render(request, 'add_announcement.html')

        # 获取教师ID
        teacher_id = request.session.get('user_id')

        # 连接到数据库
        conn = connect_db()
        if conn is None:
            messages.error(request, "无法连接到数据库，请稍后再试")
            return redirect('/login')

        try:
            cur = conn.cursor()

            # 获取当前时间
            timestamp = datetime.now()

            # 执行数据库插入公告操作
            cur.execute("""
                INSERT INTO Announcements (teacher_id, title, content, created_at)
                VALUES (%s, %s, %s, %s)
            """, (teacher_id, title, content, timestamp))

            conn.commit()  # 提交事务

            messages.success(request, "公告发布成功")  # 发布成功提示
            return redirect('/announcements')  # 可选择重定向到公告列表页（假设你有此页面）

        except Exception as e:
            messages.error(request, f"发生错误: {e}")
            return render(request, 'add_announcement.html')

        finally:
            if conn:
                close_db_connection(conn)

    return render(request, 'add_announcement.html')

# 学生查看已注册课程
def my_courses(request):

    return render(request, 'my_courses.html')

# 学生查看成绩
def my_scores(request):

    return render(request, 'my_scores.html')

def my_announcements(request):
    # 假设学生公告是对所有学生可见的

    return render(request, 'my_announcements.html')

def teacher_scores(request):
    return render(request, 'teacher_scores.html')

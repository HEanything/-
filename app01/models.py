from django.db import models
from django.contrib.auth.models import User

class Teacher(models.Model):
    teacher_id = models.CharField(max_length=50, primary_key=True)  # 教师工号
    name = models.CharField(max_length=100)                         # 教师姓名
    password = models.CharField(max_length=255)                     # 密码
    email = models.CharField(max_length=100)                        # 邮箱
    create_date = models.DateTimeField(auto_now_add=True)           # 创建时间

    def __str__(self):
        return self.name


class Student(models.Model):
    student_id = models.CharField(max_length=50, primary_key=True)  # 学号
    name = models.CharField(max_length=100)                         # 学生姓名
    password = models.CharField(max_length=255)                     # 密码
    email = models.CharField(max_length=100)                        # 邮箱
    create_date = models.DateTimeField(auto_now_add=True)           # 创建时间

    def __str__(self):
        return self.name


class Course(models.Model):
    course_name = models.CharField(max_length=200, unique=True)  # 课程名称
    course_code = models.CharField(max_length=50, unique=True)   # 课程代码
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='courses')  # 教师工号
    usual_score_ratio = models.DecimalField(max_digits=5, decimal_places=2)  # 平时成绩占比
    attendance_score_ratio = models.DecimalField(max_digits=5, decimal_places=2)  # 出勤成绩占比
    final_score_ratio = models.DecimalField(max_digits=5, decimal_places=2)  # 期末成绩占比

    def __str__(self):
        return self.course_name


class StudentScore(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='scores')  # 学生
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='student_scores')  # 课程
    usual_score = models.DecimalField(max_digits=5, decimal_places=2)  # 平时成绩
    attendance_score = models.DecimalField(max_digits=5, decimal_places=2)  # 出勤成绩
    final_score = models.DecimalField(max_digits=5, decimal_places=2)  # 期末成绩
    total_score = models.DecimalField(max_digits=5, decimal_places=2)  # 总成绩
    grade = models.CharField(max_length=2)  # 成绩等级

    def __str__(self):
        return f"{self.student.name} - {self.course.course_name}"


class Announcement(models.Model):
    title = models.CharField(max_length=200)  # 公告标题
    content = models.TextField()  # 公告内容
    publish_date = models.DateTimeField(auto_now_add=True)  # 发布时间
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='announcements')  # 发布公告的教师工号

    def __str__(self):
        return self.title
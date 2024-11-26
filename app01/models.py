from django.db import models

# 用户表（用户可以是学生或教师）
class User(models.Model):
    ROLE_CHOICES = [
        ('student', '学生'),
        ('teacher', '教师'),
    ]
    user_name = models.CharField(max_length=100, unique=True)  # 用户名
    password = models.CharField(max_length=255)  # 密码（需要加密存储）
    email = models.EmailField(max_length=100)  # 邮箱
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)  # 用户角色（学生或教师）
    create_date = models.DateTimeField(auto_now_add=True)  # 创建时间

    def __str__(self):
        return self.user_name

# 课程表
class Course(models.Model):
    course_name = models.CharField(max_length=200, unique=True)  # 课程名称
    course_code = models.CharField(max_length=50, unique=True)  # 课程代码
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='courses')  # 关联教师

    def __str__(self):
        return self.course_name
# 学生成绩表（StudentScores），记录学生成绩
class StudentScore(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})  # 学生
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # 课程
    usual_score = models.FloatField(null=True, blank=True)  # 平时成绩
    attendance_score = models.FloatField(null=True, blank=True)  # 出勤成绩
    final_score = models.FloatField(null=True, blank=True)  # 期末成绩
    total_score = models.FloatField(null=True, blank=True)  # 总成绩
    grade = models.CharField(max_length=2, null=True, blank=True)  # 成绩等级（如A, B, C, D, F）

    def __str__(self):
        return f"{self.student.user_name} - {self.course.course_name}"

    # 计算总成绩并保存
    def save(self, *args, **kwargs):
        if self.usual_score is not None and self.attendance_score is not None and self.final_score is not None:
            # 计算总成绩
            self.total_score = self.usual_score + self.attendance_score + self.final_score
            # 根据总成绩确定成绩等级
            if self.total_score >= 90:
                self.grade = 'A'
            elif self.total_score >= 80:
                self.grade = 'B'
            elif self.total_score >= 70:
                self.grade = 'C'
            elif self.total_score >= 60:
                self.grade = 'D'
            else:
                self.grade = 'F'
        super(StudentScore, self).save(*args, **kwargs)
# 学生课程关联表（存储学生的课程信息和成绩）
class StudentCourse(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_courses')  # 关联学生
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='students')  # 关联课程
    usual_score = models.FloatField(null=True, blank=True)  # 平时成绩
    attendance = models.FloatField(null=True, blank=True)  # 出勤
    final_score = models.FloatField(null=True, blank=True)  # 期末成绩
    total_score = models.FloatField(null=True, blank=True)  # 总成绩
    grade = models.CharField(max_length=10, null=True, blank=True)  # 成绩等级（例如：A, B, C）

    def __str__(self):
        return f'{self.student.user_name} - {self.course.course_name}'

# 公告表
class Announcement(models.Model):
    title = models.CharField(max_length=200)  # 公告标题
    content = models.TextField()  # 公告内容
    publish_date = models.DateTimeField(auto_now_add=True)  # 公告发布时间
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='announcements')  # 发布公告的教师

    def __str__(self):
        return self.title
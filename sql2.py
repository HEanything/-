import psycopg2

# 连接数据库
def connect_db():
    try:
        conn = psycopg2.connect(database="Score_Manage", user="postgres", password="123", host="localhost", port="5432")
    except Exception as e:
        print("Connect DB error:", e)
    else:
        return conn
    return None

# 提交数据库语句并断开数据库连接
def close_db_connection(conn):
    conn.commit()
    conn.close()


def drop_all_tables():
    # 连接到学校数据库
    conn = psycopg2.connect(database="Score_Manage", user="postgres", password="123", host="localhost", port="5432")
    cur = conn.cursor()

    # 获取所有表的名字
    cur.execute("""
        SELECT tablename 
        FROM pg_tables
        WHERE schemaname = 'public';
    """)

    tables = cur.fetchall()

    # 删除每个表
    for table in tables:
        table_name = table[0]
        print(f"Deleting table: {table_name}")
        cur.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE;")

    # 提交事务
    conn.commit()

    # 关闭连接
    cur.close()
    conn.close()

if __name__ == "__main__":
    drop_all_tables()
    conn = connect_db()  # 连接数据库
    cur = conn.cursor()  # 创建会话

    # 创建 Students 表（学生表）
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Students (
        student_id VARCHAR(50) PRIMARY KEY,  -- 学号
        name VARCHAR(100),                   -- 学生姓名
        password VARCHAR(255),               -- 密码
        email VARCHAR(100),                  -- 邮箱
        create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP   -- 创建时间
    );
    """)

    # 创建 Teachers 表（教师表）
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Teachers (
        teacher_id VARCHAR(50) PRIMARY KEY,  -- 工号
        name VARCHAR(100),                   -- 教师姓名
        password VARCHAR(255),               -- 密码
        email VARCHAR(100),                  -- 邮箱
        create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP   -- 创建时间
    );
    """)

    # 创建 Courses 表（课程表）- 存储课程的基本信息
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Courses (
        course_code VARCHAR(50) PRIMARY KEY, -- 课程代码
        course_name VARCHAR(200) UNIQUE,     -- 课程名称
        course_type VARCHAR(50),             -- 课程类型（如：必修、选修）
        credits DECIMAL(3,1)                 -- 学分
    );
    """)

    # 创建 TeacherCourses 表（教师教授课程表）- 存储教师教授课程的信息
    cur.execute("""
    CREATE TABLE IF NOT EXISTS TeacherCourses (
        course_code VARCHAR(50),             -- 课程代码
        course_seq INT,                      -- 课程序号（多位教师教授同一门课程）
        teacher_id VARCHAR(50),              -- 教师工号
        usual_score_ratio DECIMAL(5,2),      -- 平时成绩占比
        attendance_score_ratio DECIMAL(5,2), -- 出勤成绩占比
        final_score_ratio DECIMAL(5,2),      -- 期末成绩占比
        PRIMARY KEY (course_code, course_seq), -- 课程代码 + 课程序号组成主键
        FOREIGN KEY (course_code) REFERENCES Courses(course_code), -- 外键关联课程表
        FOREIGN KEY (teacher_id) REFERENCES Teachers(teacher_id)  -- 外键关联教师表
    );
    """)

    # 创建 StudentScores 表（学生成绩表）- 存储学生成绩信息
    cur.execute("""
    CREATE TABLE IF NOT EXISTS StudentScores (
        id SERIAL PRIMARY KEY,               -- 成绩记录ID
        student_id VARCHAR(50),              -- 学号
        course_code VARCHAR(50),             -- 课程代码
        course_seq INTEGER,                  -- 课序号
        usual_score DECIMAL(5,2),            -- 平时成绩
        attendance_score DECIMAL(5,2),       -- 出勤成绩
        final_score DECIMAL(5,2),            -- 期末成绩
        total_score DECIMAL(5,2),            -- 总成绩
        grade CHAR(2),                       -- 成绩等级（A, B, C, D, F）
        FOREIGN KEY (student_id) REFERENCES Students(student_id),  -- 外键关联学生表
        FOREIGN KEY (course_code) REFERENCES Courses(course_code)  -- 外键关联课程表
    );
    """)

    # 创建 Announcements 表（公告表）- 存储教师发布的公告
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Announcements (
        id SERIAL PRIMARY KEY,               -- 公告ID
        title VARCHAR(200),                  -- 公告标题
        content TEXT,                        -- 公告内容
        publish_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 发布时间
        teacher_id VARCHAR(50),              -- 发布公告的教师工号
        FOREIGN KEY (teacher_id) REFERENCES Teachers(teacher_id)  -- 外键关联教师表
    );
    """)

    # 创建 StudentCourses 表（学生选课表）- 记录学生选修的课程信息
    cur.execute("""
    CREATE TABLE IF NOT EXISTS StudentCourses (
        student_id VARCHAR(50),              -- 学号
        course_code VARCHAR(50),             -- 课程代码
        PRIMARY KEY (student_id, course_code), -- 学号 + 课程代码 组成主键
        FOREIGN KEY (student_id) REFERENCES Students(student_id),  -- 外键关联学生表
        FOREIGN KEY (course_code) REFERENCES Courses(course_code)  -- 外键关联课程表
    );
    """)

    # 插入学生数据
    cur.execute(
        "INSERT INTO Students (student_id, name, password, email) VALUES ('S12345678', '张三', 'password123', 'student1@example.com')")
    cur.execute(
        "INSERT INTO Students (student_id, name, password, email) VALUES ('S23456789', '李四', 'password123', 'student2@example.com')")

    # 插入教师数据
    cur.execute(
        "INSERT INTO Teachers (teacher_id, name, password, email) VALUES ('T1001', '王老师', 'password123', 'teacher1@example.com')")
    cur.execute(
        "INSERT INTO Teachers (teacher_id, name, password, email) VALUES ('T1002', '赵老师', 'password123', 'teacher2@example.com')")

    # 插入课程数据
    cur.execute(
        "INSERT INTO Courses (course_code, course_name, course_type, credits) VALUES ('CS101', '数据库原理', '必修', 3.0)")
    cur.execute(
        "INSERT INTO Courses (course_code, course_name, course_type, credits) VALUES ('CS102', '操作系统', '必修', 3.0)")
    cur.execute(
        "INSERT INTO Courses (course_code, course_name, course_type, credits) VALUES ('CS103', '算法设计', '选修', 2.5)")

    # 插入教师教授课程数据
    cur.execute("""
    INSERT INTO TeacherCourses (course_code, course_seq, teacher_id, usual_score_ratio, attendance_score_ratio, final_score_ratio)
    VALUES
        ('CS101', 1, 'T1001', 30.00, 20.00, 50.00),
        ('CS102', 1, 'T1001', 30.00, 20.00, 50.00),
        ('CS103', 1, 'T1002', 40.00, 20.00, 40.00);
    """)

    # 插入学生选课数据
    cur.execute("""
    INSERT INTO StudentCourses (student_id, course_code) 
    VALUES 
        ('S12345678', 'CS101'),
        ('S12345678', 'CS102'),
        ('S23456789', 'CS101'),
        ('S23456789', 'CS103');
    """)

    # 插入学生成绩数据（包含课序号）
    cur.execute("""
    INSERT INTO StudentScores (student_id, course_code, course_seq, usual_score, attendance_score, final_score, total_score, grade)
    VALUES
        ('S12345678', 'CS101', 1, 80.0, 85.0, 90.0, 255.0, 'A'),
        ('S12345678', 'CS102', 1, 70.0, 75.0, 80.0, 225.0, 'B'),
        ('S23456789', 'CS101', 1, 85.0, 90.0, 95.0, 270.0, 'A'),
        ('S23456789', 'CS103', 1, 88.0, 92.0, 93.0, 273.0, 'A');
    """)

    # 插入公告数据
    cur.execute("""
    INSERT INTO Announcements (title, content, teacher_id)
    VALUES
        ('课程安排调整', '由于特殊情况，本学期的课程安排有所调整，请同学们留意。', 'T1001'),
        ('期中考试通知', '期中考试将于下周一举行，请同学们做好准备。', 'T1002');
    """)

    close_db_connection(conn)
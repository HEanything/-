import psycopg2

# 连接数据库
def connect_db():
    try:
        conn = psycopg2.connect(database="stu_score", user="postgres", password="123", host="localhost", port="5432")
    except Exception as e:
        print("Connect DB error:", e)
    else:
        return conn
    return None

# 提交数据库语句并断开数据库连接
def close_db_connection(conn):
    conn.commit()
    conn.close()

if __name__ == "__main__":
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

    # 创建 Courses 表（课程表）
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Courses (
        id SERIAL PRIMARY KEY,               -- 课程ID
        course_name VARCHAR(200) UNIQUE,     -- 课程名称
        course_code VARCHAR(50) UNIQUE,      -- 课程代码
        teacher_id VARCHAR(50),              -- 教师工号
        usual_score_ratio DECIMAL(5,2),      -- 平时成绩占比（例如 30.00）
        attendance_score_ratio DECIMAL(5,2), -- 出勤成绩占比（例如 20.00）
        final_score_ratio DECIMAL(5,2),      -- 期末成绩占比（例如 50.00）
        FOREIGN KEY (teacher_id) REFERENCES Teachers (teacher_id)  -- 关联教师
    );
    """)

    # 创建 StudentScores 表（学生成绩表）
    cur.execute("""
    CREATE TABLE IF NOT EXISTS StudentScores (
        id SERIAL PRIMARY KEY,               -- 成绩记录ID
        student_id VARCHAR(50),              -- 学号
        course_id INTEGER,                   -- 课程ID
        usual_score DECIMAL(5,2),            -- 平时成绩
        attendance_score DECIMAL(5,2),       -- 出勤成绩
        final_score DECIMAL(5,2),            -- 期末成绩
        total_score DECIMAL(5,2),            -- 总成绩
        grade CHAR(2),                       -- 成绩等级（A, B, C, D, F）
        FOREIGN KEY (student_id) REFERENCES Students (student_id),  -- 关联学生
        FOREIGN KEY (course_id) REFERENCES Courses (id)  -- 关联课程
    );
    """)

    # 创建 Announcements 表（公告表）
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Announcements (
        id SERIAL PRIMARY KEY,               -- 公告ID
        title VARCHAR(200),                  -- 公告标题
        content TEXT,                        -- 公告内容
        publish_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 发布时间
        teacher_id VARCHAR(50),              -- 发布公告的教师工号
        FOREIGN KEY (teacher_id) REFERENCES Teachers (teacher_id)  -- 关联教师
    );
    """)

    # 插入测试数据

    # 插入学生数据
    cur.execute("INSERT INTO Students (student_id, name, password, email) VALUES ('S12345678', '张三', 'password123', 'student1@example.com')")
    cur.execute("INSERT INTO Students (student_id, name, password, email) VALUES ('S23456789', '李四', 'password123', 'student2@example.com')")

    # 插入教师数据
    cur.execute("INSERT INTO Teachers (teacher_id, name, password, email) VALUES ('T1001', '王老师', 'password123', 'teacher1@example.com')")
    cur.execute("INSERT INTO Teachers (teacher_id, name, password, email) VALUES ('T1002', '赵老师', 'password123', 'teacher2@example.com')")

    # 插入课程数据
    cur.execute("INSERT INTO Courses (course_name, course_code, teacher_id, usual_score_ratio, attendance_score_ratio, final_score_ratio) VALUES ('数据库原理', 'CS101', 'T1001', 30.00, 20.00, 50.00)")
    cur.execute("INSERT INTO Courses (course_name, course_code, teacher_id, usual_score_ratio, attendance_score_ratio, final_score_ratio) VALUES ('操作系统', 'CS102', 'T1001', 30.00, 20.00, 50.00)")
    cur.execute("INSERT INTO Courses (course_name, course_code, teacher_id, usual_score_ratio, attendance_score_ratio, final_score_ratio) VALUES ('算法设计', 'CS103', 'T1002', 40.00, 20.00, 40.00)")

    cur.execute(
        "INSERT INTO StudentScores (student_id, course_id, usual_score, attendance_score, final_score, total_score, grade) VALUES ('S12345678', 1, 80.0, 85.0, 90.0, 255.0, 'A')")
    cur.execute(
        "INSERT INTO StudentScores (student_id, course_id, usual_score, attendance_score, final_score, total_score, grade) VALUES ('S12345678', 2, 70.0, 75.0, 80.0, 225.0, 'B')")
    cur.execute(
        "INSERT INTO StudentScores (student_id, course_id, usual_score, attendance_score, final_score, total_score, grade) VALUES ('S23456789', 1, 85.0, 90.0, 95.0, 270.0, 'A')")
    cur.execute(
        "INSERT INTO StudentScores (student_id, course_id, usual_score, attendance_score, final_score, total_score, grade) VALUES ('S23456789', 3, 88.0, 92.0, 93.0, 273.0, 'A')")

    # 插入公告数据
    cur.execute(
        "INSERT INTO Announcements (title, content, teacher_id) VALUES ('课程安排调整', '由于特殊情况，本学期的课程安排有所调整，请同学们留意。', 'T1001')")
    cur.execute(
        "INSERT INTO Announcements (title, content, teacher_id) VALUES ('期中考试通知', '期中考试将于下周一举行，请同学们做好准备。', 'T1002')")

    close_db_connection(conn)
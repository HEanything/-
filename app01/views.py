import time

import psycopg2
from django.shortcuts import render, redirect
from django.contrib import messages

def login(request):
    # 处理登录请求
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # 尝试连接数据库
        try:
            conn = psycopg2.connect(
                dbname="postgres",
                user=username,
                password=password,
                host="localhost",
                port="5432"
            )
            conn.close()

            # 将用户名和密码保存到会话中
            request.session['db_username'] = username
            request.session['db_password'] = password

            return redirect('/index')  # 重定向到 index 页面
        except psycopg2.OperationalError as e:
            # 连接失败
            messages.error(request, '用户名或密码错误：')
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')

    return render(request, 'login.html')




def index(req):
    name='数据库原理'
    list=['a','b',1,2,3]
    dict={"name":"张三",'age':12,"grade":2}
    list_dict=[
        {"name":"张三",'age':12,"grade":2},
        {"name":"李四",'age':12,"grade":2},
        {"name":"王五",'age':12,"grade":2}
    ]
    return render(req,'index.html',{'name':name,
                                    'list':list,
                                    'dict':dict,
                                    "list_dict":list_dict})

def table_datatable(request):
    db_username = request.session.get('db_username')
    db_password = request.session.get('db_password')

    if not db_username or not db_password:
        messages.error(request, 'You need to log in first.')
        return redirect('/login')

    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=db_username,
            password=db_password,
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        # 查询表结构
        cursor.execute("""
            SELECT table_name, column_name, data_type
            FROM information_schema.columns
            WHERE table_schema = 'public'
            ORDER BY table_name, ordinal_position;
        """)
        columns = cursor.fetchall()

        cursor.close()
        conn.close()

        context = {
            'columns': columns
        }

        return render(request, 'table-datatable.html', context)
    except Exception as e:
        messages.error(request, f'An error occurred: {e}')
        return redirect('/login')
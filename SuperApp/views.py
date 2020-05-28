from django.shortcuts import render
from django.shortcuts import HttpResponse
from mysql.sql import mysql
from spider.movie_spider import movie_spider
from spider.tieba_spider import TiebaSpider
import pymysql
import json
sqls = [
    "select * from user",#0
    "select * from movies",#1
    "select * from user where username='%s'",#2
    "insert into user(username,password) values ('%s','%s')",#3
    "delete from movies where id ='%s' ",#4
    "delete from user where id ='%s' ",#5
    "update user set password = '%s' where id = '%s'",#6
    "select * from movies where title like '%s'",#7
    "select * from movies where id>='%s' limit 10",  # 8
    "select * from movies where id>='%s' and title like '%s' limit 10"#9
]

def paging(page,user_list):#分页
    data = (int(user_list[(int(page) - 1) * 10]['id']),)
    userlist = connectToTheDatabase(8, data, 'movies')
    return userlist
def selMsg(request):  # 展示数据
    user_list = connectToTheDatabase(1, str='movies')
    count=len(user_list)
    page = request.GET.get('page', None)
    userlist=paging(page,user_list)
    return HttpResponse(json.dumps({"code": 0, "msg": "", "count": count, "data": userlist}),
                        content_type='application/json')


def select(request):  # 模糊查询
    title = request.GET.get('title', None)
    data = ('%'+title + '%',)
    page=request.GET.get('page',None)
    userlist = connectToTheDatabase(7, data,str='movies')
    count=len(userlist)
    data = (int(userlist[(int(page) - 1) * 10]['id']),'%'+title + '%')
    userlist = connectToTheDatabase(9, data, str='movies')
    print(userlist)
    return HttpResponse(json.dumps({"code": 0, "msg": "", "count": count, "data": userlist}),
                        content_type='application/json')


def delMovie(request):  # 根据id删除数据库
    id = request.GET.get('id', None)
    page=request.GET.get('page',None)
    data = (id,)
    connectToTheDatabase(4, data)
    userlist = connectToTheDatabase(1, str='movies')
    count=len(userlist)
    userlist=paging(page,userlist)
    return HttpResponse(json.dumps({"code": 0, "msg": "", "count":count, "data": userlist}),
                        content_type='application/json')


def connectToTheDatabase(num, data=None, str='user'):  # 连接数据库
    global sqls
    user_list = []
    con = pymysql.Connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="root",
        db="homework",
        charset="utf8"
    )
    cursor = con.cursor()
    if data != None:
        cursor.execute(sqls[num] % data)
        con.commit()
    else:
        cursor.execute(sqls[num])
        con.commit()
    if (str == 'user'):
        for x in cursor.fetchall():
            dict = {}
            dict["id"] = x[0]
            dict["username"] = x[1]
            dict["password"] = x[2]
            user_list.append(dict)
    elif (str == 'movies'):
        for x in cursor.fetchall():
            dict = {}
            dict["id"] = x[0]
            dict["title"] = x[3]
            dict["url"] = x[1]
            dict["cover"] = x[2]
            user_list.append(dict)
    cursor.close()
    con.close()
    return user_list


def editUser(request):  # 修改密码
    id = request.GET.get("id", None)
    newpassword = request.GET.get("newpsw", None)
    data = (newpassword, id)
    connectToTheDatabase(6, data)
    user_list = connectToTheDatabase(0)
    return render(request, "allUsers.html", {"data": user_list})


def delUser(request):  # 注销用户
    # 获取用户输入的值
    userid = request.GET.get("id", None)
    data = (userid,)
    connectToTheDatabase(5, data)
    user_list = connectToTheDatabase(0)
    return render(request, "allUsers.html", {"data": user_list})


def toRegister(request):
    return render(request, "register.html")


def register(request):  # 注册
    username = request.POST.get("name", None)
    password = request.POST.get("password", None)
    data = (username, password)
    if data[0] != None or data[1] != None:
        connectToTheDatabase(3, data)
        user_list = connectToTheDatabase(0)
        return render(request, "login.html")
    else:
        return render(request, "register.html")


def to_login(request):
    return render(request, "login.html")
def toIndex(request):
    return render(request,"index.html")
def showData(request):
    return render(request,"main2.html")

def login(request):  # 登录
    username = request.POST.get("username", None)
    password = request.POST.get("password", None)
    data = (username,)
    uselist = connectToTheDatabase(2, data)
    if len(uselist) == 0:
        return render(request, "login.html", {"info": "用户不存在"})
    else:
        for x in uselist:
            if x['password'] == password:
                return render(request, "index.html", {"msg": '欢迎'+username})
        return render(request, "login.html", {"info": "密码输入错误"})



#爬贴吧
def tieba(request):
    # 获取输入的贴吧名
    tiebaName = request.GET.get('tiebaName', None)
    page=request.GET.get('page', None)
    if page==None:
        page=2
    else:page=eval(page)
    TiebaSpider(tiebaName,page).run()
    return render(request, 'index.html',{"msg":"爬取完成"})

#爬电影
def spiderMovies(request):
    # 连接mysql数据库
    con, cursor = mysql().connect_sql()
    movieList = []
    # 爬取
    movie_spider(2).run()
    cursor.close()
    return render(request, "index.html",{"msg":"爬取完成"})
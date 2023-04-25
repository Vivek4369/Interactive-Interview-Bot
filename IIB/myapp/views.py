from django.shortcuts import render
#User_app
from django.http import HttpResponse  
from myapp.functions.functions import handle_uploaded_file  
from myapp.forms import StudentForm  

import mysql.connector as sql
fn=''
ln=''
mail=''
pw=''
cpw=''
id = 0

resumeScore=''
job=''


def demo(request):  
    if request.method == 'POST':  
        global fn,ln,mail,job,resumeScore
        student = StudentForm(request.POST, request.FILES) 
        context={}
        score = handle_uploaded_file(request.FILES['file'],request.POST['job'])
        # context = {
        #     'score': score,
        #     'name': request.POST['firstname'],
        #     'job' : request.POST['job']
        # }
        m = sql.connect(host='localhost', user='root', passwd='Viv@4369',database='iib')
        cursor = m.cursor()
        data = request.POST
        for key,value in data.items():
            if key=="firstname":
                fn = value
            if key =="lastname":
                ln = value
            if key=="email":
                mail = value
            if key =="job":
                job = value
        

        cmd = "insert into resume Values('{}','{}','{}','{}','{}')".format(fn,ln,mail,job,score)
        cursor.execute(cmd)
        m.commit()

        cmd = "select * from resume"
        cursor.execute(cmd)
        t = tuple(cursor.fetchall())
        context = {
            'score': score,
            'name': request.POST['firstname'],
            'job' : request.POST['job'],
            'resumedata' : t
        }
        return render(request,"result.html",context)
        
        # if student.is_valid():  
        #     handle_uploaded_file(request.FILES['file'])  
        #     # return HttpResponse("File uploaded successfuly")  
        #     score = num
        #     return render(request,"result.html",score)
    else:  
        student = StudentForm()  
        return render(request,"demo.html",{'form':student})  

def login(request):
    global mail,pw,id
    if request.method == 'POST':
        m = sql.connect(host='localhost', user='root', passwd='Viv@4369',database='iib')
        cursor = m.cursor()
        data = request.POST
        for key,value in data.items():
            if key=="email":
                mail = value
            if key =="password":
                pw = value

        cmd = "select * from users where email='{}' and password='{}'".format(mail,pw)
        cursor.execute(cmd)
        t = tuple(cursor.fetchall())
        if t==():
            context = {
                'msg': 'wrong email or password'
            }
            return render(request,'login.html',context)
        else:
            cmd = "select UserID from users where email='{}'".format(mail)
            cursor.execute(cmd)
            t = tuple(cursor.fetchall())
            id = t[0][0]
            return render(request,'home.html')

    else:
        return render(request,"login.html")

def home(request):
    return render(request,"home.html")

def features(request):
    return render(request,"features.html")

def integration(request):
    return render(request,"integration.html")

def resources(request):
    return render(request,"resources.html")

def solutions(request):
    return render(request,"solutions.html")

def registration(request):
    global mail,pw 
    global fn,ln,mail,pw,cpw 
    if request.method == 'POST':
        m = sql.connect(host='localhost', user='root', passwd='Viv@4369',database='iib')
        cursor = m.cursor()
        data = request.POST
        for key,value in data.items():
            if key=="firstname":
                fn = value
            if key =="lastname":
                ln = value
            if key=="email":
                mail = value
            if key =="password":
                pw = value
            if key =="cpassword":
                cpw = value

        cmd = "insert into users(FirstName,LastName,Email,Password,cPassword) Values('{}','{}','{}','{}','{}')".format(fn,ln,mail,pw,cpw)
        cursor.execute(cmd)
        m.commit()
        context = {
            'msg': 'Sucessfully registered'
        }
        return render(request,'signup.html',context)

    else:
        return render(request,"signup.html")

def result(request):
    m = sql.connect(host='localhost', user='root', passwd='Viv@4369',database='iib')
    cursor = m.cursor()
    
    cmd = "select * from users"
    cursor.execute(cmd)
    t = tuple(cursor.fetchall())
    context = {
        'data' : t
    }
    return render(request,"result.html",context)

def dashboard(request):
    global id
    m = sql.connect(host='localhost', user='root', passwd='Viv@4369',database='iib')
    cursor = m.cursor()

    cmd = "select * from users where UserID='{}'".format(id)
    cursor.execute(cmd)
    t = tuple(cursor.fetchall())
    context = {
        'data' : t
    }
    return render(request,"dashboard.html",context)

def jobs(request):
    global id
    m = sql.connect(host='localhost', user='root', passwd='Viv@4369',database='iib')
    cursor = m.cursor()

    cmd = "select * from job"
    cursor.execute(cmd)
    t = tuple(cursor.fetchall())
    context = {
        'data' : t
    }
    return render(request,"jobs.html",context)

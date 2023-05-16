from django.shortcuts import render
#Admin_app
from django.http import HttpResponse  
from myapp.functions.functions import handle_uploaded_file  
from myapp.forms import StudentForm  

import mysql.connector as sql
fn=''
ln=''
mail=''
pw=''
cpw=''
cmp_name=''

resumeScore=''
job=''
title=''
desc=''
req=''
res=''


def admin_demo(request):  
    if request.user.is_authenticated:
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
    else:
        return render(request,"admin_signup.html")


def admin_login(request):
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

        cmd = "select * from admin where business_email='{}' and password='{}'".format(mail,pw)
        cursor.execute(cmd)
        t = tuple(cursor.fetchall())
        if t==():
            context = {
                'msg': 'wrong email or password'
            }
            return render(request,'admin_login.html',context)
        else:
            cmd = "select admin_id from admin where business_email='{}'".format(mail)
            cursor.execute(cmd)
            t = tuple(cursor.fetchall())
            id = t[0][0]
            return render(request,'admin_home.html')

    else:
        return render(request,"admin_login.html")

def admin_home(request):
    return render(request,"admin_home.html")

def admin_features(request):
    return render(request,"features.html")

def admin_integration(request):
    return render(request,"integration.html")

def admin_resources(request):
    return render(request,"resources.html")

def admin_solutions(request):
    return render(request,"solutions.html")

def admin_registration(request):
    global mail,pw 
    global fn,ln,mail,pw,cpw,cmp_name 
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
            if key =="company_name":
                cmp_name = value

        cmd = "insert into admin(business_email, password, first_name, last_name, company_name) Values('{}','{}','{}','{}','{}')".format(mail,pw,fn,ln,cmp_name)
        cursor.execute(cmd)
        m.commit()
        context = {
            'msg': 'Sucessfully registered'
        }
        return render(request,'admin_signup.html',context)

    else:
        return render(request,"admin_signup.html")

def admin_result(request):
    m = sql.connect(host='localhost', user='root', passwd='Viv@4369',database='iib')
    cursor = m.cursor()
    
    cmd = "select * from users"
    cursor.execute(cmd)
    t = tuple(cursor.fetchall())
    context = {
        'data' : t
    }
    return render(request,"result.html",context)

def admin_dashboard(request):
    global id

    m = sql.connect(host='localhost', user='root', passwd='Viv@4369',database='iib')
    cursor = m.cursor()

    cmd = "select * from admin where admin_id='{}'".format(id)
    cursor.execute(cmd)
    t = tuple(cursor.fetchall())
    context = {
        'data' : t
    }
    return render(request,"admin_dashboard.html",context)


def new_job(request):
    global title,desc,res,req,id
    if request.method == 'POST':
        m = sql.connect(host='localhost', user='root', passwd='Viv@4369',database='iib')
        cursor = m.cursor()
        data = request.POST
        for key,value in data.items():
            if key=="jobtitle":
                title = value
            if key =="desctiption":
                desc = value
            if key=="requirements":
                req = value
            if key =="responsibility":
                res = value

        cmd = "insert into job(adminid,title,description,requirements,responsibility) Values('{}','{}','{}','{}','{}')".format(id,title,desc,req,res)
        cursor.execute(cmd)
        m.commit()
        context = {
            'msg': 'Sucessfully Created'
        }
        return render(request,'admin_dashboard.html',context)

    else:
        return render(request,"new_job.html")
    
def admin_jobs(request):
    global id
    m = sql.connect(host='localhost', user='root', passwd='Viv@4369',database='iib')
    cursor = m.cursor()

    cmd = "select * from job"
    cursor.execute(cmd)
    t = tuple(cursor.fetchall())
    context = {
        'data' : t
    }
    return render(request,"admin_jobs.html",context)
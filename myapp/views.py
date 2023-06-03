from django.shortcuts import render
#User_app
from django.http import HttpResponse  
from myapp.functions.functions import handle_uploaded_file  
from myapp.forms import StudentForm  
import numpy as np
from numpy.core.numeric import NaN
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import pandas as pd
# import seaborn as sns
import matplotlib.pyplot as plt
import json
import re
import time
import cv2
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
# from flask import Flask , render_template , request , url_for , jsonify , Response
# from werkzeug.utils import redirect, secure_filename
# from flask_mail import Mail , Message
# from flask_mysqldb import MySQL
from pyresparser import ResumeParser
# from fer import Video
# from fer import FER
# from video_analysis import extract_text , analyze_tone
# from decouple import config
import mysql.connector as sql
import os

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


        fname = request.POST['firstname'].capitalize()
        lname = request.POST['lastname'].capitalize()
        age = int(request.POST['age'])
        gender = request.POST['gender']
        email = request.POST['email']
        file = request.FILES['resume']
        
        val1 = request.POST['openness']
        val2 = request.POST['neuroticism']
        val3 = request.POST['conscientiousness']
        val4 = request.POST['agreeableness']
        val5 = request.POST['extraversion']

        df = pd.read_csv(r'myapp\static\trainDataset.csv')
        le = LabelEncoder()
        df['Gender'] = le.fit_transform(df['Gender'])
        x_train = df.iloc[:, :-1].to_numpy()
        y_train = df.iloc[:, -1].to_numpy(dtype = str)
        lreg = LogisticRegression(multi_class='multinomial', solver='newton-cg',max_iter =1000)
        lreg.fit(x_train, y_train)

        if gender == 'male':
            gender = 1
        elif gender == 'female': 
            gender = 0
        input =  [gender, age, val1, val2, val3, val4, val5]

        pred = str(lreg.predict([input])[0]).capitalize()

        # get data from the resume
        score = handle_uploaded_file(request.FILES['resume'],'software developer')
        msg = ''
        if score<50 :
            msg = 'You have low resume score, work on your resume to get hired easily'
        elif score<70 :
            msg = 'You have a good resume score'
        else:
            msg = 'You have a great resume score'

        result = {'Name':fname+' '+lname , 'Age':age , 'Email':email , 'score':score, 'msg':msg, 'PredictedPersonality':pred}

        return render(request,"result.html",result)
    else:  
        student = StudentForm()  
        return render(request,"demo.html") 

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

def about_job(request):
    global id
    m = sql.connect(host='localhost', user='root', passwd='Viv@4369',database='iib')
    cursor = m.cursor()

    cmd = "select * from job"
    cursor.execute(cmd)
    t = tuple(cursor.fetchall())
    context = {
        'data' : t
    }
    return render(request,"about_job.html",context)

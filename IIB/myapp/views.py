from django.shortcuts import render

from django.http import HttpResponse  
from myapp.functions.functions import handle_uploaded_file  
from myapp.forms import StudentForm  
import random
num = random.random()
score = num
def demo(request):  
    if request.method == 'POST':  
        student = StudentForm(request.POST, request.FILES) 
        context={}
        score = random.randint(40,100)
        score = score%100
        context['score'] = score
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
    return render(request,"registration.html")
def result(request):
    return render(request,"result.html")
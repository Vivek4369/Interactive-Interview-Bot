import PyPDF2
import re
import math
import string
import pandas as pd
import csv
from collections import Counter
WORD = re.compile(r"\w+")

def getText(pdfReader):
    num_pages = pdfReader.numPages

    # Initialize a count for the number of pages
    count = 0

    # Initialize a text empty etring variable
    text = ''

    # Extract text from every page on the file
    while count < num_pages:
        pageObj = pdfReader.getPage(count)
        count +=1
        text += pageObj.extractText() 
        
    # Convert all strings to lowercase
    text = text.lower()

    # Remove numbers
    text = re.sub(r'\d+',' ',text)
    text = re.sub(r'\n',' ',text)
    text = re.sub(r',',' ',text)

    # Remove punctuation
    text = text.translate(str.maketrans('','',string.punctuation))
    return text

def getJobData(job):
    with open('myapp/static/jobdata.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        jobData = ''
        for row in csv_reader:
            if row["job"] == job:
                jobData = row["data"]
                break

    # jobData = "B.Tech or M.Tech in EE/ECE/CSE from a reputed engineering college Programming knowledge of C/C++ for HLS is required. SystemC is a plus Proficiency in C++ is mandatory Knowledge of one of the scripting languages like Perl, Tcl.  Experience with LINUX platforms. Basics of Verilog/VHDL and experience in Logic Synthesis/High-Level Synthesis is plus Sound knowledge of windows technologies Good debugging and investigation skills  software engineer, A background in software engineering, software design or architecture and an understanding of how your area of expertise supports our customers Along with at least four years of experience in software development streams Have implementation knowledge of PySpark and Data warehousing, and good SQL query skills Experience in implementing programming best practice, especially around scalability, automation, virtualization, optimization, availability and performance An understanding of cloud, ideally AWS Experience in working with code repositories, bug tracking tools and wikis Coding experience in multiple programming languages Experience with DevOps and Agile methodology and associated toolsets and methodologies A background in solving highly complex, analytical and numerical problems"            
    jobData = jobData.lower()

    # Remove numbers
    jobData = re.sub(r'\d+',' ',jobData)
    jobData = re.sub(r'\n',' ',jobData)
    jobData = jobData.translate(str.maketrans('','',string.punctuation))
    return jobData

def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)


def getScore(text1, text2): #get similarity using cosine similarity
    vec1 = text_to_vector(text1)
    vec2 = text_to_vector(text2)
    
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def handle_uploaded_file(f):  
    with open('myapp/static/'+f.name, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)  


    job = 'software developer'
    jobData = getJobData(job)

    pdfFileObj = open('myapp/static/'+f.name ,'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    
    resumeText = getText(pdfReader)

    score = getScore(resumeText,jobData) * 100
    
    score = float(f'{score:.2f}')
    return score
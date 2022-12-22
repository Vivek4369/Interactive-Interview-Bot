from django import forms  
JOB_CHOICES= [
    ('software developer', 'Software Developer'),
    ('software engineer', 'Software Engineer'),
    ('data scientist', 'Data Scientist'),
    ('ui developer', 'UI Developer'),
    ('senior developer', 'Senior Develpoper'),
    ]

class StudentForm(forms.Form):  
    firstname = forms.CharField(label="Enter first name",max_length=50)  
    lastname  = forms.CharField(label="Enter last name", max_length = 10)  
    email     = forms.EmailField(label="Enter Email")  
    job       = forms.CharField(label='Select the job', widget=forms.Select(choices=JOB_CHOICES))
    file      = forms.FileField() # for creating file input  
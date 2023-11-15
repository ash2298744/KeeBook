import os
from django.shortcuts import render,redirect
from django.http import HttpResponse
from core.settings import BASE_DIR
from .utils import send_email_to_client

def send_email(request):
    send_email_to_client()
    return redirect('/')
    
def home(request):
    peoples=[
        {'name':'Ashish Gupta','age':22},
        {'name':'Abhijeet Gupta','age':26},
        {'name':'Vivky Kaushal','age':17},
        {'name':'Deepanshu Chaurasiya','age':24},
        {'name':'Sandeep Maheshwari','age':29}
    ]
    
    vegetabels = ["Pumpkin", "Tomato", "Potato"]
    
    return render(request,"index.html",context={'peoples': peoples,'vegetables': vegetabels})
    # return HttpResponse("<h1>Hey I am a Django Server.</h1>")

def success_page(request):
    return HttpResponse("This is success page")
# Create your views here.

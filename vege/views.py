import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from core.settings import BASE_DIR
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.core.paginator import Paginator
from django.db.models import Q,Sum
# Create your views here.

@login_required(login_url="/login/")
def books(request):
    if request.method == "POST":
        data = request.POST
        
        book_name = data.get('book_name')
        book_description = data.get('book_description')
        book_image = request.FILES.get('book_image')
        
        Book.objects.create(book_name=book_name, book_description=book_description, book_image=book_image)
        # print(receipe_name)
        # print(receipe_description)
        # print(receipe_image)
    
        return redirect('/books/')
    
    queryset = Book.objects.all()
    
    if request.GET.get('search'):
        queryset = queryset.filter(book_name__icontains = request.GET.get('search'))
    
    
    context = {'books':queryset}
    return render(request,"books.html", context)

@login_required(login_url="/login/")
def delete_book(request, id):
    queryset =  Book.objects.get(id = id)
    queryset.delete()
    return redirect('/books/')

@login_required(login_url="/login/")
def update_book(request,id):
    queryset =  Book.objects.get(id = id)
    
    if request.method == "POST":
        data=request.POST
        
        book_name = data.get('book_name')
        book_description = data.get('book_description')
        book_image = request.FILES.get('book_image')
        
        queryset.book_name = book_name
        queryset.book_description = book_description
        
        if book_image:
            queryset.book_image = book_image
            
        queryset.save()
        return redirect('/books/')
    
    context = {'books':queryset}
    return render(request,"update_books.html", context)

def login_page(request):
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not User.objects.filter(username = username).exists():
            messages.info(request,"Username doesn't exists")
            return redirect('/login/')
        
        user = authenticate(username = username, password = password)
        
        if not user:
            messages.info(request,"Incorrect Password")
            return redirect('/login/')
        else:
            login(request, user = user)
            return redirect('/books/')
        
    return render(request, "login.html")


def logout_page(request):
    logout(request)
    return redirect("/login/")


def register(request):
    
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = User.objects.filter(username = username)
        
        if user.exists():
            messages.info(request,"Username already taken")
            return redirect('/register/')
        
        user = User.objects.create(
            first_name=first_name, 
            last_name=last_name,
            username=username
        )
        
        user.set_password(password)
        user.save()
        
        messages.info(request,"Account created succesfully")
        return redirect('/register/')
        
        
    return render(request, "register.html")


def get_students(request):
    queryset = Student.objects.all()
    
    if request.GET.get('search'):
        search = request.GET.get('search')
        queryset = queryset.filter(
                Q(student_name__icontains = search) |
                Q(department__department__icontains = search) |
                Q(student_id__student_id__icontains = search) |
                Q(student_email__icontains = search) |
                Q(student_age__icontains = search)               
            )
    paginator = Paginator(queryset, 25) #25 rows per page
    page_number = request.GET.get("page" , 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'report/students.html', {'queryset' : page_obj})

from .seed import generate_report_card
def see_marks(request, student_id):
    queryset = SubjectMarks.objects.filter(student__student_id__student_id = student_id)
    total_marks = queryset.aggregate(total_marks = Sum('marks'))
    
    ranks = Student.objects.annotate(marks = Sum('studentmarks__marks')).order_by('-marks', '-student_age')
    

    return render(request, 'report/see_marks.html', {'queryset' : queryset, 'total_marks' : total_marks })
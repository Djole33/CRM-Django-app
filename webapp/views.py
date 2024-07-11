from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import *
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import *

def home(request):
    return render(request, 'webapp/index.html')

def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect('/my-login')
    
    return render(request, 'webapp/register.html', {'form':form})

def my_login(request):
    form = LoginForm(request, data=request.POST)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.info(request, "Logged in successfully!")
            return redirect('/dashboard')

    return render(request, 'webapp/my-login.html', {'form':form})

def user_logout(request):
    auth.logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("my-login")

@login_required(login_url='my-login')
def dashboard(request):
    my_records = Record.objects.all()
    return render(request, 'webapp/dashboard.html', {'records': my_records})

@login_required(login_url='my-login')
def create_record(request):
    form = CreateRecordForm()
    if request.method == "POST":
        form = CreateRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Record created successfully!")
            return redirect('/dashboard')
    
    return render(request, 'webapp/create-record.html', {'form':form})

@login_required(login_url='my-login')
def update_record(request, pk):
    record = Record.objects.get(id=pk)
    form = UpdateRecordForm(instance=record)
    if request.method == "POST":
        form = UpdateRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.info(request, "Record updated successfully!")
            return redirect('/dashboard')
    
    return render(request, 'webapp/update-record.html', {'form':form})

@login_required(login_url='my-login')
def view_record(request, pk):
    all_records = Record.objects.get(id=pk)
    
    return render(request, 'webapp/view-record.html', {'record':all_records})

@login_required(login_url='my-login')
def delete_record(request, pk):
    record = Record.objects.get(id=pk)
    record.delete()
    messages.error(request, "Record deleted successfully!")
    
    return redirect("dashboard")

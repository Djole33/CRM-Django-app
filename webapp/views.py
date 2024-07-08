from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import *
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

def home(request):
    return render(request, 'webapp/index.html')

def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
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
            return redirect('/')

    return render(request, 'webapp/my-login.html', {'form':form})

def user_logout(request):
    auth.logout(request)
    return redirect("my-login")

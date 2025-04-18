from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from tasks.forms import RegisterForm

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        print(request.POST.get('password1'))
        print(request.POST.get('password2'))

        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()  
                login(request, user)  
                return redirect('signin')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': form,
                    'error': 'El usuario ya existe'
                })
        else:
            return render(request, 'signup.html', {
                'form': form,
                'error': 'Las contraseñas no coinciden o datos inválidos'
            })
    else:
        form = RegisterForm()
        return render(request, 'signup.html', {'form': form})
    
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html',{
            'form': AuthenticationForm()
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST
            ['password'])
        if user is None:
            return render(request, 'signin.html',{
                'form': AuthenticationForm(),
                'error': 'Usuario o contraseña incorrectos'
            }) 
        else:
            login(request, user)
            return redirect('admin')
        
def signout(request):
    logout(request)
    return redirect('landing')
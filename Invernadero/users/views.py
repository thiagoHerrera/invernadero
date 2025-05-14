from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from users.forms import RegisterForm

def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']

            # Verificar que las contraseñas coinciden
            if password1 != password2:
                return render(request, 'signup.html', {
                    'form': form,
                    'error': 'Las contraseñas no coinciden'
                })
            
            try:
                user = form.save()  # Guardar el usuario en la base de datos
                login(request, user)  # Iniciar sesión automáticamente
                return redirect('signin')  # Redirigir al login
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': form,
                    'error': 'El usuario ya existe'
                })
        else:
            return render(request, 'signup.html', {
                'form': form,
                'error': 'Hay datos inválidos en el formulario'
            })
    else:
        form = RegisterForm()
        return render(request, 'signup.html', {'form': form})

    
    
def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Autenticar al usuario con los datos proporcionados
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirigir a la página principal
        else:
            return render(request, 'signin.html', {
                'form': form,
                'error': 'Usuario o contraseña incorrectos'
            })
    else:
        form = AuthenticationForm()
        return render(request, 'signin.html', {
            'form': form
        })


def logout_view(request):
    logout(request)  
    return redirect('landing')  

        
def signout(request):
    logout(request)
    return redirect('landing')
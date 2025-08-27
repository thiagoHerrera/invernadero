from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from users.forms import RegisterForm
from django.core.exceptions import ValidationError


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
                    'error': 'Contraseñas no coinciden'
                })
            
            try:
                user = form.save()  # Guardar el usuario
                login(request, user)  # Iniciar sesión automáticamente
                return redirect('signin')  # Ir al login
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': form,
                    'error': 'Usuario ya registrado'
                })
        else:
            # Unificar errores del formulario en mensajes cortos
            error_map = {
                'username': 'Nombre de usuario inválido',
                'email': 'Email inválido',
                'password1': 'Contraseña inválida',
                'password2': 'Confirmación de contraseña inválida'
            }
            for field, errors in form.errors.items():
                error_msg = error_map.get(field, 'Error en el formulario')
                break  # Tomamos solo el primer error
            return render(request, 'signup.html', {
                'form': form,
                'error': error_msg
            })
    else:
        form = RegisterForm()
        return render(request, 'signup.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            # Mensaje corto y común
            error_msg = "Usuario o contraseña incorrecta"
            return render(request, 'signin.html', {
                'form': form,
                'error': error_msg
            })
    else:
        form = AuthenticationForm()
        return render(request, 'signin.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('landing')


def signout(request):
    logout(request)
    return redirect('landing')

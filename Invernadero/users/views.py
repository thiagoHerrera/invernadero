from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from users.forms import RegisterForm
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from users.tokens import account_activation_token
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.urls import reverse

def home(request):
    return render(request, 'home.html')

def landing(request):
    return render(request, 'landing.html')

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

@login_required
def disable_2fa(request):
    if request.method == 'POST':
        TOTPDevice.objects.filter(user=request.user).delete()
        return redirect('home')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Cuenta activada. Ahora podés iniciar sesión.')
        return redirect('login')
    else:
        return render(request, 'registration/activation_invalid.html')
    
def reenviar_activacion(request):
    user = request.user

    if user.is_active:
        messages.info(request, "Tu cuenta ya está activada.")
        return redirect('home')

    # Generar token de activación
    token = account_activation_token.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    activation_link = request.build_absolute_uri(
        reverse('activar_cuenta', kwargs={'uidb64': uid, 'token': token})
    )

    # Enviar el correo
    subject = 'Activa tu cuenta en BandLink'
    message = render_to_string('users/activation_email.html', {
        'user': user,
        'activation_link': activation_link,
    })

    email = EmailMessage(subject, message, to=[user.email])
    email.content_subtype = 'html'
    email.send()

    messages.success(request, 'Te enviamos un nuevo correo de activación 📬')
    return redirect('home')
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.urls import reverse
from Invernadero.Verificacion2FA.tokens import account_activation_token

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

    token = account_activation_token.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    activation_link = request.build_absolute_uri(
        reverse('activar_cuenta', kwargs={'uidb64': uid, 'token': token})
    )

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


# Create your views here.

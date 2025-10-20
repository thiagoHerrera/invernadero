#!/usr/bin/env python3
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'invernadero.settings')
django.setup()

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

def test_password_reset_email():
    try:
        user = User.objects.get(email='floracoreai@gmail.com')
        
        send_mail(
            subject='Prueba Reset FloraCore',
            message=f'Hola {user.username}, este es un email de prueba para reset de contraseña.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        print(f"[OK] Email enviado a {user.email}")
        
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == '__main__':
    test_password_reset_email()
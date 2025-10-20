#!/usr/bin/env python3
"""
Script para probar el envío de emails
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'invernadero.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_email():
    """Probar envío de email"""
    try:
        print(f"[INFO] Configuración de email:")
        print(f"  - Host: {settings.EMAIL_HOST}")
        print(f"  - Puerto: {settings.EMAIL_PORT}")
        print(f"  - Usuario: {settings.EMAIL_HOST_USER}")
        print(f"  - TLS: {settings.EMAIL_USE_TLS}")
        
        # Enviar email de prueba
        send_mail(
            subject='Prueba de FloraCore',
            message='Este es un email de prueba desde FloraCore.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['test@example.com'],  # Cambia por tu email
            fail_silently=False,
        )
        print("[OK] Email enviado exitosamente")
        
    except Exception as e:
        print(f"[ERROR] Error enviando email: {e}")
        print("\n[INFO] Para configurar Gmail:")
        print("1. Activa verificación en 2 pasos en tu cuenta Google")
        print("2. Ve a Seguridad > Contraseñas de aplicaciones")
        print("3. Genera una contraseña para 'Correo'")
        print("4. Actualiza el archivo .env con tu email y contraseña de aplicación")

if __name__ == '__main__':
    test_email()
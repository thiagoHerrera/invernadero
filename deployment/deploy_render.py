#!/usr/bin/env python
"""
Script para preparar el despliegue en Render
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def setup_production():
    """Configura el entorno de producción"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'invernadero.settings')
    os.environ.setdefault('DEBUG', 'False')
    
    try:
        django.setup()
        
        print("🔄 Ejecutando migraciones...")
        execute_from_command_line(['manage.py', 'migrate', '--noinput'])
        
        print("📦 Recopilando archivos estáticos...")
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        
        print("👤 Creando superusuario...")
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@floracore.com',
                password='floracore2025'
            )
            print("✅ Superusuario creado: admin/floracore2025")
        else:
            print("ℹ️  Superusuario ya existe")
            
        print("✅ Configuración de producción completada!")
        
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        sys.exit(1)

if __name__ == '__main__':
    setup_production()
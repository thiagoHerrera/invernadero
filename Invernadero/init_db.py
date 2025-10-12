#!/usr/bin/env python3
"""
Script para inicializar base de datos forzadamente
"""
import os
import django
from django.core.management import execute_from_command_line
from django.db import connection

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'invernadero.settings')
django.setup()

def force_create_tables():
    """Forzar creación de tablas"""
    print("Forzando creación de tablas...")
    
    # Ejecutar migraciones core de Django
    execute_from_command_line(['manage.py', 'migrate', 'auth', '--run-syncdb'])
    execute_from_command_line(['manage.py', 'migrate', 'contenttypes', '--run-syncdb'])
    execute_from_command_line(['manage.py', 'migrate', 'sessions', '--run-syncdb'])
    execute_from_command_line(['manage.py', 'migrate', 'admin', '--run-syncdb'])
    
    # Crear migraciones para apps
    execute_from_command_line(['manage.py', 'makemigrations'])
    
    # Ejecutar todas las migraciones
    execute_from_command_line(['manage.py', 'migrate', '--run-syncdb'])
    
    print("Tablas creadas exitosamente")

def create_superuser():
    """Crear superusuario"""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create_superuser('admin', 'admin@floracore.com', 'floracore2025')
        print("Superusuario creado")
    else:
        print("Superusuario ya existe")

if __name__ == '__main__':
    force_create_tables()
    create_superuser()
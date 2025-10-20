#!/usr/bin/env python3
"""
Script para solucionar problemas de despliegue en Render
"""
import os
import django
from django.core.management import execute_from_command_line
from django.conf import settings

def setup_django():
    """Configurar Django"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'invernadero.settings')
    django.setup()

def run_migrations():
    """Ejecutar migraciones de forma segura"""
    print("🔄 Ejecutando migraciones...")
    
    # Crear migraciones si no existen
    execute_from_command_line(['manage.py', 'makemigrations'])
    
    # Ejecutar migraciones con --run-syncdb para crear tablas faltantes
    execute_from_command_line(['manage.py', 'migrate', '--run-syncdb'])
    
    print("✅ Migraciones completadas")

def create_superuser():
    """Crear superusuario si no existe"""
    print("👤 Verificando superusuario...")
    
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create_superuser('admin', 'admin@floracore.com', 'floracore2025')
        print("✅ Superusuario creado")
    else:
        print("ℹ️ Superusuario ya existe")

def collect_static():
    """Recopilar archivos estáticos"""
    print("📁 Recopilando archivos estáticos...")
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput', '--clear'])
    print("✅ Archivos estáticos recopilados")

def main():
    """Función principal"""
    print("🚀 Iniciando configuración de despliegue...")
    
    setup_django()
    run_migrations()
    create_superuser()
    collect_static()
    
    print("🎉 Configuración completada exitosamente")

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""
Script para verificar la configuración de base de datos
"""
import os
import django
from django.core.management import execute_from_command_line

def setup_django():
    """Configurar Django"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'invernadero.settings')
    django.setup()

def check_database():
    """Verificar conexión a base de datos"""
    print("[INFO] Verificando conexión a base de datos...")
    
    try:
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        print("[OK] Conexión a base de datos exitosa")
        return True
    except Exception as e:
        print(f"[ERROR] Error de conexión: {e}")
        return False

def check_migrations():
    """Verificar estado de migraciones"""
    print("[INFO] Verificando migraciones...")
    
    try:
        from django.core.management.commands.showmigrations import Command
        from io import StringIO
        import sys
        
        # Capturar output
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        execute_from_command_line(['manage.py', 'showmigrations'])
        
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        
        if '[X]' in output:
            print("[OK] Migraciones aplicadas")
            return True
        else:
            print("[WARN] Algunas migraciones pendientes")
            print(output)
            return False
            
    except Exception as e:
        print(f"[ERROR] Error verificando migraciones: {e}")
        return False

def check_auth_tables():
    """Verificar tablas de autenticación"""
    print("[INFO] Verificando tablas de autenticación...")
    
    try:
        from django.contrib.auth.models import User
        count = User.objects.count()
        print(f"[OK] Tabla auth_user existe - {count} usuarios")
        return True
    except Exception as e:
        print(f"[ERROR] Tabla auth_user no existe: {e}")
        return False

def main():
    """Función principal"""
    print("[INFO] Verificando configuración de base de datos...\n")
    
    setup_django()
    
    checks = [
        check_database(),
        check_migrations(),
        check_auth_tables(),
    ]
    
    if all(checks):
        print("\n[SUCCESS] Base de datos configurada correctamente")
    else:
        print("\n[ERROR] Problemas con la configuración de base de datos")
        print("Ejecuta: python manage.py migrate --run-syncdb")

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""
Script para diagnosticar y solucionar el problema de usuarios que se borran
"""
import os
import django
import shutil
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'invernadero.settings')
django.setup()

from django.contrib.auth.models import User
from django.db import connection

def backup_database():
    """Crear backup de la base de datos"""
    db_path = 'db.sqlite3'
    if os.path.exists(db_path):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = f'db_backup_{timestamp}.sqlite3'
        shutil.copy2(db_path, backup_path)
        print(f"[OK] Backup creado: {backup_path}")
        return backup_path
    return None

def check_database_integrity():
    """Verificar integridad de la base de datos"""
    try:
        cursor = connection.cursor()
        cursor.execute("PRAGMA integrity_check;")
        result = cursor.fetchone()
        if result[0] == 'ok':
            print("[OK] Base de datos integra")
            return True
        else:
            print(f"[ERROR] Problemas de integridad: {result[0]}")
            return False
    except Exception as e:
        print(f"[ERROR] Error verificando integridad: {e}")
        return False

def check_users():
    """Verificar usuarios existentes"""
    try:
        users = User.objects.all()
        print(f"[INFO] Usuarios encontrados: {users.count()}")
        for user in users:
            print(f"   - {user.username} (ID: {user.id}, Activo: {user.is_active})")
        return users.count()
    except Exception as e:
        print(f"[ERROR] Error verificando usuarios: {e}")
        return 0

def fix_session_settings():
    """Verificar y ajustar configuración de sesiones"""
    from django.conf import settings
    
    print("[INFO] Verificando configuracion de sesiones...")
    
    # Verificar si las sesiones están configuradas correctamente
    if 'django.contrib.sessions' in settings.INSTALLED_APPS:
        print("[OK] App de sesiones instalada")
    else:
        print("[ERROR] App de sesiones NO instalada")
    
    if 'django.contrib.sessions.middleware.SessionMiddleware' in settings.MIDDLEWARE:
        print("[OK] Middleware de sesiones configurado")
    else:
        print("[ERROR] Middleware de sesiones NO configurado")

def create_test_user():
    """Crear usuario de prueba"""
    try:
        username = 'testuser'
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username,
                email='test@floracore.com',
                password='test123456'
            )
            print(f"[OK] Usuario de prueba creado: {username}")
            return user
        else:
            print(f"[INFO] Usuario de prueba ya existe: {username}")
            return User.objects.get(username=username)
    except Exception as e:
        print(f"[ERROR] Error creando usuario de prueba: {e}")
        return None

def main():
    """Función principal"""
    print("[INFO] Diagnosticando problema de usuarios que se borran...\n")
    
    # 1. Backup de la base de datos
    backup_database()
    
    # 2. Verificar integridad
    check_database_integrity()
    
    # 3. Verificar usuarios actuales
    user_count = check_users()
    
    # 4. Verificar configuración de sesiones
    fix_session_settings()
    
    # 5. Crear usuario de prueba si no hay usuarios
    if user_count <= 1:  # Solo admin
        print("\n[WARN] Solo hay usuario admin, creando usuario de prueba...")
        create_test_user()
    
    print("\n[INFO] RECOMENDACIONES:")
    print("1. Usa siempre 'python manage.py runserver' para iniciar el servidor")
    print("2. No ejecutes scripts que puedan resetear la DB sin querer")
    print("3. Verifica que no haya procesos que eliminen db.sqlite3")
    print("4. Considera usar PostgreSQL para mayor estabilidad")
    
    print("\n[INFO] PRUEBA:")
    print("1. Crea un usuario nuevo")
    print("2. Cierra el servidor")
    print("3. Ejecuta este script para verificar si el usuario persiste")
    print("4. Inicia el servidor nuevamente")

if __name__ == '__main__':
    main()
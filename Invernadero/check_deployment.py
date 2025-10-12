#!/usr/bin/env python3
"""
Script para verificar la configuración de despliegue
"""
import os
import sys
from pathlib import Path

def check_files():
    """Verificar archivos necesarios"""
    print("[INFO] Verificando archivos necesarios...")
    
    required_files = [
        'manage.py',
        'requirements.txt',
        'build.sh',
        'invernadero/settings.py',
        'invernadero/wsgi.py',
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"[ERROR] Archivos faltantes: {missing_files}")
        return False
    else:
        print("[OK] Todos los archivos necesarios están presentes")
        return True

def check_static_files():
    """Verificar configuración de archivos estáticos"""
    print("[INFO] Verificando archivos estáticos...")
    
    static_dirs = [
        'static',
        'users/static',
        'Windows/static',
    ]
    
    found_static = []
    for dir_path in static_dirs:
        if Path(dir_path).exists():
            found_static.append(dir_path)
    
    if found_static:
        print(f"[OK] Directorios estáticos encontrados: {found_static}")
        return True
    else:
        print("[WARN] No se encontraron directorios estáticos")
        return False

def check_settings():
    """Verificar configuración de settings.py"""
    print("[INFO] Verificando configuración de Django...")
    
    try:
        with open('invernadero/settings.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        checks = {
            'STATIC_ROOT': 'STATIC_ROOT' in content,
            'STATICFILES_DIRS': 'STATICFILES_DIRS' in content,
            'WhiteNoise': 'whitenoise' in content.lower(),
            'ALLOWED_HOSTS': 'floracore.onrender.com' in content,
            'dj_database_url': 'dj_database_url' in content,
        }
        
        for check, passed in checks.items():
            status = "[OK]" if passed else "[ERROR]"
            print(f"  {status} {check}")
        
        return all(checks.values())
        
    except Exception as e:
        print(f"[ERROR] Error leyendo settings.py: {e}")
        return False

def check_requirements():
    """Verificar requirements.txt"""
    print("[INFO] Verificando requirements.txt...")
    
    try:
        with open('requirements.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_packages = [
            'Django',
            'gunicorn',
            'whitenoise',
            'dj-database-url',
        ]
        
        missing_packages = []
        for package in required_packages:
            if package.lower() not in content.lower():
                missing_packages.append(package)
        
        if missing_packages:
            print(f"[ERROR] Paquetes faltantes: {missing_packages}")
            return False
        else:
            print("[OK] Todos los paquetes necesarios están presentes")
            return True
            
    except Exception as e:
        print(f"[ERROR] Error leyendo requirements.txt: {e}")
        return False

def main():
    """Función principal"""
    print("[INFO] Verificando configuración de despliegue para Render...\n")
    
    checks = [
        check_files(),
        check_static_files(),
        check_settings(),
        check_requirements(),
    ]
    
    if all(checks):
        print("\n[SUCCESS] Configuración lista para despliegue!")
        print("\n[INFO] Pasos para desplegar en Render:")
        print("1. Hacer commit y push de todos los cambios")
        print("2. En Render, crear nuevo Web Service")
        print("3. Conectar repositorio de GitHub")
        print("4. Configurar:")
        print("   - Build Command: ./build.sh")
        print("   - Start Command: gunicorn invernadero.wsgi:application")
        print("   - Environment: Python 3")
        print("5. Agregar variables de entorno:")
        print("   - DEBUG=False")
        print("   - DJANGO_SETTINGS_MODULE=invernadero.settings")
    else:
        print("\n[ERROR] Hay problemas que necesitan ser solucionados antes del despliegue")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
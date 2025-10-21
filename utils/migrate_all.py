#!/usr/bin/env python
"""
Script para aplicar todas las migraciones automáticamente
Uso: python migrate_all.py
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def main():
    """Ejecuta las migraciones automáticamente"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'invernadero.settings')
    
    try:
        django.setup()
        
        print("🔄 Aplicando migraciones...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        print("✅ Migraciones aplicadas exitosamente!")
        
        # Verificar estado
        print("\n📊 Estado de migraciones:")
        execute_from_command_line(['manage.py', 'showmigrations'])
        
    except Exception as e:
        print(f"❌ Error al aplicar migraciones: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
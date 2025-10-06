"""
Utilidades de mantenimiento de base de datos para FloraCore
"""

import os
import sys
import django
from django.core.management import call_command
from django.db import connection

def check_migrations():
    """Verifica si hay migraciones pendientes"""
    try:
        from django.core.management.commands.migrate import Command
        from django.db.migrations.executor import MigrationExecutor
        
        executor = MigrationExecutor(connection)
        plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
        
        if plan:
            print(f"⚠️  Hay {len(plan)} migraciones pendientes")
            return False
        else:
            print("✅ Todas las migraciones están aplicadas")
            return True
            
    except Exception as e:
        print(f"❌ Error verificando migraciones: {e}")
        return False

def apply_migrations():
    """Aplica todas las migraciones pendientes"""
    try:
        print("🔄 Aplicando migraciones...")
        call_command('migrate', verbosity=1)
        print("✅ Migraciones aplicadas exitosamente")
        return True
    except Exception as e:
        print(f"❌ Error aplicando migraciones: {e}")
        return False

def reset_migrations():
    """Resetea todas las migraciones (CUIDADO: Borra datos)"""
    response = input("⚠️  ADVERTENCIA: Esto borrará todos los datos. ¿Continuar? (yes/no): ")
    if response.lower() != 'yes':
        print("❌ Operación cancelada")
        return False
        
    try:
        print("🗑️  Eliminando base de datos...")
        if os.path.exists('db.sqlite3'):
            os.remove('db.sqlite3')
            
        print("🔄 Aplicando migraciones desde cero...")
        call_command('migrate', verbosity=1)
        
        print("✅ Base de datos reseteada exitosamente")
        return True
    except Exception as e:
        print(f"❌ Error reseteando migraciones: {e}")
        return False

def main():
    """Función principal"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'invernadero.settings')
    django.setup()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'check':
            check_migrations()
        elif command == 'apply':
            apply_migrations()
        elif command == 'reset':
            reset_migrations()
        else:
            print("Comandos disponibles: check, apply, reset")
    else:
        print("🔍 Verificando estado de migraciones...")
        if not check_migrations():
            print("🔧 Aplicando migraciones automáticamente...")
            apply_migrations()

if __name__ == '__main__':
    main()
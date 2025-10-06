#!/bin/bash

# Script para configurar la base de datos completamente
# Uso: ./setup_db.sh

echo "🚀 Configurando base de datos FloraCore..."

# Aplicar migraciones
echo "📦 Aplicando migraciones..."
python manage.py migrate

# Crear superusuario si no existe
echo "👤 Verificando superusuario..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin', 'admin@floracore.com', 'admin123')
    print('✅ Superusuario creado: admin/admin123')
else:
    print('ℹ️  Superusuario ya existe')
"

# Verificar estado
echo "📊 Estado final de migraciones:"
python manage.py showmigrations

echo "✅ Base de datos configurada correctamente!"
echo "🌐 Puedes iniciar el servidor con: python manage.py runserver"
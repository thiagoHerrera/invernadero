#!/usr/bin/env bash
# Build script para Render

set -o errexit

echo "Instalando dependencias..."
pip install -r requirements.txt

echo "Configurando base de datos..."
python manage.py setup_db

echo "Recopilando archivos estáticos..."
python manage.py collectstatic --noinput --clear

echo "Build completado exitosamente"
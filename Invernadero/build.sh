#!/usr/bin/env bash
# Build script para Render

set -o errexit

echo "Instalando dependencias..."
pip install -r requirements.txt

echo "Inicializando base de datos..."
python init_db.py

echo "Recopilando archivos estáticos..."
python manage.py collectstatic --noinput --clear

echo "Build completado exitosamente"
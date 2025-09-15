#!/bin/bash
set -e

# Simple start script for Render
echo "Starting Django app..."

# Install dependencies if not already installed
pip install -r requirements.txt

# Set environment
export DJANGO_ENV=production
export DEBUG=False

# Navigate to Django project
cd Invernadero

# Run migrations
python3 manage.py migrate

# Collect static files
python3 manage.py collectstatic --noinput --clear

# Start server
echo "Starting Gunicorn..."
exec gunicorn invernadero.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 30
#!/bin/bash

# Manual deployment script for Render
# Use this if render.yaml is not working

echo "=== Manual Render Deployment ==="
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Setting up environment..."
export DJANGO_ENV=production
export DEBUG=False
# Add other environment variables as needed

echo "Running migrations..."
cd Invernadero
python3 manage.py migrate

echo "Collecting static files..."
python3 manage.py collectstatic --noinput --clear

echo "Starting server..."
exec gunicorn invernadero.wsgi:application --bind 0.0.0.0:$PORT --log-level info
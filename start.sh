#!/bin/bash

# Exit on error
set -e

# Run migrations
python Invernadero/manage.py migrate

# Collect static files
python Invernadero/manage.py collectstatic --noinput

# Start Gunicorn server
gunicorn invernadero.wsgi:application --bind 0.0.0.0:$PORT
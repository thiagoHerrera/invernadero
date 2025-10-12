"""
WSGI config for invernadero project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'invernadero.settings')

# Ejecutar migraciones al iniciar
try:
    execute_from_command_line(['manage.py', 'setup_db'])
except:
    pass

application = get_wsgi_application()

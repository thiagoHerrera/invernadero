"""
Django settings for invernadero project.

This file imports settings based on the environment.
"""

import os

# Determine which settings to use
ENVIRONMENT = os.getenv('DJANGO_ENV', 'development')

if ENVIRONMENT == 'production':
    from .settings.production import *
elif ENVIRONMENT == 'development':
    from .settings.development import *
else:
    from .settings.development import *

"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/

IMPORTANTE:
- Este archivo es usado por Gunicorn en producción (Render)
- Carga las variables de entorno desde .env antes de inicializar Django
"""

import os
from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application

# Cargar variables de entorno desde .env ANTES de inicializar Django
# Esto es CRÍTICO para que Gunicorn lea las variables en producción
load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()

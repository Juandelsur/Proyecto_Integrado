"""
Django settings for SCA Hospital Backend.

Configuración optimizada para producción (Render + NeonTech) y desarrollo local.
Usa variables de entorno para credenciales sensibles.

IMPORTANTE:
- En desarrollo: Las variables se cargan desde .env (python-dotenv)
- En producción: Las variables se configuran en el panel de Render
- La base de datos usa SSL en producción (NeonTech)
"""

import os
from pathlib import Path
from datetime import timedelta
import dj_database_url

# ==============================================================================
# BASE DIRECTORY
# ==============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent

# NOTA: load_dotenv() se ejecuta en manage.py y wsgi.py
# No es necesario ejecutarlo aquí para evitar duplicación

# ==============================================================================
# SECURITY SETTINGS
# ==============================================================================

# SECURITY WARNING: keep the secret key used in production secret!
# En producción, SIEMPRE configura SECRET_KEY en las variables de entorno de Render
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default-key-CHANGE-IN-PRODUCTION')

# SECURITY WARNING: don't run with debug turned on in production!
# Por defecto es False (seguro). Solo True si explícitamente se configura DEBUG=True
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Hosts permitidos (Render, localhost, etc.)
# En producción: tu-app.onrender.com,tu-dominio.com
# En desarrollo: localhost,127.0.0.1
#ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '192.168.1.13',  # IP local para pruebas en red
]

# CSRF Trusted Origins (CRÍTICO para Django 4+ con HTTPS en Render)
# En producción: https://tu-app.onrender.com,https://tu-dominio.com
# En desarrollo: http://localhost
CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', 'http://localhost').split(',')


# ==============================================================================
# APPLICATION DEFINITION
# ==============================================================================

INSTALLED_APPS = [
    # Django Core Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party Apps
    'corsheaders',              # CORS headers
    'rest_framework',           # Django REST Framework
    'rest_framework_simplejwt', # JWT Authentication
    'drf_spectacular',          # API Documentation (Swagger/OpenAPI)
    'django_filters',           # Filtros para DRF

    # Local Apps
    'core',  # App principal con modelos, serializers, views, admin
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # DEBE estar PRIMERO
    'whitenoise.middleware.WhiteNoiseMiddleware',     # SEGUNDO (archivos estáticos)
    'corsheaders.middleware.CorsMiddleware',          # TERCERO (CORS)
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'core.middleware.CurrentRequestMiddleware',      # Middleware personalizado para auditoría
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# ==============================================================================
# DATABASE CONFIGURATION
# ==============================================================================
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# Configuración dinámica para Render + NeonTech (PostgreSQL con SSL)
# Si DATABASE_URL existe (producción), usa dj-database-url con SSL
# Si no existe (desarrollo local), usa configuración manual
if os.environ.get('DATABASE_URL'):
    # PRODUCCIÓN: NeonTech PostgreSQL con SSL
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,           # Pool de conexiones (10 minutos)
            conn_health_checks=True,    # Verificar salud de conexiones
            ssl_require=True            # SSL REQUERIDO para NeonTech
        )
    }
else:
    # DESARROLLO LOCAL: PostgreSQL sin SSL (Docker o local)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME', 'sca_hospital'),
            'USER': os.environ.get('DB_USER', 'sca_user'),
            'PASSWORD': os.environ.get('DB_PASSWORD', 'sca_password'),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '5432'),
        }
    }

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ==============================================================================
# INTERNATIONALIZATION
# ==============================================================================
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'America/Santiago'  # Ajustar según tu zona horaria

USE_I18N = True

USE_TZ = True


# ==============================================================================
# STATIC FILES (Whitenoise para producción)
# ==============================================================================
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Whitenoise: Compresión y caché de archivos estáticos en producción
# Sirve archivos estáticos sin necesidad de Nginx o servidor adicional
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ==============================================================================
# DEFAULT PRIMARY KEY FIELD TYPE
# ==============================================================================
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==============================================================================
# CUSTOM USER MODEL
# ==============================================================================
# https://docs.djangoproject.com/en/5.2/topics/auth/customizing/#substituting-a-custom-user-model

AUTH_USER_MODEL = 'core.Usuario'

# ==============================================================================
# CORS CONFIGURATION
# ==============================================================================

# Para desarrollo: permitir todos los orígenes (True)
# Para producción: especificar orígenes permitidos (False)
#CORS_ALLOW_ALL_ORIGINS = os.environ.get('CORS_ALLOW_ALL', 'True') == 'True'
CORS_ALLOW_ALL_ORIGINS = True

# Orígenes permitidos en producción (separados por comas en variable de entorno)
# Ejemplo: https://tu-frontend.vercel.app,https://tu-dominio.com


#CORS_ALLOWED_ORIGINS_STR = os.environ.get('CORS_ALLOWED_ORIGINS', 'http://localhost:5173,http://127.0.0.1:5173')
#CORS_ALLOWED_ORIGINS = [origin.strip() for origin in CORS_ALLOWED_ORIGINS_STR.split(',') if origin.strip()]

# Permitir cookies y credenciales en requests CORS
CORS_ALLOW_CREDENTIALS = True

# ==============================================================================
# REST FRAMEWORK CONFIGURATION
# ==============================================================================

REST_FRAMEWORK = {
    # Schema para documentación automática (Swagger/OpenAPI)
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

    # Autenticación: JWT (primario) + Session (para browsable API)
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        #'rest_framework.authentication.SessionAuthentication',
    ],

    # Permisos: Autenticado para escribir, público para leer
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],

    # Paginación: 20 items por página
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,

    # Filtros: Búsqueda y ordenamiento
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

# ==============================================================================
# JWT CONFIGURATION (Simple JWT)
# ==============================================================================

# Configuración de tokens JWT para autenticación
SIMPLE_JWT = {
    # Tiempo de vida de tokens (configurable desde variables de entorno)
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=int(os.environ.get('JWT_ACCESS_TOKEN_LIFETIME', '60'))),
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=int(os.environ.get('JWT_REFRESH_TOKEN_LIFETIME', '1440'))),

    # Rotación de tokens para mayor seguridad
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,

    # Algoritmo de firma
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    # Headers y claims
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    # Clases de tokens
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}

# ==============================================================================
# DRF-SPECTACULAR (API DOCUMENTATION) CONFIGURATION
# ==============================================================================

# Configuración de Swagger/OpenAPI para documentación automática de la API
SPECTACULAR_SETTINGS = {
    'TITLE': 'API SCA Hospital',
    'DESCRIPTION': 'Sistema de Control de Activos - API REST para gestión hospitalaria',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': r'/api/',

    # Configuración de Swagger UI
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,              # Links profundos en la UI
        'persistAuthorization': True,     # Mantener token JWT entre recargas
        'displayOperationId': True,       # Mostrar IDs de operaciones
    },

    # Seguridad: JWT Bearer Token
    'SECURITY': [
        {
            'Bearer': {
                'type': 'http',
                'scheme': 'bearer',
                'bearerFormat': 'JWT',
            }
        }
    ],
}
#!/usr/bin/env python
"""
Script de diagnóstico para errores 403 Forbidden en producción.

Uso:
    python diagnostico_403.py

Este script verifica:
1. Configuración de CORS y CSRF
2. Configuración de JWT
3. Estado de usuarios
4. Permisos de ViewSets
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings
from core.models import Usuario, Rol
from datetime import timedelta


def print_header(title):
    """Imprime un encabezado formateado."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_ok(message):
    """Imprime un mensaje de éxito."""
    print(f"✅ {message}")


def print_warning(message):
    """Imprime un mensaje de advertencia."""
    print(f"⚠️  {message}")


def print_error(message):
    """Imprime un mensaje de error."""
    print(f"❌ {message}")


def check_cors_csrf():
    """Verifica la configuración de CORS y CSRF."""
    print_header("1. CONFIGURACIÓN DE CORS Y CSRF")
    
    # CORS_ALLOWED_ORIGINS
    cors_origins = getattr(settings, 'CORS_ALLOWED_ORIGINS', [])
    print(f"\nCORS_ALLOWED_ORIGINS:")
    if cors_origins:
        for origin in cors_origins:
            if origin.endswith('/'):
                print_error(f"  {origin} (tiene slash al final - INCORRECTO)")
            elif origin.startswith('https://'):
                print_ok(f"  {origin}")
            else:
                print_warning(f"  {origin} (no usa HTTPS)")
    else:
        print_warning("  No configurado (usando CORS_ALLOW_ALL)")
    
    # CORS_ALLOW_ALL
    cors_allow_all = getattr(settings, 'CORS_ALLOW_ALL_ORIGINS', False)
    print(f"\nCORS_ALLOW_ALL_ORIGINS: {cors_allow_all}")
    if cors_allow_all and not settings.DEBUG:
        print_error("  CORS_ALLOW_ALL está en True en producción (INSEGURO)")
    elif cors_allow_all and settings.DEBUG:
        print_ok("  Permitido en desarrollo")
    else:
        print_ok("  Desactivado correctamente en producción")
    
    # CSRF_TRUSTED_ORIGINS
    csrf_origins = getattr(settings, 'CSRF_TRUSTED_ORIGINS', [])
    print(f"\nCSRF_TRUSTED_ORIGINS:")
    if csrf_origins:
        for origin in csrf_origins:
            if origin.startswith('https://'):
                print_ok(f"  {origin}")
            elif origin.startswith('http://') and settings.DEBUG:
                print_warning(f"  {origin} (HTTP solo válido en desarrollo)")
            else:
                print_error(f"  {origin} (debe usar HTTPS en producción)")
    else:
        print_error("  No configurado (CRÍTICO en producción con HTTPS)")
    
    # CORS_ALLOW_CREDENTIALS
    cors_credentials = getattr(settings, 'CORS_ALLOW_CREDENTIALS', False)
    print(f"\nCORS_ALLOW_CREDENTIALS: {cors_credentials}")
    if cors_credentials:
        print_ok("  Permite enviar credenciales (cookies, headers)")
    else:
        print_warning("  No permite credenciales (puede causar problemas con JWT)")


def check_jwt():
    """Verifica la configuración de JWT."""
    print_header("2. CONFIGURACIÓN DE JWT")
    
    simple_jwt = getattr(settings, 'SIMPLE_JWT', {})
    
    # Access Token Lifetime
    access_lifetime = simple_jwt.get('ACCESS_TOKEN_LIFETIME', timedelta(minutes=5))
    print(f"\nACCESS_TOKEN_LIFETIME: {access_lifetime}")
    if access_lifetime.total_seconds() < 300:  # 5 minutos
        print_warning(f"  Muy corto ({access_lifetime.total_seconds() / 60:.0f} minutos)")
    elif access_lifetime.total_seconds() > 86400:  # 24 horas
        print_warning(f"  Muy largo ({access_lifetime.total_seconds() / 3600:.0f} horas)")
    else:
        print_ok(f"  Duración adecuada ({access_lifetime.total_seconds() / 60:.0f} minutos)")
    
    # Refresh Token Lifetime
    refresh_lifetime = simple_jwt.get('REFRESH_TOKEN_LIFETIME', timedelta(days=1))
    print(f"\nREFRESH_TOKEN_LIFETIME: {refresh_lifetime}")
    print_ok(f"  {refresh_lifetime.total_seconds() / 3600:.0f} horas")
    
    # Rotate Refresh Tokens
    rotate = simple_jwt.get('ROTATE_REFRESH_TOKENS', False)
    print(f"\nROTATE_REFRESH_TOKENS: {rotate}")
    if rotate:
        print_ok("  Tokens se rotan automáticamente (más seguro)")
    else:
        print_warning("  Tokens no se rotan (menos seguro)")


def check_users():
    """Verifica el estado de los usuarios."""
    print_header("3. ESTADO DE USUARIOS")
    
    total_users = Usuario.objects.count()
    active_users = Usuario.objects.filter(is_active=True).count()
    inactive_users = total_users - active_users
    
    print(f"\nTotal de usuarios: {total_users}")
    print(f"Usuarios activos: {active_users}")
    print(f"Usuarios inactivos: {inactive_users}")
    
    # Usuarios sin rol
    users_without_role = Usuario.objects.filter(rol__isnull=True).count()
    if users_without_role > 0:
        print_error(f"  {users_without_role} usuarios sin rol asignado")
        print("\n  Usuarios sin rol:")
        for user in Usuario.objects.filter(rol__isnull=True):
            print(f"    - {user.username} ({user.nombre_completo})")
    else:
        print_ok("  Todos los usuarios tienen rol asignado")
    
    # Usuarios inactivos
    if inactive_users > 0:
        print_warning(f"  {inactive_users} usuarios inactivos")
        print("\n  Usuarios inactivos:")
        for user in Usuario.objects.filter(is_active=False):
            rol_nombre = user.rol.nombre_rol if user.rol else "Sin rol"
            print(f"    - {user.username} ({user.nombre_completo}) - Rol: {rol_nombre}")
    
    # Distribución por rol
    print("\n  Distribución por rol:")
    for rol in Rol.objects.all():
        count = Usuario.objects.filter(rol=rol, is_active=True).count()
        print(f"    - {rol.nombre_rol}: {count} usuarios activos")


def check_permissions():
    """Verifica la configuración de permisos de DRF."""
    print_header("4. CONFIGURACIÓN DE PERMISOS DRF")
    
    rest_framework = getattr(settings, 'REST_FRAMEWORK', {})
    
    # Default Permission Classes
    default_perms = rest_framework.get('DEFAULT_PERMISSION_CLASSES', [])
    print(f"\nDEFAULT_PERMISSION_CLASSES:")
    for perm in default_perms:
        print(f"  - {perm}")
        if 'AllowAny' in perm:
            print_error("    Permite acceso sin autenticación (INSEGURO)")
        elif 'IsAuthenticatedOrReadOnly' in perm:
            print_warning("    Permite lectura sin autenticación")
        elif 'IsAuthenticated' in perm:
            print_ok("    Requiere autenticación")
    
    # Default Authentication Classes
    default_auth = rest_framework.get('DEFAULT_AUTHENTICATION_CLASSES', [])
    print(f"\nDEFAULT_AUTHENTICATION_CLASSES:")
    for auth in default_auth:
        print(f"  - {auth}")
        if 'JWT' in auth:
            print_ok("    JWT configurado")


def main():
    """Función principal."""
    print("\n" + "=" * 80)
    print("  DIAGNÓSTICO DE CONFIGURACIÓN - ERROR 403 FORBIDDEN")
    print("  SCA Hospital - Backend Django REST Framework")
    print("=" * 80)
    
    print(f"\nEntorno: {'DESARROLLO' if settings.DEBUG else 'PRODUCCIÓN'}")
    print(f"DEBUG: {settings.DEBUG}")
    print(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    
    check_cors_csrf()
    check_jwt()
    check_users()
    check_permissions()
    
    print_header("RESUMEN")
    print("\n✅ Si todos los checks están en verde, la configuración es correcta.")
    print("⚠️  Los warnings indican configuraciones que podrían mejorarse.")
    print("❌ Los errores indican problemas críticos que deben corregirse.\n")
    print("Si el problema persiste, revisa los logs de Render y comparte el output")
    print("de este script para un diagnóstico más detallado.\n")


if __name__ == '__main__':
    main()


#!/usr/bin/env python
"""
Script de prueba para el endpoint GET /api/usuarios/me/

Este script verifica que el endpoint crítico para el frontend funcione correctamente.

Pruebas:
1. Login con diferentes usuarios (admin, tecnico1, jefe1)
2. Obtener información del usuario autenticado con el token
3. Verificar que se retorne el rol correctamente
4. Verificar que el password NO se retorne

Uso:
    python test_me_endpoint.py
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

import requests
from colorama import Fore, Style, init

# Inicializar colorama
init(autoreset=True)

# Configuración
BASE_URL = "http://localhost:8000"
LOGIN_URL = f"{BASE_URL}/api/token/"
ME_URL = f"{BASE_URL}/api/usuarios/me/"

# Usuarios de prueba
USUARIOS = [
    {"username": "admin", "password": "admin123", "rol_esperado": "Administrador"},
    {"username": "tecnico1", "password": "tecnico1123", "rol_esperado": "Técnico"},
    {"username": "jefe1", "password": "jefe1123", "rol_esperado": "Jefe de Departamento"},
]


def print_header(text):
    """Imprime un encabezado destacado."""
    print(f"\n{Fore.CYAN}{'=' * 80}")
    print(f"{Fore.CYAN}{text.center(80)}")
    print(f"{Fore.CYAN}{'=' * 80}{Style.RESET_ALL}\n")


def print_success(text):
    """Imprime un mensaje de éxito."""
    print(f"{Fore.GREEN}✅ {text}{Style.RESET_ALL}")


def print_error(text):
    """Imprime un mensaje de error."""
    print(f"{Fore.RED}❌ {text}{Style.RESET_ALL}")


def print_info(text):
    """Imprime un mensaje informativo."""
    print(f"{Fore.YELLOW}ℹ️  {text}{Style.RESET_ALL}")


def test_login(username, password):
    """
    Prueba el login y retorna el token de acceso.
    
    Args:
        username: Nombre de usuario
        password: Contraseña
    
    Returns:
        str: Token de acceso o None si falla
    """
    try:
        response = requests.post(LOGIN_URL, json={
            "username": username,
            "password": password
        })
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('access')
            print_success(f"Login exitoso para '{username}'")
            return token
        else:
            print_error(f"Login fallido para '{username}': {response.status_code}")
            return None
    except Exception as e:
        print_error(f"Error en login: {str(e)}")
        return None


def test_me_endpoint(token, username, rol_esperado):
    """
    Prueba el endpoint /api/usuarios/me/ con el token.
    
    Args:
        token: Token JWT de acceso
        username: Nombre de usuario (para verificación)
        rol_esperado: Rol esperado del usuario
    
    Returns:
        bool: True si la prueba es exitosa, False en caso contrario
    """
    try:
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        response = requests.get(ME_URL, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            
            print_info(f"Respuesta del endpoint /api/usuarios/me/:")
            print(f"  - ID: {data.get('id')}")
            print(f"  - Username: {data.get('username')}")
            print(f"  - Email: {data.get('email')}")
            print(f"  - Nombre Completo: {data.get('nombre_completo')}")
            print(f"  - Rol: {data.get('rol', {}).get('nombre_rol')}")
            print(f"  - Is Active: {data.get('is_active')}")
            print(f"  - Is Staff: {data.get('is_staff')}")
            
            # Verificaciones
            errores = []
            
            # 1. Verificar que el username coincida
            if data.get('username') != username:
                errores.append(f"Username no coincide: esperado '{username}', recibido '{data.get('username')}'")
            
            # 2. Verificar que el rol sea correcto
            rol_recibido = data.get('rol', {}).get('nombre_rol')
            if rol_recibido != rol_esperado:
                errores.append(f"Rol no coincide: esperado '{rol_esperado}', recibido '{rol_recibido}'")
            
            # 3. Verificar que el password NO esté en la respuesta
            if 'password' in data:
                errores.append("¡CRÍTICO! El password está en la respuesta (debe ser write_only)")
            
            # 4. Verificar que el rol sea un objeto completo
            if not isinstance(data.get('rol'), dict):
                errores.append("El rol no es un objeto completo")
            
            if errores:
                for error in errores:
                    print_error(error)
                return False
            else:
                print_success(f"Todas las verificaciones pasaron para '{username}'")
                return True
        else:
            print_error(f"Error en endpoint /me/: {response.status_code}")
            print(f"  Respuesta: {response.text}")
            return False
    except Exception as e:
        print_error(f"Error en prueba: {str(e)}")
        return False


def main():
    """Función principal."""
    print_header("PRUEBA DEL ENDPOINT GET /api/usuarios/me/")
    
    print_info("Este script prueba el endpoint crítico para el frontend")
    print_info(f"Base URL: {BASE_URL}")
    print_info(f"Endpoint: {ME_URL}\n")
    
    resultados = []
    
    for usuario in USUARIOS:
        username = usuario['username']
        password = usuario['password']
        rol_esperado = usuario['rol_esperado']
        
        print_header(f"PROBANDO USUARIO: {username}")
        
        # 1. Login
        token = test_login(username, password)
        if not token:
            print_error(f"No se pudo obtener token para '{username}'\n")
            resultados.append(False)
            continue
        
        # 2. Probar endpoint /me/
        exito = test_me_endpoint(token, username, rol_esperado)
        resultados.append(exito)
        
        print()
    
    # Resumen final
    print_header("RESUMEN DE PRUEBAS")
    
    exitosas = sum(resultados)
    total = len(resultados)
    
    print(f"Total de pruebas: {total}")
    print(f"Exitosas: {exitosas}")
    print(f"Fallidas: {total - exitosas}\n")
    
    if exitosas == total:
        print_success("¡TODAS LAS PRUEBAS PASARON! ✅")
        print_info("El endpoint /api/usuarios/me/ está funcionando correctamente")
        print_info("El frontend puede usar este endpoint para obtener el rol del usuario")
        return 0
    else:
        print_error("ALGUNAS PRUEBAS FALLARON ❌")
        print_info("Revisa los errores anteriores")
        return 1


if __name__ == "__main__":
    sys.exit(main())


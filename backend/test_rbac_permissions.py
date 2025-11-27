#!/usr/bin/env python
"""
Script de prueba para validar el sistema RBAC (Control de Acceso Basado en Roles).

Este script prueba los permisos de cada rol (Administrador, Técnico, Jefe) en todos
los endpoints de la API para verificar que el sistema de seguridad funciona correctamente.

Uso:
    python test_rbac_permissions.py

Requisitos:
    - Servidor Django corriendo en http://localhost:8000
    - Base de datos poblada con seed_hospital.py
    - Usuarios de prueba: admin, tecnico1, jefe1
"""

import requests
import json
from typing import Dict, Tuple

# Configuración
BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api"

# Credenciales de prueba (creadas por seed_hospital.py)
USUARIOS = {
    "admin": {"username": "admin", "password": "admin123"},
    "tecnico": {"username": "tecnico1", "password": "tecnico1123"},
    "jefe": {"username": "jefe1", "password": "jefe1123"}
}

# Colores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def obtener_token(username: str, password: str) -> str:
    """Obtiene un token JWT para el usuario."""
    response = requests.post(
        f"{API_URL}/token/",
        json={"username": username, "password": password}
    )
    if response.status_code == 200:
        return response.json()["access"]
    else:
        raise Exception(f"Error al obtener token: {response.status_code}")


def probar_endpoint(token: str, method: str, endpoint: str, data: Dict = None) -> Tuple[int, str]:
    """
    Prueba un endpoint con un token específico.
    
    Returns:
        Tuple[int, str]: (status_code, descripción del resultado)
    """
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{API_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method == "PUT":
            response = requests.put(url, headers=headers, json=data)
        elif method == "PATCH":
            response = requests.patch(url, headers=headers, json=data)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            return 0, "Método no soportado"
        
        return response.status_code, response.text[:100]
    except Exception as e:
        return 0, str(e)


def print_resultado(rol: str, operacion: str, endpoint: str, esperado: bool, obtenido: int):
    """Imprime el resultado de una prueba con formato."""
    exito = (esperado and obtenido in [200, 201]) or (not esperado and obtenido == 403)
    
    simbolo = f"{Colors.GREEN}✓{Colors.RESET}" if exito else f"{Colors.RED}✗{Colors.RESET}"
    esperado_str = f"{Colors.GREEN}PERMITIDO{Colors.RESET}" if esperado else f"{Colors.RED}DENEGADO{Colors.RESET}"
    obtenido_str = f"{Colors.GREEN}{obtenido}{Colors.RESET}" if exito else f"{Colors.RED}{obtenido}{Colors.RESET}"
    
    print(f"  {simbolo} {rol:12} | {operacion:6} | {endpoint:30} | Esperado: {esperado_str:20} | Obtenido: {obtenido_str}")


def main():
    """Función principal que ejecuta todas las pruebas."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*100}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}PRUEBAS DE CONTROL DE ACCESO BASADO EN ROLES (RBAC){Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*100}{Colors.RESET}\n")
    
    # Obtener tokens
    print(f"{Colors.YELLOW}Obteniendo tokens JWT...{Colors.RESET}")
    try:
        tokens = {
            "admin": obtener_token(**USUARIOS["admin"]),
            "tecnico": obtener_token(**USUARIOS["tecnico"]),
            "jefe": obtener_token(**USUARIOS["jefe"])
        }
        print(f"{Colors.GREEN}✓ Tokens obtenidos exitosamente{Colors.RESET}\n")
    except Exception as e:
        print(f"{Colors.RED}✗ Error al obtener tokens: {e}{Colors.RESET}")
        print(f"{Colors.YELLOW}Asegúrate de que el servidor esté corriendo y los usuarios existan.{Colors.RESET}")
        return
    
    # Definir pruebas
    pruebas = [
        # Formato: (endpoint, método, admin_permitido, tecnico_permitido, jefe_permitido)
        
        # MAESTROS (Solo Admin)
        ("/roles/", "GET", True, False, False),
        ("/departamentos/", "GET", True, False, False),
        ("/tipos-equipo/", "GET", True, False, False),
        ("/estados-activo/", "GET", True, False, False),
        ("/ubicaciones/", "GET", True, False, False),
        ("/usuarios/", "GET", True, False, False),
        
        # ACTIVOS (Admin: todo, Técnico: GET/POST/PUT/PATCH, Jefe: GET)
        ("/activos/", "GET", True, True, True),
        
        # HISTORIAL (Admin: todo, Técnico: GET, Jefe: GET)
        ("/historial-movimientos/", "GET", True, True, True),
        
        # AUDITORÍA (Admin: GET, Jefe: GET, Técnico: NO)
        ("/auditoria-logs/", "GET", True, False, True),
    ]
    
    # Ejecutar pruebas
    print(f"{Colors.BOLD}RESULTADOS DE PRUEBAS:{Colors.RESET}\n")
    
    for endpoint, metodo, admin_ok, tecnico_ok, jefe_ok in pruebas:
        # Probar con Admin
        status_admin, _ = probar_endpoint(tokens["admin"], metodo, endpoint)
        print_resultado("Admin", metodo, endpoint, admin_ok, status_admin)
        
        # Probar con Técnico
        status_tecnico, _ = probar_endpoint(tokens["tecnico"], metodo, endpoint)
        print_resultado("Técnico", metodo, endpoint, tecnico_ok, status_tecnico)
        
        # Probar con Jefe
        status_jefe, _ = probar_endpoint(tokens["jefe"], metodo, endpoint)
        print_resultado("Jefe", metodo, endpoint, jefe_ok, status_jefe)
        
        print()  # Línea en blanco entre grupos
    
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*100}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.GREEN}PRUEBAS COMPLETADAS{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*100}{Colors.RESET}\n")


if __name__ == "__main__":
    main()


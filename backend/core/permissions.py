"""
Sistema de Control de Acceso Basado en Roles (RBAC) para el SCA Hospital.

Este módulo define permisos personalizados de Django REST Framework que implementan
la lógica de autorización según los roles definidos en la base de datos:
- Administrador: Acceso total a todos los recursos
- Técnico: Operaciones CRUD excepto DELETE en activos, sin acceso a maestros
- Jefe de Departamento: Solo lectura en activos y auditoría

Arquitectura de Seguridad:
- Todos los permisos verifican autenticación primero
- Se valida la existencia del rol antes de evaluar permisos
- Principio de menor privilegio: se deniega por defecto
- Separación de responsabilidades por tipo de operación
"""

from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Permiso exclusivo para usuarios con rol 'Administrador'.
    
    Casos de uso:
    - Gestión de usuarios (crear, editar, eliminar)
    - Gestión de maestros (departamentos, ubicaciones, tipos de equipo, estados)
    - Acceso completo a todos los recursos del sistema
    
    Retorna:
        True: Si el usuario autenticado tiene rol 'Administrador'
        False: En cualquier otro caso
    """
    
    def has_permission(self, request, view):
        # Verificar autenticación
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Verificar existencia de rol
        if not hasattr(request.user, 'rol') or not request.user.rol:
            return False
        
        # Validar rol de Administrador
        return request.user.rol.nombre_rol == 'Administrador'
    
    message = 'Solo los Administradores tienen acceso a este recurso.'


class IsJefeOrAdminReadOnly(permissions.BasePermission):
    """
    Permiso para Jefes de Departamento (solo lectura) y Administradores (acceso total).
    
    Reglas de negocio:
    - Administrador: Acceso completo (GET, POST, PUT, PATCH, DELETE)
    - Jefe de Departamento: Solo métodos seguros (GET, HEAD, OPTIONS)
    - Otros roles: Acceso denegado
    
    Casos de uso:
    - Jefes pueden consultar activos para supervisión
    - Jefes pueden ver auditoría y historial para control
    - Jefes NO pueden modificar datos (principio de segregación de funciones)
    
    Retorna:
        True: Si es Admin (cualquier método) o Jefe (solo lectura)
        False: En cualquier otro caso
    """
    
    def has_permission(self, request, view):
        # Verificar autenticación
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Verificar existencia de rol
        if not hasattr(request.user, 'rol') or not request.user.rol:
            return False
        
        rol_nombre = request.user.rol.nombre_rol
        
        # Administrador: acceso total
        if rol_nombre == 'Administrador':
            return True
        
        # Jefe de Departamento: solo lectura (métodos seguros)
        if rol_nombre == 'Jefe de Departamento':
            return request.method in permissions.SAFE_METHODS
        
        # Otros roles: denegado
        return False
    
    message = 'Solo Administradores y Jefes de Departamento (lectura) tienen acceso.'


class IsTecnicoOperativo(permissions.BasePermission):
    """
    Permiso para Técnicos (operaciones CRUD sin DELETE) y Administradores (acceso total).
    
    Reglas de negocio:
    - Administrador: Acceso completo (GET, POST, PUT, PATCH, DELETE)
    - Técnico: Lectura y escritura (GET, POST, PUT, PATCH) pero NO DELETE
    - Otros roles: Acceso denegado
    
    Casos de uso:
    - Técnicos pueden registrar nuevos activos (POST)
    - Técnicos pueden actualizar información de activos (PUT/PATCH)
    - Técnicos pueden movilizar activos entre ubicaciones (POST a acción personalizada)
    - Técnicos NO pueden eliminar activos (requiere aprobación de Admin)
    
    IMPORTANTE: Este permiso debe combinarse con CanDeleteActivo para bloquear DELETE.
    
    Retorna:
        True: Si es Admin (cualquier método) o Técnico (excepto DELETE)
        False: En cualquier otro caso
    """
    
    def has_permission(self, request, view):
        # Verificar autenticación
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Verificar existencia de rol
        if not hasattr(request.user, 'rol') or not request.user.rol:
            return False
        
        rol_nombre = request.user.rol.nombre_rol
        
        # Administrador: acceso total
        if rol_nombre == 'Administrador':
            return True
        
        # Técnico: lectura y escritura, pero NO DELETE
        if rol_nombre == 'Técnico':
            # Métodos permitidos: GET, HEAD, OPTIONS, POST, PUT, PATCH
            # Método bloqueado: DELETE
            return request.method in ['GET', 'HEAD', 'OPTIONS', 'POST', 'PUT', 'PATCH']
        
        # Otros roles: denegado
        return False
    
    message = 'Solo Administradores y Técnicos (sin DELETE) tienen acceso.'


class CanDeleteActivo(permissions.BasePermission):
    """
    Permiso específico para operaciones DELETE.
    
    Reglas de negocio:
    - Solo Administradores pueden eliminar recursos
    - Técnicos y Jefes NO pueden eliminar (control de auditoría)
    - Para métodos distintos a DELETE, este permiso no aplica (retorna True)
    
    Casos de uso:
    - Prevenir eliminación accidental de activos por técnicos
    - Mantener trazabilidad completa (solo Admin puede eliminar registros)
    - Cumplir con políticas de auditoría hospitalaria
    
    IMPORTANTE: Este permiso debe usarse en combinación con otros permisos.
    Se evalúa DESPUÉS de los permisos de rol para validar DELETE específicamente.
    
    Retorna:
        True: Si el método NO es DELETE, o si es DELETE y el usuario es Admin
        False: Si es DELETE y el usuario NO es Admin
    """
    
    def has_permission(self, request, view):
        # Si no es DELETE, permitir (otros permisos ya validaron el acceso)
        if request.method != 'DELETE':
            return True
        
        # Si es DELETE, verificar que sea Administrador
        if not request.user or not request.user.is_authenticated:
            return False
        
        if not hasattr(request.user, 'rol') or not request.user.rol:
            return False
        
        return request.user.rol.nombre_rol == 'Administrador'
    
    message = 'Solo los Administradores pueden eliminar recursos.'


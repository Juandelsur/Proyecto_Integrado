"""
Configuración de URLs para la API REST del Sistema de Control de Activos (SCA) Hospital.

Este módulo define las rutas de la API usando Django REST Framework Router.

Características:
- Router automático para ViewSets
- URLs RESTful estándar con nombres limpios (roles, activos, usuarios, logs)
- Integración con drf-spectacular para documentación OpenAPI
- Tags organizados: Maestros, Core, Trazabilidad, Auditoría

Rutas generadas automáticamente:
- /api/roles/                    (Maestros)
- /api/departamentos/            (Maestros)
- /api/tipos-equipo/             (Maestros)
- /api/estados-activo/           (Maestros)
- /api/ubicaciones/              (Core)
- /api/usuarios/                 (Core)
- /api/activos/                  (Core - CRÍTICO)
- /api/historial-movimientos/    (Trazabilidad)
- /api/auditoria-logs/           (Auditoría - SOLO LECTURA)
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    RolViewSet,
    UsuarioViewSet,
    DepartamentoViewSet,
    UbicacionViewSet,
    TipoEquipoViewSet,
    EstadoActivoViewSet,
    ActivoViewSet,
    HistorialMovimientoViewSet,
    AuditoriaLogViewSet
)

# ==============================================================================
# CONFIGURACIÓN DEL ROUTER
# ==============================================================================

# DefaultRouter genera automáticamente las rutas RESTful estándar:
# - GET /resource/ (list)
# - POST /resource/ (create)
# - GET /resource/{id}/ (retrieve)
# - PUT /resource/{id}/ (update)
# - PATCH /resource/{id}/ (partial_update)
# - DELETE /resource/{id}/ (destroy)

router = DefaultRouter()

# ==============================================================================
# REGISTRO DE VIEWSETS
# ==============================================================================

# Maestros básicos
router.register(r'roles', RolViewSet, basename='rol')
router.register(r'departamentos', DepartamentoViewSet, basename='departamento')
router.register(r'tipos-equipo', TipoEquipoViewSet, basename='tipoequipo')
router.register(r'estados-activo', EstadoActivoViewSet, basename='estadoactivo')

# Entidades con relaciones
router.register(r'ubicaciones', UbicacionViewSet, basename='ubicacion')
router.register(r'usuarios', UsuarioViewSet, basename='usuario')

# Activos (entidad central)
router.register(r'activos', ActivoViewSet, basename='activo')

# Trazabilidad y auditoría
router.register(r'historial-movimientos', HistorialMovimientoViewSet, basename='historialmovimiento')
router.register(r'auditoria-logs', AuditoriaLogViewSet, basename='auditorialog')

# ==============================================================================
# URLS
# ==============================================================================

urlpatterns = [
    path('', include(router.urls)),
]

# ==============================================================================
# RUTAS GENERADAS
# ==============================================================================
"""
El router genera automáticamente las siguientes rutas:

ROLES:
- GET    /api/roles/           - Listar todos los roles
- POST   /api/roles/           - Crear un nuevo rol
- GET    /api/roles/{id}/      - Obtener un rol específico
- PUT    /api/roles/{id}/      - Actualizar un rol completo
- PATCH  /api/roles/{id}/      - Actualizar parcialmente un rol
- DELETE /api/roles/{id}/      - Eliminar un rol

DEPARTAMENTOS:
- GET    /api/departamentos/           - Listar todos los departamentos
- POST   /api/departamentos/           - Crear un nuevo departamento
- GET    /api/departamentos/{id}/      - Obtener un departamento específico
- PUT    /api/departamentos/{id}/      - Actualizar un departamento completo
- PATCH  /api/departamentos/{id}/      - Actualizar parcialmente un departamento
- DELETE /api/departamentos/{id}/      - Eliminar un departamento

TIPOS DE EQUIPO:
- GET    /api/tipos-equipo/           - Listar todos los tipos de equipo
- POST   /api/tipos-equipo/           - Crear un nuevo tipo de equipo
- GET    /api/tipos-equipo/{id}/      - Obtener un tipo de equipo específico
- PUT    /api/tipos-equipo/{id}/      - Actualizar un tipo de equipo completo
- PATCH  /api/tipos-equipo/{id}/      - Actualizar parcialmente un tipo de equipo
- DELETE /api/tipos-equipo/{id}/      - Eliminar un tipo de equipo

ESTADOS DE ACTIVO:
- GET    /api/estados-activo/           - Listar todos los estados de activo
- POST   /api/estados-activo/           - Crear un nuevo estado de activo
- GET    /api/estados-activo/{id}/      - Obtener un estado de activo específico
- PUT    /api/estados-activo/{id}/      - Actualizar un estado de activo completo
- PATCH  /api/estados-activo/{id}/      - Actualizar parcialmente un estado de activo
- DELETE /api/estados-activo/{id}/      - Eliminar un estado de activo

UBICACIONES:
- GET    /api/ubicaciones/           - Listar todas las ubicaciones
- POST   /api/ubicaciones/           - Crear una nueva ubicación
- GET    /api/ubicaciones/{id}/      - Obtener una ubicación específica
- PUT    /api/ubicaciones/{id}/      - Actualizar una ubicación completa
- PATCH  /api/ubicaciones/{id}/      - Actualizar parcialmente una ubicación
- DELETE /api/ubicaciones/{id}/      - Eliminar una ubicación

USUARIOS:
- GET    /api/usuarios/           - Listar todos los usuarios
- POST   /api/usuarios/           - Crear un nuevo usuario
- GET    /api/usuarios/{id}/      - Obtener un usuario específico
- PUT    /api/usuarios/{id}/      - Actualizar un usuario completo
- PATCH  /api/usuarios/{id}/      - Actualizar parcialmente un usuario
- DELETE /api/usuarios/{id}/      - Eliminar un usuario

ACTIVOS (CRÍTICO):
- GET    /api/activos/           - Listar todos los activos con información completa
- POST   /api/activos/           - Crear un nuevo activo
- GET    /api/activos/{id}/      - Obtener un activo específico
- PUT    /api/activos/{id}/      - Actualizar un activo completo
- PATCH  /api/activos/{id}/      - Actualizar parcialmente un activo
- DELETE /api/activos/{id}/      - Eliminar un activo

HISTORIAL DE MOVIMIENTOS:
- GET    /api/historial-movimientos/           - Listar todos los movimientos
- POST   /api/historial-movimientos/           - Registrar un nuevo movimiento
- GET    /api/historial-movimientos/{id}/      - Obtener un movimiento específico
- PUT    /api/historial-movimientos/{id}/      - Actualizar un movimiento completo
- PATCH  /api/historial-movimientos/{id}/      - Actualizar parcialmente un movimiento
- DELETE /api/historial-movimientos/{id}/      - Eliminar un movimiento

AUDITORÍA (SOLO LECTURA):
- GET    /api/auditoria-logs/           - Listar todos los logs de auditoría
- GET    /api/auditoria-logs/{id}/      - Obtener un log específico
"""



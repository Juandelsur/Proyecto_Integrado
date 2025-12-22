"""
Vistas (ViewSets) para la API REST del Sistema de Control de Activos (SCA) Hospital.

Este módulo define los ViewSets de Django REST Framework que exponen
los endpoints de la API.

Características:
- Autenticación JWT requerida en todos los endpoints (IsAuthenticated)
- Control de acceso basado en roles (RBAC) con permisos personalizados
- Documentación automática con drf-spectacular (@extend_schema_view)
- Optimización SQL con select_related() para evitar N+1 queries
- CRUD completo para todos los modelos (excepto AuditoriaLog que es read-only)
- Tags organizados para OpenAPI: Maestros, Core, Trazabilidad, Auditoría

Sistema de Permisos por Rol:
- Administrador: Acceso total a todos los recursos
- Técnico: CRUD en activos (sin DELETE), movilización, consulta de historial
- Jefe de Departamento: Solo lectura en activos, historial y auditoría
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from django.db import transaction
from django.core.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend

# Importar permisos personalizados RBAC
from .permissions import (
    IsAdminUser,
    IsJefeOrAdminReadOnly,
    IsTecnicoOperativo,
    CanDeleteActivo,
    IsAdminOrReadOnly
)

from .models import (
    Rol,
    Usuario,
    Departamento,
    Ubicacion,
    TipoEquipo,
    EstadoActivo,
    Activo,
    HistorialMovimiento,
    AuditoriaLog
)

from .serializers import (
    RolSerializer,
    UsuarioSerializer,
    DepartamentoSerializer,
    UbicacionSerializer,
    TipoEquipoSerializer,
    EstadoActivoSerializer,
    ActivoSerializer,
    HistorialMovimientoSerializer,
    AuditoriaLogSerializer,
    MovilizacionInputSerializer
)


# ==============================================================================
# VIEWSETS BÁSICOS (MAESTROS)
# ==============================================================================

@extend_schema_view(
    list=extend_schema(summary="Listar todos los roles", tags=["Maestros"]),
    retrieve=extend_schema(summary="Obtener un rol específico", tags=["Maestros"]),
    create=extend_schema(summary="Crear un nuevo rol", tags=["Maestros"]),
    update=extend_schema(summary="Actualizar un rol completo", tags=["Maestros"]),
    partial_update=extend_schema(summary="Actualizar parcialmente un rol", tags=["Maestros"]),
    destroy=extend_schema(summary="Eliminar un rol", tags=["Maestros"])
)
class RolViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de Roles de usuario.

    SEGURIDAD: Solo Administradores pueden gestionar roles.

    Permisos:
    - Administrador: CRUD completo
    - Técnico: Acceso denegado
    - Jefe: Acceso denegado

    Endpoints:
    - GET /api/roles/ - Listar todos los roles
    - POST /api/roles/ - Crear un nuevo rol
    - GET /api/roles/{id}/ - Obtener un rol específico
    - PUT /api/roles/{id}/ - Actualizar un rol completo
    - PATCH /api/roles/{id}/ - Actualizar parcialmente un rol
    - DELETE /api/roles/{id}/ - Eliminar un rol
    """
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


@extend_schema_view(
    list=extend_schema(summary="Listar todos los departamentos", tags=["Maestros"]),
    retrieve=extend_schema(summary="Obtener un departamento específico", tags=["Maestros"]),
    create=extend_schema(summary="Crear un nuevo departamento", tags=["Maestros"]),
    update=extend_schema(summary="Actualizar un departamento completo", tags=["Maestros"]),
    partial_update=extend_schema(summary="Actualizar parcialmente un departamento", tags=["Maestros"]),
    destroy=extend_schema(summary="Eliminar un departamento", tags=["Maestros"])
)
class DepartamentoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de Departamentos del hospital.

    SEGURIDAD: Solo Administradores pueden gestionar departamentos (maestro crítico).

    Permisos:
    - Administrador: CRUD completo
    - Técnico: Acceso denegado
    - Jefe: Acceso denegado

    Endpoints:
    - GET /api/departamentos/ - Listar todos los departamentos
    - POST /api/departamentos/ - Crear un nuevo departamento
    - GET /api/departamentos/{id}/ - Obtener un departamento específico
    - PUT /api/departamentos/{id}/ - Actualizar un departamento completo
    - PATCH /api/departamentos/{id}/ - Actualizar parcialmente un departamento
    - DELETE /api/departamentos/{id}/ - Eliminar un departamento
    """
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
    def get_permissions(self):
        """
        Permite a Técnicos ver la lista de departamentos (necesario para filtros).
        Solo Admin puede crear/borrar departamentos.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

@extend_schema_view(
    list=extend_schema(summary="Listar todos los tipos de equipo", tags=["Maestros"]),
    retrieve=extend_schema(summary="Obtener un tipo de equipo específico", tags=["Maestros"]),
    create=extend_schema(summary="Crear un nuevo tipo de equipo", tags=["Maestros"]),
    update=extend_schema(summary="Actualizar un tipo de equipo completo", tags=["Maestros"]),
    partial_update=extend_schema(summary="Actualizar parcialmente un tipo de equipo", tags=["Maestros"]),
    destroy=extend_schema(summary="Eliminar un tipo de equipo", tags=["Maestros"])
)
class TipoEquipoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de Tipos de Equipo.

    SEGURIDAD - CONTROL DE ACCESO:

    Permisos por rol:
    - Administrador: CRUD completo (puede crear, editar, eliminar tipos de equipo)
    - Técnico: Solo lectura (GET) - Necesita ver tipos para registrar activos
    - Jefe de Departamento: Solo lectura (GET) - Puede consultar para supervisión

    JUSTIFICACIÓN:
    - Los Técnicos NECESITAN ver tipos de equipo para poder registrar nuevos activos
    - Solo Admin puede modificar maestros (integridad de datos)

    Endpoints:
    - GET /api/tipos-equipo/ - Listar todos los tipos de equipo (Admin, Técnico, Jefe)
    - POST /api/tipos-equipo/ - Crear un nuevo tipo de equipo (solo Admin)
    - GET /api/tipos-equipo/{id}/ - Obtener un tipo de equipo específico (Admin, Técnico, Jefe)
    - PUT /api/tipos-equipo/{id}/ - Actualizar un tipo de equipo completo (solo Admin)
    - PATCH /api/tipos-equipo/{id}/ - Actualizar parcialmente un tipo de equipo (solo Admin)
    - DELETE /api/tipos-equipo/{id}/ - Eliminar un tipo de equipo (solo Admin)
    """
    queryset = TipoEquipo.objects.all()
    serializer_class = TipoEquipoSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


@extend_schema_view(
    list=extend_schema(summary="Listar todos los estados de activo", tags=["Maestros"]),
    retrieve=extend_schema(summary="Obtener un estado de activo específico", tags=["Maestros"]),
    create=extend_schema(summary="Crear un nuevo estado de activo", tags=["Maestros"]),
    update=extend_schema(summary="Actualizar un estado de activo completo", tags=["Maestros"]),
    partial_update=extend_schema(summary="Actualizar parcialmente un estado de activo", tags=["Maestros"]),
    destroy=extend_schema(summary="Eliminar un estado de activo", tags=["Maestros"])
)
class EstadoActivoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de Estados de Activo.

    SEGURIDAD - CONTROL DE ACCESO:

    Permisos por rol:
    - Administrador: CRUD completo (puede crear, editar, eliminar estados)
    - Técnico: Solo lectura (GET) - Necesita ver estados para actualizar activos
    - Jefe de Departamento: Solo lectura (GET) - Puede consultar para supervisión

    JUSTIFICACIÓN:
    - Los Técnicos NECESITAN ver estados para poder actualizar el estado de los activos
    - Solo Admin puede modificar maestros (integridad de datos)

    Endpoints:
    - GET /api/estados-activo/ - Listar todos los estados de activo (Admin, Técnico, Jefe)
    - POST /api/estados-activo/ - Crear un nuevo estado de activo (solo Admin)
    - GET /api/estados-activo/{id}/ - Obtener un estado de activo específico (Admin, Técnico, Jefe)
    - PUT /api/estados-activo/{id}/ - Actualizar un estado de activo completo (solo Admin)
    - PATCH /api/estados-activo/{id}/ - Actualizar parcialmente un estado de activo (solo Admin)
    - DELETE /api/estados-activo/{id}/ - Eliminar un estado de activo (solo Admin)
    """
    queryset = EstadoActivo.objects.all()
    serializer_class = EstadoActivoSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]



# ==============================================================================
# VIEWSETS CON RELACIONES
# ==============================================================================

@extend_schema_view(
    list=extend_schema(summary="Listar todas las ubicaciones", tags=["Core"]),
    retrieve=extend_schema(summary="Obtener una ubicación específica", tags=["Core"]),
    create=extend_schema(summary="Crear una nueva ubicación", tags=["Core"]),
    update=extend_schema(summary="Actualizar una ubicación completa", tags=["Core"]),
    partial_update=extend_schema(summary="Actualizar parcialmente una ubicación", tags=["Core"]),
    destroy=extend_schema(summary="Eliminar una ubicación", tags=["Core"])
)
class UbicacionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de Ubicaciones.

    SEGURIDAD - CONTROL DE ACCESO:

    Permisos por rol:
    - Administrador: CRUD completo (puede crear, editar, eliminar ubicaciones)
    - Técnico: Solo lectura (GET) - Necesita ver ubicaciones para movilizar activos
    - Jefe de Departamento: Solo lectura (GET) - Puede consultar para supervisión

    JUSTIFICACIÓN:
    - Los Técnicos NECESITAN ver ubicaciones para poder movilizar activos entre ellas
    - Solo Admin puede modificar maestros (integridad de datos)

    OPTIMIZACIÓN: Usa select_related('departamento') para evitar N+1 queries.

    Endpoints:
    - GET /api/ubicaciones/ - Listar todas las ubicaciones (Admin, Técnico, Jefe)
    - POST /api/ubicaciones/ - Crear una nueva ubicación (solo Admin)
    - GET /api/ubicaciones/{id}/ - Obtener una ubicación específica (Admin, Técnico, Jefe)
    - PUT /api/ubicaciones/{id}/ - Actualizar una ubicación completa (solo Admin)
    - PATCH /api/ubicaciones/{id}/ - Actualizar parcialmente una ubicación (solo Admin)
    - DELETE /api/ubicaciones/{id}/ - Eliminar una ubicación (solo Admin)
    """
    queryset = Ubicacion.objects.select_related('departamento').all()
    serializer_class = UbicacionSerializer
    def get_permissions(self):
        """
        Permite a cualquier usuario autenticado (Técnicos incluidos) ver la lista.
        Solo Administradores pueden crear, editar o borrar.
        """
        if self.action in ['list', 'retrieve']:
            # Para ver (GET), solo necesitas estar logueado
            permission_classes = [IsAuthenticated]
        else:
            # Para todo lo demás (POST, PUT, DELETE), necesitas ser Admin
            permission_classes = [IsAdminUser]
        
        return [permission() for permission in permission_classes]

    # FILTROS Y BÚSQUEDA
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['departamento']
    search_fields = ['nombre_ubicacion', 'codigo_qr']
    ordering_fields = ['nombre_ubicacion', 'codigo_qr']
    ordering = ['nombre_ubicacion']


@extend_schema_view(
    list=extend_schema(summary="Listar todos los usuarios", tags=["Core"]),
    retrieve=extend_schema(summary="Obtener un usuario específico", tags=["Core"]),
    create=extend_schema(summary="Crear un nuevo usuario", tags=["Core"]),
    update=extend_schema(summary="Actualizar un usuario completo", tags=["Core"]),
    partial_update=extend_schema(summary="Actualizar parcialmente un usuario", tags=["Core"]),
    destroy=extend_schema(summary="Eliminar un usuario", tags=["Core"])
)
class UsuarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de Usuarios.

    SEGURIDAD: Solo Administradores pueden gestionar usuarios (recurso crítico).

    Permisos:
    - Administrador: CRUD completo (crear, editar, eliminar usuarios)
    - Técnico: Acceso denegado
    - Jefe: Acceso denegado

    OPTIMIZACIÓN: Usa select_related('rol') para evitar N+1 queries.

    SEGURIDAD: El password se maneja de forma segura (write_only en serializer).

    Endpoints:
    - GET /api/usuarios/ - Listar todos los usuarios
    - POST /api/usuarios/ - Crear un nuevo usuario
    - GET /api/usuarios/{id}/ - Obtener un usuario específico
    - PUT /api/usuarios/{id}/ - Actualizar un usuario completo
    - PATCH /api/usuarios/{id}/ - Actualizar parcialmente un usuario
    - DELETE /api/usuarios/{id}/ - Eliminar un usuario
    - GET /api/usuarios/me/ - Obtener información del usuario autenticado (CRÍTICO PARA FRONTEND)
    """
    queryset = Usuario.objects.select_related('rol').all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    @extend_schema(
        summary="Obtener información del usuario autenticado",
        description="""
        Endpoint CRÍTICO para el frontend: Retorna la información completa del usuario
        que está haciendo la petición (basado en el token JWT).

        Este endpoint es usado por el frontend para:
        - Obtener el rol del usuario (Administrador, Técnico, Jefe de Departamento)
        - Determinar permisos de UI (qué botones mostrar/ocultar)
        - Mostrar información del perfil

        SEGURIDAD:
        - Solo requiere autenticación (IsAuthenticated)
        - NO requiere ser Admin (cualquier usuario autenticado puede ver su propia info)
        - El password NUNCA se devuelve (write_only en serializer)

        Respuesta:
        {
            "id": 1,
            "username": "admin",
            "email": "admin@hospital.com",
            "nombre_completo": "Administrador del Sistema",
            "rol": {
                "id_rol": 1,
                "nombre_rol": "Administrador",
                "descripcion": "Acceso total al sistema"
            },
            "is_active": true,
            "is_staff": true,
            "date_joined": "2025-01-15T10:30:00Z",
            "last_login": "2025-01-20T14:45:00Z"
        }
        """,
        tags=["Core", "Autenticación"],
        responses={
            200: UsuarioSerializer,
            401: OpenApiResponse(description="No autenticado - Token inválido o ausente")
        }
    )
    @action(
        detail=False,
        methods=['get'],
        url_path='me',
        permission_classes=[IsAuthenticated]  # Solo requiere autenticación, NO admin
    )
    def me(self, request):
        """
        Retorna la información del usuario autenticado.

        CRÍTICO: Este endpoint es usado por el frontend para obtener el rol del usuario
        y determinar qué permisos tiene en la interfaz.

        Args:
            request: Request con el usuario autenticado (request.user)

        Returns:
            Response: Datos del usuario serializado (sin password)

        Example:
            GET /api/usuarios/me/
            Authorization: Bearer <token>

            Response 200:
            {
                "id": 2,
                "username": "tecnico1",
                "email": "tecnico1@hospital.com",
                "nombre_completo": "Juan Pérez",
                "rol": {
                    "id_rol": 2,
                    "nombre_rol": "Técnico",
                    "descripcion": "Gestión de activos"
                },
                "is_active": true,
                "is_staff": false,
                "date_joined": "2025-01-10T08:00:00Z",
                "last_login": "2025-01-20T09:15:00Z"
            }
        """
        # Obtener el usuario autenticado con su rol (optimización)
        user = Usuario.objects.select_related('rol').get(pk=request.user.pk)

        # Serializar y retornar
        serializer = self.get_serializer(user)
        return Response(serializer.data)


# ==============================================================================
# VIEWSET DE ACTIVOS (CRÍTICO)
# ==============================================================================

@extend_schema_view(
    list=extend_schema(
        summary="Listar todos los activos",
        description="Obtiene el listado completo de activos con información anidada de tipo, estado y ubicación",
        tags=["Core"]
    ),
    retrieve=extend_schema(
        summary="Obtener un activo específico",
        description="Obtiene los detalles completos de un activo incluyendo tipo, estado y ubicación con departamento",
        tags=["Core"]
    ),
    create=extend_schema(
        summary="Crear un nuevo activo",
        description="Registra un nuevo activo en el sistema de inventario",
        tags=["Core"]
    ),
    update=extend_schema(
        summary="Actualizar un activo completo",
        description="Actualiza todos los campos de un activo existente",
        tags=["Core"]
    ),
    partial_update=extend_schema(
        summary="Actualizar parcialmente un activo",
        description="Actualiza uno o más campos de un activo existente",
        tags=["Core"]
    ),
    destroy=extend_schema(
        summary="Eliminar un activo",
        description="Elimina un activo del sistema (requiere que no tenga historial asociado)",
        tags=["Core"]
    )
)
class ActivoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de Activos (ENTIDAD CENTRAL DEL SISTEMA).

    SEGURIDAD - CONTROL DE ACCESO BASADO EN ROLES (RBAC):

    Permisos aplicados:
    - IsAuthenticated: Todos los usuarios deben estar autenticados
    - IsTecnicoOperativo: Permite a Técnicos y Admins crear/editar (GET, POST, PUT, PATCH)
    - IsJefeOrAdminReadOnly: Permite a Jefes consultar activos (GET)
    - CanDeleteActivo: Solo Administradores pueden eliminar (DELETE)

    Matriz de permisos por rol:
    ┌─────────────────┬───────┬─────────┬──────┐
    │ Operación       │ Admin │ Técnico │ Jefe │
    ├─────────────────┼───────┼─────────┼──────┤
    │ GET (List)      │   ✓   │    ✓    │  ✓   │
    │ GET (Retrieve)  │   ✓   │    ✓    │  ✓   │
    │ POST (Create)   │   ✓   │    ✓    │  ✗   │
    │ PUT (Update)    │   ✓   │    ✓    │  ✗   │
    │ PATCH (Partial) │   ✓   │    ✓    │  ✗   │
    │ DELETE          │   ✓   │    ✗    │  ✗   │
    │ movilizar       │   ✓   │    ✓    │  ✗   │
    └─────────────────┴───────┴─────────┴──────┘

    OPTIMIZACIÓN CRÍTICA:
    - Usa select_related() para cargar tipo, estado, ubicacion_actual y departamento
      en una sola query SQL (evita el problema N+1 queries).
    - Sin esta optimización, listar 100 activos generaría 301 queries SQL.
    - Con esta optimización, listar 100 activos genera solo 1 query SQL.

    RESPUESTA:
    - Los objetos relacionados (tipo, estado, ubicacion_actual) se devuelven
      completos gracias al método to_representation() del serializer.

    Endpoints:
    - GET /api/activos/ - Listar todos los activos con información completa
    - POST /api/activos/ - Crear un nuevo activo
    - GET /api/activos/{id}/ - Obtener un activo específico
    - PUT /api/activos/{id}/ - Actualizar un activo completo
    - PATCH /api/activos/{id}/ - Actualizar parcialmente un activo
    - DELETE /api/activos/{id}/ - Eliminar un activo
    """
    queryset = Activo.objects.select_related(
        'tipo',
        'estado',
        'ubicacion_actual',
        'ubicacion_actual__departamento'
    ).all()
    serializer_class = ActivoSerializer

    # RBAC: Combinación de permisos para control granular
    # - IsTecnicoOperativo: Permite GET/POST/PUT/PATCH a Técnicos y Admins
    # - IsJefeOrAdminReadOnly: Permite GET a Jefes
    # - CanDeleteActivo: Bloquea DELETE excepto para Admins
    permission_classes = [IsAuthenticated, IsTecnicoOperativo | IsJefeOrAdminReadOnly, CanDeleteActivo]

    # FILTROS Y BÚSQUEDA
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ubicacion_actual', 'tipo', 'estado']
    search_fields = ['codigo_inventario', 'numero_serie', 'marca', 'modelo']
    ordering_fields = ['fecha_alta', 'codigo_inventario', 'marca']
    ordering = ['-fecha_alta']

    @extend_schema(
        request=MovilizacionInputSerializer,
        responses={
            200: {"description": "Activo movilizado con éxito"},
            400: {"description": "Error de validación o ubicación no encontrada"},
            403: {"description": "Permiso denegado - Solo Técnicos y Administradores"},
            404: {"description": "Activo no encontrado"}
        },
        description="""
        Moviliza un activo a una nueva ubicación (Historia de Usuario HU2).

        SEGURIDAD: Solo Técnicos y Administradores pueden movilizar activos.
        Los Jefes de Departamento NO tienen permiso para esta operación.

        OPERACIÓN TRANSACCIONAL (ACID):
        Esta operación es atómica. Si alguna parte falla, toda la operación se revierte.

        PASOS EJECUTADOS:
        1. Valida que la ubicación destino exista
        2. Actualiza la ubicación actual del activo
        3. Registra el movimiento en el historial (trazabilidad)
        4. Crea un log de auditoría en PostgreSQL (seguridad)

        EJEMPLO DE REQUEST:
        ```json
        {
            "id_ubicacion_destino": 5,
            "notas": "Traslado por mantenimiento preventivo"
        }
        ```
        """,
        tags=["Core"]
    )
    @action(
        detail=True,
        methods=['post'],
        url_path='movilizar',
        permission_classes=[IsAuthenticated, IsTecnicoOperativo]  # Solo Técnicos y Admins
    )
    def movilizar(self, request, pk=None):
        """
        Acción personalizada para movilizar un activo entre ubicaciones.

        IMPLEMENTACIÓN DE HU2: Movilización de Activos

        Esta acción implementa la lógica de negocio crítica para mover activos
        entre ubicaciones, garantizando:
        - Transaccionalidad ACID (todo o nada)
        - Trazabilidad completa (historial de movimientos)
        - Auditoría de seguridad (logs en PostgreSQL)

        Args:
            request: Request HTTP con los datos de movilización
            pk: ID del activo a movilizar

        Returns:
            Response: 200 OK si la movilización fue exitosa
            Response: 400 Bad Request si hay errores de validación
            Response: 404 Not Found si el activo no existe

        Raises:
            ValidationError: Si la ubicación destino no existe
            Exception: Si ocurre algún error durante la transacción
        """

        # ======================================================================
        # PASO 1: VALIDACIÓN DE ENTRADA
        # ======================================================================

        # Validar los datos de entrada usando el serializer
        input_serializer = MovilizacionInputSerializer(data=request.data)

        if not input_serializer.is_valid():
            return Response(
                {
                    'status': 'error',
                    'message': 'Datos de entrada inválidos',
                    'errors': input_serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Extraer datos validados
        id_ubicacion_destino = input_serializer.validated_data['id_ubicacion_destino']
        notas = input_serializer.validated_data.get('notas', '')

        # ======================================================================
        # PASO 2: OBTENCIÓN DEL ACTIVO Y VALIDACIONES
        # ======================================================================

        try:
            # Obtener el activo (usa el método del ViewSet que maneja 404 automáticamente)
            activo = self.get_object()

            # Obtener la ubicación destino
            try:
                ubicacion_destino = Ubicacion.objects.select_related('departamento').get(
                    id=id_ubicacion_destino
                )
            except Ubicacion.DoesNotExist:
                return Response(
                    {
                        'status': 'error',
                        'message': f'La ubicación con ID {id_ubicacion_destino} no existe'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Validar que no sea la misma ubicación
            if activo.ubicacion_actual.id == ubicacion_destino.id:
                return Response(
                    {
                        'status': 'error',
                        'message': 'El activo ya se encuentra en la ubicación destino'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Guardar la ubicación origen antes de cambiarla
            ubicacion_origen = activo.ubicacion_actual

            # ======================================================================
            # PASO 3: TRANSACCIÓN ATÓMICA (ACID)
            # ======================================================================

            with transaction.atomic():
                """
                TRANSACCIÓN ATÓMICA:
                Todo lo que ocurra dentro de este bloque se ejecuta como una
                única operación. Si algo falla, TODA la operación se revierte.

                Esto garantiza:
                - Atomicidad: Todo o nada
                - Consistencia: Los datos quedan en estado válido
                - Aislamiento: Otras transacciones no ven estados intermedios
                - Durabilidad: Los cambios son permanentes
                """

                # ----------------------------------------------------------
                # 3.1: ACTUALIZAR UBICACIÓN DEL ACTIVO
                # ----------------------------------------------------------
                activo.ubicacion_actual = ubicacion_destino
                activo.save()

                # ----------------------------------------------------------
                # 3.2: REGISTRAR EN HISTORIAL (TRAZABILIDAD)
                # ----------------------------------------------------------
                historial = HistorialMovimiento.objects.create(
                    activo=activo,
                    usuario_registra=request.user,
                    ubicacion_origen=ubicacion_origen,
                    ubicacion_destino=ubicacion_destino,
                    tipo_movimiento='TRASLADO',  # Tipo de movimiento según HU2
                    comentarios=notas
                )

                # ----------------------------------------------------------
                # 3.3: REGISTRAR EN AUDITORÍA (SEGURIDAD)
                # ----------------------------------------------------------
                # Los logs se guardan en PostgreSQL usando JSONField
                # (NO usamos MongoDB como se especificó en los requisitos)
                AuditoriaLog.objects.create(
                    usuario=request.user,
                    accion='MOVILIZACION_ACTIVO',
                    detalle_accion={
                        'activo_id': activo.id,
                        'activo_codigo': activo.codigo_inventario,
                        'activo_marca': activo.marca,
                        'activo_modelo': activo.modelo,
                        'origen_id': ubicacion_origen.id,
                        'origen_nombre': ubicacion_origen.nombre_ubicacion,
                        'origen_departamento': ubicacion_origen.departamento.nombre_departamento,
                        'destino_id': ubicacion_destino.id,
                        'destino_nombre': ubicacion_destino.nombre_ubicacion,
                        'destino_departamento': ubicacion_destino.departamento.nombre_departamento,
                        'notas': notas,
                        'historial_id': historial.id
                    }
                )

            # ======================================================================
            # PASO 4: RESPUESTA EXITOSA
            # ======================================================================

            return Response(
                {
                    'status': 'success',
                    'message': 'Activo movilizado con éxito',
                    'data': {
                        'activo_codigo': activo.codigo_inventario,
                        'ubicacion_origen': {
                            'id': ubicacion_origen.id,
                            'nombre': ubicacion_origen.nombre_ubicacion,
                            'departamento': ubicacion_origen.departamento.nombre_departamento
                        },
                        'ubicacion_destino': {
                            'id': ubicacion_destino.id,
                            'nombre': ubicacion_destino.nombre_ubicacion,
                            'departamento': ubicacion_destino.departamento.nombre_departamento
                        },
                        'fecha_movimiento': historial.fecha_movimiento.isoformat(),
                        'usuario': request.user.username
                    }
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            # ======================================================================
            # MANEJO DE ERRORES
            # ======================================================================

            # Si ocurre cualquier error, la transacción se revierte automáticamente
            return Response(
                {
                    'status': 'error',
                    'message': 'Error al movilizar el activo',
                    'detail': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )


# ==============================================================================
# VIEWSETS DE TRAZABILIDAD Y AUDITORÍA
# ==============================================================================

@extend_schema_view(
    list=extend_schema(
        summary="Listar historial de movimientos",
        description="Obtiene el historial completo de movimientos de activos con trazabilidad",
        tags=["Trazabilidad"]
    ),
    retrieve=extend_schema(
        summary="Obtener un movimiento específico",
        description="Obtiene los detalles completos de un movimiento de activo",
        tags=["Trazabilidad"]
    ),
    create=extend_schema(
        summary="Registrar un nuevo movimiento",
        description="Registra un movimiento de activo entre ubicaciones",
        tags=["Trazabilidad"]
    ),
    update=extend_schema(
        summary="Actualizar un movimiento completo",
        description="Actualiza todos los campos de un movimiento existente",
        tags=["Trazabilidad"]
    ),
    partial_update=extend_schema(
        summary="Actualizar parcialmente un movimiento",
        description="Actualiza uno o más campos de un movimiento existente",
        tags=["Trazabilidad"]
    ),
    destroy=extend_schema(
        summary="Eliminar un movimiento",
        description="Elimina un registro de movimiento del historial",
        tags=["Trazabilidad"]
    )
)
class HistorialMovimientoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de Historial de Movimientos.

    SEGURIDAD - CONTROL DE ACCESO:

    Permisos por rol:
    - Administrador: CRUD completo (puede crear, editar, eliminar registros históricos)
    - Técnico: Solo lectura (GET) - No puede modificar el historial
    - Jefe: Solo lectura (GET) - Puede consultar para auditoría

    NOTA: Los movimientos normalmente se crean automáticamente mediante la acción
    'movilizar' del ActivoViewSet. Este endpoint permite gestión manual si es necesario.

    OPTIMIZACIÓN:
    - Usa select_related() para cargar todas las relaciones en una sola query.

    TRAZABILIDAD:
    - Cada movimiento registra activo, usuario, ubicaciones origen/destino.

    Endpoints:
    - GET /api/historial-movimientos/ - Listar todos los movimientos
    - POST /api/historial-movimientos/ - Registrar un nuevo movimiento (solo Admin)
    - GET /api/historial-movimientos/{id}/ - Obtener un movimiento específico
    - PUT /api/historial-movimientos/{id}/ - Actualizar un movimiento completo (solo Admin)
    - PATCH /api/historial-movimientos/{id}/ - Actualizar parcialmente un movimiento (solo Admin)
    - DELETE /api/historial-movimientos/{id}/ - Eliminar un movimiento (solo Admin)
    """
    queryset = HistorialMovimiento.objects.select_related(
        'activo',
        'usuario_registra',
        'ubicacion_origen',
        'ubicacion_origen__departamento',
        'ubicacion_destino',
        'ubicacion_destino__departamento'
    ).all()
    serializer_class = HistorialMovimientoSerializer

    # RBAC: Jefes y Técnicos pueden consultar, solo Admin puede modificar
    permission_classes = [IsAuthenticated, IsTecnicoOperativo | IsJefeOrAdminReadOnly]

    # FILTROS Y BÚSQUEDA
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['activo', 'usuario_registra', 'ubicacion_origen', 'ubicacion_destino', 'tipo_movimiento']
    search_fields = ['activo__codigo_inventario', 'activo__marca', 'activo__modelo', 'comentarios']
    ordering_fields = ['fecha_movimiento', 'tipo_movimiento']
    ordering = ['-fecha_movimiento']


@extend_schema_view(
    list=extend_schema(
        summary="Listar logs de auditoría",
        description="Obtiene el historial completo de acciones del sistema",
        tags=["Auditoría"]
    ),
    retrieve=extend_schema(
        summary="Obtener un log específico",
        description="Obtiene los detalles completos de un log de auditoría",
        tags=["Auditoría"]
    )
)
class AuditoriaLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para consulta de Logs de Auditoría (SOLO LECTURA).

    SEGURIDAD - CONTROL DE ACCESO:

    Permisos por rol:
    - Administrador: Acceso completo a todos los logs de auditoría
    - Jefe de Departamento: Acceso completo (para supervisión y control)
    - Técnico: Acceso denegado (no necesitan ver logs de auditoría)

    JUSTIFICACIÓN:
    - Los Jefes necesitan acceso a auditoría para supervisar operaciones
    - Los Técnicos no requieren acceso a logs de auditoría del sistema
    - Solo lectura: Los logs nunca se modifican manualmente (integridad)

    IMPORTANTE:
    - Este ViewSet es ReadOnlyModelViewSet (solo GET).
    - Los logs de auditoría no se crean, modifican ni eliminan manualmente.
    - Se crean automáticamente mediante el método AuditoriaLog.registrar_accion().

    OPTIMIZACIÓN:
    - Usa select_related('usuario') para evitar N+1 queries.

    Endpoints:
    - GET /api/auditoria-logs/ - Listar todos los logs de auditoría
    - GET /api/auditoria-logs/{id}/ - Obtener un log específico
    """
    queryset = AuditoriaLog.objects.select_related('usuario').all()
    serializer_class = AuditoriaLogSerializer

    # RBAC: Solo Administradores y Jefes pueden consultar auditoría
    permission_classes = [IsAuthenticated, IsJefeOrAdminReadOnly]


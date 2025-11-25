"""
Serializers para la API REST del Sistema de Control de Activos (SCA) Hospital.

Este módulo define los serializers de Django REST Framework para convertir
los modelos de Django en JSON y viceversa.

Características:
- Nombres de campo limpios para el frontend (rol en lugar de fk_id_rol)
- Validación automática de datos
- Manejo seguro de passwords (write_only)
- Relaciones anidadas para lectura (to_representation)
- Híbrido lectura/escritura: objetos completos en GET, IDs en POST/PUT
- Documentación automática para OpenAPI/Swagger
"""

from rest_framework import serializers
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


# ==============================================================================
# SERIALIZERS BÁSICOS (MAESTROS)
# ==============================================================================

class RolSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Rol.

    Permite crear, leer, actualizar y eliminar roles de usuario.

    Campos:
    - id: Identificador único del rol
    - nombre_rol: Nombre descriptivo del rol (ej: Administrador, Técnico)
    """

    class Meta:
        model = Rol
        fields = ['id', 'nombre_rol']
        read_only_fields = ['id']


class DepartamentoSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Departamento.

    Representa áreas o departamentos del hospital.

    Campos:
    - id: Identificador único del departamento
    - nombre_departamento: Nombre del departamento (ej: Urgencias, UCI)
    """

    class Meta:
        model = Departamento
        fields = ['id', 'nombre_departamento']
        read_only_fields = ['id']


class TipoEquipoSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo TipoEquipo.

    Clasifica los tipos de equipos/activos del sistema.

    Campos:
    - id: Identificador único del tipo
    - nombre_tipo: Nombre del tipo (ej: Computador, Monitor, Impresora)
    """

    class Meta:
        model = TipoEquipo
        fields = ['id', 'nombre_tipo']
        read_only_fields = ['id']


class EstadoActivoSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo EstadoActivo.

    Define los estados posibles de un activo.

    Campos:
    - id: Identificador único del estado
    - nombre_estado: Nombre del estado (ej: Operativo, En Mantención, De Baja)
    """

    class Meta:
        model = EstadoActivo
        fields = ['id', 'nombre_estado']
        read_only_fields = ['id']


# ==============================================================================
# SERIALIZERS CON RELACIONES
# ==============================================================================

class UbicacionSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Ubicacion.

    HÍBRIDO LECTURA/ESCRITURA:
    - Escritura (POST/PUT): Acepta 'departamento_id' (solo el ID)
    - Lectura (GET): Devuelve 'departamento' como objeto completo

    Campos:
    - id: Identificador único de la ubicación
    - nombre_ubicacion: Nombre de la ubicación (ej: Sala 101, Box 3)
    - departamento_id: ID del departamento (solo escritura)
    - departamento: Objeto departamento completo (solo lectura)

    Ejemplo de escritura:
    {
        "nombre_ubicacion": "Sala 101",
        "departamento_id": 1
    }

    Ejemplo de lectura:
    {
        "id": 1,
        "nombre_ubicacion": "Sala 101",
        "departamento": {
            "id": 1,
            "nombre_departamento": "Urgencias"
        }
    }
    """

    # Campo limpio para escritura (acepta ID)
    departamento_id = serializers.PrimaryKeyRelatedField(
        queryset=Departamento.objects.all(),
        source='departamento',
        write_only=True,
        help_text="ID del departamento al que pertenece esta ubicación"
    )

    # Campo para lectura (objeto completo)
    departamento = DepartamentoSerializer(read_only=True)

    class Meta:
        model = Ubicacion
        fields = ['id', 'nombre_ubicacion', 'departamento_id', 'departamento']
        read_only_fields = ['id', 'departamento']


class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Usuario (Custom User Model).

    HÍBRIDO LECTURA/ESCRITURA:
    - Escritura (POST/PUT): Acepta 'rol_id' (solo el ID) y 'password' (write_only)
    - Lectura (GET): Devuelve 'rol' como objeto completo, sin password

    Campos:
    - id: Identificador único del usuario
    - username: Nombre de usuario único
    - password: Contraseña (solo escritura, se hashea automáticamente)
    - email: Correo electrónico
    - nombre_completo: Nombre completo del usuario
    - rol_id: ID del rol (solo escritura)
    - rol: Objeto rol completo (solo lectura)
    - is_active: Usuario activo
    - is_staff: Usuario es staff
    - date_joined: Fecha de registro
    - last_login: Último inicio de sesión

    SEGURIDAD:
    - El password NUNCA se devuelve en las respuestas (write_only=True)
    - El password se hashea automáticamente usando create_user()
    """

    # Campo password solo para escritura
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text="Contraseña del usuario (será hasheada automáticamente)"
    )

    # Campo limpio para escritura (acepta ID)
    rol_id = serializers.PrimaryKeyRelatedField(
        queryset=Rol.objects.all(),
        source='rol',
        write_only=True,
        required=False,
        allow_null=True,
        help_text="ID del rol asignado al usuario"
    )

    # Campo para lectura (objeto completo)
    rol = RolSerializer(read_only=True)

    class Meta:
        model = Usuario
        fields = [
            'id',
            'username',
            'password',
            'email',
            'nombre_completo',
            'rol_id',
            'rol',
            'is_active',
            'is_staff',
            'date_joined',
            'last_login'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login', 'rol']

    def create(self, validated_data):
        """
        Crea un nuevo usuario hasheando correctamente el password.

        CRÍTICO: Usa create_user() en lugar de create() para que
        Django hashee el password automáticamente.
        """
        password = validated_data.pop('password')
        user = Usuario.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user



# ==============================================================================
# SERIALIZER DE ACTIVOS (CRÍTICO)
# ==============================================================================

class ActivoSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Activo (ENTIDAD CENTRAL DEL SISTEMA).

    HÍBRIDO LECTURA/ESCRITURA (CRÍTICO):
    - Escritura (POST/PUT): Acepta 'tipo_id', 'estado_id', 'ubicacion_actual_id' (solo IDs)
    - Lectura (GET): Devuelve 'tipo', 'estado', 'ubicacion_actual' como objetos completos

    Campos:
    - id: Identificador único del activo
    - codigo_inventario: Código único de inventario (ej: ACT-2024-001)
    - numero_serie: Número de serie del fabricante
    - marca: Marca o fabricante (ej: HP, Dell, Samsung)
    - modelo: Modelo específico (ej: EliteBook 840 G8)
    - fecha_alta: Fecha de registro en el sistema (auto)
    - tipo_id: ID del tipo de equipo (solo escritura)
    - tipo: Objeto tipo completo (solo lectura)
    - estado_id: ID del estado (solo escritura)
    - estado: Objeto estado completo (solo lectura)
    - ubicacion_actual_id: ID de la ubicación (solo escritura)
    - ubicacion_actual: Objeto ubicación completo con departamento (solo lectura)

    VENTAJA PARA EL FRONTEND:
    - En una sola petición GET obtiene toda la información necesaria
    - No necesita hacer 3 peticiones adicionales para tipo, estado y ubicación
    - Evita el problema N+1 queries en el frontend

    Ejemplo de escritura (POST):
    {
        "codigo_inventario": "ACT-2024-001",
        "numero_serie": "SN123456",
        "marca": "HP",
        "modelo": "EliteBook 840 G8",
        "tipo_id": 1,
        "estado_id": 1,
        "ubicacion_actual_id": 1
    }

    Ejemplo de lectura (GET):
    {
        "id": 1,
        "codigo_inventario": "ACT-2024-001",
        "numero_serie": "SN123456",
        "marca": "HP",
        "modelo": "EliteBook 840 G8",
        "fecha_alta": "2024-01-15T10:30:00Z",
        "tipo": {
            "id": 1,
            "nombre_tipo": "Computador"
        },
        "estado": {
            "id": 1,
            "nombre_estado": "Operativo"
        },
        "ubicacion_actual": {
            "id": 1,
            "nombre_ubicacion": "Sala 101",
            "departamento": {
                "id": 1,
                "nombre_departamento": "Urgencias"
            }
        }
    }
    """

    # Campos limpios para escritura (aceptan IDs)
    tipo_id = serializers.PrimaryKeyRelatedField(
        queryset=TipoEquipo.objects.all(),
        source='tipo',
        write_only=True,
        help_text="ID del tipo de equipo"
    )

    estado_id = serializers.PrimaryKeyRelatedField(
        queryset=EstadoActivo.objects.all(),
        source='estado',
        write_only=True,
        help_text="ID del estado del activo"
    )

    ubicacion_actual_id = serializers.PrimaryKeyRelatedField(
        queryset=Ubicacion.objects.all(),
        source='ubicacion_actual',
        write_only=True,
        help_text="ID de la ubicación actual del activo"
    )

    # Campos para lectura (objetos completos)
    tipo = TipoEquipoSerializer(read_only=True)
    estado = EstadoActivoSerializer(read_only=True)
    ubicacion_actual = UbicacionSerializer(read_only=True)

    class Meta:
        model = Activo
        fields = [
            'id',
            'codigo_inventario',
            'numero_serie',
            'marca',
            'modelo',
            'fecha_alta',
            'tipo_id',
            'tipo',
            'estado_id',
            'estado',
            'ubicacion_actual_id',
            'ubicacion_actual'
        ]
        read_only_fields = ['id', 'fecha_alta', 'tipo', 'estado', 'ubicacion_actual']


# ==============================================================================
# SERIALIZERS DE TRAZABILIDAD Y AUDITORÍA
# ==============================================================================

class HistorialMovimientoSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo HistorialMovimiento.

    HÍBRIDO LECTURA/ESCRITURA:
    - Escritura (POST/PUT): Acepta IDs limpios (activo_id, usuario_registra_id, etc.)
    - Lectura (GET): Devuelve objetos completos para trazabilidad completa

    Campos:
    - id: Identificador único del movimiento
    - activo_id: ID del activo movido (solo escritura)
    - activo: Objeto activo con código e info básica (solo lectura)
    - usuario_registra_id: ID del usuario que registra (solo escritura)
    - usuario_registra: Objeto usuario completo (solo lectura)
    - ubicacion_origen_id: ID de la ubicación origen (solo escritura)
    - ubicacion_origen: Objeto ubicación origen con departamento (solo lectura)
    - ubicacion_destino_id: ID de la ubicación destino (solo escritura)
    - ubicacion_destino: Objeto ubicación destino con departamento (solo lectura)
    - fecha_movimiento: Timestamp del movimiento (auto)
    - tipo_movimiento: Tipo (TRASLADO, ASIGNACION, DEVOLUCION, BAJA)
    - comentarios: Observaciones adicionales
    """

    # Campos limpios para escritura (aceptan IDs)
    activo_id = serializers.PrimaryKeyRelatedField(
        queryset=Activo.objects.all(),
        source='activo',
        write_only=True,
        help_text="ID del activo que se está moviendo"
    )

    usuario_registra_id = serializers.PrimaryKeyRelatedField(
        queryset=Usuario.objects.all(),
        source='usuario_registra',
        write_only=True,
        help_text="ID del usuario que registra el movimiento"
    )

    ubicacion_origen_id = serializers.PrimaryKeyRelatedField(
        queryset=Ubicacion.objects.all(),
        source='ubicacion_origen',
        write_only=True,
        help_text="ID de la ubicación de origen"
    )

    ubicacion_destino_id = serializers.PrimaryKeyRelatedField(
        queryset=Ubicacion.objects.all(),
        source='ubicacion_destino',
        write_only=True,
        help_text="ID de la ubicación de destino"
    )

    # Campos para lectura (objetos completos) - Serializados manualmente
    activo = serializers.SerializerMethodField(read_only=True)
    usuario_registra = serializers.SerializerMethodField(read_only=True)
    ubicacion_origen = serializers.SerializerMethodField(read_only=True)
    ubicacion_destino = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = HistorialMovimiento
        fields = [
            'id',
            'activo_id',
            'activo',
            'usuario_registra_id',
            'usuario_registra',
            'ubicacion_origen_id',
            'ubicacion_origen',
            'ubicacion_destino_id',
            'ubicacion_destino',
            'fecha_movimiento',
            'tipo_movimiento',
            'comentarios'
        ]
        read_only_fields = [
            'id',
            'fecha_movimiento',
            'activo',
            'usuario_registra',
            'ubicacion_origen',
            'ubicacion_destino'
        ]

    def get_activo(self, obj):
        """Devuelve información básica del activo."""
        return {
            'id': obj.activo.id,
            'codigo_inventario': obj.activo.codigo_inventario,
            'marca': obj.activo.marca,
            'modelo': obj.activo.modelo
        }

    def get_usuario_registra(self, obj):
        """Devuelve información del usuario que registró el movimiento."""
        return {
            'id': obj.usuario_registra.id,
            'username': obj.usuario_registra.username,
            'nombre_completo': obj.usuario_registra.nombre_completo
        }

    def get_ubicacion_origen(self, obj):
        """Devuelve información completa de la ubicación origen."""
        return {
            'id': obj.ubicacion_origen.id,
            'nombre_ubicacion': obj.ubicacion_origen.nombre_ubicacion,
            'departamento': obj.ubicacion_origen.departamento.nombre_departamento
        }

    def get_ubicacion_destino(self, obj):
        """Devuelve información completa de la ubicación destino."""
        return {
            'id': obj.ubicacion_destino.id,
            'nombre_ubicacion': obj.ubicacion_destino.nombre_ubicacion,
            'departamento': obj.ubicacion_destino.departamento.nombre_departamento
        }


class AuditoriaLogSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo AuditoriaLog (SOLO LECTURA).

    Este serializer es para consulta de logs de auditoría en el Dashboard de Admin.
    Los logs NO se crean, modifican ni eliminan vía API.

    Campos:
    - id: Identificador único del log
    - usuario: Objeto usuario completo (username, nombre_completo) o null si fue eliminado
    - accion: Tipo de acción realizada (CREATE, UPDATE, DELETE, LOGIN, etc.)
    - detalle_accion: Detalles flexibles en formato JSON
    - timestamp: Fecha y hora exacta de la acción

    IMPORTANTE:
    - Todos los campos son read_only
    - Los logs se crean automáticamente usando AuditoriaLog.registrar_accion()
    - El usuario puede ser null si fue eliminado (on_delete=SET_NULL)

    Ejemplo de respuesta:
    {
        "id": 1,
        "usuario": {
            "id": 1,
            "username": "admin",
            "nombre_completo": "Administrador Sistema"
        },
        "accion": "CREATE",
        "detalle_accion": {
            "modelo": "Activo",
            "objeto_id": "ACT-2024-001",
            "ip": "192.168.1.100"
        },
        "timestamp": "2024-01-15T10:30:00Z"
    }
    """

    # Campo usuario anidado (solo lectura)
    usuario_username = serializers.CharField(
        source='usuario.username',
        read_only=True,
        help_text="Nombre de usuario que realizó la acción"
    )

    usuario_nombre_completo = serializers.CharField(
        source='usuario.nombre_completo',
        read_only=True,
        help_text="Nombre completo del usuario"
    )

    class Meta:
        model = AuditoriaLog
        fields = [
            'id',
            'usuario',
            'usuario_username',
            'usuario_nombre_completo',
            'accion',
            'detalle_accion',
            'timestamp'
        ]
        read_only_fields = '__all__'  # Todos los campos son de solo lectura


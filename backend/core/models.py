"""
Modelos de datos para el Sistema de Control de Activos (SCA) Hospital.

Este módulo implementa EXACTAMENTE el esquema de base de datos definido en el diseño.
Usa db_column en las Foreign Keys para mantener los nombres 'fk_id_...' del diseño.

Características:
- Nombres de tablas y campos exactos del diseño
- Integridad referencial con PROTECT
- Documentación automática para OpenAPI/Swagger
- JSONField para auditoría (reemplazo de MongoDB)
"""

from django.db import models
from django.contrib.auth.models import AbstractUser


# ==============================================================================
# 1. ROLES Y USUARIOS
# ==============================================================================

class Rol(models.Model):
    """
    Modelo para definir roles de usuario en el sistema.

    Tabla: Tbl_Roles

    Ejemplos de roles:
    - Administrador
    - Técnico
    - Supervisor
    - Usuario de Consulta
    """

    nombre_rol = models.CharField(
        max_length=100,
        unique=True,
        help_text="Nombre del rol (ej: Administrador, Técnico, Supervisor)"
    )

    class Meta:
        db_table = 'Tbl_Roles'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'
        ordering = ['nombre_rol']

    def __str__(self):
        return self.nombre_rol


class Usuario(AbstractUser):
    """
    Modelo de usuario personalizado que extiende AbstractUser de Django.

    Tabla: Tbl_Usuarios

    Hereda de AbstractUser:
    - username, password, email
    - is_active, is_staff, is_superuser
    - date_joined, last_login

    Campos adicionales:
    - nombre_completo
    - rol (FK a Rol con db_column='fk_id_rol')
    """

    nombre_completo = models.CharField(
        max_length=200,
        help_text="Nombre completo del usuario"
    )

    rol = models.ForeignKey(
        Rol,
        on_delete=models.PROTECT,
        related_name='usuarios',
        db_column='fk_id_rol',
        null=True,
        blank=True,
        help_text="Rol asignado al usuario. PROTECT evita eliminar roles con usuarios asignados"
    )

    class Meta:
        db_table = 'Tbl_Usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['username']

    def __str__(self):
        return f"{self.username} - {self.nombre_completo}"


# ==============================================================================
# 2. UBICACIONES
# ==============================================================================

class Departamento(models.Model):
    """
    Modelo para representar departamentos o áreas del hospital.

    Tabla: Tbl_Departamentos

    Ejemplos:
    - Urgencias
    - Pabellón
    - UCI
    - Radiología
    """

    nombre_departamento = models.CharField(
        max_length=100,
        unique=True,
        help_text="Nombre del departamento (ej: Urgencias, Pabellón, UCI)"
    )

    class Meta:
        db_table = 'Tbl_Departamentos'
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
        ordering = ['nombre_departamento']

    def __str__(self):
        return self.nombre_departamento


class Ubicacion(models.Model):
    """
    Modelo para ubicaciones específicas dentro de los departamentos.

    Tabla: Tbl_Ubicaciones

    Ejemplos:
    - Sala 101
    - Box 3
    - Oficina Administración
    """

    nombre_ubicacion = models.CharField(
        max_length=100,
        help_text="Nombre de la ubicación específica (ej: Sala 101, Box 3)"
    )

    departamento = models.ForeignKey(
        Departamento,
        on_delete=models.PROTECT,
        related_name='ubicaciones',
        db_column='fk_id_departamento',
        help_text="Departamento al que pertenece esta ubicación. PROTECT evita eliminar departamentos con ubicaciones"
    )

    class Meta:
        db_table = 'Tbl_Ubicaciones'
        verbose_name = 'Ubicación'
        verbose_name_plural = 'Ubicaciones'
        ordering = ['departamento', 'nombre_ubicacion']
        unique_together = [['nombre_ubicacion', 'departamento']]

    def __str__(self):
        return f"{self.nombre_ubicacion} ({self.departamento.nombre_departamento})"


# ==============================================================================
# 3. MAESTROS
# ==============================================================================

class TipoEquipo(models.Model):
    """
    Modelo para clasificación de tipos de equipos/activos.

    Tabla: Tbl_Tipos_Equipo

    Ejemplos:
    - Monitor
    - Computador
    - Impresora
    - Equipo Médico
    """

    nombre_tipo = models.CharField(
        max_length=100,
        unique=True,
        help_text="Nombre del tipo de equipo (ej: Monitor, Computador, Impresora)"
    )

    class Meta:
        db_table = 'Tbl_Tipos_Equipo'
        verbose_name = 'Tipo de Equipo'
        verbose_name_plural = 'Tipos de Equipo'
        ordering = ['nombre_tipo']

    def __str__(self):
        return self.nombre_tipo


class EstadoActivo(models.Model):
    """
    Modelo para estados posibles de un activo.

    Tabla: Tbl_Estados_Activo

    Ejemplos:
    - Operativo
    - En Mantención
    - En Reparación
    - De Baja
    """

    nombre_estado = models.CharField(
        max_length=50,
        unique=True,
        help_text="Nombre del estado (ej: Operativo, En Mantención, En Reparación)"
    )

    class Meta:
        db_table = 'Tbl_Estados_Activo'
        verbose_name = 'Estado de Activo'
        verbose_name_plural = 'Estados de Activo'
        ordering = ['nombre_estado']

    def __str__(self):
        return self.nombre_estado



# ==============================================================================
# 4. ACTIVOS
# ==============================================================================

class Activo(models.Model):
    """
    Modelo central del sistema que representa un activo físico del hospital.

    Tabla: Tbl_Activos

    Características:
    - Código de inventario único
    - Número de serie único
    - Relaciones con tipo, estado y ubicación usando db_column
    - Trazabilidad completa de movimientos
    """

    codigo_inventario = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        help_text="Código único de inventario del activo (ej: ACT-2024-001)"
    )

    numero_serie = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text="Número de serie del fabricante (único por activo)"
    )

    marca = models.CharField(
        max_length=100,
        help_text="Marca o fabricante del activo (ej: HP, Dell, Samsung)"
    )

    modelo = models.CharField(
        max_length=100,
        help_text="Modelo específico del activo (ej: EliteBook 840 G8)"
    )

    fecha_alta = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora de registro del activo en el sistema"
    )

    # Foreign Keys con db_column para coincidir con el diseño
    tipo = models.ForeignKey(
        TipoEquipo,
        on_delete=models.PROTECT,
        related_name='activos',
        db_column='fk_id_tipo',
        help_text="Tipo de equipo al que pertenece este activo. PROTECT evita eliminar tipos con activos asociados"
    )

    estado = models.ForeignKey(
        EstadoActivo,
        on_delete=models.PROTECT,
        related_name='activos',
        db_column='fk_id_estado',
        help_text="Estado actual del activo. PROTECT evita eliminar estados con activos asociados"
    )

    ubicacion_actual = models.ForeignKey(
        Ubicacion,
        on_delete=models.PROTECT,
        related_name='activos_actuales',
        db_column='fk_id_ubicacion_actual',
        help_text="Ubicación en tiempo real del activo. CRÍTICO para trazabilidad"
    )

    class Meta:
        db_table = 'Tbl_Activos'
        verbose_name = 'Activo'
        verbose_name_plural = 'Activos'
        ordering = ['-fecha_alta']
        indexes = [
            models.Index(fields=['codigo_inventario']),
            models.Index(fields=['numero_serie']),
            models.Index(fields=['fecha_alta']),
        ]

    def __str__(self):
        return f"{self.codigo_inventario} - {self.marca} {self.modelo}"

    def get_ubicacion_completa(self):
        """Retorna la ubicación completa del activo incluyendo departamento."""
        return f"{self.ubicacion_actual.nombre_ubicacion} ({self.ubicacion_actual.departamento.nombre_departamento})"


# ==============================================================================
# 5. HISTORIAL (TRAZABILIDAD)
# ==============================================================================

class HistorialMovimiento(models.Model):
    """
    Modelo para registrar todos los movimientos de activos entre ubicaciones.

    Tabla: Tbl_Historial_Movimientos

    Características:
    - Trazabilidad completa de cada movimiento
    - Registro de usuario que realizó el movimiento
    - Ubicación origen y destino con db_column
    - Tipo de movimiento y comentarios
    """

    TIPOS_MOVIMIENTO = [
        ('TRASLADO', 'Traslado'),
        ('ASIGNACION', 'Asignación'),
        ('DEVOLUCION', 'Devolución'),
        ('MANTENIMIENTO', 'Envío a Mantenimiento'),
        ('RETORNO', 'Retorno de Mantenimiento'),
        ('BAJA', 'Baja de Activo'),
    ]

    activo = models.ForeignKey(
        Activo,
        on_delete=models.PROTECT,
        related_name='historial_movimientos',
        db_column='fk_id_activo',
        help_text="Activo que fue movido. PROTECT evita eliminar activos con historial"
    )

    usuario_registra = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        related_name='movimientos_registrados',
        db_column='fk_id_usuario_registra',
        help_text="Usuario que registró el movimiento. PROTECT evita eliminar usuarios con movimientos registrados"
    )

    ubicacion_origen = models.ForeignKey(
        Ubicacion,
        on_delete=models.PROTECT,
        related_name='movimientos_origen',
        db_column='fk_id_ubicacion_origen',
        help_text="Ubicación desde donde se movió el activo. PROTECT mantiene integridad del historial"
    )

    ubicacion_destino = models.ForeignKey(
        Ubicacion,
        on_delete=models.PROTECT,
        related_name='movimientos_destino',
        db_column='fk_id_ubicacion_destino',
        help_text="Ubicación hacia donde se movió el activo. PROTECT mantiene integridad del historial"
    )

    fecha_movimiento = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text="Fecha y hora exacta del movimiento (se registra automáticamente)"
    )

    tipo_movimiento = models.CharField(
        max_length=30,
        choices=TIPOS_MOVIMIENTO,
        default='TRASLADO',
        help_text="Tipo de movimiento realizado"
    )

    comentarios = models.TextField(
        null=True,
        blank=True,
        help_text="Comentarios o motivo del movimiento"
    )

    class Meta:
        db_table = 'Tbl_Historial_Movimientos'
        verbose_name = 'Historial de Movimiento'
        verbose_name_plural = 'Historial de Movimientos'
        ordering = ['-fecha_movimiento']
        indexes = [
            models.Index(fields=['fecha_movimiento']),
            models.Index(fields=['-fecha_movimiento']),
        ]

    def __str__(self):
        return f"{self.activo.codigo_inventario} - {self.tipo_movimiento} - {self.fecha_movimiento.strftime('%Y-%m-%d %H:%M')}"

    def get_descripcion_completa(self):
        """Retorna una descripción completa del movimiento."""
        return (
            f"{self.tipo_movimiento}: {self.activo.codigo_inventario} "
            f"desde {self.ubicacion_origen.nombre_ubicacion} "
            f"hacia {self.ubicacion_destino.nombre_ubicacion} "
            f"por {self.usuario_registra.username}"
        )


# ==============================================================================
# 6. AUDITORÍA (LOGS)
# ==============================================================================

class AuditoriaLog(models.Model):
    """
    Modelo para registrar todas las acciones de auditoría del sistema.

    Tabla: Tbl_Auditoria_Logs

    IMPORTANTE: Este modelo reemplaza la necesidad de MongoDB.
    Usa JSONField de PostgreSQL para almacenar detalles flexibles de las acciones.

    Características:
    - Registro de todas las acciones críticas del sistema
    - Usuario que realizó la acción con db_column
    - Timestamp automático
    - Detalles flexibles en formato JSON
    """

    TIPOS_ACCION = [
        ('CREATE', 'Creación'),
        ('UPDATE', 'Actualización'),
        ('DELETE', 'Eliminación'),
        ('LOGIN', 'Inicio de Sesión'),
        ('LOGOUT', 'Cierre de Sesión'),
        ('EXPORT', 'Exportación de Datos'),
        ('IMPORT', 'Importación de Datos'),
        ('VIEW', 'Visualización'),
        ('OTHER', 'Otra Acción'),
    ]

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='acciones_auditoria',
        db_column='fk_id_usuario',
        help_text="Usuario que realizó la acción. SET_NULL permite mantener el log aunque se elimine el usuario"
    )

    accion = models.CharField(
        max_length=50,
        choices=TIPOS_ACCION,
        db_index=True,
        help_text="Tipo de acción realizada en el sistema"
    )

    detalle_accion = models.JSONField(
        default=dict,
        blank=True,
        help_text=(
            "Detalles flexibles de la acción en formato JSON. "
            "Puede incluir: modelo afectado, ID del objeto, campos modificados, "
            "valores anteriores y nuevos, IP del usuario, etc."
        )
    )

    timestamp = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text="Fecha y hora exacta de la acción (se registra automáticamente)"
    )

    class Meta:
        db_table = 'Tbl_Auditoria_Logs'
        verbose_name = 'Log de Auditoría'
        verbose_name_plural = 'Logs de Auditoría'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['accion', '-timestamp']),
        ]

    def __str__(self):
        usuario_str = self.usuario.username if self.usuario else 'Usuario Eliminado'
        return f"{self.accion} - {usuario_str} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"

    @classmethod
    def registrar_accion(cls, usuario, accion, detalle=None):
        """
        Método de clase para registrar fácilmente una acción de auditoría.

        Uso:
            AuditoriaLog.registrar_accion(
                usuario=request.user,
                accion='CREATE',
                detalle={'modelo': 'Activo', 'objeto_id': 'ACT-2024-001'}
            )
        """
        return cls.objects.create(
            usuario=usuario,
            accion=accion,
            detalle_accion=detalle or {}
        )

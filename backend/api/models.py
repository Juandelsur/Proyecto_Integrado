"""
Modelos de datos para el Sistema de Control de Activos (SCA) Hospital.

Este módulo contiene todos los modelos de la base de datos PostgreSQL:
- Gestión de Usuarios y Roles
- Ubicaciones y Departamentos
- Maestros de Activos (Tipos y Estados)
- Activos (Entidad Central)
- Trazabilidad (Historial de Movimientos)
- Auditoría (Logs de acciones)

Características:
- Integridad referencial con PROTECT para evitar borrados accidentales
- Documentación completa para generación automática de OpenAPI/Swagger
- JSONField para logs de auditoría flexibles (reemplazo de MongoDB)
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# ==============================================================================
# 1. GESTIÓN DE USUARIOS Y ROLES
# ==============================================================================

class Rol(models.Model):
    """
    Modelo para definir roles de usuario en el sistema.

    Ejemplos de roles:
    - Administrador
    - Técnico
    - Supervisor
    - Usuario de Consulta
    """

    nombre_rol = models.CharField(
        max_length=50,
        unique=True,
        help_text="Nombre del rol (ej: Administrador, Técnico, Supervisor)"
    )

    descripcion = models.TextField(
        blank=True,
        null=True,
        help_text="Descripción detallada de los permisos y responsabilidades del rol"
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora de creación del rol"
    )

    activo = models.BooleanField(
        default=True,
        help_text="Indica si el rol está activo en el sistema"
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

    Agrega funcionalidad específica del negocio:
    - Relación con Rol
    - Campos adicionales para el hospital

    Hereda de AbstractUser:
    - username, email, password
    - first_name, last_name
    - is_staff, is_active, is_superuser
    - date_joined, last_login
    """

    fk_id_rol = models.ForeignKey(
        Rol,
        on_delete=models.PROTECT,
        related_name='usuarios',
        null=True,
        blank=True,
        help_text="Rol asignado al usuario. PROTECT evita eliminar roles con usuarios asignados"
    )

    rut = models.CharField(
        max_length=12,
        unique=True,
        null=True,
        blank=True,
        help_text="RUT del usuario (formato: 12345678-9)"
    )

    telefono = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text="Teléfono de contacto del usuario"
    )

    cargo = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Cargo o posición del usuario en el hospital"
    )

    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        help_text="Fecha y hora de la última actualización del perfil"
    )

    class Meta:
        db_table = 'Tbl_Usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['username']

    def __str__(self):
        return f"{self.get_full_name()} ({self.username})" if self.get_full_name() else self.username

    def get_rol_nombre(self):
        """Retorna el nombre del rol del usuario o 'Sin Rol' si no tiene."""
        return self.fk_id_rol.nombre_rol if self.fk_id_rol else 'Sin Rol'


# ==============================================================================
# 2. UBICACIONES Y DEPARTAMENTOS
# ==============================================================================

class Departamento(models.Model):
    """
    Modelo para representar departamentos o áreas del hospital.

    Ejemplos:
    - Urgencias
    - Pabellón
    - UCI
    - Radiología
    - Administración
    """

    nombre_departamento = models.CharField(
        max_length=100,
        unique=True,
        help_text="Nombre del departamento o área del hospital"
    )

    codigo_departamento = models.CharField(
        max_length=20,
        unique=True,
        help_text="Código único del departamento (ej: URG, PAB, UCI)"
    )

    descripcion = models.TextField(
        blank=True,
        null=True,
        help_text="Descripción del departamento y sus funciones"
    )

    responsable = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Nombre del responsable o jefe del departamento"
    )

    activo = models.BooleanField(
        default=True,
        help_text="Indica si el departamento está activo"
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha de creación del registro"
    )

    class Meta:
        db_table = 'Tbl_Departamentos'
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
        ordering = ['nombre_departamento']

    def __str__(self):
        return f"{self.codigo_departamento} - {self.nombre_departamento}"


class Ubicacion(models.Model):
    """
    Modelo para representar ubicaciones específicas dentro de los departamentos.

    Ejemplos:
    - Sala 101 (dentro de Urgencias)
    - Box 3 (dentro de Pabellón)
    - Oficina Administración (dentro de Administración)
    """

    nombre_ubicacion = models.CharField(
        max_length=100,
        help_text="Nombre específico de la ubicación (ej: Sala 101, Box 3)"
    )

    fk_departamento = models.ForeignKey(
        Departamento,
        on_delete=models.PROTECT,
        related_name='ubicaciones',
        help_text="Departamento al que pertenece esta ubicación. PROTECT evita eliminar departamentos con ubicaciones"
    )

    codigo_ubicacion = models.CharField(
        max_length=20,
        unique=True,
        help_text="Código único de la ubicación (ej: URG-101, PAB-B3)"
    )

    descripcion = models.TextField(
        blank=True,
        null=True,
        help_text="Descripción adicional de la ubicación"
    )

    piso = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text="Piso o nivel donde se encuentra la ubicación"
    )

    capacidad_activos = models.IntegerField(
        null=True,
        blank=True,
        help_text="Capacidad máxima de activos que puede albergar esta ubicación"
    )

    activo = models.BooleanField(
        default=True,
        help_text="Indica si la ubicación está activa y disponible"
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha de creación del registro"
    )

    class Meta:
        db_table = 'Tbl_Ubicaciones'
        verbose_name = 'Ubicación'
        verbose_name_plural = 'Ubicaciones'
        ordering = ['fk_departamento', 'nombre_ubicacion']
        unique_together = [['nombre_ubicacion', 'fk_departamento']]

    def __str__(self):
        return f"{self.codigo_ubicacion} - {self.nombre_ubicacion} ({self.fk_departamento.nombre_departamento})"

    def get_nombre_completo(self):
        """Retorna el nombre completo de la ubicación incluyendo el departamento."""
        return f"{self.fk_departamento.nombre_departamento} / {self.nombre_ubicacion}"


# ==============================================================================
# 3. MAESTROS DE ACTIVOS
# ==============================================================================

class TipoEquipo(models.Model):
    """
    Modelo para clasificar los tipos de equipos/activos.

    Ejemplos:
    - Monitor
    - PC/Computador
    - Impresora
    - Equipo Médico
    - Mobiliario
    """

    nombre_tipo = models.CharField(
        max_length=100,
        unique=True,
        help_text="Nombre del tipo de equipo (ej: Monitor, PC, Impresora)"
    )

    codigo_tipo = models.CharField(
        max_length=20,
        unique=True,
        help_text="Código único del tipo de equipo (ej: MON, PC, IMP)"
    )

    descripcion = models.TextField(
        blank=True,
        null=True,
        help_text="Descripción del tipo de equipo y sus características"
    )

    requiere_mantenimiento = models.BooleanField(
        default=True,
        help_text="Indica si este tipo de equipo requiere mantenimiento periódico"
    )

    vida_util_anos = models.IntegerField(
        null=True,
        blank=True,
        help_text="Vida útil estimada del equipo en años"
    )

    activo = models.BooleanField(
        default=True,
        help_text="Indica si el tipo de equipo está activo en el sistema"
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha de creación del registro"
    )

    class Meta:
        db_table = 'Tbl_Tipos_Equipo'
        verbose_name = 'Tipo de Equipo'
        verbose_name_plural = 'Tipos de Equipo'
        ordering = ['nombre_tipo']

    def __str__(self):
        return f"{self.codigo_tipo} - {self.nombre_tipo}"



class EstadoActivo(models.Model):
    """
    Modelo para definir los estados posibles de un activo.

    Ejemplos:
    - Operativo
    - En Mantención
    - En Reparación
    - De Baja
    - En Tránsito
    """

    nombre_estado = models.CharField(
        max_length=50,
        unique=True,
        help_text="Nombre del estado del activo (ej: Operativo, En Mantención)"
    )

    codigo_estado = models.CharField(
        max_length=20,
        unique=True,
        help_text="Código único del estado (ej: OPE, MAN, REP, BAJA)"
    )

    descripcion = models.TextField(
        blank=True,
        null=True,
        help_text="Descripción del estado y sus implicaciones"
    )

    permite_uso = models.BooleanField(
        default=True,
        help_text="Indica si el activo puede ser usado cuando está en este estado"
    )

    color_hex = models.CharField(
        max_length=7,
        blank=True,
        null=True,
        help_text="Color hexadecimal para representar el estado en la UI (ej: #00FF00)"
    )

    activo = models.BooleanField(
        default=True,
        help_text="Indica si el estado está activo en el sistema"
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha de creación del registro"
    )

    class Meta:
        db_table = 'Tbl_Estados_Activo'
        verbose_name = 'Estado de Activo'
        verbose_name_plural = 'Estados de Activo'
        ordering = ['nombre_estado']

    def __str__(self):
        return f"{self.codigo_estado} - {self.nombre_estado}"


# ==============================================================================
# 4. ACTIVOS (ENTIDAD CENTRAL)
# ==============================================================================

class Activo(models.Model):
    """
    Modelo central del sistema que representa un activo físico del hospital.

    Características:
    - Código de inventario único
    - Número de serie único
    - Relaciones con tipo, estado y ubicación
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

    descripcion = models.TextField(
        blank=True,
        null=True,
        help_text="Descripción detallada del activo y sus características"
    )

    # Foreign Keys con PROTECT para integridad referencial
    fk_tipo_equipo = models.ForeignKey(
        TipoEquipo,
        on_delete=models.PROTECT,
        related_name='activos',
        help_text="Tipo de equipo al que pertenece este activo. PROTECT evita eliminar tipos con activos asociados"
    )

    fk_estado = models.ForeignKey(
        EstadoActivo,
        on_delete=models.PROTECT,
        related_name='activos',
        help_text="Estado actual del activo. PROTECT evita eliminar estados con activos asociados"
    )

    fk_ubicacion_actual = models.ForeignKey(
        Ubicacion,
        on_delete=models.PROTECT,
        related_name='activos_actuales',
        help_text="Ubicación en tiempo real del activo. CRÍTICO para trazabilidad. PROTECT evita eliminar ubicaciones con activos"
    )

    # Campos adicionales
    fecha_adquisicion = models.DateField(
        null=True,
        blank=True,
        help_text="Fecha de adquisición o compra del activo"
    )

    valor_adquisicion = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Valor de adquisición del activo en pesos chilenos"
    )

    proveedor = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Nombre del proveedor o empresa que vendió el activo"
    )

    garantia_meses = models.IntegerField(
        null=True,
        blank=True,
        help_text="Duración de la garantía en meses"
    )

    fecha_vencimiento_garantia = models.DateField(
        null=True,
        blank=True,
        help_text="Fecha de vencimiento de la garantía"
    )

    observaciones = models.TextField(
        blank=True,
        null=True,
        help_text="Observaciones adicionales sobre el activo"
    )

    activo = models.BooleanField(
        default=True,
        help_text="Indica si el activo está activo en el sistema"
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha de creación del registro en el sistema"
    )

    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        help_text="Fecha de la última actualización del registro"
    )

    class Meta:
        db_table = 'Tbl_Activos'
        verbose_name = 'Activo'
        verbose_name_plural = 'Activos'
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['codigo_inventario']),
            models.Index(fields=['numero_serie']),
            models.Index(fields=['fk_ubicacion_actual']),
            models.Index(fields=['fk_estado']),
        ]

    def __str__(self):
        return f"{self.codigo_inventario} - {self.marca} {self.modelo}"

    def get_nombre_completo(self):
        """Retorna el nombre completo del activo con todos sus detalles."""
        return f"{self.fk_tipo_equipo.nombre_tipo} {self.marca} {self.modelo} ({self.codigo_inventario})"

    def esta_en_garantia(self):
        """Verifica si el activo está actualmente en garantía."""
        if self.fecha_vencimiento_garantia:
            return timezone.now().date() <= self.fecha_vencimiento_garantia
        return False

    def get_ubicacion_completa(self):
        """Retorna la ubicación completa del activo incluyendo departamento."""
        return self.fk_ubicacion_actual.get_nombre_completo()



# ==============================================================================
# 5. TRAZABILIDAD (TRANSACCIONAL)
# ==============================================================================

class HistorialMovimiento(models.Model):
    """
    Modelo para registrar todos los movimientos de activos entre ubicaciones.

    Características:
    - Trazabilidad completa de cada movimiento
    - Registro de usuario que realizó el movimiento
    - Ubicación origen y destino
    - Tipo de movimiento (traslado, asignación, devolución, etc.)
    - Timestamp automático
    """

    TIPOS_MOVIMIENTO = [
        ('TRASLADO', 'Traslado'),
        ('ASIGNACION', 'Asignación'),
        ('DEVOLUCION', 'Devolución'),
        ('MANTENIMIENTO', 'Envío a Mantenimiento'),
        ('RETORNO_MANTENIMIENTO', 'Retorno de Mantenimiento'),
        ('BAJA', 'Baja de Activo'),
        ('REUBICACION', 'Reubicación'),
    ]

    fk_activo = models.ForeignKey(
        Activo,
        on_delete=models.PROTECT,
        related_name='historial_movimientos',
        help_text="Activo que fue movido. PROTECT evita eliminar activos con historial"
    )

    fk_usuario_registra = models.ForeignKey(
        'Usuario',
        on_delete=models.PROTECT,
        related_name='movimientos_registrados',
        help_text="Usuario que registró el movimiento. PROTECT evita eliminar usuarios con movimientos registrados"
    )

    fk_ubicacion_origen = models.ForeignKey(
        Ubicacion,
        on_delete=models.PROTECT,
        related_name='movimientos_origen',
        help_text="Ubicación desde donde se movió el activo. PROTECT mantiene integridad del historial"
    )

    fk_ubicacion_destino = models.ForeignKey(
        Ubicacion,
        on_delete=models.PROTECT,
        related_name='movimientos_destino',
        help_text="Ubicación hacia donde se movió el activo. PROTECT mantiene integridad del historial"
    )

    tipo_movimiento = models.CharField(
        max_length=30,
        choices=TIPOS_MOVIMIENTO,
        default='TRASLADO',
        help_text="Tipo de movimiento realizado"
    )

    fecha_movimiento = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text="Fecha y hora exacta del movimiento (se registra automáticamente)"
    )

    motivo = models.TextField(
        blank=True,
        null=True,
        help_text="Motivo o razón del movimiento"
    )

    observaciones = models.TextField(
        blank=True,
        null=True,
        help_text="Observaciones adicionales sobre el movimiento"
    )

    documento_referencia = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Número de documento de referencia (orden de trabajo, ticket, etc.)"
    )

    class Meta:
        db_table = 'Tbl_Historial_Movimientos'
        verbose_name = 'Historial de Movimiento'
        verbose_name_plural = 'Historial de Movimientos'
        ordering = ['-fecha_movimiento']
        indexes = [
            models.Index(fields=['fk_activo', '-fecha_movimiento']),
            models.Index(fields=['fecha_movimiento']),
            models.Index(fields=['fk_usuario_registra']),
        ]

    def __str__(self):
        return f"{self.fk_activo.codigo_inventario} - {self.tipo_movimiento} - {self.fecha_movimiento.strftime('%Y-%m-%d %H:%M')}"

    def get_descripcion_completa(self):
        """Retorna una descripción completa del movimiento."""
        return (
            f"{self.tipo_movimiento}: {self.fk_activo.codigo_inventario} "
            f"desde {self.fk_ubicacion_origen.nombre_ubicacion} "
            f"hacia {self.fk_ubicacion_destino.nombre_ubicacion} "
            f"por {self.fk_usuario_registra.get_full_name()}"
        )


# ==============================================================================
# 6. AUDITORÍA (REEMPLAZO DE MONGODB)
# ==============================================================================

class AuditoriaLog(models.Model):
    """
    Modelo para registrar todas las acciones de auditoría del sistema.

    IMPORTANTE: Este modelo reemplaza la necesidad de MongoDB.
    Usa JSONField de PostgreSQL para almacenar detalles flexibles de las acciones.

    Características:
    - Registro de todas las acciones críticas del sistema
    - Usuario que realizó la acción (nullable por si se elimina el usuario)
    - Timestamp automático
    - Detalles flexibles en formato JSON
    - Trazabilidad completa para auditorías
    """

    TIPOS_ACCION = [
        ('CREATE', 'Creación'),
        ('UPDATE', 'Actualización'),
        ('DELETE', 'Eliminación'),
        ('LOGIN', 'Inicio de Sesión'),
        ('LOGOUT', 'Cierre de Sesión'),
        ('EXPORT', 'Exportación de Datos'),
        ('IMPORT', 'Importación de Datos'),
        ('PRINT', 'Impresión'),
        ('VIEW', 'Visualización'),
        ('DOWNLOAD', 'Descarga'),
        ('UPLOAD', 'Carga'),
        ('CHANGE_PASSWORD', 'Cambio de Contraseña'),
        ('PERMISSION_CHANGE', 'Cambio de Permisos'),
        ('CONFIG_CHANGE', 'Cambio de Configuración'),
        ('REPORT_GENERATE', 'Generación de Reporte'),
        ('OTHER', 'Otra Acción'),
    ]

    fk_usuario = models.ForeignKey(
        'Usuario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='acciones_auditoria',
        help_text="Usuario que realizó la acción. SET_NULL permite mantener el log aunque se elimine el usuario"
    )

    accion = models.CharField(
        max_length=50,
        choices=TIPOS_ACCION,
        db_index=True,
        help_text="Tipo de acción realizada en el sistema"
    )

    timestamp = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text="Fecha y hora exacta de la acción (se registra automáticamente)"
    )

    detalle_accion = models.JSONField(
        default=dict,
        blank=True,
        help_text=(
            "Detalles flexibles de la acción en formato JSON. "
            "Puede incluir: modelo afectado, ID del objeto, campos modificados, "
            "valores anteriores y nuevos, IP del usuario, user agent, etc."
        )
    )

    modelo_afectado = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        db_index=True,
        help_text="Nombre del modelo/tabla afectado (ej: Activo, Usuario, Ubicacion)"
    )

    objeto_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="ID del objeto afectado (puede ser código de inventario, username, etc.)"
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        help_text="Dirección IP desde donde se realizó la acción"
    )

    user_agent = models.TextField(
        blank=True,
        null=True,
        help_text="User Agent del navegador/cliente que realizó la acción"
    )

    resultado = models.CharField(
        max_length=20,
        choices=[
            ('SUCCESS', 'Exitoso'),
            ('FAILED', 'Fallido'),
            ('PARTIAL', 'Parcial'),
        ],
        default='SUCCESS',
        help_text="Resultado de la acción"
    )

    mensaje_error = models.TextField(
        blank=True,
        null=True,
        help_text="Mensaje de error si la acción falló"
    )

    class Meta:
        db_table = 'Tbl_Auditoria_Logs'
        verbose_name = 'Log de Auditoría'
        verbose_name_plural = 'Logs de Auditoría'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['fk_usuario', '-timestamp']),
            models.Index(fields=['accion', '-timestamp']),
            models.Index(fields=['modelo_afectado', '-timestamp']),
        ]

    def __str__(self):
        usuario_str = self.fk_usuario.username if self.fk_usuario else 'Usuario Eliminado'
        return f"{self.accion} - {usuario_str} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"

    def get_descripcion_completa(self):
        """Retorna una descripción completa del log de auditoría."""
        usuario_str = self.fk_usuario.get_full_name() if self.fk_usuario else 'Usuario Eliminado'
        modelo_str = f" en {self.modelo_afectado}" if self.modelo_afectado else ""
        objeto_str = f" (ID: {self.objeto_id})" if self.objeto_id else ""
        return f"{self.get_accion_display()}{modelo_str}{objeto_str} por {usuario_str}"

    @classmethod
    def registrar_accion(cls, usuario, accion, detalle=None, modelo=None, objeto_id=None,
                        ip=None, user_agent=None, resultado='SUCCESS', error=None):
        """
        Método de clase para registrar fácilmente una acción de auditoría.

        Uso:
            AuditoriaLog.registrar_accion(
                usuario=request.user,
                accion='CREATE',
                detalle={'campo': 'valor'},
                modelo='Activo',
                objeto_id='ACT-2024-001'
            )
        """
        return cls.objects.create(
            fk_usuario=usuario,
            accion=accion,
            detalle_accion=detalle or {},
            modelo_afectado=modelo,
            objeto_id=objeto_id,
            ip_address=ip,
            user_agent=user_agent,
            resultado=resultado,
            mensaje_error=error
        )
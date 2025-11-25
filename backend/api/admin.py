"""
Configuración del panel de administración de Django para el SCA Hospital.

Este módulo registra todos los modelos en el admin de Django con
configuraciones personalizadas para mejorar la experiencia de administración.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
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
# GESTIÓN DE USUARIOS Y ROLES
# ==============================================================================

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    """Administración de Roles."""
    list_display = ['nombre_rol', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'fecha_creacion']
    search_fields = ['nombre_rol', 'descripcion']
    ordering = ['nombre_rol']
    readonly_fields = ['fecha_creacion']


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """Administración de Usuarios personalizada."""
    list_display = ['username', 'email', 'first_name', 'last_name', 'fk_id_rol', 'is_active', 'is_staff']
    list_filter = ['is_active', 'is_staff', 'is_superuser', 'fk_id_rol', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'rut']
    ordering = ['username']

    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {
            'fields': ('fk_id_rol', 'rut', 'telefono', 'cargo', 'fecha_actualizacion')
        }),
    )

    readonly_fields = ['date_joined', 'last_login', 'fecha_actualizacion']


# ==============================================================================
# UBICACIONES Y DEPARTAMENTOS
# ==============================================================================

@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    """Administración de Departamentos."""
    list_display = ['codigo_departamento', 'nombre_departamento', 'responsable', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'fecha_creacion']
    search_fields = ['nombre_departamento', 'codigo_departamento', 'responsable']
    ordering = ['nombre_departamento']
    readonly_fields = ['fecha_creacion']


@admin.register(Ubicacion)
class UbicacionAdmin(admin.ModelAdmin):
    """Administración de Ubicaciones."""
    list_display = ['codigo_ubicacion', 'nombre_ubicacion', 'fk_departamento', 'piso', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'fk_departamento', 'piso', 'fecha_creacion']
    search_fields = ['nombre_ubicacion', 'codigo_ubicacion', 'descripcion']
    ordering = ['fk_departamento', 'nombre_ubicacion']
    readonly_fields = ['fecha_creacion']
    autocomplete_fields = ['fk_departamento']


# ==============================================================================
# MAESTROS DE ACTIVOS
# ==============================================================================

@admin.register(TipoEquipo)
class TipoEquipoAdmin(admin.ModelAdmin):
    """Administración de Tipos de Equipo."""
    list_display = ['codigo_tipo', 'nombre_tipo', 'requiere_mantenimiento', 'vida_util_anos', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'requiere_mantenimiento', 'fecha_creacion']
    search_fields = ['nombre_tipo', 'codigo_tipo', 'descripcion']
    ordering = ['nombre_tipo']
    readonly_fields = ['fecha_creacion']


@admin.register(EstadoActivo)
class EstadoActivoAdmin(admin.ModelAdmin):
    """Administración de Estados de Activo."""
    list_display = ['codigo_estado', 'nombre_estado', 'permite_uso', 'color_hex', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'permite_uso', 'fecha_creacion']
    search_fields = ['nombre_estado', 'codigo_estado', 'descripcion']
    ordering = ['nombre_estado']
    readonly_fields = ['fecha_creacion']


# ==============================================================================
# ACTIVOS
# ==============================================================================

@admin.register(Activo)
class ActivoAdmin(admin.ModelAdmin):
    """Administración de Activos."""
    list_display = [
        'codigo_inventario',
        'numero_serie',
        'marca',
        'modelo',
        'fk_tipo_equipo',
        'fk_estado',
        'fk_ubicacion_actual',
        'activo',
        'fecha_creacion'
    ]
    list_filter = [
        'activo',
        'fk_tipo_equipo',
        'fk_estado',
        'fk_ubicacion_actual__fk_departamento',
        'fecha_creacion',
        'fecha_adquisicion'
    ]
    search_fields = [
        'codigo_inventario',
        'numero_serie',
        'marca',
        'modelo',
        'descripcion',
        'proveedor'
    ]
    ordering = ['-fecha_creacion']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    autocomplete_fields = ['fk_tipo_equipo', 'fk_estado', 'fk_ubicacion_actual']

    fieldsets = (
        ('Información Básica', {
            'fields': ('codigo_inventario', 'numero_serie', 'marca', 'modelo', 'descripcion')
        }),
        ('Clasificación', {
            'fields': ('fk_tipo_equipo', 'fk_estado', 'fk_ubicacion_actual')
        }),
        ('Información de Adquisición', {
            'fields': ('fecha_adquisicion', 'valor_adquisicion', 'proveedor')
        }),
        ('Garantía', {
            'fields': ('garantia_meses', 'fecha_vencimiento_garantia')
        }),
        ('Adicional', {
            'fields': ('observaciones', 'activo', 'fecha_creacion', 'fecha_actualizacion')
        }),
    )


# ==============================================================================
# TRAZABILIDAD
# ==============================================================================

@admin.register(HistorialMovimiento)
class HistorialMovimientoAdmin(admin.ModelAdmin):
    """Administración de Historial de Movimientos."""
    list_display = [
        'fk_activo',
        'tipo_movimiento',
        'fk_ubicacion_origen',
        'fk_ubicacion_destino',
        'fk_usuario_registra',
        'fecha_movimiento'
    ]
    list_filter = [
        'tipo_movimiento',
        'fecha_movimiento',
        'fk_ubicacion_origen__fk_departamento',
        'fk_ubicacion_destino__fk_departamento'
    ]
    search_fields = [
        'fk_activo__codigo_inventario',
        'fk_activo__numero_serie',
        'motivo',
        'observaciones',
        'documento_referencia'
    ]
    ordering = ['-fecha_movimiento']
    readonly_fields = ['fecha_movimiento']
    autocomplete_fields = ['fk_activo', 'fk_usuario_registra', 'fk_ubicacion_origen', 'fk_ubicacion_destino']

    fieldsets = (
        ('Información del Movimiento', {
            'fields': ('fk_activo', 'tipo_movimiento', 'fecha_movimiento')
        }),
        ('Ubicaciones', {
            'fields': ('fk_ubicacion_origen', 'fk_ubicacion_destino')
        }),
        ('Detalles', {
            'fields': ('fk_usuario_registra', 'motivo', 'observaciones', 'documento_referencia')
        }),
    )


# ==============================================================================
# AUDITORÍA
# ==============================================================================

@admin.register(AuditoriaLog)
class AuditoriaLogAdmin(admin.ModelAdmin):
    """Administración de Logs de Auditoría."""
    list_display = [
        'timestamp',
        'fk_usuario',
        'accion',
        'modelo_afectado',
        'objeto_id',
        'resultado',
        'ip_address'
    ]
    list_filter = [
        'accion',
        'resultado',
        'modelo_afectado',
        'timestamp'
    ]
    search_fields = [
        'fk_usuario__username',
        'modelo_afectado',
        'objeto_id',
        'ip_address',
        'mensaje_error'
    ]
    ordering = ['-timestamp']
    readonly_fields = ['timestamp', 'detalle_accion']

    fieldsets = (
        ('Información Básica', {
            'fields': ('timestamp', 'fk_usuario', 'accion', 'resultado')
        }),
        ('Objeto Afectado', {
            'fields': ('modelo_afectado', 'objeto_id')
        }),
        ('Detalles', {
            'fields': ('detalle_accion', 'mensaje_error')
        }),
        ('Información Técnica', {
            'fields': ('ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        """Los logs de auditoría no se crean manualmente."""
        return False

    def has_change_permission(self, request, obj=None):
        """Los logs de auditoría no se modifican."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Los logs de auditoría no se eliminan (solo superusuarios)."""
        return request.user.is_superuser

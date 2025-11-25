"""
Configuración del panel de administración de Django para el SCA Hospital.

Este módulo registra todos los modelos de 'core' en el admin de Django con
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
# ROLES Y USUARIOS
# ==============================================================================

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    """Administración de Roles."""
    list_display = ['nombre_rol', 'id']
    search_fields = ['nombre_rol']
    ordering = ['nombre_rol']


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """Administración de Usuarios personalizada."""
    list_display = ['username', 'nombre_completo', 'email', 'rol', 'is_active', 'is_staff']
    list_filter = ['is_active', 'is_staff', 'is_superuser', 'rol', 'date_joined']
    search_fields = ['username', 'email', 'nombre_completo']
    ordering = ['username']

    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {
            'fields': ('nombre_completo', 'rol')
        }),
    )

    readonly_fields = ['date_joined', 'last_login']


# ==============================================================================
# UBICACIONES
# ==============================================================================

@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    """Administración de Departamentos."""
    list_display = ['nombre_departamento', 'id']
    search_fields = ['nombre_departamento']
    ordering = ['nombre_departamento']


@admin.register(Ubicacion)
class UbicacionAdmin(admin.ModelAdmin):
    """Administración de Ubicaciones."""
    list_display = ['nombre_ubicacion', 'departamento', 'id']
    list_filter = ['departamento']
    search_fields = ['nombre_ubicacion']
    ordering = ['departamento', 'nombre_ubicacion']
    autocomplete_fields = ['departamento']


# ==============================================================================
# MAESTROS
# ==============================================================================

@admin.register(TipoEquipo)
class TipoEquipoAdmin(admin.ModelAdmin):
    """Administración de Tipos de Equipo."""
    list_display = ['nombre_tipo', 'id']
    search_fields = ['nombre_tipo']
    ordering = ['nombre_tipo']


@admin.register(EstadoActivo)
class EstadoActivoAdmin(admin.ModelAdmin):
    """Administración de Estados de Activo."""
    list_display = ['nombre_estado', 'id']
    search_fields = ['nombre_estado']
    ordering = ['nombre_estado']


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
        'tipo',
        'estado',
        'ubicacion_actual',
        'fecha_alta'
    ]
    list_filter = ['tipo', 'estado', 'ubicacion_actual__departamento', 'fecha_alta']
    search_fields = ['codigo_inventario', 'numero_serie', 'marca', 'modelo']
    ordering = ['-fecha_alta']
    readonly_fields = ['fecha_alta']
    autocomplete_fields = ['tipo', 'estado', 'ubicacion_actual']

    fieldsets = (
        ('Información Básica', {
            'fields': ('codigo_inventario', 'numero_serie', 'marca', 'modelo')
        }),
        ('Clasificación', {
            'fields': ('tipo', 'estado', 'ubicacion_actual')
        }),
        ('Fechas', {
            'fields': ('fecha_alta',)
        }),
    )


# ==============================================================================
# TRAZABILIDAD
# ==============================================================================

@admin.register(HistorialMovimiento)
class HistorialMovimientoAdmin(admin.ModelAdmin):
    """Administración de Historial de Movimientos."""
    list_display = [
        'activo',
        'tipo_movimiento',
        'ubicacion_origen',
        'ubicacion_destino',
        'usuario_registra',
        'fecha_movimiento'
    ]
    list_filter = ['tipo_movimiento', 'fecha_movimiento', 'ubicacion_origen__departamento', 'ubicacion_destino__departamento']
    search_fields = ['activo__codigo_inventario', 'activo__numero_serie', 'comentarios']
    ordering = ['-fecha_movimiento']
    readonly_fields = ['fecha_movimiento']
    autocomplete_fields = ['activo', 'usuario_registra', 'ubicacion_origen', 'ubicacion_destino']

    fieldsets = (
        ('Información del Movimiento', {
            'fields': ('activo', 'tipo_movimiento', 'fecha_movimiento')
        }),
        ('Ubicaciones', {
            'fields': ('ubicacion_origen', 'ubicacion_destino')
        }),
        ('Detalles', {
            'fields': ('usuario_registra', 'comentarios')
        }),
    )


# ==============================================================================
# AUDITORÍA
# ==============================================================================

@admin.register(AuditoriaLog)
class AuditoriaLogAdmin(admin.ModelAdmin):
    """Administración de Logs de Auditoría."""
    list_display = ['timestamp', 'usuario', 'accion', 'id']
    list_filter = ['accion', 'timestamp']
    search_fields = ['usuario__username', 'detalle_accion']
    ordering = ['-timestamp']
    readonly_fields = ['timestamp', 'detalle_accion']

    fieldsets = (
        ('Información Básica', {
            'fields': ('timestamp', 'usuario', 'accion')
        }),
        ('Detalles', {
            'fields': ('detalle_accion',)
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

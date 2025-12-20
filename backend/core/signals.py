# core/signals.py
"""
Sistema de Auditoría Automática
Registra todas las acciones CRUD en AuditoriaLog
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out

# Importar tus modelos (ajusta según tus nombres exactos)
from .models import (
    Activo, 
    Usuario, 
    Ubicacion, 
    Departamento,
    HistorialMovimiento,
    AuditoriaLog,
    # Agrega otros modelos que quieras auditar
)


# ============================================================================
# HELPERS
# ============================================================================

def get_current_user():
    """
    Obtiene el usuario actual del thread-local storage
    Retorna None si no hay usuario (ej: operaciones del sistema)
    """
    from .middleware import get_current_request
    request = get_current_request()
    if request and hasattr(request, 'user') and request.user.is_authenticated:
        return request.user
    return None


def crear_detalle_auditoria(instance, accion):
    """
    Crea el objeto de detalle para la auditoría con información relevante
    """
    detalle = {
        'modelo': instance.__class__.__name__,
        'objeto_id': instance.pk,
        'accion': accion,
    }
    
    # Agregar campos específicos según el modelo
    if isinstance(instance, Activo):
        detalle.update({
            'codigo_inventario': instance.codigo_inventario,
            'marca': instance.marca,
            'modelo': instance.modelo,
            'tipo': instance.tipo.nombre_tipo if instance.tipo else None,
        })
    
    elif isinstance(instance, Usuario):
        detalle.update({
            'username': instance.username,
            'email': instance.email,
            'nombre_completo': f"{instance.first_name} {instance.last_name}".strip(),
        })
    
    elif isinstance(instance, Departamento):
        detalle.update({
            'nombre': instance.nombre_departamento,
        })
    
    elif isinstance(instance, Ubicacion):
        detalle.update({
            'nombre': instance.nombre_ubicacion,
            'departamento': instance.departamento.nombre_departamento if instance.departamento else None,
        })
    
    elif isinstance(instance, HistorialMovimiento):
        detalle.update({
            'activo': instance.activo.codigo_inventario if instance.activo else None,
            'ubicacion_origen': instance.ubicacion_origen.nombre_ubicacion if instance.ubicacion_origen else None,
            'ubicacion_destino': instance.ubicacion_destino.nombre_ubicacion if instance.ubicacion_destino else None,
        })
    
    return detalle


# ============================================================================
# SIGNALS PARA ACTIVOS
# ============================================================================

@receiver(post_save, sender=Activo)
def auditar_activo_guardado(sender, instance, created, **kwargs):
    """
    Registra cuando se crea o actualiza un activo
    """
    # Evitar recursión infinita
    if kwargs.get('raw', False):
        return
    
    accion = 'CREATE' if created else 'UPDATE'
    usuario = get_current_user()
    detalle = crear_detalle_auditoria(instance, accion)
    
    AuditoriaLog.registrar_accion(
        usuario=usuario,
        accion=accion,
        detalle=detalle
    )


@receiver(post_delete, sender=Activo)
def auditar_activo_eliminado(sender, instance, **kwargs):
    """
    Registra cuando se elimina un activo
    """
    usuario = get_current_user()
    detalle = crear_detalle_auditoria(instance, 'DELETE')
    
    AuditoriaLog.registrar_accion(
        usuario=usuario,
        accion='DELETE',
        detalle=detalle
    )


# ============================================================================
# SIGNALS PARA USUARIOS
# ============================================================================

@receiver(post_save, sender=Usuario)
def auditar_usuario_guardado(sender, instance, created, **kwargs):
    """
    Registra cuando se crea o actualiza un usuario
    """
    if kwargs.get('raw', False):
        return
    
    accion = 'CREATE' if created else 'UPDATE'
    usuario = get_current_user()
    detalle = crear_detalle_auditoria(instance, accion)
    
    AuditoriaLog.registrar_accion(
        usuario=usuario,
        accion=accion,
        detalle=detalle
    )


@receiver(post_delete, sender=Usuario)
def auditar_usuario_eliminado(sender, instance, **kwargs):
    """
    Registra cuando se elimina un usuario
    """
    usuario = get_current_user()
    detalle = crear_detalle_auditoria(instance, 'DELETE')
    
    AuditoriaLog.registrar_accion(
        usuario=usuario,
        accion='DELETE',
        detalle=detalle
    )


# ============================================================================
# SIGNALS PARA LOGIN/LOGOUT
# ============================================================================

@receiver(user_logged_in)
def auditar_login(sender, request, user, **kwargs):
    """
    Registra cuando un usuario inicia sesión
    """
    detalle = {
        'modelo': 'Usuario',
        'username': user.username,
        'ip_address': request.META.get('REMOTE_ADDR'),
        'user_agent': request.META.get('HTTP_USER_AGENT', '')[:200],
    }
    
    AuditoriaLog.registrar_accion(
        usuario=user,
        accion='LOGIN',
        detalle=detalle
    )


@receiver(user_logged_out)
def auditar_logout(sender, request, user, **kwargs):
    """
    Registra cuando un usuario cierra sesión
    """
    if user:
        detalle = {
            'modelo': 'Usuario',
            'username': user.username,
        }
        
        AuditoriaLog.registrar_accion(
            usuario=user,
            accion='LOGOUT',
            detalle=detalle
        )


# ============================================================================
# SIGNALS PARA DEPARTAMENTOS
# ============================================================================

@receiver(post_save, sender=Departamento)
def auditar_departamento_guardado(sender, instance, created, **kwargs):
    """
    Registra cuando se crea o actualiza un departamento
    """
    if kwargs.get('raw', False):
        return
    
    accion = 'CREATE' if created else 'UPDATE'
    usuario = get_current_user()
    detalle = crear_detalle_auditoria(instance, accion)
    
    AuditoriaLog.registrar_accion(
        usuario=usuario,
        accion=accion,
        detalle=detalle
    )


@receiver(post_delete, sender=Departamento)
def auditar_departamento_eliminado(sender, instance, **kwargs):
    """
    Registra cuando se elimina un departamento
    """
    usuario = get_current_user()
    detalle = crear_detalle_auditoria(instance, 'DELETE')
    
    AuditoriaLog.registrar_accion(
        usuario=usuario,
        accion='DELETE',
        detalle=detalle
    )


# ============================================================================
# SIGNALS PARA UBICACIONES
# ============================================================================

@receiver(post_save, sender=Ubicacion)
def auditar_ubicacion_guardada(sender, instance, created, **kwargs):
    """
    Registra cuando se crea o actualiza una ubicación
    """
    if kwargs.get('raw', False):
        return
    
    accion = 'CREATE' if created else 'UPDATE'
    usuario = get_current_user()
    detalle = crear_detalle_auditoria(instance, accion)
    
    AuditoriaLog.registrar_accion(
        usuario=usuario,
        accion=accion,
        detalle=detalle
    )


@receiver(post_delete, sender=Ubicacion)
def auditar_ubicacion_eliminada(sender, instance, **kwargs):
    """
    Registra cuando se elimina una ubicación
    """
    usuario = get_current_user()
    detalle = crear_detalle_auditoria(instance, 'DELETE')
    
    AuditoriaLog.registrar_accion(
        usuario=usuario,
        accion='DELETE',
        detalle=detalle
    )


# ============================================================================
# SIGNALS PARA MOVIMIENTOS DE ACTIVOS
# ============================================================================

@receiver(post_save, sender=HistorialMovimiento)
def auditar_movimiento_guardado(sender, instance, created, **kwargs):
    """
    Registra cuando se crea o actualiza un movimiento de activo
    """
    if kwargs.get('raw', False):
        return
    
    # Los movimientos generalmente solo se crean, no se actualizan
    accion = 'CREATE' if created else 'UPDATE'
    usuario = get_current_user()
    detalle = crear_detalle_auditoria(instance, accion)
    
    AuditoriaLog.registrar_accion(
        usuario=usuario,
        accion=accion,
        detalle=detalle
    )
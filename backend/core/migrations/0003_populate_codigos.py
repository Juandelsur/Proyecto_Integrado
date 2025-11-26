# Generated manually to populate existing records with codes

from django.db import migrations
import secrets
from datetime import datetime


def generar_codigo_qr():
    """Genera un código QR único en formato LOC-{HEX}."""
    hex_code = secrets.token_hex(3).upper()
    return f"LOC-{hex_code}"


def generar_codigo_inventario():
    """Genera un código de inventario único en formato INV-{YY}-{HEX}."""
    year = datetime.now().strftime('%y')
    hex_code = secrets.token_hex(3).upper()
    return f"INV-{year}-{hex_code}"


def populate_ubicacion_codigos(apps, schema_editor):
    """
    Pobla los códigos QR de las ubicaciones existentes.
    
    Esta función se ejecuta una sola vez durante la migración para asignar
    códigos QR únicos a todas las ubicaciones que no tienen uno.
    """
    Ubicacion = apps.get_model('core', 'Ubicacion')
    
    ubicaciones_sin_codigo = Ubicacion.objects.filter(codigo_qr__isnull=True)
    
    for ubicacion in ubicaciones_sin_codigo:
        # Generar código único con manejo de colisiones
        max_intentos = 100
        intentos = 0
        codigo_generado = None
        
        while intentos < max_intentos:
            codigo_candidato = generar_codigo_qr()
            
            # Verificar si el código ya existe
            if not Ubicacion.objects.filter(codigo_qr=codigo_candidato).exists():
                codigo_generado = codigo_candidato
                break
            
            intentos += 1
        
        if codigo_generado:
            ubicacion.codigo_qr = codigo_generado
            ubicacion.save(update_fields=['codigo_qr'])
        else:
            raise ValueError(
                f"No se pudo generar un código QR único para la ubicación {ubicacion.id} "
                f"después de {max_intentos} intentos."
            )


def populate_activo_codigos(apps, schema_editor):
    """
    Pobla los códigos de inventario de los activos existentes.
    
    Esta función se ejecuta una sola vez durante la migración para asignar
    códigos de inventario únicos a todos los activos que no tienen uno.
    """
    Activo = apps.get_model('core', 'Activo')
    
    activos_sin_codigo = Activo.objects.filter(codigo_inventario__isnull=True)
    
    for activo in activos_sin_codigo:
        # Generar código único con manejo de colisiones
        max_intentos = 100
        intentos = 0
        codigo_generado = None
        
        while intentos < max_intentos:
            codigo_candidato = generar_codigo_inventario()
            
            # Verificar si el código ya existe
            if not Activo.objects.filter(codigo_inventario=codigo_candidato).exists():
                codigo_generado = codigo_candidato
                break
            
            intentos += 1
        
        if codigo_generado:
            activo.codigo_inventario = codigo_generado
            activo.save(update_fields=['codigo_inventario'])
        else:
            raise ValueError(
                f"No se pudo generar un código de inventario único para el activo {activo.id} "
                f"después de {max_intentos} intentos."
            )


def reverse_populate(apps, schema_editor):
    """
    Función de reversión (no hace nada).
    
    No podemos revertir la asignación de códigos porque son generados aleatoriamente.
    Si se revierte la migración, los códigos simplemente quedarán en null.
    """
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_add_codigo_qr_and_update_codigo_inventario'),
    ]

    operations = [
        migrations.RunPython(populate_ubicacion_codigos, reverse_populate),
        migrations.RunPython(populate_activo_codigos, reverse_populate),
    ]


"""
Comando de Django para poblar la base de datos con datos de prueba.

Uso:
    python manage.py seed_data
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from api.models import (
    Rol, Usuario, Departamento, Ubicacion,
    TipoEquipo, EstadoActivo, Activo,
    HistorialMovimiento, AuditoriaLog
)


class Command(BaseCommand):
    help = 'Pobla la base de datos con datos de prueba para el SCA Hospital'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('🚀 Iniciando población de datos...'))
        
        # 1. Crear Roles
        self.stdout.write('📋 Creando Roles...')
        roles_data = [
            {'nombre_rol': 'Administrador', 'descripcion': 'Acceso total al sistema'},
            {'nombre_rol': 'Técnico', 'descripcion': 'Gestión de activos y movimientos'},
            {'nombre_rol': 'Supervisor', 'descripcion': 'Supervisión y reportes'},
            {'nombre_rol': 'Usuario Consulta', 'descripcion': 'Solo lectura'},
        ]
        roles = {}
        for data in roles_data:
            rol, created = Rol.objects.get_or_create(nombre_rol=data['nombre_rol'], defaults=data)
            roles[data['nombre_rol']] = rol
            if created:
                self.stdout.write(f'  ✅ Rol creado: {rol.nombre_rol}')
        
        # 2. Crear Departamentos
        self.stdout.write('🏥 Creando Departamentos...')
        departamentos_data = [
            {'nombre_departamento': 'Urgencias', 'codigo_departamento': 'URG', 'responsable': 'Dr. Juan Pérez'},
            {'nombre_departamento': 'Pabellón', 'codigo_departamento': 'PAB', 'responsable': 'Dra. María González'},
            {'nombre_departamento': 'UCI', 'codigo_departamento': 'UCI', 'responsable': 'Dr. Carlos Rojas'},
            {'nombre_departamento': 'Radiología', 'codigo_departamento': 'RAD', 'responsable': 'Dra. Ana Silva'},
            {'nombre_departamento': 'Administración', 'codigo_departamento': 'ADM', 'responsable': 'Sr. Pedro López'},
        ]
        departamentos = {}
        for data in departamentos_data:
            dept, created = Departamento.objects.get_or_create(
                codigo_departamento=data['codigo_departamento'],
                defaults=data
            )
            departamentos[data['codigo_departamento']] = dept
            if created:
                self.stdout.write(f'  ✅ Departamento creado: {dept.nombre_departamento}')
        
        # 3. Crear Ubicaciones
        self.stdout.write('📍 Creando Ubicaciones...')
        ubicaciones_data = [
            {'nombre_ubicacion': 'Sala 101', 'codigo_ubicacion': 'URG-101', 'fk_departamento': departamentos['URG'], 'piso': '1'},
            {'nombre_ubicacion': 'Sala 102', 'codigo_ubicacion': 'URG-102', 'fk_departamento': departamentos['URG'], 'piso': '1'},
            {'nombre_ubicacion': 'Box 1', 'codigo_ubicacion': 'PAB-B1', 'fk_departamento': departamentos['PAB'], 'piso': '2'},
            {'nombre_ubicacion': 'Box 2', 'codigo_ubicacion': 'PAB-B2', 'fk_departamento': departamentos['PAB'], 'piso': '2'},
            {'nombre_ubicacion': 'Sala UCI', 'codigo_ubicacion': 'UCI-S1', 'fk_departamento': departamentos['UCI'], 'piso': '3'},
            {'nombre_ubicacion': 'Sala Rayos X', 'codigo_ubicacion': 'RAD-RX', 'fk_departamento': departamentos['RAD'], 'piso': '1'},
            {'nombre_ubicacion': 'Oficina Principal', 'codigo_ubicacion': 'ADM-OF1', 'fk_departamento': departamentos['ADM'], 'piso': '1'},
        ]
        ubicaciones = {}
        for data in ubicaciones_data:
            ubic, created = Ubicacion.objects.get_or_create(
                codigo_ubicacion=data['codigo_ubicacion'],
                defaults=data
            )
            ubicaciones[data['codigo_ubicacion']] = ubic
            if created:
                self.stdout.write(f'  ✅ Ubicación creada: {ubic.nombre_ubicacion}')
        
        # 4. Crear Tipos de Equipo
        self.stdout.write('🔧 Creando Tipos de Equipo...')
        tipos_data = [
            {'nombre_tipo': 'Monitor', 'codigo_tipo': 'MON', 'vida_util_anos': 5},
            {'nombre_tipo': 'Computador', 'codigo_tipo': 'PC', 'vida_util_anos': 4},
            {'nombre_tipo': 'Impresora', 'codigo_tipo': 'IMP', 'vida_util_anos': 3},
            {'nombre_tipo': 'Equipo Médico', 'codigo_tipo': 'MED', 'vida_util_anos': 10},
            {'nombre_tipo': 'Mobiliario', 'codigo_tipo': 'MOB', 'vida_util_anos': 15, 'requiere_mantenimiento': False},
        ]
        tipos = {}
        for data in tipos_data:
            tipo, created = TipoEquipo.objects.get_or_create(
                codigo_tipo=data['codigo_tipo'],
                defaults=data
            )
            tipos[data['codigo_tipo']] = tipo
            if created:
                self.stdout.write(f'  ✅ Tipo creado: {tipo.nombre_tipo}')
        
        # 5. Crear Estados de Activo
        self.stdout.write('🎨 Creando Estados de Activo...')
        estados_data = [
            {'nombre_estado': 'Operativo', 'codigo_estado': 'OPE', 'permite_uso': True, 'color_hex': '#00FF00'},
            {'nombre_estado': 'En Mantención', 'codigo_estado': 'MAN', 'permite_uso': False, 'color_hex': '#FFA500'},
            {'nombre_estado': 'En Reparación', 'codigo_estado': 'REP', 'permite_uso': False, 'color_hex': '#FF0000'},
            {'nombre_estado': 'De Baja', 'codigo_estado': 'BAJA', 'permite_uso': False, 'color_hex': '#808080'},
            {'nombre_estado': 'En Tránsito', 'codigo_estado': 'TRA', 'permite_uso': False, 'color_hex': '#0000FF'},
        ]
        estados = {}
        for data in estados_data:
            estado, created = EstadoActivo.objects.get_or_create(
                codigo_estado=data['codigo_estado'],
                defaults=data
            )
            estados[data['codigo_estado']] = estado
            if created:
                self.stdout.write(f'  ✅ Estado creado: {estado.nombre_estado}')
        
        # 6. Crear Activos de ejemplo
        self.stdout.write('💻 Creando Activos de ejemplo...')
        activos_data = [
            {
                'codigo_inventario': 'ACT-2024-001',
                'numero_serie': 'MON-HP-001',
                'marca': 'HP',
                'modelo': 'EliteDisplay E243',
                'fk_tipo_equipo': tipos['MON'],
                'fk_estado': estados['OPE'],
                'fk_ubicacion_actual': ubicaciones['URG-101'],
                'valor_adquisicion': 250000,
            },
            {
                'codigo_inventario': 'ACT-2024-002',
                'numero_serie': 'PC-DELL-001',
                'marca': 'Dell',
                'modelo': 'OptiPlex 7090',
                'fk_tipo_equipo': tipos['PC'],
                'fk_estado': estados['OPE'],
                'fk_ubicacion_actual': ubicaciones['ADM-OF1'],
                'valor_adquisicion': 850000,
            },
        ]
        
        for data in activos_data:
            activo, created = Activo.objects.get_or_create(
                codigo_inventario=data['codigo_inventario'],
                defaults=data
            )
            if created:
                self.stdout.write(f'  ✅ Activo creado: {activo.codigo_inventario}')
        
        self.stdout.write(self.style.SUCCESS('\n✅ ¡Datos de prueba creados exitosamente!'))
        self.stdout.write(self.style.WARNING('\n📝 Nota: Crea un superusuario con: python manage.py createsuperuser'))


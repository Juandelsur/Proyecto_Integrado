"""
Comando personalizado de Django para poblar la base de datos con datos de prueba.

Este comando crea datos iniciales coherentes para el MVP del Sistema de Control
de Activos (SCA) Hospital.

CARACTERÍSTICAS:
- Verifica si la base de datos ya tiene datos antes de poblar
- Crea datos relacionados de forma coherente
- Usa transacciones para garantizar integridad
- Proporciona feedback detallado durante la ejecución

USO:
    python manage.py seed_data
    python manage.py seed_data --force  # Fuerza la creación incluso si hay datos

DATOS CREADOS:
- 2 Roles (Administrador, Técnico)
- 2 Usuarios (admin, juan)
- 2 Departamentos (Urgencias, Bodega Central)
- 4 Ubicaciones (Box 1, Box 2, Estante A, Estante B)
- 3 Tipos de Equipo (Monitor, Desfibrilador, Camilla)
- 3 Estados (Operativo, En Mantención, De Baja)
- 5 Activos variados distribuidos en diferentes ubicaciones
"""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.contrib.auth import get_user_model
from core.models import (
    Rol,
    Usuario,
    Departamento,
    Ubicacion,
    TipoEquipo,
    EstadoActivo,
    Activo
)

Usuario = get_user_model()


class Command(BaseCommand):
    """
    Comando para poblar la base de datos con datos de prueba.
    """
    
    help = 'Puebla la base de datos con datos de prueba para el MVP del SCA Hospital'
    
    def add_arguments(self, parser):
        """
        Agrega argumentos opcionales al comando.
        """
        parser.add_argument(
            '--force',
            action='store_true',
            help='Fuerza la creación de datos incluso si la base de datos ya tiene datos',
        )
    
    def handle(self, *args, **options):
        """
        Método principal que ejecuta el comando.
        """
        force = options.get('force', False)
        
        # ======================================================================
        # VERIFICACIÓN: ¿La base de datos ya tiene datos?
        # ======================================================================
        
        if not force and Usuario.objects.exists():
            self.stdout.write(
                self.style.WARNING(
                    '⚠️  La base de datos ya contiene datos.'
                )
            )
            self.stdout.write(
                self.style.WARNING(
                    '   Usa --force para poblar de todas formas.'
                )
            )
            return
        
        self.stdout.write(
            self.style.SUCCESS('🚀 Iniciando poblado de base de datos...\n')
        )
        
        # ======================================================================
        # TRANSACCIÓN ATÓMICA: Todo o nada
        # ======================================================================
        
        try:
            with transaction.atomic():
                # Paso 1: Crear Roles
                self._create_roles()
                
                # Paso 2: Crear Usuarios
                self._create_users()
                
                # Paso 3: Crear Departamentos
                self._create_departamentos()
                
                # Paso 4: Crear Ubicaciones
                self._create_ubicaciones()
                
                # Paso 5: Crear Tipos de Equipo
                self._create_tipos_equipo()
                
                # Paso 6: Crear Estados de Activo
                self._create_estados_activo()
                
                # Paso 7: Crear Activos
                self._create_activos()
            
            # ======================================================================
            # RESUMEN FINAL
            # ======================================================================
            
            self.stdout.write('\n' + '='*70)
            self.stdout.write(self.style.SUCCESS('✅ POBLADO COMPLETADO CON ÉXITO'))
            self.stdout.write('='*70 + '\n')
            
            self._print_summary()
            
        except Exception as e:
            raise CommandError(f'❌ Error al poblar la base de datos: {str(e)}')
    
    def _create_roles(self):
        """Crea los roles del sistema."""
        self.stdout.write('📋 Creando Roles...')
        
        rol_admin, created = Rol.objects.get_or_create(
            nombre_rol='Administrador'
        )
        if created:
            self.stdout.write(self.style.SUCCESS('   ✓ Rol "Administrador" creado'))
        
        rol_tecnico, created = Rol.objects.get_or_create(
            nombre_rol='Técnico'
        )
        if created:
            self.stdout.write(self.style.SUCCESS('   ✓ Rol "Técnico" creado'))
        
        self.stdout.write('')
    
    def _create_users(self):
        """Crea los usuarios del sistema."""
        self.stdout.write('👥 Creando Usuarios...')
        
        # Obtener roles
        rol_admin = Rol.objects.get(nombre_rol='Administrador')
        rol_tecnico = Rol.objects.get(nombre_rol='Técnico')
        
        # Usuario Administrador (Superuser)
        if not Usuario.objects.filter(username='admin').exists():
            admin_user = Usuario.objects.create_superuser(
                username='admin',
                email='admin@hospital.cl',
                password='admin123',
                nombre_completo='Administrador del Sistema',
                rol=rol_admin
            )
            self.stdout.write(
                self.style.SUCCESS('   ✓ Superusuario "admin" creado (password: admin123)')
            )
        else:
            self.stdout.write(
                self.style.WARNING('   ⚠ Usuario "admin" ya existe')
            )

        # Usuario Técnico (Usuario operativo)
        if not Usuario.objects.filter(username='juan').exists():
            juan_user = Usuario.objects.create_user(
                username='juan',
                email='juan@hospital.cl',
                password='juan123',
                nombre_completo='Juan Pérez Técnico',
                rol=rol_tecnico,
                is_staff=True  # Puede acceder al admin
            )
            self.stdout.write(
                self.style.SUCCESS('   ✓ Usuario "juan" creado (password: juan123)')
            )
        else:
            self.stdout.write(
                self.style.WARNING('   ⚠ Usuario "juan" ya existe')
            )

        self.stdout.write('')

    def _create_departamentos(self):
        """Crea los departamentos del hospital."""
        self.stdout.write('🏥 Creando Departamentos...')

        depto_urgencias, created = Departamento.objects.get_or_create(
            nombre_departamento='Urgencias'
        )
        if created:
            self.stdout.write(self.style.SUCCESS('   ✓ Departamento "Urgencias" creado'))

        depto_bodega, created = Departamento.objects.get_or_create(
            nombre_departamento='Bodega Central'
        )
        if created:
            self.stdout.write(self.style.SUCCESS('   ✓ Departamento "Bodega Central" creado'))

        self.stdout.write('')

    def _create_ubicaciones(self):
        """Crea las ubicaciones del hospital."""
        self.stdout.write('📍 Creando Ubicaciones...')

        # Obtener departamentos
        depto_urgencias = Departamento.objects.get(nombre_departamento='Urgencias')
        depto_bodega = Departamento.objects.get(nombre_departamento='Bodega Central')

        # Ubicaciones en Urgencias
        ubicaciones_urgencias = [
            ('Box 1', depto_urgencias),
            ('Box 2', depto_urgencias),
        ]

        for nombre, departamento in ubicaciones_urgencias:
            ubicacion, created = Ubicacion.objects.get_or_create(
                nombre_ubicacion=nombre,
                departamento=departamento
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'   ✓ Ubicación "{nombre}" creada en {departamento.nombre_departamento}')
                )

        # Ubicaciones en Bodega Central
        ubicaciones_bodega = [
            ('Estante A', depto_bodega),
            ('Estante B', depto_bodega),
        ]

        for nombre, departamento in ubicaciones_bodega:
            ubicacion, created = Ubicacion.objects.get_or_create(
                nombre_ubicacion=nombre,
                departamento=departamento
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'   ✓ Ubicación "{nombre}" creada en {departamento.nombre_departamento}')
                )

        self.stdout.write('')

    def _create_tipos_equipo(self):
        """Crea los tipos de equipo."""
        self.stdout.write('🔧 Creando Tipos de Equipo...')

        tipos = ['Monitor', 'Desfibrilador', 'Camilla']

        for tipo_nombre in tipos:
            tipo, created = TipoEquipo.objects.get_or_create(
                nombre_tipo=tipo_nombre
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'   ✓ Tipo "{tipo_nombre}" creado'))

        self.stdout.write('')

    def _create_estados_activo(self):
        """Crea los estados de activo."""
        self.stdout.write('📊 Creando Estados de Activo...')

        estados = ['Operativo', 'En Mantención', 'De Baja']

        for estado_nombre in estados:
            estado, created = EstadoActivo.objects.get_or_create(
                nombre_estado=estado_nombre
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'   ✓ Estado "{estado_nombre}" creado'))

        self.stdout.write('')

    def _create_activos(self):
        """Crea los activos de prueba."""
        self.stdout.write('💼 Creando Activos...')

        # Obtener referencias necesarias
        tipo_monitor = TipoEquipo.objects.get(nombre_tipo='Monitor')
        tipo_desfibrilador = TipoEquipo.objects.get(nombre_tipo='Desfibrilador')
        tipo_camilla = TipoEquipo.objects.get(nombre_tipo='Camilla')

        estado_operativo = EstadoActivo.objects.get(nombre_estado='Operativo')
        estado_mantencion = EstadoActivo.objects.get(nombre_estado='En Mantención')

        box1 = Ubicacion.objects.get(nombre_ubicacion='Box 1')
        box2 = Ubicacion.objects.get(nombre_ubicacion='Box 2')
        estante_a = Ubicacion.objects.get(nombre_ubicacion='Estante A')
        estante_b = Ubicacion.objects.get(nombre_ubicacion='Estante B')

        # Definir activos a crear
        activos_data = [
            {
                'codigo_inventario': 'INV-001',
                'numero_serie': 'MON-2024-001',
                'marca': 'Philips',
                'modelo': 'IntelliVue MX40',
                'tipo': tipo_monitor,
                'estado': estado_operativo,
                'ubicacion_actual': box1
            },
            {
                'codigo_inventario': 'INV-002',
                'numero_serie': 'MON-2024-002',
                'marca': 'GE Healthcare',
                'modelo': 'CARESCAPE B450',
                'tipo': tipo_monitor,
                'estado': estado_operativo,
                'ubicacion_actual': box2
            },
            {
                'codigo_inventario': 'INV-003',
                'numero_serie': 'DEF-2024-001',
                'marca': 'Zoll',
                'modelo': 'AED Plus',
                'tipo': tipo_desfibrilador,
                'estado': estado_operativo,
                'ubicacion_actual': box1
            },
            {
                'codigo_inventario': 'INV-004',
                'numero_serie': 'CAM-2024-001',
                'marca': 'Stryker',
                'modelo': 'Prime Series',
                'tipo': tipo_camilla,
                'estado': estado_mantencion,
                'ubicacion_actual': estante_a
            },
            {
                'codigo_inventario': 'INV-005',
                'numero_serie': 'CAM-2024-002',
                'marca': 'Hill-Rom',
                'modelo': 'Advanta 2',
                'tipo': tipo_camilla,
                'estado': estado_operativo,
                'ubicacion_actual': estante_b
            },
        ]

        # Crear activos
        for activo_data in activos_data:
            activo, created = Activo.objects.get_or_create(
                codigo_inventario=activo_data['codigo_inventario'],
                defaults=activo_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'   ✓ Activo "{activo_data["codigo_inventario"]}" '
                        f'({activo_data["marca"]} {activo_data["modelo"]}) creado'
                    )
                )

        self.stdout.write('')

    def _print_summary(self):
        """Imprime un resumen de los datos creados."""
        self.stdout.write('📊 RESUMEN DE DATOS CREADOS:\n')

        # Contar registros
        total_roles = Rol.objects.count()
        total_usuarios = Usuario.objects.count()
        total_departamentos = Departamento.objects.count()
        total_ubicaciones = Ubicacion.objects.count()
        total_tipos = TipoEquipo.objects.count()
        total_estados = EstadoActivo.objects.count()
        total_activos = Activo.objects.count()

        # Mostrar resumen
        self.stdout.write(f'   • Roles: {total_roles}')
        self.stdout.write(f'   • Usuarios: {total_usuarios}')
        self.stdout.write(f'   • Departamentos: {total_departamentos}')
        self.stdout.write(f'   • Ubicaciones: {total_ubicaciones}')
        self.stdout.write(f'   • Tipos de Equipo: {total_tipos}')
        self.stdout.write(f'   • Estados de Activo: {total_estados}')
        self.stdout.write(f'   • Activos: {total_activos}')

        self.stdout.write('\n' + '='*70)
        self.stdout.write(self.style.SUCCESS('🎉 CREDENCIALES DE ACCESO:'))
        self.stdout.write('='*70)
        self.stdout.write(self.style.SUCCESS('   Admin Panel: http://localhost:8000/admin/'))
        self.stdout.write(self.style.SUCCESS('   API Docs: http://localhost:8000/api/docs/'))
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('   👤 Superusuario:'))
        self.stdout.write(self.style.SUCCESS('      Username: admin'))
        self.stdout.write(self.style.SUCCESS('      Password: admin123'))
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('   👤 Usuario Técnico:'))
        self.stdout.write(self.style.SUCCESS('      Username: juan'))
        self.stdout.write(self.style.SUCCESS('      Password: juan123'))
        self.stdout.write('='*70 + '\n')


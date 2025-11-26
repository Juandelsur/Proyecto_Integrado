"""
Comando de gestión Django para poblar la base de datos con datos de prueba del Hospital.

Este script genera:
- 10 técnicos y 4 jefes de departamento
- 200 activos de tipo informático (Notebooks, PCs, Mouses, Discos)
- Historial de movimientos retroactivo para cada activo (1-3 movimientos)

Uso:
    python manage.py seed_hospital

CRÍTICO: Este script usa los nombres de campo correctos del modelo:
- activo (no fk_id_activo)
- usuario_registra (no fk_id_usuario_registra)
- ubicacion_origen (no fk_id_ubicacion_origen)
- ubicacion_destino (no fk_id_ubicacion_destino)
"""

import random
import datetime
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import (
    Activo,
    Ubicacion,
    TipoEquipo,
    EstadoActivo,
    Departamento,
    HistorialMovimiento,
    Rol
)
from faker import Faker

Usuario = get_user_model()


class Command(BaseCommand):
    help = 'Carga masiva de datos de prueba para el Sistema de Control de Activos Hospitalarios'

    def handle(self, *args, **kwargs):
        fake = Faker('es_ES')

        self.stdout.write(self.style.WARNING('\n' + '='*70))
        self.stdout.write(self.style.WARNING('  SEED HOSPITAL - Sistema de Control de Activos'))
        self.stdout.write(self.style.WARNING('='*70 + '\n'))

        # ======================================================================
        # 1. LIMPIEZA DE BASE DE DATOS
        # ======================================================================
        self.stdout.write(self.style.WARNING('📋 PASO 1: LIMPIANDO BASE DE DATOS'))
        self.stdout.write('-' * 70)

        # Orden correcto de eliminación (respetando foreign keys)
        count_historial = HistorialMovimiento.objects.count()
        HistorialMovimiento.objects.all().delete()
        self.stdout.write(f'   ✓ {count_historial} registros de Historial eliminados')

        count_activos = Activo.objects.count()
        Activo.objects.all().delete()
        self.stdout.write(f'   ✓ {count_activos} Activos eliminados')

        count_ubicaciones = Ubicacion.objects.count()
        Ubicacion.objects.all().delete()
        self.stdout.write(f'   ✓ {count_ubicaciones} Ubicaciones eliminadas')

        count_tipos = TipoEquipo.objects.count()
        TipoEquipo.objects.all().delete()
        self.stdout.write(f'   ✓ {count_tipos} Tipos de Equipo eliminados')

        count_estados = EstadoActivo.objects.count()
        EstadoActivo.objects.all().delete()
        self.stdout.write(f'   ✓ {count_estados} Estados eliminados')

        count_deptos = Departamento.objects.count()
        Departamento.objects.all().delete()
        self.stdout.write(f'   ✓ {count_deptos} Departamentos eliminados')

        # Eliminar usuarios excepto admin
        count_usuarios = Usuario.objects.exclude(username='admin').count()
        Usuario.objects.exclude(username='admin').delete()
        self.stdout.write(f'   ✓ {count_usuarios} Usuarios eliminados (excepto admin)')

        # Eliminar roles excepto el del admin
        roles_en_uso_por_admin = Usuario.objects.filter(username='admin').values_list('rol', flat=True)
        count_roles = Rol.objects.exclude(id__in=roles_en_uso_por_admin).count()
        Rol.objects.exclude(id__in=roles_en_uso_por_admin).delete()
        self.stdout.write(f'   ✓ {count_roles} Roles eliminados (excepto rol de admin)')

        self.stdout.write(self.style.SUCCESS('\n✅ Limpieza completada exitosamente\n'))

        # ======================================================================
        # 2. CREACIÓN DE ROLES Y USUARIOS
        # ======================================================================
        self.stdout.write(self.style.WARNING('👥 PASO 2: CREANDO ROLES Y USUARIOS'))
        self.stdout.write('-' * 70)

        # Crear roles
        rol_admin, created = Rol.objects.get_or_create(nombre_rol='Administrador')
        self.stdout.write(f'   {"✓ Creado" if created else "✓ Existente"}: Rol Administrador')

        rol_tecnico, created = Rol.objects.get_or_create(nombre_rol='Técnico')
        self.stdout.write(f'   {"✓ Creado" if created else "✓ Existente"}: Rol Técnico')

        rol_jefe, created = Rol.objects.get_or_create(nombre_rol='Jefe de Departamento')
        self.stdout.write(f'   {"✓ Creado" if created else "✓ Existente"}: Rol Jefe de Departamento')

        # Asegurar que admin tenga el rol correcto
        try:
            admin_user = Usuario.objects.get(username='admin')
            admin_user.rol = rol_admin
            admin_user.nombre_completo = 'Administrador del Sistema'
            admin_user.save()
            self.stdout.write('   ✓ Usuario admin actualizado con rol Administrador')
        except Usuario.DoesNotExist:
            self.stdout.write(self.style.WARNING('   ⚠ Usuario admin no existe'))
            admin_user = None

        # Crear 10 técnicos
        self.stdout.write('\n   Creando técnicos...')
        tecnicos_creados = []
        for i in range(1, 11):
            username = f"tecnico{i}"
            nombre_completo = f"Técnico TI {fake.first_name()} {fake.last_name()}"
            usuario = Usuario.objects.create_user(
                username=username,
                email=f"{username}@hospital.cl",
                password=f"{username}123",
                nombre_completo=nombre_completo,
                rol=rol_tecnico
            )
            tecnicos_creados.append(usuario)
            self.stdout.write(f'   ✓ {username} - {nombre_completo}')

        self.stdout.write(self.style.SUCCESS(f'\n   ✅ 10 Técnicos creados (password: username + "123")'))

        # Crear 4 jefes
        self.stdout.write('\n   Creando jefes de departamento...')
        jefes_creados = []
        for i in range(1, 5):
            username = f"jefe{i}"
            nombre_completo = f"Jefe {fake.first_name()} {fake.last_name()}"
            usuario = Usuario.objects.create_user(
                username=username,
                email=f"{username}@hospital.cl",
                password=f"{username}123",
                nombre_completo=nombre_completo,
                rol=rol_jefe
            )
            jefes_creados.append(usuario)
            self.stdout.write(f'   ✓ {username} - {nombre_completo}')

        self.stdout.write(self.style.SUCCESS(f'\n   ✅ 4 Jefes creados (password: username + "123")'))


        # ======================================================================
        # 3. CREACIÓN DE DATOS MAESTROS (DEPARTAMENTOS, TIPOS, ESTADOS)
        # ======================================================================
        self.stdout.write(self.style.WARNING('\n\n🏥 PASO 3: CREANDO DATOS MAESTROS'))
        self.stdout.write('-' * 70)

        # Crear departamentos
        self.stdout.write('\n   Creando departamentos...')
        departamentos_nombres = [
            'Urgencias',
            'UCI',
            'Pabellón',
            'Farmacia',
            'Administración',
            'Box Médico',
            'Laboratorio',
            'Bodega Central TI'
        ]
        deptos_objs = []
        for nombre in departamentos_nombres:
            depto = Departamento.objects.create(nombre_departamento=nombre)
            deptos_objs.append(depto)
            self.stdout.write(f'   ✓ {nombre}')

        self.stdout.write(self.style.SUCCESS(f'\n   ✅ {len(deptos_objs)} Departamentos creados'))

        # Identificar bodega para lógica de movimientos
        bodega_depto = next((d for d in deptos_objs if 'Bodega' in d.nombre_departamento), deptos_objs[0])

        # Crear tipos de equipos informáticos
        self.stdout.write('\n   Creando tipos de equipos...')
        tipos_pc = ['PC All-in-One', 'Notebook', 'Monitor']
        tipos_accesorios = ['Teclado', 'Mouse', 'Webcam']
        tipos_storage = ['Disco Duro (HDD)', 'Estado Sólido (SSD)', 'Memoria RAM', 'Memoria USB']
        tipos_impresion = ['Impresora Térmica', 'Lector Código Barras']

        todos_los_tipos = tipos_pc + tipos_accesorios + tipos_storage + tipos_impresion
        tipos_objs = []
        for nombre_tipo in todos_los_tipos:
            tipo = TipoEquipo.objects.create(nombre_tipo=nombre_tipo)
            tipos_objs.append(tipo)
            self.stdout.write(f'   ✓ {nombre_tipo}')

        self.stdout.write(self.style.SUCCESS(f'\n   ✅ {len(tipos_objs)} Tipos de equipos creados'))

        # Crear estados
        self.stdout.write('\n   Creando estados...')
        estados_nombres = ['Operativo', 'En Reparación', 'De Baja', 'En Bodega TI']
        estados_objs = []
        for nombre_estado in estados_nombres:
            estado = EstadoActivo.objects.create(nombre_estado=nombre_estado)
            estados_objs.append(estado)
            self.stdout.write(f'   ✓ {nombre_estado}')

        self.stdout.write(self.style.SUCCESS(f'\n   ✅ {len(estados_objs)} Estados creados'))

        # ======================================================================
        # 4. CREACIÓN DE UBICACIONES FÍSICAS
        # ======================================================================
        self.stdout.write(self.style.WARNING('\n\n📍 PASO 4: GENERANDO UBICACIONES FÍSICAS'))
        self.stdout.write('-' * 70)

        ubicaciones_objs = []
        bodega_ubicacion = None

        self.stdout.write('\n   Creando ubicaciones por departamento...')
        for depto in deptos_objs:
            for i in range(1, 4):  # 3 estaciones por departamento
                nombre_ubicacion = f"{depto.nombre_departamento} - Estación {i}"
                ubicacion = Ubicacion.objects.create(
                    nombre_ubicacion=nombre_ubicacion,
                    departamento=depto
                )
                ubicaciones_objs.append(ubicacion)

                # Guardar referencia a la bodega para lógica de movimientos
                if depto == bodega_depto and i == 1:
                    bodega_ubicacion = ubicacion

                self.stdout.write(f'   ✓ {nombre_ubicacion} (Código QR: {ubicacion.codigo_qr})')

        # Fallback si no se encontró bodega
        if not bodega_ubicacion:
            bodega_ubicacion = ubicaciones_objs[0]

        self.stdout.write(self.style.SUCCESS(f'\n   ✅ {len(ubicaciones_objs)} Ubicaciones generadas con códigos QR automáticos'))


        # ======================================================================
        # 5. GENERACIÓN DE ACTIVOS CON HISTORIAL DE MOVIMIENTOS
        # ======================================================================
        CANTIDAD_ACTIVOS = 200
        self.stdout.write(self.style.WARNING(f'\n\n💻 PASO 5: GENERANDO {CANTIDAD_ACTIVOS} ACTIVOS CON HISTORIAL'))
        self.stdout.write('-' * 70)

        # Catálogos de marcas y modelos reales
        catalogo_pc = {
            'HP': ['ProBook 440 G8', 'EliteBook 840', 'ProDesk 600'],
            'Dell': ['Latitude 5420', 'OptiPlex 7090', 'Inspiron 15'],
            'Lenovo': ['ThinkPad T14', 'IdeaPad 3', 'ThinkCentre M720'],
            'Apple': ['MacBook Air M1', 'MacBook Pro 13']
        }

        catalogo_accesorios = {
            'Logitech': ['MX Master 3', 'K380', 'C920 HD'],
            'Genius': ['SlimStar 8000', 'NetScroll 120'],
            'Microsoft': ['Sculpt Ergonomic', 'Arc Mouse']
        }

        catalogo_storage = {
            'Kingston': ['Fury DDR4 16GB', 'A400 SSD 480GB', 'DataTraveler 64GB'],
            'Samsung': ['Evo 970 SSD 1TB', 'T7 Portable 500GB'],
            'Western Digital': ['Blue HDD 1TB', 'Black SN850 SSD']
        }

        catalogo_impresion = {
            'Zebra': ['GK420t', 'ZD410'],
            'Epson': ['TM-T88V', 'L3150'],
            'HP': ['LaserJet Pro M404', 'DeskJet 2720']
        }

        # Comentarios realistas para movimientos
        observaciones_mov = [
            "Traslado por solicitud del jefe de departamento",
            "Fallas intermitentes reportadas por usuario",
            "Asignación a nuevo usuario",
            "Envío a mantenimiento preventivo",
            "Devolución desde bodega",
            "Instalación inicial en estación de trabajo",
            "Reubicación por reorganización de espacios",
            "Cambio de ubicación temporal",
            "Retorno después de reparación"
        ]

        # CRÍTICO: Convertir QuerySet a lista para evitar errores con random.choice
        tecnicos_lista = list(Usuario.objects.filter(rol__nombre_rol='Técnico'))
        ubicaciones_lista = list(ubicaciones_objs)  # Ya es lista, pero por seguridad

        if not tecnicos_lista:
            self.stdout.write(self.style.WARNING('   ⚠ No hay técnicos disponibles, usando admin'))
            tecnicos_lista = [admin_user] if admin_user else []

        if not tecnicos_lista:
            self.stdout.write(self.style.ERROR('   ❌ ERROR: No hay usuarios disponibles para registrar movimientos'))
            return

        self.stdout.write(f'\n   Generando {CANTIDAD_ACTIVOS} activos...')
        activos_creados = 0
        movimientos_creados = 0

        # Catálogo de PCs para vincular accesorios
        pcs_disponibles = ['HP ProBook 440', 'Dell Latitude 5420', 'Lenovo ThinkPad T14', 'Apple MacBook Air']

        for idx in range(CANTIDAD_ACTIVOS):
            # Seleccionar tipo de equipo
            tipo_obj = random.choice(tipos_objs)
            nombre_tipo = tipo_obj.nombre_tipo

            # Determinar catálogo según tipo
            if nombre_tipo in tipos_pc:
                catalogo = catalogo_pc
            elif nombre_tipo in tipos_accesorios:
                catalogo = catalogo_accesorios
            elif nombre_tipo in tipos_storage:
                catalogo = catalogo_storage
            else:
                catalogo = catalogo_impresion

            # Seleccionar marca y modelo
            marca = random.choice(list(catalogo.keys()))
            modelo_base = random.choice(catalogo[marca])
            modelo = f"{modelo_base}"

            # Generar nota si es accesorio (60% de probabilidad)
            nota_activo = ""
            if nombre_tipo in tipos_accesorios and random.random() < 0.6:
                pc_vinculado = random.choice(pcs_disponibles)
                nota_activo = f"Vinculado a {pc_vinculado}"

            # Ubicación final del activo
            ubicacion_final = random.choice(ubicaciones_lista)

            # Crear Activo con fecha de alta entre 2 años y 1 año atrás
            fecha_alta_generada = fake.date_between(start_date='-2y', end_date='-1y')

            activo = Activo.objects.create(
                numero_serie=fake.unique.bothify(text='SN-########').upper(),
                marca=marca,
                modelo=modelo,
                tipo=tipo_obj,
                estado=random.choice(estados_objs),
                ubicacion_actual=ubicacion_final,
                notas=nota_activo
            )

            # IMPORTANTE: Actualizar fecha_alta manualmente (auto_now_add no permite override)
            activo.fecha_alta = timezone.make_aware(
                datetime.datetime.combine(fecha_alta_generada, datetime.time(9, 0))
            )
            activo.save(update_fields=['fecha_alta'])

            activos_creados += 1

            # ================================================================
            # GENERACIÓN DE HISTORIAL DE MOVIMIENTOS (CRÍTICO)
            # ================================================================
            # Generar entre 1 y 3 movimientos retroactivos
            cantidad_movimientos = random.randint(1, 3)
            ubicacion_anterior = bodega_ubicacion  # Todos los activos empiezan en bodega

            # Fecha base para calcular movimientos
            fecha_base = activo.fecha_alta
            if isinstance(fecha_base, datetime.datetime):
                fecha_base_date = fecha_base.date()
            else:
                fecha_base_date = fecha_base

            for i in range(cantidad_movimientos):
                # Calcular fecha del movimiento (entre 30 y 120 días después del anterior)
                dias_adelante = random.randint(30, 120)
                fecha_mov_date = fecha_base_date + datetime.timedelta(days=dias_adelante)

                # CRÍTICO: No crear movimientos en el futuro
                if fecha_mov_date > timezone.now().date():
                    break

                # Convertir a datetime con hora aleatoria
                hora_aleatoria = random.randint(8, 18)
                minuto_aleatorio = random.randint(0, 59)
                fecha_mov_datetime = timezone.make_aware(
                    datetime.datetime.combine(
                        fecha_mov_date,
                        datetime.time(hora_aleatoria, minuto_aleatorio)
                    )
                )

                # Seleccionar ubicación destino
                destino_mov = random.choice(ubicaciones_lista)

                # El último movimiento debe llevar al activo a su ubicación actual
                if i == cantidad_movimientos - 1:
                    destino_mov = ubicacion_final

                # CRÍTICO: Usar nombres de campo correctos del modelo
                # activo (no fk_id_activo)
                # usuario_registra (no fk_id_usuario_registra)
                # ubicacion_origen (no fk_id_ubicacion_origen)
                # ubicacion_destino (no fk_id_ubicacion_destino)
                movimiento = HistorialMovimiento.objects.create(
                    activo=activo,  # ← Instancia de Activo
                    usuario_registra=random.choice(tecnicos_lista),  # ← Instancia de Usuario
                    ubicacion_origen=ubicacion_anterior,  # ← Instancia de Ubicacion
                    ubicacion_destino=destino_mov,  # ← Instancia de Ubicacion
                    tipo_movimiento=random.choice(['TRASLADO', 'ASIGNACION', 'MANTENIMIENTO', 'RETORNO']),
                    comentarios=random.choice(observaciones_mov)
                )

                # Actualizar fecha_movimiento manualmente (auto_now_add no permite override)
                movimiento.fecha_movimiento = fecha_mov_datetime
                movimiento.save(update_fields=['fecha_movimiento'])

                movimientos_creados += 1

                # Actualizar para el siguiente movimiento
                ubicacion_anterior = destino_mov
                fecha_base_date = fecha_mov_date

            # Mostrar progreso cada 20 activos
            if (idx + 1) % 20 == 0:
                self.stdout.write(f'   ✓ {idx + 1}/{CANTIDAD_ACTIVOS} activos creados...')

        self.stdout.write(self.style.SUCCESS(f'\n   ✅ {activos_creados} Activos creados con códigos INV-YY-XXXXXX'))
        self.stdout.write(self.style.SUCCESS(f'   ✅ {movimientos_creados} Movimientos históricos generados'))

        # ======================================================================
        # RESUMEN FINAL
        # ======================================================================
        self.stdout.write(self.style.SUCCESS('\n' + '='*70))
        self.stdout.write(self.style.SUCCESS('  ✅ CARGA COMPLETADA EXITOSAMENTE'))
        self.stdout.write(self.style.SUCCESS('='*70))
        self.stdout.write(f'\n   📊 RESUMEN:')
        self.stdout.write(f'   • Usuarios: {len(tecnicos_creados)} técnicos + {len(jefes_creados)} jefes')
        self.stdout.write(f'   • Departamentos: {len(deptos_objs)}')
        self.stdout.write(f'   • Ubicaciones: {len(ubicaciones_objs)}')
        self.stdout.write(f'   • Tipos de Equipo: {len(tipos_objs)}')
        self.stdout.write(f'   • Estados: {len(estados_objs)}')
        self.stdout.write(f'   • Activos: {activos_creados}')
        self.stdout.write(f'   • Movimientos: {movimientos_creados}')
        self.stdout.write('\n   🔐 Credenciales de acceso:')
        self.stdout.write('   • admin / admin123')
        self.stdout.write('   • tecnico1 / tecnico1123')
        self.stdout.write('   • jefe1 / jefe1123')
        self.stdout.write('\n')
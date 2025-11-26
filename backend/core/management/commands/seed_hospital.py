import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
# AJUSTA LOS IMPORTS al nombre real de tu aplicación (ej: core, api, gestion)
from core.models import Activo, Ubicacion, TipoEquipo, EstadoActivo, Departamento, HistorialMovimiento, Rol
from faker import Faker

Usuario = get_user_model()

class Command(BaseCommand):
    help = 'Carga masiva de activos informáticos, usuarios TI y notas de prueba.'

    def handle(self, *args, **kwargs):
        fake = Faker('es_ES')
        
        self.stdout.write(self.style.WARNING('--- 1. LIMPIANDO BASE DE DATOS (Admin protegido) ---'))
        
        # 1. BORRADO EN CASCADA INVERSA
        # Borramos primero los historiales para no romper Foreign Keys
        HistorialMovimiento.objects.all().delete()
        Activo.objects.all().delete()
        Ubicacion.objects.all().delete()
        TipoEquipo.objects.all().delete()
        EstadoActivo.objects.all().delete()
        Departamento.objects.all().delete()
        
        # Borramos Roles y Usuarios (Excepto admin)
        Rol.objects.all().delete()
        Usuario.objects.exclude(username='admin').delete()
        
        self.stdout.write(self.style.SUCCESS('Limpieza completada.'))

        # 2. CREACIÓN DE ROLES
        self.stdout.write("--- 2. CREANDO ESTRUCTURA ORGANIZACIONAL ---")
        
        rol_admin, _ = Rol.objects.get_or_create(nombre_rol='Administrador')
        rol_tecnico, _ = Rol.objects.get_or_create(nombre_rol='Técnico')
        rol_jefe, _ = Rol.objects.get_or_create(nombre_rol='Jefe de Departamento')

        # Aseguramos que el admin existente tenga rol de Administrador
        try:
            admin_user = Usuario.objects.get(username='admin')
            admin_user.rol = rol_admin
            admin_user.save()
        except Usuario.DoesNotExist:
            self.stdout.write(self.style.ERROR("⚠ El usuario 'admin' no existe. (Opcional)"))

        # 3. GENERACIÓN DE USUARIOS MASIVOS
        
        # --- TÉCNICOS (10) ---
        CANTIDAD_TECNICOS = 10
        self.stdout.write(f"Generando {CANTIDAD_TECNICOS} técnicos de soporte...")
        for i in range(1, CANTIDAD_TECNICOS + 1):
            username = f"tecnico{i}"
            password = f"{username}123"  # Regla fácil
            
            Usuario.objects.create_user(
                username=username,
                email=f"{username}@hospital.cl",
                password=password,
                nombre_completo=f"Soporte TI {fake.first_name()} {fake.last_name()}",
                rol=rol_tecnico
            )

        # --- JEFES (4) ---
        CANTIDAD_JEFES = 4
        self.stdout.write(f"Generando {CANTIDAD_JEFES} jefes de servicio...")
        for i in range(1, CANTIDAD_JEFES + 1):
            username = f"jefe{i}"
            password = f"{username}123"
            
            Usuario.objects.create_user(
                username=username,
                email=f"{username}@hospital.cl",
                password=password,
                nombre_completo=f"Dr. {fake.last_name()} (Jefe)",
                rol=rol_jefe
            )

        # 4. DATOS MAESTROS (Lugares Físicos del Hospital)
        deptos = ['Urgencias', 'UCI', 'Pabellón Central', 'Farmacia', 'Administración', 'Box Médico', 'Laboratorio']
        deptos_objs = [Departamento.objects.create(nombre_departamento=d) for d in deptos]

        # 5. TIPOS DE EQUIPO INFORMÁTICO (Según Diagrama Db.jpg)
        tipos_it = [
            'PC All-in-One', 
            'Notebook', 
            'Monitor', 
            'Teclado', 
            'Mouse', 
            'Disco Duro (HDD)', 
            'Estado Sólido (SSD)', 
            'Memoria RAM', 
            'Impresora Térmica',
            'Lector de Código de Barras'
        ]
        tipos_objs = [TipoEquipo.objects.create(nombre_tipo=t) for t in tipos_it]

        # 6. ESTADOS
        estados = ['Operativo', 'En Reparación', 'De Baja', 'En Bodega TI']
        estados_objs = [EstadoActivo.objects.create(nombre_estado=e) for e in estados]

        # 7. UBICACIONES (Backend generará LOC-XXXX)
        self.stdout.write("--- 3. CREANDO UBICACIONES Y CÓDIGOS QR ---")
        ubicaciones_objs = []
        for d in deptos_objs:
            # Creamos estaciones de trabajo
            for i in range(1, 4): 
                u = Ubicacion.objects.create(
                    nombre_ubicacion=f"{d.nombre_departamento} - Estación {i}",
                    fk_id_departamento=d
                )
                ubicaciones_objs.append(u)

        # 8. ACTIVOS INFORMÁTICOS (Backend generará INV-XXXX)
        CANTIDAD_ACTIVOS = 200
        self.stdout.write(f"--- 4. GENERANDO {CANTIDAD_ACTIVOS} ACTIVOS TI CON NOTAS ---")
        
        marcas_pc = ['HP', 'Dell', 'Lenovo', 'Apple', 'Acer']
        marcas_componentes = ['Kingston', 'Samsung', 'Western Digital', 'Seagate', 'Logitech', 'Zebra']
        
        # Frases típicas para las notas (Faker a veces es muy lorem ipsum)
        notas_ejemplos = [
            "El usuario reporta lentitud.",
            "Pantalla con píxeles quemados.",
            "Falta cable de poder.",
            "Asignado al turno de noche.",
            "Pendiente de actualización de RAM.",
            "Ruido extraño en el ventilador.",
            "Etiqueta de inventario borrosa.",
            "Requiere limpieza física.",
            "Teclas pegadas."
        ]

        for _ in range(CANTIDAD_ACTIVOS):
            tipo_seleccionado = random.choice(tipos_objs)
            
            # Marca coherente según tipo
            if tipo_seleccionado.nombre_tipo in ['Notebook', 'PC All-in-One', 'Monitor']:
                marca_real = random.choice(marcas_pc)
            else:
                marca_real = random.choice(marcas_componentes)

            # Generar Nota (30% de probabilidad de tener nota)
            nota_texto = ""
            if random.random() < 0.3:
                # 50% chance: Nota de la lista, 50% chance: Texto aleatorio de Faker
                if random.random() < 0.5:
                    nota_texto = random.choice(notas_ejemplos)
                else:
                    nota_texto = fake.text(max_nb_chars=60)

            Activo.objects.create(
                numero_serie=fake.unique.bothify(text='SN-#######-??').upper(),
                marca=marca_real,
                modelo=f"{fake.word().capitalize()} {fake.bothify(text='###-G#')}",
                fk_id_tipo=tipo_seleccionado,
                fk_id_estado=random.choice(estados_objs),
                fk_id_ubicacion_actual=random.choice(ubicaciones_objs),
                fecha_alta=fake.date_between(start_date='-4y', end_date='today'),
                notas=nota_texto  # <--- CAMPO NUEVO
            )

        # ================= RESUMEN =================
        self.stdout.write(self.style.SUCCESS('\n✅ PROCESO COMPLETADO EXITOSAMENTE'))
        self.stdout.write(f" - Usuarios: 10 Técnicos, 4 Jefes.")
        self.stdout.write(f" - Activos TI: {CANTIDAD_ACTIVOS} creados (Notebooks, PCs, Periféricos).")
        self.stdout.write(f" - Ubicaciones: {len(ubicaciones_objs)} creadas.")
        self.stdout.write("\n🔐 REGLA MAESTRA DE ACCESO:")
        self.stdout.write("   Usuario:  tecnico1 ... tecnico10  | jefe1 ... jefe4")
        self.stdout.write("   Password: [usuario] + 123")
        self.stdout.write("   Ejemplo:  tecnico5 -> tecnico5123")
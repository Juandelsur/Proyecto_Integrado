# 🎛️ Guía de Administración y Poblado de Datos

## ✅ Implementación Completada

Se ha configurado exitosamente el **Panel de Administración de Django** y el **Comando de Poblado de Datos** para el MVP del SCA Hospital.

---

## 📋 Archivos Creados/Configurados

### 1. `core/admin.py` (197 líneas)
✅ Todos los modelos registrados con decorador `@admin.register`  
✅ Configuración de `list_display` para tablas legibles  
✅ Configuración de `search_fields` para búsquedas  
✅ Configuración de `list_filter` para filtros  
✅ Configuración de `autocomplete_fields` para relaciones  
✅ Protección de logs de auditoría (solo lectura)  

### 2. `core/management/commands/seed_data.py` (397 líneas)
✅ Comando personalizado de Django  
✅ Verificación de datos existentes  
✅ Transacción atómica (todo o nada)  
✅ Feedback detallado durante ejecución  
✅ Resumen completo al finalizar  

---

## 🎛️ Panel de Administración

### Modelos Registrados

#### 1. Roles
- **List Display**: nombre_rol, id
- **Search**: nombre_rol
- **Ordenamiento**: nombre_rol

#### 2. Usuarios (Custom User)
- **List Display**: username, nombre_completo, email, rol, is_active, is_staff
- **Filters**: is_active, is_staff, is_superuser, rol, date_joined
- **Search**: username, email, nombre_completo
- **Fieldsets**: Información personal + Información adicional (nombre_completo, rol)

#### 3. Departamentos
- **List Display**: nombre_departamento, id
- **Search**: nombre_departamento
- **Ordenamiento**: nombre_departamento

#### 4. Ubicaciones
- **List Display**: nombre_ubicacion, departamento, id
- **Filters**: departamento
- **Search**: nombre_ubicacion
- **Autocomplete**: departamento

#### 5. Tipos de Equipo
- **List Display**: nombre_tipo, id
- **Search**: nombre_tipo
- **Ordenamiento**: nombre_tipo

#### 6. Estados de Activo
- **List Display**: nombre_estado, id
- **Search**: nombre_estado
- **Ordenamiento**: nombre_estado

#### 7. Activos (CRÍTICO)
- **List Display**: codigo_inventario, numero_serie, marca, modelo, tipo, estado, ubicacion_actual, fecha_alta
- **Filters**: tipo, estado, ubicacion_actual__departamento, fecha_alta
- **Search**: codigo_inventario, numero_serie, marca, modelo
- **Autocomplete**: tipo, estado, ubicacion_actual
- **Readonly**: fecha_alta
- **Fieldsets**: Información Básica, Clasificación, Fechas

#### 8. Historial de Movimientos
- **List Display**: activo, tipo_movimiento, ubicacion_origen, ubicacion_destino, usuario_registra, fecha_movimiento
- **Filters**: tipo_movimiento, fecha_movimiento, departamentos
- **Search**: activo__codigo_inventario, activo__numero_serie, comentarios
- **Autocomplete**: activo, usuario_registra, ubicacion_origen, ubicacion_destino
- **Readonly**: fecha_movimiento

#### 9. Logs de Auditoría (SOLO LECTURA)
- **List Display**: timestamp, usuario, accion, id
- **Filters**: accion, timestamp
- **Search**: usuario__username, detalle_accion
- **Readonly**: timestamp, detalle_accion
- **Permisos**: No se puede crear, modificar ni eliminar (excepto superusuarios)

---

## 🌱 Comando de Poblado (seed_data)

### Uso Básico

```bash
cd backend
python manage.py seed_data
```

### Uso con Forzado

```bash
python manage.py seed_data --force
```

**Nota**: El flag `--force` permite poblar la base de datos incluso si ya contiene datos.

---

## 📊 Datos Creados por el Seed

### 1. Roles (2)
- ✅ Administrador
- ✅ Técnico

### 2. Usuarios (2)

#### Superusuario
- **Username**: admin
- **Password**: admin123
- **Email**: admin@hospital.cl
- **Nombre**: Administrador del Sistema
- **Rol**: Administrador
- **Permisos**: Superusuario (acceso total)

#### Usuario Técnico
- **Username**: juan
- **Password**: juan123
- **Email**: juan@hospital.cl
- **Nombre**: Juan Pérez Técnico
- **Rol**: Técnico
- **Permisos**: Staff (acceso al admin)

### 3. Departamentos (2)
- ✅ Urgencias
- ✅ Bodega Central

### 4. Ubicaciones (4)

#### En Urgencias
- ✅ Box 1
- ✅ Box 2

#### En Bodega Central
- ✅ Estante A
- ✅ Estante B

### 5. Tipos de Equipo (3)
- ✅ Monitor
- ✅ Desfibrilador
- ✅ Camilla

### 6. Estados de Activo (3)
- ✅ Operativo
- ✅ En Mantención
- ✅ De Baja

### 7. Activos (5)

#### Activo 1: Monitor Philips
- **Código**: INV-001
- **Serie**: MON-2024-001
- **Marca**: Philips
- **Modelo**: IntelliVue MX40
- **Tipo**: Monitor
- **Estado**: Operativo
- **Ubicación**: Box 1 (Urgencias)

#### Activo 2: Monitor GE
- **Código**: INV-002
- **Serie**: MON-2024-002
- **Marca**: GE Healthcare
- **Modelo**: CARESCAPE B450
- **Tipo**: Monitor
- **Estado**: Operativo
- **Ubicación**: Box 2 (Urgencias)

#### Activo 3: Desfibrilador Zoll
- **Código**: INV-003
- **Serie**: DEF-2024-001
- **Marca**: Zoll
- **Modelo**: AED Plus
- **Tipo**: Desfibrilador
- **Estado**: Operativo
- **Ubicación**: Box 1 (Urgencias)

#### Activo 4: Camilla Stryker
- **Código**: INV-004
- **Serie**: CAM-2024-001
- **Marca**: Stryker
- **Modelo**: Prime Series
- **Tipo**: Camilla
- **Estado**: En Mantención
- **Ubicación**: Estante A (Bodega Central)

#### Activo 5: Camilla Hill-Rom
- **Código**: INV-005
- **Serie**: CAM-2024-002
- **Marca**: Hill-Rom
- **Modelo**: Advanta 2
- **Tipo**: Camilla
- **Estado**: Operativo
- **Ubicación**: Estante B (Bodega Central)

---

## 🚀 Pasos para Configurar el MVP

### Paso 1: Aplicar Migraciones

```bash
cd backend
python3 manage.py makemigrations
python3 manage.py migrate
```

**Salida esperada**:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, core, sessions
Running migrations:
  Applying core.0001_initial... OK
  ...
```

### Paso 2: Poblar la Base de Datos

```bash
python3 manage.py seed_data
```

**Salida esperada**:
```
🚀 Iniciando poblado de base de datos...

📋 Creando Roles...
   ✓ Rol "Administrador" creado
   ✓ Rol "Técnico" creado

👥 Creando Usuarios...
   ✓ Superusuario "admin" creado (password: admin123)
   ✓ Usuario "juan" creado (password: juan123)

🏥 Creando Departamentos...
   ✓ Departamento "Urgencias" creado
   ✓ Departamento "Bodega Central" creado

📍 Creando Ubicaciones...
   ✓ Ubicación "Box 1" creada en Urgencias
   ✓ Ubicación "Box 2" creada en Urgencias
   ✓ Ubicación "Estante A" creada en Bodega Central
   ✓ Ubicación "Estante B" creada en Bodega Central

🔧 Creando Tipos de Equipo...
   ✓ Tipo "Monitor" creado
   ✓ Tipo "Desfibrilador" creado
   ✓ Tipo "Camilla" creado

📊 Creando Estados de Activo...
   ✓ Estado "Operativo" creado
   ✓ Estado "En Mantención" creado
   ✓ Estado "De Baja" creado

💼 Creando Activos...
   ✓ Activo "INV-001" (Philips IntelliVue MX40) creado
   ✓ Activo "INV-002" (GE Healthcare CARESCAPE B450) creado
   ✓ Activo "INV-003" (Zoll AED Plus) creado
   ✓ Activo "INV-004" (Stryker Prime Series) creado
   ✓ Activo "INV-005" (Hill-Rom Advanta 2) creado

======================================================================
✅ POBLADO COMPLETADO CON ÉXITO
======================================================================

📊 RESUMEN DE DATOS CREADOS:

   • Roles: 2
   • Usuarios: 2
   • Departamentos: 2
   • Ubicaciones: 4
   • Tipos de Equipo: 3
   • Estados de Activo: 3
   • Activos: 5

======================================================================
🎉 CREDENCIALES DE ACCESO:
======================================================================
   Admin Panel: http://localhost:8000/admin/
   API Docs: http://localhost:8000/api/docs/

   👤 Superusuario:
      Username: admin
      Password: admin123

   👤 Usuario Técnico:
      Username: juan
      Password: juan123
======================================================================
```

### Paso 3: Iniciar el Servidor

```bash
python3 manage.py runserver
```

**Salida esperada**:
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
January 15, 2024 - 10:30:00
Django version 5.0, using settings 'config.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### Paso 4: Acceder al Panel de Administración

1. Abre tu navegador en: **http://localhost:8000/admin/**
2. Ingresa las credenciales:
   - **Username**: admin
   - **Password**: admin123
3. Explora los modelos registrados

### Paso 5: Acceder a la Documentación de la API

1. Abre tu navegador en: **http://localhost:8000/api/docs/**
2. Verás la documentación interactiva de Swagger
3. Puedes probar los endpoints directamente desde el navegador

---

## 💻 Ejemplos de Uso del Admin

### Ejemplo 1: Ver Todos los Activos

1. En el admin, haz clic en **"Activos"**
2. Verás una tabla con todos los activos:
   - Código de inventario
   - Número de serie
   - Marca y modelo
   - Tipo, estado y ubicación
   - Fecha de alta

### Ejemplo 2: Buscar un Activo

1. En la lista de activos, usa el campo de búsqueda
2. Busca por: `INV-001` o `Philips` o `MON-2024-001`
3. El sistema filtrará los resultados

### Ejemplo 3: Filtrar Activos por Estado

1. En la lista de activos, usa el panel lateral derecho
2. Haz clic en **"Estado"** → **"Operativo"**
3. Verás solo los activos operativos

### Ejemplo 4: Ver Historial de un Activo

1. En la lista de activos, haz clic en un activo
2. En la página de detalle, verás toda la información
3. Para ver el historial, ve a **"Historial de Movimientos"** en el menú principal
4. Busca por el código del activo

### Ejemplo 5: Ver Logs de Auditoría

1. En el admin, haz clic en **"Logs de Auditoría"**
2. Verás todos los logs del sistema
3. Puedes filtrar por acción o fecha
4. **Nota**: No puedes crear, modificar ni eliminar logs (solo lectura)

---

## 🧪 Pruebas Recomendadas

### Test 1: Crear un Nuevo Activo desde el Admin

1. Ve a **Activos** → **Agregar Activo**
2. Completa los campos:
   - Código: INV-006
   - Serie: TEST-001
   - Marca: Test Brand
   - Modelo: Test Model
   - Tipo: Monitor
   - Estado: Operativo
   - Ubicación: Box 1
3. Guarda
4. Verifica que aparezca en la lista

### Test 2: Movilizar un Activo desde la API

1. Ve a http://localhost:8000/api/docs/
2. Haz clic en **"Authorize"** y obtén un token JWT
3. Busca el endpoint **POST /api/activos/{id}/movilizar/**
4. Prueba mover el activo INV-001 de Box 1 a Box 2
5. Verifica en el admin que la ubicación cambió
6. Verifica en **Historial de Movimientos** que se registró el movimiento
7. Verifica en **Logs de Auditoría** que se creó el log

### Test 3: Verificar Trazabilidad

1. Moviliza un activo varias veces usando la API
2. Ve al admin → **Historial de Movimientos**
3. Busca por el código del activo
4. Verifica que todos los movimientos estén registrados
5. Verifica que cada movimiento tenga:
   - Ubicación origen
   - Ubicación destino
   - Usuario que registró
   - Fecha y hora
   - Comentarios

### Test 4: Verificar Auditoría

1. Realiza varias acciones (crear activos, movilizar, etc.)
2. Ve al admin → **Logs de Auditoría**
3. Verifica que cada acción esté registrada
4. Verifica que cada log tenga:
   - Usuario
   - Acción
   - Detalle completo en JSON
   - Timestamp

---

## 🔒 Seguridad del Admin

### Protecciones Implementadas

✅ **Autenticación requerida**: Solo usuarios autenticados pueden acceder
✅ **Permisos por modelo**: Django maneja permisos automáticamente
✅ **Logs de auditoría protegidos**: Solo lectura (excepto superusuarios)
✅ **Campos readonly**: Fechas automáticas no se pueden modificar
✅ **Validación de datos**: Django valida automáticamente

### Recomendaciones de Seguridad

⚠️ **Cambiar contraseñas en producción**:
```bash
python manage.py changepassword admin
python manage.py changepassword juan
```

⚠️ **Deshabilitar DEBUG en producción**:
```python
# config/settings.py
DEBUG = False
ALLOWED_HOSTS = ['tu-dominio.com']
```

⚠️ **Usar HTTPS en producción**:
```python
# config/settings.py
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

---

## 📚 Comandos Útiles

### Ver Datos en la Base de Datos

```bash
python3 manage.py shell
```

```python
from core.models import *

# Ver todos los activos
Activo.objects.all()

# Ver activos operativos
Activo.objects.filter(estado__nombre_estado='Operativo')

# Ver historial de un activo
activo = Activo.objects.get(codigo_inventario='INV-001')
HistorialMovimiento.objects.filter(activo=activo)

# Ver logs de auditoría
AuditoriaLog.objects.filter(accion='MOVILIZACION_ACTIVO')
```

### Limpiar la Base de Datos

```bash
# Eliminar todos los datos
python3 manage.py flush

# Volver a poblar
python3 manage.py seed_data
```

### Crear un Backup de la Base de Datos

```bash
# PostgreSQL
pg_dump -U postgres -d sca_hospital > backup.sql

# SQLite (desarrollo)
cp db.sqlite3 db.sqlite3.backup
```

---

## 🎉 Resumen de Implementación

### Archivos Creados/Configurados
✅ **core/admin.py** - Panel de administración completo (197 líneas)
✅ **core/management/commands/seed_data.py** - Comando de poblado (397 líneas)
✅ **core/management/__init__.py** - Package management
✅ **core/management/commands/__init__.py** - Package commands
✅ **ADMIN_AND_SEED_GUIDE.md** - Guía completa de uso

### Características Implementadas
✅ **9 modelos registrados** en el admin
✅ **Configuración personalizada** para cada modelo
✅ **Búsqueda y filtros** en todos los modelos
✅ **Autocomplete** para relaciones
✅ **Protección de logs** de auditoría
✅ **Comando de seed** con transacción atómica
✅ **Verificación de datos** existentes
✅ **Feedback detallado** durante ejecución
✅ **Resumen completo** al finalizar

### Datos de Prueba Creados
✅ **2 Roles** (Administrador, Técnico)
✅ **2 Usuarios** (admin, juan)
✅ **2 Departamentos** (Urgencias, Bodega Central)
✅ **4 Ubicaciones** (Box 1, Box 2, Estante A, Estante B)
✅ **3 Tipos de Equipo** (Monitor, Desfibrilador, Camilla)
✅ **3 Estados** (Operativo, En Mantención, De Baja)
✅ **5 Activos** variados distribuidos en diferentes ubicaciones

---

## 🚀 Próximos Pasos

1. ✅ **Aplicar migraciones**: `python manage.py migrate`
2. ✅ **Poblar datos**: `python manage.py seed_data`
3. ✅ **Iniciar servidor**: `python manage.py runserver`
4. ✅ **Acceder al admin**: http://localhost:8000/admin/
5. ✅ **Probar la API**: http://localhost:8000/api/docs/
6. ✅ **Movilizar activos**: Usar el endpoint de movilización
7. ✅ **Verificar trazabilidad**: Ver historial y logs

---

## 📞 Soporte

Si encuentras algún problema:
1. Verifica que las migraciones estén aplicadas
2. Verifica que el comando seed se ejecutó correctamente
3. Revisa los logs del servidor para más detalles
4. Usa `python manage.py shell` para inspeccionar los datos


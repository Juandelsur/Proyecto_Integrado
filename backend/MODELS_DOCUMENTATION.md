# 📊 Documentación de Modelos - SCA Hospital

## Estructura de Base de Datos PostgreSQL

Este documento describe la estructura completa de los modelos de datos del Sistema de Control de Activos (SCA) Hospital.

---

## 🔑 Características Principales

- ✅ **Integridad Referencial**: Uso de `models.PROTECT` en todas las FKs críticas
- ✅ **Documentación Automática**: `help_text` en todos los campos para OpenAPI/Swagger
- ✅ **Auditoría en PostgreSQL**: JSONField para logs flexibles (reemplazo de MongoDB)
- ✅ **Trazabilidad Completa**: Historial de movimientos de activos
- ✅ **Custom User Model**: Extensión de AbstractUser con roles

---

## 📋 Modelos Implementados

### 1. Gestión de Usuarios y Roles

#### **Rol** (`Tbl_Roles`)
Define los roles de usuario en el sistema.

**Campos:**
- `nombre_rol` (CharField, unique): Nombre del rol
- `descripcion` (TextField): Descripción del rol
- `fecha_creacion` (DateTimeField): Fecha de creación
- `activo` (BooleanField): Estado del rol

**Ejemplos:** Administrador, Técnico, Supervisor, Usuario de Consulta

---

#### **Usuario** (`Tbl_Usuarios`)
Modelo de usuario personalizado que extiende AbstractUser.

**Campos Heredados:**
- `username`, `email`, `password`
- `first_name`, `last_name`
- `is_staff`, `is_active`, `is_superuser`
- `date_joined`, `last_login`

**Campos Adicionales:**
- `fk_id_rol` (FK → Rol, PROTECT): Rol asignado
- `rut` (CharField, unique): RUT del usuario
- `telefono` (CharField): Teléfono de contacto
- `cargo` (CharField): Cargo en el hospital
- `fecha_actualizacion` (DateTimeField): Última actualización

**Configuración en settings.py:**
```python
AUTH_USER_MODEL = 'api.Usuario'
```

---

### 2. Ubicaciones y Departamentos

#### **Departamento** (`Tbl_Departamentos`)
Representa departamentos o áreas del hospital.

**Campos:**
- `nombre_departamento` (CharField, unique): Nombre del departamento
- `codigo_departamento` (CharField, unique): Código único (ej: URG, PAB, UCI)
- `descripcion` (TextField): Descripción del departamento
- `responsable` (CharField): Nombre del responsable
- `activo` (BooleanField): Estado del departamento
- `fecha_creacion` (DateTimeField): Fecha de creación

**Ejemplos:** Urgencias, Pabellón, UCI, Radiología, Administración

---

#### **Ubicacion** (`Tbl_Ubicaciones`)
Ubicaciones específicas dentro de los departamentos.

**Campos:**
- `nombre_ubicacion` (CharField): Nombre de la ubicación
- `fk_departamento` (FK → Departamento, PROTECT): Departamento padre
- `codigo_ubicacion` (CharField, unique): Código único (ej: URG-101)
- `descripcion` (TextField): Descripción adicional
- `piso` (CharField): Piso o nivel
- `capacidad_activos` (IntegerField): Capacidad máxima de activos
- `activo` (BooleanField): Estado de la ubicación
- `fecha_creacion` (DateTimeField): Fecha de creación

**Constraint:** `unique_together = [['nombre_ubicacion', 'fk_departamento']]`

**Ejemplos:** Sala 101, Box 3, Oficina Administración

---

### 3. Maestros de Activos

#### **TipoEquipo** (`Tbl_Tipos_Equipo`)
Clasificación de tipos de equipos/activos.

**Campos:**
- `nombre_tipo` (CharField, unique): Nombre del tipo
- `codigo_tipo` (CharField, unique): Código único (ej: MON, PC, IMP)
- `descripcion` (TextField): Descripción del tipo
- `requiere_mantenimiento` (BooleanField): Si requiere mantenimiento
- `vida_util_anos` (IntegerField): Vida útil estimada
- `activo` (BooleanField): Estado del tipo
- `fecha_creacion` (DateTimeField): Fecha de creación

**Ejemplos:** Monitor, PC/Computador, Impresora, Equipo Médico, Mobiliario

---

#### **EstadoActivo** (`Tbl_Estados_Activo`)
Estados posibles de un activo.

**Campos:**
- `nombre_estado` (CharField, unique): Nombre del estado
- `codigo_estado` (CharField, unique): Código único (ej: OPE, MAN, REP)
- `descripcion` (TextField): Descripción del estado
- `permite_uso` (BooleanField): Si permite uso del activo
- `color_hex` (CharField): Color para UI (ej: #00FF00)
- `activo` (BooleanField): Estado del registro
- `fecha_creacion` (DateTimeField): Fecha de creación

**Ejemplos:** Operativo, En Mantención, En Reparación, De Baja, En Tránsito

---

### 4. Activos (Entidad Central)

#### **Activo** (`Tbl_Activos`)
Modelo central que representa un activo físico del hospital.

**Campos Principales:**
- `codigo_inventario` (CharField, unique, indexed): Código único de inventario
- `numero_serie` (CharField, unique, indexed): Número de serie del fabricante
- `marca` (CharField): Marca o fabricante
- `modelo` (CharField): Modelo específico
- `descripcion` (TextField): Descripción detallada

**Foreign Keys (PROTECT):**
- `fk_tipo_equipo` (FK → TipoEquipo): Tipo de equipo
- `fk_estado` (FK → EstadoActivo): Estado actual
- `fk_ubicacion_actual` (FK → Ubicacion): **Ubicación en tiempo real** (CRÍTICO)

**Información de Adquisición:**
- `fecha_adquisicion` (DateField): Fecha de compra
- `valor_adquisicion` (DecimalField): Valor en pesos
- `proveedor` (CharField): Nombre del proveedor

**Garantía:**
- `garantia_meses` (IntegerField): Duración de garantía
- `fecha_vencimiento_garantia` (DateField): Fecha de vencimiento

**Adicional:**
- `observaciones` (TextField): Observaciones
- `activo` (BooleanField): Estado del registro
- `fecha_creacion` (DateTimeField): Fecha de creación
- `fecha_actualizacion` (DateTimeField): Última actualización

**Métodos:**
- `get_nombre_completo()`: Nombre completo con detalles
- `esta_en_garantia()`: Verifica si está en garantía
- `get_ubicacion_completa()`: Ubicación con departamento

**Índices:** codigo_inventario, numero_serie, fk_ubicacion_actual, fk_estado

---

### 5. Trazabilidad (Transaccional)

#### **HistorialMovimiento** (`Tbl_Historial_Movimientos`)
Registra todos los movimientos de activos entre ubicaciones.

**Campos:**
- `fk_activo` (FK → Activo, PROTECT): Activo movido
- `fk_usuario_registra` (FK → Usuario, PROTECT): Usuario que registró
- `fk_ubicacion_origen` (FK → Ubicacion, PROTECT): Ubicación origen
- `fk_ubicacion_destino` (FK → Ubicacion, PROTECT): Ubicación destino
- `tipo_movimiento` (CharField, choices): Tipo de movimiento
- `fecha_movimiento` (DateTimeField, auto_now_add, indexed): Timestamp automático
- `motivo` (TextField): Motivo del movimiento
- `observaciones` (TextField): Observaciones adicionales
- `documento_referencia` (CharField): Número de documento

**Tipos de Movimiento:**
- TRASLADO, ASIGNACION, DEVOLUCION
- MANTENIMIENTO, RETORNO_MANTENIMIENTO
- BAJA, REUBICACION

**Métodos:**
- `get_descripcion_completa()`: Descripción detallada del movimiento

**Índices:** (fk_activo, fecha_movimiento), fecha_movimiento, fk_usuario_registra

---

### 6. Auditoría (Reemplazo de MongoDB)

#### **AuditoriaLog** (`Tbl_Auditoria_Logs`)
Registra todas las acciones de auditoría del sistema usando PostgreSQL.

**IMPORTANTE:** Usa `JSONField` para detalles flexibles (reemplazo de MongoDB).

**Campos:**
- `fk_usuario` (FK → Usuario, SET_NULL): Usuario que realizó la acción
- `accion` (CharField, choices, indexed): Tipo de acción
- `timestamp` (DateTimeField, auto_now_add, indexed): Timestamp automático
- `detalle_accion` (JSONField): **Detalles flexibles en JSON**
- `modelo_afectado` (CharField, indexed): Modelo/tabla afectado
- `objeto_id` (CharField): ID del objeto afectado
- `ip_address` (GenericIPAddressField): IP del usuario
- `user_agent` (TextField): User Agent del navegador
- `resultado` (CharField, choices): SUCCESS, FAILED, PARTIAL
- `mensaje_error` (TextField): Mensaje de error si falló

**Tipos de Acción:**
- CREATE, UPDATE, DELETE
- LOGIN, LOGOUT
- EXPORT, IMPORT, PRINT
- VIEW, DOWNLOAD, UPLOAD
- CHANGE_PASSWORD, PERMISSION_CHANGE
- CONFIG_CHANGE, REPORT_GENERATE
- OTHER

**Métodos:**
- `get_descripcion_completa()`: Descripción detallada del log
- `registrar_accion()` (classmethod): Método helper para registrar acciones

**Ejemplo de Uso:**
```python
AuditoriaLog.registrar_accion(
    usuario=request.user,
    accion='CREATE',
    detalle={'campo': 'valor', 'cambios': {...}},
    modelo='Activo',
    objeto_id='ACT-2024-001',
    ip=request.META.get('REMOTE_ADDR'),
    user_agent=request.META.get('HTTP_USER_AGENT')
)
```

**Índices:** timestamp, (fk_usuario, timestamp), (accion, timestamp), (modelo_afectado, timestamp)

---

## 🔒 Políticas de Integridad Referencial

### `models.PROTECT`
Usado en todas las FKs críticas para evitar eliminaciones accidentales:
- Rol → Usuario
- Departamento → Ubicacion
- TipoEquipo → Activo
- EstadoActivo → Activo
- Ubicacion → Activo
- Activo → HistorialMovimiento
- Usuario → HistorialMovimiento
- Ubicacion → HistorialMovimiento

### `models.SET_NULL`
Usado solo en AuditoriaLog para mantener logs aunque se elimine el usuario.

---

## 📚 Próximos Pasos

1. **Crear migraciones:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Crear superusuario:**
   ```bash
   python manage.py createsuperuser
   ```

3. **Acceder al admin:**
   http://localhost:8000/admin/

4. **Ver documentación API:**
   http://localhost:8000/api/docs/

---

## 🎯 Ventajas de esta Estructura

✅ **Sin MongoDB**: Todo en PostgreSQL con JSONField
✅ **Documentación Automática**: help_text genera Swagger/OpenAPI
✅ **Integridad Garantizada**: PROTECT evita borrados accidentales
✅ **Trazabilidad Completa**: Historial de movimientos y auditoría
✅ **Escalable**: Estructura preparada para crecimiento
✅ **Mantenible**: Código bien documentado y organizado


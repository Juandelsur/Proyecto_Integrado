# 📊 Esquema Exacto de Modelos - core/models.py

## ✅ Implementación del Diseño de Base de Datos

Este documento describe el esquema **EXACTO** implementado en `core/models.py` que replica fielmente el diseño de base de datos.

---

## 🔑 Características Clave

- ✅ **Nombres de tablas exactos**: Uso de `db_table` en Meta
- ✅ **Nombres de columnas FK exactos**: Uso de `db_column='fk_id_...'` en Foreign Keys
- ✅ **Integridad referencial**: `models.PROTECT` en todas las FKs críticas
- ✅ **Documentación automática**: `help_text` para OpenAPI/Swagger
- ✅ **PostgreSQL puro**: JSONField para auditoría (sin MongoDB)

---

## 📋 Modelos Implementados

### 1. Rol (`Tbl_Roles`)

```python
class Rol(models.Model):
    nombre_rol = models.CharField(max_length=100, unique=True)
    
    class Meta:
        db_table = 'Tbl_Roles'
```

**Tabla en DB**: `Tbl_Roles`

**Campos**:
- `id` (AutoField, PK) - Generado automáticamente por Django
- `nombre_rol` (VARCHAR(100), UNIQUE)

---

### 2. Usuario (`Tbl_Usuarios`)

```python
class Usuario(AbstractUser):
    nombre_completo = models.CharField(max_length=200)
    rol = models.ForeignKey(Rol, db_column='fk_id_rol', ...)
    
    class Meta:
        db_table = 'Tbl_Usuarios'
```

**Tabla en DB**: `Tbl_Usuarios`

**Campos propios**:
- `id` (AutoField, PK)
- `nombre_completo` (VARCHAR(200))
- `fk_id_rol` (INTEGER, FK → Tbl_Roles.id) ⚠️ **Nombre exacto en DB**

**Campos heredados de AbstractUser**:
- `username`, `password`, `email`
- `is_active`, `is_staff`, `is_superuser`
- `date_joined`, `last_login`

**Configuración en settings.py**:
```python
AUTH_USER_MODEL = 'core.Usuario'
```

---

### 3. Departamento (`Tbl_Departamentos`)

```python
class Departamento(models.Model):
    nombre_departamento = models.CharField(max_length=100, unique=True)
    
    class Meta:
        db_table = 'Tbl_Departamentos'
```

**Tabla en DB**: `Tbl_Departamentos`

**Campos**:
- `id` (AutoField, PK)
- `nombre_departamento` (VARCHAR(100), UNIQUE)

---

### 4. Ubicacion (`Tbl_Ubicaciones`)

```python
class Ubicacion(models.Model):
    nombre_ubicacion = models.CharField(max_length=100)
    departamento = models.ForeignKey(Departamento, db_column='fk_id_departamento', ...)
    
    class Meta:
        db_table = 'Tbl_Ubicaciones'
        unique_together = [['nombre_ubicacion', 'departamento']]
```

**Tabla en DB**: `Tbl_Ubicaciones`

**Campos**:
- `id` (AutoField, PK)
- `nombre_ubicacion` (VARCHAR(100))
- `fk_id_departamento` (INTEGER, FK → Tbl_Departamentos.id) ⚠️ **Nombre exacto en DB**

**Constraint**: UNIQUE(nombre_ubicacion, fk_id_departamento)

---

### 5. TipoEquipo (`Tbl_Tipos_Equipo`)

```python
class TipoEquipo(models.Model):
    nombre_tipo = models.CharField(max_length=100, unique=True)
    
    class Meta:
        db_table = 'Tbl_Tipos_Equipo'
```

**Tabla en DB**: `Tbl_Tipos_Equipo`

**Campos**:
- `id` (AutoField, PK)
- `nombre_tipo` (VARCHAR(100), UNIQUE)

---

### 6. EstadoActivo (`Tbl_Estados_Activo`)

```python
class EstadoActivo(models.Model):
    nombre_estado = models.CharField(max_length=50, unique=True)
    
    class Meta:
        db_table = 'Tbl_Estados_Activo'
```

**Tabla en DB**: `Tbl_Estados_Activo`

**Campos**:
- `id` (AutoField, PK)
- `nombre_estado` (VARCHAR(50), UNIQUE)

---

### 7. Activo (`Tbl_Activos`)

```python
class Activo(models.Model):
    codigo_inventario = models.CharField(max_length=50, unique=True)
    numero_serie = models.CharField(max_length=100, unique=True)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    fecha_alta = models.DateTimeField(auto_now_add=True)
    tipo = models.ForeignKey(TipoEquipo, db_column='fk_id_tipo', ...)
    estado = models.ForeignKey(EstadoActivo, db_column='fk_id_estado', ...)
    ubicacion_actual = models.ForeignKey(Ubicacion, db_column='fk_id_ubicacion_actual', ...)
    
    class Meta:
        db_table = 'Tbl_Activos'
```

**Tabla en DB**: `Tbl_Activos`

**Campos**:
- `id` (AutoField, PK)
- `codigo_inventario` (VARCHAR(50), UNIQUE, INDEXED)
- `numero_serie` (VARCHAR(100), UNIQUE, INDEXED)
- `marca` (VARCHAR(100))
- `modelo` (VARCHAR(100))
- `fecha_alta` (TIMESTAMP, auto_now_add)
- `fk_id_tipo` (INTEGER, FK → Tbl_Tipos_Equipo.id) ⚠️ **Nombre exacto en DB**
- `fk_id_estado` (INTEGER, FK → Tbl_Estados_Activo.id) ⚠️ **Nombre exacto en DB**
- `fk_id_ubicacion_actual` (INTEGER, FK → Tbl_Ubicaciones.id) ⚠️ **Nombre exacto en DB**

**Índices**:
- INDEX(codigo_inventario)
- INDEX(numero_serie)
- INDEX(fecha_alta)

---

### 8. HistorialMovimiento (`Tbl_Historial_Movimientos`)

```python
class HistorialMovimiento(models.Model):
    activo = models.ForeignKey(Activo, db_column='fk_id_activo', ...)
    usuario_registra = models.ForeignKey(Usuario, db_column='fk_id_usuario_registra', ...)
    ubicacion_origen = models.ForeignKey(Ubicacion, db_column='fk_id_ubicacion_origen', ...)
    ubicacion_destino = models.ForeignKey(Ubicacion, db_column='fk_id_ubicacion_destino', ...)
    fecha_movimiento = models.DateTimeField(auto_now_add=True)
    tipo_movimiento = models.CharField(max_length=30, choices=...)
    comentarios = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'Tbl_Historial_Movimientos'
```

**Tabla en DB**: `Tbl_Historial_Movimientos`

**Campos**:
- `id` (AutoField, PK)
- `fk_id_activo` (INTEGER, FK → Tbl_Activos.id) ⚠️ **Nombre exacto en DB**
- `fk_id_usuario_registra` (INTEGER, FK → Tbl_Usuarios.id) ⚠️ **Nombre exacto en DB**
- `fk_id_ubicacion_origen` (INTEGER, FK → Tbl_Ubicaciones.id) ⚠️ **Nombre exacto en DB**
- `fk_id_ubicacion_destino` (INTEGER, FK → Tbl_Ubicaciones.id) ⚠️ **Nombre exacto en DB**
- `fecha_movimiento` (TIMESTAMP, auto_now_add, INDEXED)
- `tipo_movimiento` (VARCHAR(30))
- `comentarios` (TEXT, nullable)

**Índices**:
- INDEX(fecha_movimiento)
- INDEX(fecha_movimiento DESC)

---

### 9. AuditoriaLog (`Tbl_Auditoria_Logs`)

```python
class AuditoriaLog(models.Model):
    usuario = models.ForeignKey(Usuario, db_column='fk_id_usuario', on_delete=models.SET_NULL, ...)
    accion = models.CharField(max_length=50, choices=...)
    detalle_accion = models.JSONField(default=dict)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'Tbl_Auditoria_Logs'
```

**Tabla en DB**: `Tbl_Auditoria_Logs`

**Campos**:
- `id` (AutoField, PK)
- `fk_id_usuario` (INTEGER, FK → Tbl_Usuarios.id, nullable) ⚠️ **Nombre exacto en DB**
- `accion` (VARCHAR(50), INDEXED)
- `detalle_accion` (JSONB) - **PostgreSQL JSONField**
- `timestamp` (TIMESTAMP, auto_now_add, INDEXED)

**Índices**:
- INDEX(timestamp DESC)
- INDEX(accion, timestamp DESC)

---

## 🔒 Políticas de Integridad Referencial

### `models.PROTECT` (Todas las FKs excepto auditoría)
- Rol → Usuario
- Departamento → Ubicacion
- TipoEquipo → Activo
- EstadoActivo → Activo
- Ubicacion → Activo
- Activo → HistorialMovimiento
- Usuario → HistorialMovimiento
- Ubicacion → HistorialMovimiento (origen y destino)

### `models.SET_NULL` (Solo auditoría)
- Usuario → AuditoriaLog (permite mantener logs aunque se elimine el usuario)

---

## 📚 Próximos Pasos

### 1️⃣ Crear Migraciones

```bash
cd backend
python3 manage.py makemigrations core
python3 manage.py migrate
```

### 2️⃣ Crear Superusuario

```bash
python3 manage.py createsuperuser
```

### 3️⃣ Verificar en Admin

```
http://localhost:8000/admin/
```

---

## ✅ Verificación del Esquema

Para verificar que las tablas se crearon con los nombres exactos:

```sql
-- Conectar a PostgreSQL
psql -U sca_user -d sca_db

-- Listar tablas
\dt

-- Ver estructura de una tabla
\d Tbl_Activos

-- Verificar nombres de columnas FK
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'Tbl_Activos' 
AND column_name LIKE 'fk_%';
```

**Resultado esperado**:
```
 column_name           | data_type
-----------------------+-----------
 fk_id_tipo            | integer
 fk_id_estado          | integer
 fk_id_ubicacion_actual| integer
```

---

## 🎯 Resumen de Nombres Exactos

| Modelo Python | Tabla en DB | FK en Python | Columna FK en DB |
|---------------|-------------|--------------|------------------|
| Rol | Tbl_Roles | - | - |
| Usuario | Tbl_Usuarios | rol | fk_id_rol |
| Departamento | Tbl_Departamentos | - | - |
| Ubicacion | Tbl_Ubicaciones | departamento | fk_id_departamento |
| TipoEquipo | Tbl_Tipos_Equipo | - | - |
| EstadoActivo | Tbl_Estados_Activo | - | - |
| Activo | Tbl_Activos | tipo | fk_id_tipo |
| | | estado | fk_id_estado |
| | | ubicacion_actual | fk_id_ubicacion_actual |
| HistorialMovimiento | Tbl_Historial_Movimientos | activo | fk_id_activo |
| | | usuario_registra | fk_id_usuario_registra |
| | | ubicacion_origen | fk_id_ubicacion_origen |
| | | ubicacion_destino | fk_id_ubicacion_destino |
| AuditoriaLog | Tbl_Auditoria_Logs | usuario | fk_id_usuario |

---

## 💡 Notas Importantes

1. **db_column**: Usado en TODAS las Foreign Keys para mantener nombres exactos del diseño
2. **db_table**: Usado en TODOS los modelos para nombres exactos de tablas
3. **Custom User Model**: Configurado en settings.py como `AUTH_USER_MODEL = 'core.Usuario'`
4. **JSONField**: Nativo de PostgreSQL, no requiere MongoDB
5. **Integridad**: PROTECT evita eliminaciones accidentales en cascada


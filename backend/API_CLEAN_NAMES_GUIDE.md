# 🎯 Guía de Nombres Limpios en la API

## ✅ Cambios Implementados

Se han regenerado los archivos de la capa API con **nombres limpios para el frontend**, eliminando los prefijos técnicos de base de datos.

---

## 📋 Comparación: Base de Datos vs API

### Antes (Nombres Técnicos de DB)
```json
{
  "fk_id_rol": 1,
  "fk_id_departamento": 2,
  "fk_id_tipo": 3,
  "fk_id_estado": 4,
  "fk_id_ubicacion_actual": 5
}
```

### Ahora (Nombres Limpios para Frontend)
```json
{
  "rol_id": 1,
  "departamento_id": 2,
  "tipo_id": 3,
  "estado_id": 4,
  "ubicacion_actual_id": 5
}
```

---

## 🔄 Patrón Híbrido Lectura/Escritura

### Concepto
- **Escritura (POST/PUT/PATCH)**: El frontend envía solo IDs (ej: `rol_id: 1`)
- **Lectura (GET)**: El backend devuelve objetos completos (ej: `rol: {id: 1, nombre_rol: "Admin"}`)

### Ventajas
✅ **Simplicidad en escritura**: Solo envías IDs  
✅ **Completitud en lectura**: Recibes toda la información necesaria  
✅ **Rendimiento**: Evita N+1 queries en el frontend  
✅ **UX mejorada**: No necesitas hacer múltiples peticiones  

---

## 📝 Ejemplos Prácticos

### 1. Crear una Ubicación

**Request (POST /api/ubicaciones/)**
```json
{
  "nombre_ubicacion": "Sala 101",
  "departamento_id": 1
}
```

**Response (201 Created)**
```json
{
  "id": 1,
  "nombre_ubicacion": "Sala 101",
  "departamento": {
    "id": 1,
    "nombre_departamento": "Urgencias"
  }
}
```

**Nota**: Enviaste solo `departamento_id`, pero recibes el objeto `departamento` completo.

---

### 2. Crear un Usuario

**Request (POST /api/usuarios/)**
```json
{
  "username": "jperez",
  "password": "password123",
  "email": "jperez@hospital.cl",
  "nombre_completo": "Juan Pérez",
  "rol_id": 2
}
```

**Response (201 Created)**
```json
{
  "id": 1,
  "username": "jperez",
  "email": "jperez@hospital.cl",
  "nombre_completo": "Juan Pérez",
  "rol": {
    "id": 2,
    "nombre_rol": "Técnico"
  },
  "is_active": true,
  "is_staff": false,
  "date_joined": "2024-01-15T10:30:00Z",
  "last_login": null
}
```

**Seguridad**: El `password` NUNCA se devuelve en las respuestas.

---

### 3. Crear un Activo (CRÍTICO)

**Request (POST /api/activos/)**
```json
{
  "codigo_inventario": "ACT-2024-001",
  "numero_serie": "SN123456",
  "marca": "HP",
  "modelo": "EliteBook 840 G8",
  "tipo_id": 1,
  "estado_id": 1,
  "ubicacion_actual_id": 1
}
```

**Response (201 Created)**
```json
{
  "id": 1,
  "codigo_inventario": "ACT-2024-001",
  "numero_serie": "SN123456",
  "marca": "HP",
  "modelo": "EliteBook 840 G8",
  "fecha_alta": "2024-01-15T10:30:00Z",
  "tipo": {
    "id": 1,
    "nombre_tipo": "Computador"
  },
  "estado": {
    "id": 1,
    "nombre_estado": "Operativo"
  },
  "ubicacion_actual": {
    "id": 1,
    "nombre_ubicacion": "Sala 101",
    "departamento": {
      "id": 1,
      "nombre_departamento": "Urgencias"
    }
  }
}
```

**Ventaja**: En una sola petición GET obtienes:
- Información del activo
- Tipo completo
- Estado completo
- Ubicación completa con departamento

**Sin este patrón**, necesitarías 4 peticiones:
1. GET /api/activos/1/
2. GET /api/tipos-equipo/1/
3. GET /api/estados-activo/1/
4. GET /api/ubicaciones/1/

---

### 4. Registrar un Movimiento

**Request (POST /api/historial-movimientos/)**
```json
{
  "activo_id": 1,
  "usuario_registra_id": 1,
  "ubicacion_origen_id": 1,
  "ubicacion_destino_id": 2,
  "tipo_movimiento": "TRASLADO",
  "comentarios": "Traslado por mantenimiento preventivo"
}
```

**Response (201 Created)**
```json
{
  "id": 1,
  "activo": {
    "id": 1,
    "codigo_inventario": "ACT-2024-001",
    "marca": "HP",
    "modelo": "EliteBook 840 G8"
  },
  "usuario_registra": {
    "id": 1,
    "username": "admin",
    "nombre_completo": "Administrador Sistema"
  },
  "ubicacion_origen": {
    "id": 1,
    "nombre_ubicacion": "Sala 101",
    "departamento": "Urgencias"
  },
  "ubicacion_destino": {
    "id": 2,
    "nombre_ubicacion": "Sala 102",
    "departamento": "Urgencias"
  },
  "fecha_movimiento": "2024-01-15T10:30:00Z",
  "tipo_movimiento": "TRASLADO",
  "comentarios": "Traslado por mantenimiento preventivo"
}
```

---

## 🔐 Auditoría (Solo Lectura)

### Consultar Logs

**Request (GET /api/auditoria-logs/)**

**Response (200 OK)**
```json
[
  {
    "id": 1,
    "usuario": 1,
    "usuario_username": "admin",
    "usuario_nombre_completo": "Administrador Sistema",
    "accion": "CREATE",
    "detalle_accion": {
      "modelo": "Activo",
      "objeto_id": "ACT-2024-001",
      "ip": "192.168.1.100"
    },
    "timestamp": "2024-01-15T10:30:00Z"
  }
]
```

**IMPORTANTE**: Este endpoint es de **SOLO LECTURA**. No puedes crear, modificar ni eliminar logs vía API.

---

## 📊 Optimizaciones SQL Implementadas

### Problema N+1 Queries

**Sin optimización** (100 activos):
```python
# ❌ MALO - Genera 301 queries SQL
Activo.objects.all()
```

**Con optimización** (100 activos):
```python
# ✅ BUENO - Genera 1 query SQL
Activo.objects.select_related(
    'tipo',
    'estado',
    'ubicacion_actual',
    'ubicacion_actual__departamento'
).all()
```

### ViewSets Optimizados

Todos los ViewSets con relaciones usan `select_related()`:

✅ **UbicacionViewSet**
```python
queryset = Ubicacion.objects.select_related('departamento').all()
```

✅ **UsuarioViewSet**
```python
queryset = Usuario.objects.select_related('rol').all()
```

✅ **ActivoViewSet** (CRÍTICO)
```python
queryset = Activo.objects.select_related(
    'tipo',
    'estado',
    'ubicacion_actual',
    'ubicacion_actual__departamento'
).all()
```

✅ **HistorialMovimientoViewSet**
```python
queryset = HistorialMovimiento.objects.select_related(
    'activo',
    'usuario_registra',
    'ubicacion_origen',
    'ubicacion_origen__departamento',
    'ubicacion_destino',
    'ubicacion_destino__departamento'
).all()
```

✅ **AuditoriaLogViewSet**
```python
queryset = AuditoriaLog.objects.select_related('usuario').all()
```

---

## 📚 Tags de Documentación OpenAPI

Los endpoints están organizados en 4 categorías:

### 1. Maestros
- Roles
- Departamentos
- Tipos de Equipo
- Estados de Activo

### 2. Core
- Ubicaciones
- Usuarios
- Activos (CRÍTICO)

### 3. Trazabilidad
- Historial de Movimientos

### 4. Auditoría
- Logs de Auditoría (Solo Lectura)

---

## 🎯 Resumen de Cambios

### Serializers (core/serializers.py)
✅ Nombres limpios: `rol_id`, `departamento_id`, `tipo_id`, etc.
✅ Patrón híbrido: IDs en escritura, objetos en lectura
✅ Password seguro (write_only)
✅ Documentación completa con docstrings

### Views (core/views.py)
✅ Tags organizados: Maestros, Core, Trazabilidad, Auditoría
✅ Optimización SQL con select_related()
✅ ReadOnlyModelViewSet para auditoría
✅ Documentación con @extend_schema_view

### URLs (core/urls.py)
✅ Rutas limpias: /api/roles/, /api/activos/, /api/logs/
✅ Router configurado correctamente
✅ Documentación de rutas generadas

---

## 🚀 Próximos Pasos

### 1. Verificar la API
```bash
cd backend
python3 manage.py check
```

### 2. Crear Migraciones
```bash
python3 manage.py makemigrations core
python3 manage.py migrate
```

### 3. Crear Superusuario
```bash
python3 manage.py createsuperuser
```

### 4. Iniciar Servidor
```bash
python3 manage.py runserver
```

### 5. Probar en Swagger
```
http://localhost:8000/api/docs/
```

---

## 💡 Consejos para el Frontend

### 1. Crear Activo
```javascript
// Envía solo IDs
const response = await fetch('/api/activos/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    codigo_inventario: 'ACT-2024-001',
    numero_serie: 'SN123456',
    marca: 'HP',
    modelo: 'EliteBook 840 G8',
    tipo_id: 1,           // Solo el ID
    estado_id: 1,         // Solo el ID
    ubicacion_actual_id: 1 // Solo el ID
  })
});

// Recibes objetos completos
const activo = await response.json();
console.log(activo.tipo.nombre_tipo);  // "Computador"
console.log(activo.estado.nombre_estado);  // "Operativo"
console.log(activo.ubicacion_actual.departamento.nombre_departamento);  // "Urgencias"
```

### 2. Listar Activos
```javascript
// Una sola petición
const response = await fetch('/api/activos/', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});

const activos = await response.json();

// Toda la información ya está disponible
activos.forEach(activo => {
  console.log(`${activo.codigo_inventario} - ${activo.tipo.nombre_tipo}`);
  console.log(`Estado: ${activo.estado.nombre_estado}`);
  console.log(`Ubicación: ${activo.ubicacion_actual.nombre_ubicacion}`);
});
```

---

## ✅ Resumen Final

✅ **Nombres limpios** para el frontend (sin prefijos técnicos)
✅ **Patrón híbrido** (IDs en escritura, objetos en lectura)
✅ **Optimización SQL** (select_related en todos los ViewSets)
✅ **Seguridad** (password write_only, JWT requerido)
✅ **Documentación** (OpenAPI con tags organizados)
✅ **Auditoría** (endpoint de solo lectura para Dashboard Admin)
✅ **Rendimiento** (evita N+1 queries en frontend y backend)


# 🚀 Documentación de la API REST - SCA Hospital

## ✅ Implementación Completada

Se han generado exitosamente los archivos para exponer los modelos vía API REST usando Django REST Framework.

---

## 📁 Archivos Generados

### 1. **core/serializers.py** (407 líneas)
- ✅ 9 serializers implementados
- ✅ Manejo seguro de passwords (write_only)
- ✅ Relaciones anidadas en lectura (to_representation)
- ✅ Validación automática de datos

### 2. **core/views.py** (373 líneas)
- ✅ 9 ViewSets implementados
- ✅ Autenticación requerida (IsAuthenticated)
- ✅ Documentación con drf-spectacular
- ✅ Optimización con select_related()

### 3. **core/urls.py** (155 líneas)
- ✅ Router configurado
- ✅ 9 recursos registrados
- ✅ URLs RESTful automáticas

### 4. **config/urls.py** (actualizado)
- ✅ Integración con core.urls
- ✅ JWT y documentación configurados

---

## 🔐 Seguridad

### Autenticación Requerida
**Todos los endpoints requieren autenticación JWT.**

```python
permission_classes = [IsAuthenticated]
```

### Obtener Token JWT

```bash
# 1. Obtener token
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "tu_password"
  }'

# Respuesta:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

# 2. Usar el token en las peticiones
curl -X GET http://localhost:8000/api/activos/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

---

## 📋 Endpoints Disponibles

### **Maestros Básicos**

#### 1. Roles
```
GET    /api/roles/           - Listar todos los roles
POST   /api/roles/           - Crear un nuevo rol
GET    /api/roles/{id}/      - Obtener un rol específico
PUT    /api/roles/{id}/      - Actualizar un rol completo
PATCH  /api/roles/{id}/      - Actualizar parcialmente un rol
DELETE /api/roles/{id}/      - Eliminar un rol
```

#### 2. Departamentos
```
GET    /api/departamentos/           - Listar todos los departamentos
POST   /api/departamentos/           - Crear un nuevo departamento
GET    /api/departamentos/{id}/      - Obtener un departamento específico
PUT    /api/departamentos/{id}/      - Actualizar un departamento completo
PATCH  /api/departamentos/{id}/      - Actualizar parcialmente un departamento
DELETE /api/departamentos/{id}/      - Eliminar un departamento
```

#### 3. Tipos de Equipo
```
GET    /api/tipos-equipo/           - Listar todos los tipos de equipo
POST   /api/tipos-equipo/           - Crear un nuevo tipo de equipo
GET    /api/tipos-equipo/{id}/      - Obtener un tipo de equipo específico
PUT    /api/tipos-equipo/{id}/      - Actualizar un tipo de equipo completo
PATCH  /api/tipos-equipo/{id}/      - Actualizar parcialmente un tipo de equipo
DELETE /api/tipos-equipo/{id}/      - Eliminar un tipo de equipo
```

#### 4. Estados de Activo
```
GET    /api/estados-activo/           - Listar todos los estados de activo
POST   /api/estados-activo/           - Crear un nuevo estado de activo
GET    /api/estados-activo/{id}/      - Obtener un estado de activo específico
PUT    /api/estados-activo/{id}/      - Actualizar un estado de activo completo
PATCH  /api/estados-activo/{id}/      - Actualizar parcialmente un estado de activo
DELETE /api/estados-activo/{id}/      - Eliminar un estado de activo
```

### **Entidades con Relaciones**

#### 5. Ubicaciones
```
GET    /api/ubicaciones/           - Listar todas las ubicaciones
POST   /api/ubicaciones/           - Crear una nueva ubicación
GET    /api/ubicaciones/{id}/      - Obtener una ubicación específica
PUT    /api/ubicaciones/{id}/      - Actualizar una ubicación completa
PATCH  /api/ubicaciones/{id}/      - Actualizar parcialmente una ubicación
DELETE /api/ubicaciones/{id}/      - Eliminar una ubicación
```

**Optimización**: Usa `select_related('departamento')` para evitar N+1 queries.

**Respuesta de lectura** (con departamento anidado):
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

#### 6. Usuarios
```
GET    /api/usuarios/           - Listar todos los usuarios
POST   /api/usuarios/           - Crear un nuevo usuario
GET    /api/usuarios/{id}/      - Obtener un usuario específico
PUT    /api/usuarios/{id}/      - Actualizar un usuario completo
PATCH  /api/usuarios/{id}/      - Actualizar parcialmente un usuario
DELETE /api/usuarios/{id}/      - Eliminar un usuario
```

**Seguridad**: El campo `password` es `write_only` (nunca se devuelve en las respuestas).

**Crear usuario**:
```json
POST /api/usuarios/
{
  "username": "jperez",
  "password": "password123",
  "email": "jperez@hospital.cl",
  "nombre_completo": "Juan Pérez",
  "rol": 1
}
```

**Respuesta de lectura** (sin password, con rol anidado):
```json
{
  "id": 1,
  "username": "jperez",
  "email": "jperez@hospital.cl",
  "nombre_completo": "Juan Pérez",
  "rol": {
    "id": 1,
    "nombre_rol": "Técnico"
  },
  "is_active": true,
  "is_staff": false,
  "date_joined": "2024-01-15T10:30:00Z",
  "last_login": null
}
```

### **Activos (CRÍTICO)**

#### 7. Activos
```
GET    /api/activos/           - Listar todos los activos con información completa
POST   /api/activos/           - Crear un nuevo activo
GET    /api/activos/{id}/      - Obtener un activo específico
PUT    /api/activos/{id}/      - Actualizar un activo completo
PATCH  /api/activos/{id}/      - Actualizar parcialmente un activo
DELETE /api/activos/{id}/      - Eliminar un activo
```

**Optimización CRÍTICA**: Usa `select_related('tipo', 'estado', 'ubicacion_actual', 'ubicacion_actual__departamento')`.

**Crear activo** (escritura con IDs):
```json
POST /api/activos/
{
  "codigo_inventario": "ACT-2024-001",
  "numero_serie": "SN123456",
  "marca": "HP",
  "modelo": "EliteBook 840 G8",
  "tipo": 1,
  "estado": 1,
  "ubicacion_actual": 1
}
```

**Respuesta de lectura** (con objetos anidados completos):
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

**Ventaja**: El frontend obtiene toda la información en una sola petición, sin necesidad de hacer 3 peticiones adicionales para obtener tipo, estado y ubicación.

### **Trazabilidad y Auditoría**

#### 8. Historial de Movimientos
```
GET    /api/historial-movimientos/           - Listar todos los movimientos
POST   /api/historial-movimientos/           - Registrar un nuevo movimiento
GET    /api/historial-movimientos/{id}/      - Obtener un movimiento específico
PUT    /api/historial-movimientos/{id}/      - Actualizar un movimiento completo
PATCH  /api/historial-movimientos/{id}/      - Actualizar parcialmente un movimiento
DELETE /api/historial-movimientos/{id}/      - Eliminar un movimiento
```

**Registrar movimiento**:
```json
POST /api/historial-movimientos/
{
  "activo": 1,
  "usuario_registra": 1,
  "ubicacion_origen": 1,
  "ubicacion_destino": 2,
  "tipo_movimiento": "TRASLADO",
  "comentarios": "Traslado por mantenimiento preventivo"
}
```

#### 9. Auditoría (SOLO LECTURA)
```
GET    /api/auditoria-logs/           - Listar todos los logs de auditoría
GET    /api/auditoria-logs/{id}/      - Obtener un log específico
```

**IMPORTANTE**: Este endpoint es de solo lectura. Los logs se crean automáticamente usando:
```python
from core.models import AuditoriaLog

AuditoriaLog.registrar_accion(
    usuario=request.user,
    accion='CREATE',
    detalle={'modelo': 'Activo', 'objeto_id': 'ACT-2024-001'}
)
```

---

## 📊 Optimización de Queries

### Problema N+1 Queries

**Sin optimización** (100 activos = 301 queries):
```python
queryset = Activo.objects.all()  # ❌ MALO
```

**Con optimización** (100 activos = 1 query):
```python
queryset = Activo.objects.select_related(
    'tipo',
    'estado',
    'ubicacion_actual',
    'ubicacion_actual__departamento'
).all()  # ✅ BUENO
```

### ViewSets Optimizados

Todos los ViewSets con relaciones usan `select_related()`:
- ✅ UbicacionViewSet
- ✅ UsuarioViewSet
- ✅ ActivoViewSet (CRÍTICO)
- ✅ HistorialMovimientoViewSet
- ✅ AuditoriaLogViewSet

---

## 📚 Documentación Automática

### Swagger UI (Interactivo)
```
http://localhost:8000/api/docs/
```

### ReDoc (Documentación)
```
http://localhost:8000/api/redoc/
```

### Schema OpenAPI (JSON)
```
http://localhost:8000/api/schema/
```

---

## 🧪 Pruebas con cURL

### 1. Obtener Token
```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### 2. Listar Activos
```bash
curl -X GET http://localhost:8000/api/activos/ \
  -H "Authorization: Bearer <tu_token>"
```

### 3. Crear Activo
```bash
curl -X POST http://localhost:8000/api/activos/ \
  -H "Authorization: Bearer <tu_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "codigo_inventario": "ACT-2024-001",
    "numero_serie": "SN123456",
    "marca": "HP",
    "modelo": "EliteBook 840 G8",
    "tipo": 1,
    "estado": 1,
    "ubicacion_actual": 1
  }'
```

### 4. Actualizar Activo (PATCH)
```bash
curl -X PATCH http://localhost:8000/api/activos/1/ \
  -H "Authorization: Bearer <tu_token>" \
  -H "Content-Type: application/json" \
  -d '{"estado": 2}'
```

---

## 🎯 Características Implementadas

### ✅ Serializers
- ✅ 9 serializers completos
- ✅ Password seguro (write_only)
- ✅ Relaciones anidadas en lectura
- ✅ Validación automática

### ✅ ViewSets
- ✅ 9 ViewSets con CRUD completo
- ✅ Autenticación JWT requerida
- ✅ Documentación con @extend_schema
- ✅ Optimización con select_related()

### ✅ URLs
- ✅ Router configurado
- ✅ URLs RESTful automáticas
- ✅ Integración con JWT y Swagger

### ✅ Seguridad
- ✅ IsAuthenticated en todos los endpoints
- ✅ Password hasheado correctamente
- ✅ Tokens JWT con expiración

---

## 🚀 Próximos Pasos

### 1️⃣ Verificar que no hay errores
```bash
cd backend
python3 manage.py check
```

### 2️⃣ Crear y aplicar migraciones
```bash
python3 manage.py makemigrations core
python3 manage.py migrate
```

### 3️⃣ Crear superusuario
```bash
python3 manage.py createsuperuser
```

### 4️⃣ Iniciar servidor
```bash
python3 manage.py runserver
```

### 5️⃣ Probar la API
- Swagger: http://localhost:8000/api/docs/
- Admin: http://localhost:8000/admin/

---

## 📝 Resumen

✅ **3 archivos creados**: serializers.py, views.py, urls.py
✅ **1 archivo actualizado**: config/urls.py
✅ **9 recursos expuestos**: Roles, Departamentos, Tipos, Estados, Ubicaciones, Usuarios, Activos, Historial, Auditoría
✅ **Autenticación JWT**: Todos los endpoints protegidos
✅ **Documentación automática**: Swagger y ReDoc
✅ **Optimización**: select_related() en todos los ViewSets con relaciones
✅ **Relaciones anidadas**: to_representation() para respuestas completas
✅ **Seguridad**: Password write_only, tokens JWT

---

## 💡 Notas Importantes

1. **Relaciones Anidadas**: Los serializers devuelven objetos completos en lectura, pero aceptan IDs en escritura.
2. **Optimización**: Todos los ViewSets con relaciones usan `select_related()` para evitar N+1 queries.
3. **Seguridad**: El password nunca se devuelve en las respuestas (write_only=True).
4. **Auditoría**: Los logs son de solo lectura y se crean automáticamente.
5. **Documentación**: Swagger UI permite probar todos los endpoints interactivamente.


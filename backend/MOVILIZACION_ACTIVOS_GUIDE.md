# 🚚 Guía de Movilización de Activos (HU2)

## ✅ Implementación Completada

Se ha implementado exitosamente la **Historia de Usuario HU2: Movilización de Activos** con todas las garantías ACID y de seguridad requeridas.

---

## 📋 Archivos Modificados

### 1. `core/serializers.py`
- ✅ Agregado `MovilizacionInputSerializer` para validación de entrada
- ✅ Validación automática de existencia de ubicación destino
- ✅ Documentación completa con ejemplos

### 2. `core/views.py`
- ✅ Agregada acción personalizada `movilizar` en `ActivoViewSet`
- ✅ Implementación transaccional con `transaction.atomic()`
- ✅ Registro en historial de movimientos (trazabilidad)
- ✅ Registro en auditoría con PostgreSQL JSONField (seguridad)
- ✅ Documentación OpenAPI con `@extend_schema`

---

## 🔐 Garantías ACID Implementadas

### Atomicidad
✅ **Todo o nada**: Si falla cualquier paso, toda la operación se revierte.

```python
with transaction.atomic():
    # 1. Actualizar ubicación del activo
    activo.ubicacion_actual = ubicacion_destino
    activo.save()
    
    # 2. Registrar en historial
    HistorialMovimiento.objects.create(...)
    
    # 3. Registrar en auditoría
    AuditoriaLog.objects.create(...)
```

### Consistencia
✅ **Estado válido**: Los datos siempre quedan en un estado consistente.
- El activo SIEMPRE tiene una ubicación válida
- El historial SIEMPRE tiene origen y destino válidos
- La auditoría SIEMPRE tiene todos los detalles

### Aislamiento
✅ **Sin interferencias**: Otras transacciones no ven estados intermedios.
- Django maneja el aislamiento automáticamente
- Nivel de aislamiento: READ COMMITTED (PostgreSQL default)

### Durabilidad
✅ **Permanencia**: Los cambios son permanentes una vez confirmados.
- PostgreSQL garantiza la durabilidad con WAL (Write-Ahead Logging)

---

## 🎯 Endpoint Implementado

### POST /api/activos/{id}/movilizar/

**Descripción**: Moviliza un activo a una nueva ubicación.

**Autenticación**: JWT Token requerido

**URL**: `http://localhost:8000/api/activos/{id}/movilizar/`

**Método**: POST

**Headers**:
```http
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

**Request Body**:
```json
{
  "id_ubicacion_destino": 5,
  "notas": "Traslado por mantenimiento preventivo programado"
}
```

**Response 200 OK**:
```json
{
  "status": "success",
  "message": "Activo movilizado con éxito",
  "data": {
    "activo_codigo": "ACT-2024-001",
    "ubicacion_origen": {
      "id": 1,
      "nombre": "Sala 101",
      "departamento": "Urgencias"
    },
    "ubicacion_destino": {
      "id": 5,
      "nombre": "Sala de Mantenimiento",
      "departamento": "Servicios Generales"
    },
    "fecha_movimiento": "2024-01-15T10:30:00Z",
    "usuario": "admin"
  }
}
```

**Response 400 Bad Request** (Validación):
```json
{
  "status": "error",
  "message": "Datos de entrada inválidos",
  "errors": {
    "id_ubicacion_destino": ["Este campo es requerido"]
  }
}
```

**Response 400 Bad Request** (Ubicación no existe):
```json
{
  "status": "error",
  "message": "La ubicación con ID 999 no existe"
}
```

**Response 400 Bad Request** (Misma ubicación):
```json
{
  "status": "error",
  "message": "El activo ya se encuentra en la ubicación destino"
}
```

**Response 404 Not Found**:
```json
{
  "detail": "No encontrado."
}
```

---

## 📊 Flujo de Ejecución

```
1. REQUEST
   ↓
2. VALIDACIÓN DE ENTRADA (MovilizacionInputSerializer)
   ↓
3. OBTENCIÓN DEL ACTIVO (get_object)
   ↓
4. VALIDACIÓN DE UBICACIÓN DESTINO
   ↓
5. VALIDACIÓN: ¿Misma ubicación?
   ↓
6. INICIO TRANSACCIÓN ATÓMICA
   ├─ 6.1: Actualizar activo.ubicacion_actual
   ├─ 6.2: Crear registro en HistorialMovimiento
   └─ 6.3: Crear registro en AuditoriaLog
   ↓
7. COMMIT TRANSACCIÓN
   ↓
8. RESPONSE 200 OK
```

---

## 🔍 Trazabilidad Implementada

### Historial de Movimientos (Tabla: Tbl_Historial_Movimientos)

Cada movilización crea un registro con:
- ✅ Activo movilizado
- ✅ Usuario que registró el movimiento
- ✅ Ubicación origen
- ✅ Ubicación destino
- ✅ Tipo de movimiento: 'TRASLADO'
- ✅ Fecha y hora exacta
- ✅ Comentarios/notas

### Auditoría de Seguridad (Tabla: Tbl_Auditoria_Logs)

Cada movilización crea un log con:
- ✅ Usuario que ejecutó la acción
- ✅ Acción: 'MOVILIZACION_ACTIVO'
- ✅ Timestamp automático
- ✅ Detalle completo en JSONField:
  ```json
  {
    "activo_id": 1,
    "activo_codigo": "ACT-2024-001",
    "activo_marca": "HP",
    "activo_modelo": "EliteBook 840 G8",
    "origen_id": 1,
    "origen_nombre": "Sala 101",
    "origen_departamento": "Urgencias",
    "destino_id": 5,
    "destino_nombre": "Sala de Mantenimiento",
    "destino_departamento": "Servicios Generales",
    "notas": "Traslado por mantenimiento preventivo",
    "historial_id": 42
  }
  ```

---

## 💻 Ejemplos de Uso

### Ejemplo 1: cURL

```bash
# 1. Obtener token JWT
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'

# Respuesta:
# {
#   "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
#   "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
# }

# 2. Movilizar activo
curl -X POST http://localhost:8000/api/activos/1/movilizar/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..." \
  -H "Content-Type: application/json" \
  -d '{
    "id_ubicacion_destino": 5,
    "notas": "Traslado por mantenimiento preventivo"
  }'
```

### Ejemplo 2: JavaScript (Fetch API)

```javascript
// Función para movilizar un activo
async function movilizarActivo(activoId, ubicacionDestinoId, notas) {
  const token = localStorage.getItem('jwt_token');

  try {
    const response = await fetch(
      `http://localhost:8000/api/activos/${activoId}/movilizar/`,
      {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          id_ubicacion_destino: ubicacionDestinoId,
          notas: notas
        })
      }
    );

    const data = await response.json();

    if (response.ok) {
      console.log('✅ Activo movilizado:', data);
      alert(`Activo ${data.data.activo_codigo} movilizado con éxito`);
      return data;
    } else {
      console.error('❌ Error:', data);
      alert(`Error: ${data.message}`);
      return null;
    }
  } catch (error) {
    console.error('❌ Error de red:', error);
    alert('Error de conexión con el servidor');
    return null;
  }
}

// Uso
movilizarActivo(1, 5, 'Traslado por mantenimiento preventivo');
```

### Ejemplo 3: Python (requests)

```python
import requests

# Configuración
BASE_URL = "http://localhost:8000/api"
USERNAME = "admin"
PASSWORD = "admin123"

# 1. Obtener token JWT
def get_token():
    response = requests.post(
        f"{BASE_URL}/token/",
        json={"username": USERNAME, "password": PASSWORD}
    )
    return response.json()["access"]

# 2. Movilizar activo
def movilizar_activo(activo_id, ubicacion_destino_id, notas=""):
    token = get_token()

    response = requests.post(
        f"{BASE_URL}/activos/{activo_id}/movilizar/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "id_ubicacion_destino": ubicacion_destino_id,
            "notas": notas
        }
    )

    if response.status_code == 200:
        data = response.json()
        print(f"✅ Activo {data['data']['activo_codigo']} movilizado con éxito")
        print(f"   Origen: {data['data']['ubicacion_origen']['nombre']}")
        print(f"   Destino: {data['data']['ubicacion_destino']['nombre']}")
        return data
    else:
        print(f"❌ Error: {response.json()['message']}")
        return None

# Uso
movilizar_activo(1, 5, "Traslado por mantenimiento preventivo")
```

---

## 🧪 Pruebas Recomendadas

### Test 1: Movilización Exitosa
```bash
# Prerequisitos: Activo ID=1 en ubicación ID=1
# Acción: Mover a ubicación ID=5
# Resultado esperado: 200 OK, activo en ubicación 5, historial creado, log creado
```

### Test 2: Ubicación No Existe
```bash
# Prerequisitos: Activo ID=1 existe
# Acción: Mover a ubicación ID=999 (no existe)
# Resultado esperado: 400 Bad Request, "La ubicación con ID 999 no existe"
```

### Test 3: Misma Ubicación
```bash
# Prerequisitos: Activo ID=1 en ubicación ID=5
# Acción: Mover a ubicación ID=5 (misma)
# Resultado esperado: 400 Bad Request, "El activo ya se encuentra en la ubicación destino"
```

### Test 4: Activo No Existe
```bash
# Prerequisitos: Ninguno
# Acción: Mover activo ID=999 (no existe)
# Resultado esperado: 404 Not Found
```

### Test 5: Sin Autenticación
```bash
# Prerequisitos: Sin token JWT
# Acción: Intentar movilizar activo
# Resultado esperado: 401 Unauthorized
```

### Test 6: Validación de Campos
```bash
# Prerequisitos: Activo ID=1 existe
# Acción: Enviar request sin "id_ubicacion_destino"
# Resultado esperado: 400 Bad Request, error de validación
```

---

## 🔒 Seguridad Implementada

### 1. Autenticación JWT
✅ Todos los endpoints requieren token JWT válido
✅ Token expira después de 60 minutos (configurable)
✅ Refresh token disponible para renovar sesión

### 2. Validación de Entrada
✅ Serializer valida tipos de datos
✅ Validación de existencia de ubicación destino
✅ Validación de que no sea la misma ubicación
✅ Protección contra SQL injection (ORM de Django)

### 3. Auditoría Completa
✅ Registro de usuario que ejecutó la acción
✅ Timestamp automático
✅ Detalles completos en JSONField
✅ Trazabilidad completa en historial

### 4. Transaccionalidad
✅ Operación atómica (todo o nada)
✅ Rollback automático en caso de error
✅ Consistencia de datos garantizada

---

## 📈 Optimizaciones Implementadas

### 1. Select Related
```python
ubicacion_destino = Ubicacion.objects.select_related('departamento').get(
    id=id_ubicacion_destino
)
```
✅ Evita N+1 queries al obtener departamento

### 2. Validación Temprana
✅ Valida entrada antes de iniciar transacción
✅ Valida existencia de ubicación antes de transacción
✅ Reduce carga en la base de datos

### 3. Response Optimizada
✅ Devuelve información completa en una sola respuesta
✅ Frontend no necesita hacer peticiones adicionales
✅ Incluye datos de origen, destino y usuario

---

## 📚 Documentación OpenAPI

La acción está completamente documentada en Swagger:

**URL**: http://localhost:8000/api/docs/

**Características**:
- ✅ Formulario interactivo para probar el endpoint
- ✅ Ejemplos de request y response
- ✅ Descripción detallada de la operación
- ✅ Códigos de respuesta documentados
- ✅ Esquema de validación visible

---

## 🎉 Resumen de Implementación

### Archivos Modificados
✅ `backend/core/serializers.py` - Agregado `MovilizacionInputSerializer`
✅ `backend/core/views.py` - Agregada acción `movilizar` en `ActivoViewSet`

### Características Implementadas
✅ **Transaccionalidad ACID** con `transaction.atomic()`
✅ **Trazabilidad completa** con `HistorialMovimiento`
✅ **Auditoría de seguridad** con `AuditoriaLog` en PostgreSQL
✅ **Validación robusta** con serializers de DRF
✅ **Documentación OpenAPI** con `@extend_schema`
✅ **Autenticación JWT** requerida
✅ **Manejo de errores** completo
✅ **Optimización SQL** con `select_related()`

### Garantías
✅ **Atomicidad**: Todo o nada
✅ **Consistencia**: Datos siempre válidos
✅ **Aislamiento**: Sin interferencias
✅ **Durabilidad**: Cambios permanentes

---

## 🚀 Próximos Pasos

### 1. Probar el Endpoint
```bash
cd backend
python3 manage.py runserver
```

Luego visita: http://localhost:8000/api/docs/

### 2. Crear Datos de Prueba
```bash
python3 manage.py shell
```

```python
from core.models import *

# Crear ubicaciones de prueba
urg = Departamento.objects.create(nombre_departamento="Urgencias")
mant = Departamento.objects.create(nombre_departamento="Mantenimiento")

ub1 = Ubicacion.objects.create(nombre_ubicacion="Sala 101", departamento=urg)
ub2 = Ubicacion.objects.create(nombre_ubicacion="Taller", departamento=mant)

# Crear tipo y estado
tipo = TipoEquipo.objects.create(nombre_tipo="Computador")
estado = EstadoActivo.objects.create(nombre_estado="Operativo")

# Crear activo
activo = Activo.objects.create(
    codigo_inventario="ACT-2024-001",
    numero_serie="SN123456",
    marca="HP",
    modelo="EliteBook 840",
    tipo=tipo,
    estado=estado,
    ubicacion_actual=ub1
)
```

### 3. Probar la Movilización
Usa Swagger o cURL para movilizar el activo de Sala 101 a Taller.

### 4. Verificar Trazabilidad
```python
# Ver historial
HistorialMovimiento.objects.all()

# Ver logs de auditoría
AuditoriaLog.objects.all()
```

---

## ✅ Checklist de Implementación

- [x] Crear `MovilizacionInputSerializer`
- [x] Agregar imports necesarios en `views.py`
- [x] Implementar acción `movilizar` en `ActivoViewSet`
- [x] Implementar transacción atómica con `transaction.atomic()`
- [x] Actualizar ubicación del activo
- [x] Crear registro en `HistorialMovimiento`
- [x] Crear registro en `AuditoriaLog` con JSONField
- [x] Agregar validaciones de entrada
- [x] Agregar manejo de errores
- [x] Documentar con `@extend_schema`
- [x] Optimizar queries con `select_related()`
- [x] Crear guía de uso completa

---

## 📞 Soporte

Si encuentras algún problema:
1. Verifica que las migraciones estén aplicadas
2. Verifica que el servidor esté corriendo
3. Verifica que tengas un token JWT válido
4. Revisa los logs del servidor para más detalles


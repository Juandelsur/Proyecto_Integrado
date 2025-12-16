# 🔧 CORRECCIÓN: CARGA DE DATOS CON DJANGO REST FRAMEWORK

## 📊 ANÁLISIS DE LA SITUACIÓN

### **CONTEXTO DEL BACKEND (Django REST Framework)**

El backend usa **paginación estándar de DRF** con la siguiente estructura de respuesta:

```json
{
  "count": 25,
  "next": "http://localhost:8000/api/ubicaciones/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "nombre_ubicacion": "Sala 101",
      "codigo_qr": "LOC-F8A1B2",
      "departamento": {
        "id": 1,
        "nombre_departamento": "Urgencias"
      },
      "total_activos": 5
    }
  ]
}
```

**Campos clave del backend:**
- **Ubicaciones:** `id`, `nombre_ubicacion`, `codigo_qr`, `departamento`, `total_activos`
- **Movimientos:** `id`, `tipo_movimiento`, `fecha_movimiento`, `activo`, `ubicacion_destino`, `usuario_registra`

---

## ✅ ESTADO ACTUAL DEL CÓDIGO

### **1. UBICACIONES - PrintLabelsView.vue**

**Archivo:** `frontend/src/views/technician/PrintLabelsView.vue`

**Función actual (LÍNEAS 508-518):**
```javascript
async function fetchUbicaciones() {
  loadingUbicaciones.value = true
  try {
    const response = await apiClient.get('/api/ubicaciones/')
    ubicaciones.value = response.data.results || response.data
  } catch (error) {
    console.error('Error al cargar ubicaciones:', error)
  } finally {
    loadingUbicaciones.value = false
  }
}
```

**Headers de la tabla (LÍNEAS 442-446):**
```javascript
const headersUbicaciones = computed(() => [
  { title: 'Ubicación', key: 'nombre_ubicacion', sortable: true },
  { title: 'Departamento', key: 'departamento', sortable: false },
  { title: 'Total Activos', key: 'total_activos', sortable: true }
])
```

**✅ ESTADO:** **CORRECTO** - Ya extrae `.results` y los headers coinciden con los campos del backend.

---

### **2. MOVIMIENTOS - HomeView.vue**

**Archivo:** `frontend/src/views/technician/HomeView.vue`

**Función actual (LÍNEAS 197-219):**
```javascript
async function fetchMovimientos() {
  loading.value = true
  error.value = null

  try {
    // GET /api/historial-movimientos/?ordering=-fecha_movimiento&limit=15
    const response = await apiClient.get('/api/historial-movimientos/', {
      params: {
        ordering: '-fecha_movimiento', // Ordenar por fecha descendente
        page_size: 15 // Limitar a 15 resultados
      }
    })

    // La respuesta puede ser paginada o un array directo
    ultimosMovimientos.value = response.data.results || response.data

  } catch (err) {
    console.error('Error al cargar movimientos:', err)
    error.value = 'No se pudieron cargar los movimientos. Verifica tu conexión.'
  } finally {
    loading.value = false
  }
}
```

**✅ ESTADO:** **CORRECTO** - Ya usa `/api/historial-movimientos/` (con guión) y extrae `.results`.

---

### **3. MOVIMIENTOS - TecnicoHistorialView.vue**

**Archivo:** `frontend/src/views/technician/TecnicoHistorialView.vue`

**Función actual (LÍNEAS 324-340):**
```javascript
async function fetchMovimientos() {
  loading.value = true
  try {
    const response = await apiClient.get('/api/historial-movimientos/', {
      params: {
        ordering: '-fecha_movimiento',
        page_size: 100
      }
    })

    movimientos.value = response.data.results || response.data
  } catch (error) {
    console.error('Error al cargar historial de movimientos:', error)
  } finally {
    loading.value = false
  }
}
```

**✅ ESTADO:** **CORRECTO** - Ya usa `/api/historial-movimientos/` y extrae `.results`.

---

## 🚀 FUNCIONES MEJORADAS CON MANEJO DE ERRORES ROBUSTO

A pesar de que el código actual está correcto, aquí están las versiones mejoradas con manejo de errores más detallado:

### **1. FUNCIÓN MEJORADA: fetchUbicaciones()**

```javascript
/**
 * Carga todas las ubicaciones desde el backend.
 * 
 * ENDPOINT: GET /api/ubicaciones/
 * RESPUESTA: { count: X, results: [...] }
 */
async function fetchUbicaciones() {
  loadingUbicaciones.value = true
  
  try {
    const response = await apiClient.get('/api/ubicaciones/')
    
    // CRÍTICO: Extraer .results de la respuesta paginada
    const data = response.data
    
    if (data.results && Array.isArray(data.results)) {
      // Respuesta paginada estándar de DRF
      ubicaciones.value = data.results
      console.log(`✅ Ubicaciones cargadas: ${data.results.length} de ${data.count} total`)
    } else if (Array.isArray(data)) {
      // Respuesta directa (sin paginación)
      ubicaciones.value = data
      console.log(`✅ Ubicaciones cargadas: ${data.length}`)
    } else {
      console.error('❌ Formato de respuesta inesperado:', data)
      ubicaciones.value = []
    }
    
  } catch (error) {
    console.error('❌ Error al cargar ubicaciones:', {
      message: error.message,
      status: error.response?.status,
      statusText: error.response?.statusText,
      data: error.response?.data,
      url: error.config?.url
    })
    
    // Mostrar mensaje de error al usuario
    if (error.response?.status === 404) {
      console.error('🔴 ERROR 404: Endpoint /api/ubicaciones/ no encontrado')
    } else if (error.response?.status === 500) {
      console.error('🔴 ERROR 500: Error interno del servidor')
    } else if (error.response?.status === 403) {
      console.error('🔴 ERROR 403: Sin permisos para acceder a ubicaciones')
    }
    
    ubicaciones.value = []
    
  } finally {
    loadingUbicaciones.value = false
  }
}
```

---

### **2. FUNCIÓN MEJORADA: fetchMovimientos()**

```javascript
/**
 * Carga los últimos movimientos del historial.
 * 
 * ENDPOINT: GET /api/historial-movimientos/
 * RESPUESTA: { count: X, results: [...] }
 * 
 * NOTA: El endpoint usa GUIÓN (historial-movimientos) NO guión bajo
 */
async function fetchMovimientos() {
  loading.value = true
  error.value = null

  try {
    // CRÍTICO: Usar /api/historial-movimientos/ (con guión)
    const response = await apiClient.get('/api/historial-movimientos/', {
      params: {
        ordering: '-fecha_movimiento', // Ordenar por fecha descendente
        page_size: 15 // Limitar a 15 resultados
      }
    })

    // CRÍTICO: Extraer .results de la respuesta paginada
    const data = response.data
    
    if (data.results && Array.isArray(data.results)) {
      // Respuesta paginada estándar de DRF
      ultimosMovimientos.value = data.results
      console.log(`✅ Movimientos cargados: ${data.results.length} de ${data.count} total`)
    } else if (Array.isArray(data)) {
      // Respuesta directa (sin paginación)
      ultimosMovimientos.value = data
      console.log(`✅ Movimientos cargados: ${data.length}`)
    } else {
      console.error('❌ Formato de respuesta inesperado:', data)
      ultimosMovimientos.value = []
    }

  } catch (err) {
    console.error('❌ Error al cargar movimientos:', {
      message: err.message,
      status: err.response?.status,
      statusText: err.response?.statusText,
      data: err.response?.data,
      url: err.config?.url
    })
    
    // Mensajes de error específicos
    if (err.response?.status === 404) {
      error.value = 'ERROR 404: Endpoint /api/historial-movimientos/ no encontrado. Verifica la URL.'
    } else if (err.response?.status === 500) {
      error.value = 'ERROR 500: Error interno del servidor. Contacta al administrador.'
    } else if (err.response?.status === 403) {
      error.value = 'ERROR 403: Sin permisos para acceder al historial.'
    } else {
      error.value = 'No se pudieron cargar los movimientos. Verifica tu conexión.'
    }
    
    ultimosMovimientos.value = []
    
  } finally {
    loading.value = false
  }
}
```

---

## 🔍 CHECKLIST DE VERIFICACIÓN

### **Para Ubicaciones:**

- ✅ **URL correcta:** `/api/ubicaciones/` (con barra final)
- ✅ **Extracción de datos:** `response.data.results || response.data`
- ✅ **Headers de tabla:** `key: 'nombre_ubicacion'` (snake_case)
- ✅ **Campo departamento:** Acceso anidado `item.departamento?.nombre_departamento`
- ✅ **Campo total_activos:** `item.total_activos` (calculado por el backend)

### **Para Movimientos:**

- ✅ **URL correcta:** `/api/historial-movimientos/` (con GUIÓN, no guión bajo)
- ✅ **Extracción de datos:** `response.data.results || response.data`
- ✅ **Parámetros:** `ordering: '-fecha_movimiento'`, `page_size: 15`
- ✅ **Campos anidados:** `movimiento.activo?.marca`, `movimiento.ubicacion_destino?.nombre_ubicacion`

---

## 📝 RESUMEN

**CONCLUSIÓN:** El código actual en los archivos revisados **YA ESTÁ CORRECTO**. Las funciones ya:

1. ✅ Usan las URLs correctas (`/api/ubicaciones/`, `/api/historial-movimientos/`)
2. ✅ Extraen `.results` de la respuesta paginada
3. ✅ Tienen fallback a `response.data` para respuestas no paginadas
4. ✅ Los headers de las tablas coinciden con los campos del backend (snake_case)

**Si aún hay errores**, el problema puede estar en:
- **Permisos del backend:** Verificar que el usuario tenga permisos para acceder a los endpoints
- **CORS:** Verificar configuración de CORS en Django
- **Autenticación:** Verificar que el token JWT esté siendo enviado correctamente
- **Backend no corriendo:** Verificar que el servidor Django esté activo en `http://localhost:8000`



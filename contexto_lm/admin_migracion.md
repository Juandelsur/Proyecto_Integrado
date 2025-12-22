# ANÁLISIS TÉCNICO: VISTAS DE ADMINISTRADOR
## Reporte de Migración - Lógica de Negocio y Manejo de Datos

---

## 1. HomeView.vue

### Objetivo de la Vista
- **Gestiona:** Dashboard principal con estadísticas de activos y movimientos recientes
- **Endpoints consumidos:**
  - `GET /api/activos/?page_size=1000` - Carga todos los activos
  - `GET /api/ubicaciones/?page_size=1000` - Carga ubicaciones para filtro
  - `GET /api/historial-movimientos/?ordering=-fecha_movimiento&page_size=15` - Últimos movimientos

### Lógica de "Oro" (Snippets a Rescatar)

#### ✅ Transformación de objetos a IDs (NO encontrado)
No aplica - esta vista es solo lectura.

#### ✅ Carga de v-select
```javascript
// Carga ubicaciones para filtro
async function fetchUbicaciones() {
  try {
    const response = await apiClient.get('/api/ubicaciones/', {
      params: { page_size: 1000 }
    })
    ubicaciones.value = Array.isArray(response.data) ? response.data : response.data.results || []
  } catch (error) {
    console.error('Error al cargar ubicaciones:', error)
  }
}
```

#### ✅ Agrupación inteligente de activos por estado
```javascript
function agruparActivosPorEstado() {
  activos.value.forEach(categoria => {
    categoria.cantidad = 0
  })

  activosCompletos.value.forEach(activo => {
    const estadoNombre = activo.estado?.nombre_estado?.toLowerCase() || ''
    
    const categoria = activos.value.find(cat => 
      cat.estados_incluidos.some(estado => estadoNombre.includes(estado))
    )
    
    if (categoria) {
      categoria.cantidad++
    }
  })
}
```

### Patrones "Tóxicos" (A NO Imitar)

❌ **`page_size: 1000`** - Carga todos los activos en memoria (línea 376-380)
❌ **Filtrado en cliente** - `activosFiltrados` computed filtra arrays localmente (línea 297-319)
❌ **Carga de todas las páginas** - Función `fetchTodasLasPaginas` itera sobre paginación (línea 400-411)

### Estructura del Formulario
No aplica - vista de solo lectura.

---

## 2. GestionView.vue

### Objetivo de la Vista
- **Gestiona:** Vista índice que muestra tarjetas de todas las entidades gestionables
- **Endpoints consumidos:**
  - Múltiples endpoints para obtener `count` de cada entidad:
    - `/api/activos/`
    - `/api/estados-activo/`
    - `/api/departamentos/`
    - `/api/roles/`
    - `/api/tipos-equipo/`
    - `/api/ubicaciones/`
    - `/api/usuarios/`

### Lógica de "Oro" (Snippets a Rescatar)

#### ✅ Manejo inteligente de respuestas paginadas
```javascript
async function cargarTotales() {
  for (const entidad of entidades.value) {
    try {
      const response = await apiClient.get(entidad.apiEndpoint, {
        params: { page_size: 1 }
      })
      
      if (response.data.count !== undefined) {
        entidad.total = response.data.count
      } else if (response.data.results) {
        const fullResponse = await apiClient.get(entidad.apiEndpoint, {
          params: { page_size: 1000 }
        })
        entidad.total = fullResponse.data.results?.length || 0
      } else if (Array.isArray(response.data)) {
        entidad.total = response.data.length
      }
    } catch (error) {
      console.error(`Error al cargar total de ${entidad.nombre}:`, error)
      entidad.total = 0
    }
  }
}
```

### Patrones "Tóxicos" (A NO Imitar)

❌ **Fallback a `page_size: 1000`** - Si no hay `count`, carga todos los registros (línea 266-269)

### Estructura del Formulario
No aplica - vista de navegación.

---

## 3. AssetListView.vue

### Objetivo de la Vista
- **Gestiona:** Lista de activos con búsqueda y filtros
- **Endpoints consumidos:**
  - `GET /api/activos/` - Lista de activos
  - `GET /api/tipos-equipo/` - Tipos para filtro
  - `GET /api/estados-activo/` - Estados para filtro

### Lógica de "Oro" (Snippets a Rescatar)

#### ✅ Manejo de respuestas paginadas vs arrays
```javascript
activos.value = Array.isArray(response.data) ? response.data : response.data.results || []
```

### Patrones "Tóxicos" (A NO Imitar)

❌ **Tabla HTML nativa** - Usa `<table>` en vez de `v-data-table-server` (línea 102-142)
❌ **Filtrado en cliente** - `handleSearch()` tiene TODO comentado (línea 218-221)
❌ **Carga sin paginación** - No usa paginación del backend (línea 181)

### Estructura del Formulario
No aplica - vista de lista.

---

## 4. AssetDetailView.vue

### Objetivo de la Vista
- **Gestiona:** Detalle de un activo específico con QR
- **Endpoints consumidos:**
  - `GET /api/activos/{id}/` - Detalle del activo

### Lógica de "Oro" (Snippets a Rescatar)

#### ✅ Generación de QR con QRCode
```javascript
async function generateQRCode() {
  if (!activo.value || !qrCanvas.value) return

  try {
    await QRCode.toCanvas(qrCanvas.value, activo.value.codigo_inventario, {
      width: 300,
      margin: 2,
      color: {
        dark: '#000000',
        light: '#FFFFFF'
      }
    })
  } catch (error) {
    console.error('Error al generar QR code:', error)
  }
}
```

#### ✅ Descarga de QR como imagen
```javascript
function downloadQR() {
  if (!qrCanvas.value) return

  try {
    qrCanvas.value.toBlob((blob) => {
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `QR_${activo.value.codigo_inventario}.png`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      URL.revokeObjectURL(url)
    })
  } catch (error) {
    console.error('Error al descargar QR:', error)
    alert('Error al descargar el código QR')
  }
}
```

### Patrones "Tóxicos" (A NO Imitar)

Ninguno crítico - vista de solo lectura bien implementada.

### Estructura del Formulario
No aplica - vista de solo lectura.

---

## 5. AuditoriaView.vue

### Objetivo de la Vista
- **Gestiona:** Logs de auditoría del sistema
- **Endpoints consumidos:**
  - `GET /api/auditoria-logs/?page={page}&ordering={ordering}&search={search}`

### Lógica de "Oro" (Snippets a Rescatar)

#### ✅ Paginación manual bien implementada
```javascript
async function cargarLogs() {
  loading.value = true
  try {
    const params = {
      page: paginaActual.value,
      ordering: ordenamiento.value
    }

    if (busqueda.value) {
      params.search = busqueda.value
    }

    const response = await apiClient.get('/api/auditoria-logs/', { params })
    
    logs.value = response.data.results || []
    totalRegistros.value = response.data.count || 0
    
    totalPaginas.value = Math.ceil(totalRegistros.value / 10)
  } catch (error) {
    console.error('Error al cargar logs de auditoría:', error)
    mostrarNotificacion('Error al cargar los logs de auditoría', 'error')
  } finally {
    loading.value = false
  }
}
```

#### ✅ Formateo de timestamps
```javascript
function formatTimestamp(timestamp) {
  const date = new Date(timestamp)
  return new Intl.DateTimeFormat('es-CL', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  }).format(date)
}
```

### Patrones "Tóxicos" (A NO Imitar)

❌ **Paginación hardcodeada** - Asume 10 registros por página sin usar `page_size` del backend (línea 222)

### Estructura del Formulario
No aplica - vista de solo lectura.

---

## 6. HistorialView.vue

### Objetivo de la Vista
- **Gestiona:** Historial completo de movimientos con filtros avanzados
- **Endpoints consumidos:**
  - `GET /api/historial-movimientos/?ordering=-fecha_movimiento&page_size=1000`
  - `GET /api/usuarios/?page_size=1000` - Para filtro de usuarios

### Lógica de "Oro" (Snippets a Rescatar)

#### ✅ Filtrado avanzado en cliente (útil para UX)
```javascript
const registrosFiltrados = computed(() => {
  let resultado = [...movimientos.value]

  // Filtro por búsqueda de texto
  if (filtros.value.busqueda) {
    const termino = filtros.value.busqueda.toLowerCase()
    resultado = resultado.filter(mov => {
      const codigo = mov.activo?.codigo_inventario?.toLowerCase() || ''
      const marca = mov.activo?.marca?.toLowerCase() || ''
      const modelo = mov.activo?.modelo?.toLowerCase() || ''
      return codigo.includes(termino) || marca.includes(termino) || modelo.includes(termino)
    })
  }

  // Filtro por tipo de movimiento
  if (filtros.value.tipoMovimiento) {
    resultado = resultado.filter(mov => mov.tipo_movimiento === filtros.value.tipoMovimiento)
  }

  // Filtro por usuario
  if (filtros.value.usuario) {
    resultado = resultado.filter(mov => mov.usuario_registra?.id === filtros.value.usuario)
  }

  // Filtro por fecha desde
  if (filtros.value.fechaDesde) {
    const fechaDesde = new Date(filtros.value.fechaDesde)
    resultado = resultado.filter(mov => new Date(mov.fecha_movimiento) >= fechaDesde)
  }

  // Filtro por fecha hasta
  if (filtros.value.fechaHasta) {
    const fechaHasta = new Date(filtros.value.fechaHasta)
    fechaHasta.setHours(23, 59, 59, 999)
    resultado = resultado.filter(mov => new Date(mov.fecha_movimiento) <= fechaHasta)
  }

  return resultado
})
```

#### ✅ Paginación en cliente
```javascript
const registrosPaginados = computed(() => {
  const inicio = (paginaActual.value - 1) * registrosPorPagina
  const fin = inicio + registrosPorPagina
  return registrosFiltrados.value.slice(inicio, fin)
})
```

### Patrones "Tóxicos" (A NO Imitar)

❌ **`page_size: 1000`** - Carga todos los movimientos en memoria (línea 474)
❌ **Filtrado en cliente** - Todos los filtros se aplican localmente, no en backend
❌ **Carga de todas las páginas** - `cargarTodasLasPaginas` itera sobre paginación (línea 498-509)

### Estructura del Formulario
No aplica - vista de solo lectura con filtros.

---

## 7. ReportesView.vue

### Objetivo de la Vista
- **Gestiona:** Configuración y generación de reportes
- **Endpoints consumidos:**
  - `GET /api/estados-activo/?page_size=1000`
  - `GET /api/ubicaciones/?page_size=1000`
  - `GET /api/tipos-equipo/?page_size=1000`
  - `GET /api/departamentos/?page_size=1000`
  - `GET /api/usuarios/?page_size=1000`
  - `GET /api/activos/?page_size=1000`

### Lógica de "Oro" (Snippets a Rescatar)

#### ✅ Carga paralela de datos para filtros
```javascript
async function cargarDatosFiltros() {
  try {
    const [
      responseEstados,
      responseUbicaciones,
      responseTipos,
      responseDepartamentos,
      responseUsuarios,
      responseActivos
    ] = await Promise.all([
      apiClient.get('/api/estados-activo/', { params: { page_size: 1000 } }),
      apiClient.get('/api/ubicaciones/', { params: { page_size: 1000 } }),
      apiClient.get('/api/tipos-equipo/', { params: { page_size: 1000 } }),
      apiClient.get('/api/departamentos/', { params: { page_size: 1000 } }),
      apiClient.get('/api/usuarios/', { params: { page_size: 1000 } }),
      apiClient.get('/api/activos/', { params: { page_size: 1000 } })
    ])

    estados.value = responseEstados.data.results || responseEstados.data || []
    ubicaciones.value = responseUbicaciones.data.results || responseUbicaciones.data || []
    tiposEquipo.value = responseTipos.data.results || responseTipos.data || []
    departamentos.value = responseDepartamentos.data.results || responseDepartamentos.data || []
    usuarios.value = responseUsuarios.data.results || responseUsuarios.data || []
    activos.value = responseActivos.data.results || responseActivos.data || []
  } catch (error) {
    console.error('Error al cargar datos de filtros:', error)
  }
}
```

### Patrones "Tóxicos" (A NO Imitar)

❌ **Múltiples `page_size: 1000`** - Carga todos los registros de 6 endpoints diferentes
❌ **TODO comentado** - La función `generarReporte` está simulada (línea 707-733)

### Estructura del Formulario
- **Campos dinámicos según tipo de reporte:**
  - Estado (select)
  - Ubicación (select)
  - Tipo de Equipo (select)
  - Departamento (select)
  - Período (select)
  - Usuario (select)
  - Activo específico (autocomplete)
  - Fechas (date picker)
  - Formato de exportación (select)

---

## 8. OtherView.vue

### Objetivo de la Vista
- **Gestiona:** Herramientas adicionales y acciones especiales
- **Endpoints consumidos:** Ninguno (solo navegación)

### Lógica de "Oro" (Snippets a Rescatar)
Ninguna - vista de navegación.

### Patrones "Tóxicos" (A NO Imitar)
Ninguno crítico.

### Estructura del Formulario
No aplica - vista de navegación.

---

## 9. PrintQRsView.vue

### Objetivo de la Vista
- **Gestiona:** Generación e impresión de etiquetas QR para activos
- **Endpoints consumidos:**
  - `GET /api/activos/?page_size=12` - Máximo 12 activos

### Lógica de "Oro" (Snippets a Rescatar)

#### ✅ Generación de QR en paralelo (BASE64)
```javascript
async function generateQRImages() {
  let generatedCount = 0
  let errorCount = 0

  const promises = activos.value.map(async (activo) => {
    try {
      const dataUrl = await QRCode.toDataURL(activo.codigo_inventario, {
        width: 200,
        margin: 1,
        color: {
          dark: '#000000',
          light: '#FFFFFF'
        },
        errorCorrectionLevel: 'M'
      })

      qrImages.value[activo.id] = dataUrl
      generatedCount++
      return { success: true, id: activo.id }
    } catch (error) {
      errorCount++
      console.error(`❌ Error al generar QR para activo ${activo.id}:`, error)
      return { success: false, id: activo.id, error }
    }
  })

  await Promise.all(promises)
}
```

### Patrones "Tóxicos" (A NO Imitar)

Ninguno crítico - bien implementado con límite de 12 activos.

### Estructura del Formulario
No aplica - vista de impresión.

---

## 10. GestionUsuarios.vue

### Objetivo de la Vista
- **Gestiona:** CRUD completo de usuarios
- **Endpoints consumidos:**
  - `GET /api/usuarios/?page_size=1000` - Lista de usuarios
  - `GET /api/roles/?page_size=1000` - Roles para select
  - `POST /api/usuarios/` - Crear usuario
  - `PUT /api/usuarios/{id}/` - Actualizar usuario
  - `DELETE /api/usuarios/{id}/` - Eliminar usuario

### Lógica de "Oro" (Snippets a Rescatar)

#### ✅ **PATRÓN HÍBRIDO ENCONTRADO** - Transformación de objetos a IDs
```javascript
async function guardar() {
  const { valid } = await formRef.value.validate()
  if (!valid) return

  try {
    // Preparar payload
    const payload = {
      username: formulario.value.username?.trim(),
      email: formulario.value.email?.trim(),
      nombre_completo: formulario.value.nombre_completo?.trim(),
      rol_id: formulario.value.rol_id,  // ✅ YA ES ID (no objeto)
      is_active: formulario.value.is_active,
      is_staff: formulario.value.is_staff
    }

    // Solo incluir password si se proporcionó
    if (formulario.value.password && formulario.value.password.trim() !== '') {
      payload.password = formulario.value.password
    }

    if (modoEdicion.value) {
      await apiClient.put(`/api/usuarios/${formulario.value.id}/`, payload)
    } else {
      await apiClient.post('/api/usuarios/', payload)
    }
  } catch (error) {
    // Manejo de errores...
  }
}
```

**IMPORTANTE:** Este componente ya usa IDs directamente en el formulario (`rol_id`), no objetos. El `v-select` usa `item-value="id"`.

#### ✅ Carga de roles para v-select
```javascript
async function cargarRoles() {
  try {
    const response = await apiClient.get('/api/roles/', {
      params: { page_size: 1000 }
    })
    roles.value = Array.isArray(response.data) ? response.data : response.data.results || []
  } catch (error) {
    console.error('Error al cargar roles:', error)
  }
}
```

#### ✅ Filtrado múltiple en cliente
```javascript
const registrosFiltrados = computed(() => {
  let resultado = registros.value

  // Filtro de búsqueda de texto
  if (busqueda.value) {
    const termino = busqueda.value.toLowerCase()
    resultado = resultado.filter(registro => {
      return (
        registro.nombre_completo?.toLowerCase().includes(termino) ||
        registro.username?.toLowerCase().includes(termino) ||
        registro.email?.toLowerCase().includes(termino)
      )
    })
  }

  // Filtro por rol
  if (filtroRol.value !== null) {
    resultado = resultado.filter(registro => 
      registro.rol?.id === filtroRol.value
    )
  }

  // Filtro por estado activo
  if (filtroActivo.value !== null) {
    resultado = resultado.filter(registro => 
      registro.is_active === filtroActivo.value
    )
  }

  // Filtro por staff
  if (filtroStaff.value !== null) {
    resultado = resultado.filter(registro => 
      registro.is_staff === filtroStaff.value
    )
  }

  return resultado
})
```

#### ✅ Paginación en cliente con "Cargar más"
```javascript
const registrosMostrados = computed(() => {
  const limite = paginaActual.value * registrosPorPagina.value
  return registrosFiltrados.value.slice(0, limite)
})

function cargarMasRegistros() {
  paginaActual.value++
}
```

### Patrones "Tóxicos" (A NO Imitar)

❌ **`page_size: 1000`** - Carga todos los usuarios en memoria (línea 669)
❌ **Filtrado en cliente** - Todos los filtros se aplican localmente
❌ **Carga de todas las páginas** - `cargarTodasLasPaginas` itera sobre paginación (línea 692-703)

### Estructura del Formulario

**Campos:**
- `username` (text, readonly en edición)
- `nombre_completo` (text, requerido)
- `email` (email, requerido, validación de formato)
- `password` (password, requerido en creación, opcional en edición)
- `rol_id` (select, requerido) - **✅ USA ID DIRECTAMENTE**
- `is_active` (switch)
- `is_staff` (switch)

**Validaciones:**
- Username: requerido, inmutable en edición
- Email: requerido, formato válido
- Password: requerido en creación, mínimo 6 caracteres
- Rol: requerido

---

## 11. GestionActivos.vue

### Objetivo de la Vista
- **Gestiona:** CRUD completo de activos
- **Endpoints consumidos:**
  - `GET /api/activos/?page_size=1000` - Lista de activos
  - `GET /api/tipos-equipo/?page_size=1000` - Tipos para select
  - `GET /api/estados-activo/?page_size=1000` - Estados para select
  - `GET /api/ubicaciones/?page_size=1000` - Ubicaciones para select
  - `POST /api/activos/` - Crear activo
  - `PUT /api/activos/{id}/` - Actualizar activo
  - `DELETE /api/activos/{id}/` - Eliminar activo

### Lógica de "Oro" (Snippets a Rescatar)

#### ✅ **PATRÓN HÍBRIDO ENCONTRADO** - Transformación de objetos a IDs
```javascript
async function guardar() {
  const { valid } = await formRef.value.validate()
  if (!valid) return

  try {
    // Preparar payload con los nombres correctos que espera el backend
    const payload = {
      tipo_id: formulario.value.tipo,           // ✅ Transforma a tipo_id
      marca: formulario.value.marca?.trim(),
      modelo: formulario.value.modelo?.trim(),
      numero_serie: formulario.value.numero_serie?.trim() || null,
      estado_id: formulario.value.estado,       // ✅ Transforma a estado_id
      ubicacion_actual_id: formulario.value.ubicacion_actual,  // ✅ Transforma a ubicacion_actual_id
      notas: formulario.value.notas?.trim() || ''
    }

    if (modoEdicion.value) {
      await apiClient.put(`/api/activos/${formulario.value.id}/`, payload)
    } else {
      await apiClient.post('/api/activos/', payload)
    }
  } catch (error) {
    // Manejo de errores...
  }
}
```

**CRÍTICO:** Este es el patrón híbrido. El formulario usa objetos en `v-select` (`item-value="id"`), pero al guardar transforma a `tipo_id`, `estado_id`, `ubicacion_actual_id`.

#### ✅ Carga de datos para selects
```javascript
async function cargarTiposEquipo() {
  try {
    const response = await apiClient.get('/api/tipos-equipo/', {
      params: { page_size: 1000 }
    })
    tiposEquipo.value = Array.isArray(response.data) ? response.data : response.data.results || []
  } catch (error) {
    console.error('Error al cargar tipos de equipo:', error)
  }
}
```

#### ✅ Extracción de IDs al editar
```javascript
function abrirModalEditar(registro) {
  modoEdicion.value = true
  formulario.value = {
    id: registro.id,
    codigo_inventario: registro.codigo_inventario,
    tipo: registro.tipo?.id || null,                    // ✅ Extrae ID del objeto
    marca: registro.marca,
    modelo: registro.modelo,
    numero_serie: registro.numero_serie,
    estado: registro.estado?.id || null,                // ✅ Extrae ID del objeto
    ubicacion_actual: registro.ubicacion_actual?.id || null,  // ✅ Extrae ID del objeto
    notas: registro.notas || ''
  }
  showModal.value = true
}
```

### Patrones "Tóxicos" (A NO Imitar)

❌ **`page_size: 1000`** - Carga todos los activos en memoria (línea 659)
❌ **Filtrado en cliente** - Búsqueda y filtros se aplican localmente
❌ **Carga de todas las páginas** - `cargarTodasLasPaginas` itera sobre paginación (línea 682-693)

### Estructura del Formulario

**Campos:**
- `codigo_inventario` (text, readonly, generado automáticamente)
- `tipo` (select, requerido) - **USA `item-value="id"`**
- `marca` (text, requerido)
- `modelo` (text, requerido)
- `numero_serie` (text, opcional)
- `estado` (select, requerido) - **USA `item-value="id"`**
- `ubicacion_actual` (select, requerido) - **USA `item-value="id"`**
- `notas` (textarea, opcional)

**Validaciones:**
- Tipo: requerido
- Marca: requerido
- Modelo: requerido
- Estado: requerido
- Ubicación Actual: requerido

---

## 12. GestionDepartamentos.vue

### Objetivo de la Vista
- **Gestiona:** CRUD de departamentos
- **Endpoints consumidos:**
  - `GET /api/departamentos/?page_size=1000`
  - `POST /api/departamentos/`
  - `PUT /api/departamentos/{id}/`
  - `DELETE /api/departamentos/{id}/`

### Lógica de "Oro" (Snippets a Rescatar)

#### ✅ Manejo de errores de integridad referencial
```javascript
async function eliminar() {
  try {
    await apiClient.delete(`/api/departamentos/${registroAEliminar.value.id}/`)
    mostrarNotificacion('Departamento eliminado correctamente', 'success')
  } catch (error) {
    if (error.response?.status === 500 || error.response?.status === 400) {
      const errorMsg = error.response?.data
      
      if (errorMsg && typeof errorMsg === 'string' && errorMsg.includes('ProtectedError')) {
        mostrarNotificacion(
          'No se puede eliminar este departamento porque está siendo usado por uno o más activos', 
          'error'
        )
      } else {
        mostrarNotificacion('Error al eliminar el departamento. Puede estar en uso por otros registros.', 'error')
      }
    }
  }
}
```

### Patrones "Tóxicos" (A NO Imitar)

❌ **`page_size: 1000`** - Carga todos los departamentos (línea 303)
❌ **Bug en filtro** - Filtra por `nombre_estado` en vez de `nombre_departamento` (línea 277)
❌ **Filtrado en cliente** - Búsqueda se aplica localmente

### Estructura del Formulario

**Campos:**
- `nombre_departamento` (text, requerido)

**Validaciones:**
- Nombre: requerido

---

## 13. GestionUbicaciones.vue

### Objetivo de la Vista
- **Gestiona:** CRUD de ubicaciones
- **Endpoints consumidos:**
  - `GET /api/ubicaciones/?page_size=1000`
  - `GET /api/departamentos/?page_size=1000` - Para select
  - `POST /api/ubicaciones/`
  - `PUT /api/ubicaciones/{id}/`
  - `DELETE /api/ubicaciones/{id}/`

### Lógica de "Oro" (Snippets a Rescatar)

#### ✅ **PATRÓN HÍBRIDO ENCONTRADO** - Transformación de objetos a IDs
```javascript
async function guardar() {
  const { valid } = await formRef.value.validate()
  if (!valid) return

  try {
    // Preparar payload
    const payload = {
      nombre_ubicacion: formulario.value.nombre_ubicacion?.trim(),
      departamento_id: formulario.value.departamento_id  // ✅ Ya es ID
    }

    if (modoEdicion.value) {
      await apiClient.put(`/api/ubicaciones/${formulario.value.id}/`, payload)
    } else {
      await apiClient.post('/api/ubicaciones/', payload)
    }
  } catch (error) {
    // Manejo de errores...
  }
}
```

#### ✅ Extracción de ID al editar
```javascript
function abrirModalEditar(registro) {
  modoEdicion.value = true
  formulario.value = {
    id: registro.id,
    nombre_ubicacion: registro.nombre_ubicacion,
    departamento_id: registro.departamento?.id || null,  // ✅ Extrae ID del objeto
    codigo_qr: registro.codigo_qr,
    total_activos: registro.total_activos || 0
  }
  showModal.value = true
}
```

### Patrones "Tóxicos" (A NO Imitar)

❌ **`page_size: 1000`** - Carga todas las ubicaciones (línea 502)
❌ **Filtrado en cliente** - Búsqueda y filtros se aplican localmente

### Estructura del Formulario

**Campos:**
- `codigo_qr` (text, readonly, generado automáticamente)
- `nombre_ubicacion` (text, requerido)
- `departamento_id` (select, requerido) - **USA `item-value="id"`**

**Validaciones:**
- Nombre: requerido
- Departamento: requerido

---

## 14. GestionRoles.vue

### Objetivo de la Vista
- **Gestiona:** CRUD de roles
- **Endpoints consumidos:**
  - `GET /api/roles/?page_size=1000`
  - `POST /api/roles/`
  - `PUT /api/roles/{id}/`
  - `DELETE /api/roles/{id}/`

### Lógica de "Oro" (Snippets a Rescatar)

Ninguna especial - CRUD simple.

### Patrones "Tóxicos" (A NO Imitar)

❌ **`page_size: 1000`** - Carga todos los roles (línea 303)
❌ **Bug en filtro** - Filtra por `nombre_estado` en vez de `nombre_rol` (línea 277)
❌ **Filtrado en cliente** - Búsqueda se aplica localmente

### Estructura del Formulario

**Campos:**
- `nombre_rol` (text, requerido)

**Validaciones:**
- Nombre: requerido

---

## 15. GestionTipoEquipo.vue

### Objetivo de la Vista
- **Gestiona:** CRUD de tipos de equipo
- **Endpoints consumidos:**
  - `GET /api/tipos-equipo/?page_size=1000`
  - `POST /api/tipos-equipo/`
  - `PUT /api/tipos-equipo/{id}/`
  - `DELETE /api/tipos-equipo/{id}/`

### Lógica de "Oro" (Snippets a Rescatar)

Ninguna especial - CRUD simple.

### Patrones "Tóxicos" (A NO Imitar)

❌ **`page_size: 1000`** - Carga todos los tipos (línea 303)
❌ **Bug en filtro** - Filtra por `nombre_estado` en vez de `nombre_tipo` (línea 277)
❌ **Filtrado en cliente** - Búsqueda se aplica localmente

### Estructura del Formulario

**Campos:**
- `nombre_tipo` (text, requerido)

**Validaciones:**
- Nombre: requerido

---

## 16. GestionEstadoActivo.vue

### Objetivo de la Vista
- **Gestiona:** CRUD de estados de activo
- **Endpoints consumidos:**
  - `GET /api/estados-activo/?page_size=1000`
  - `POST /api/estados-activo/`
  - `PUT /api/estados-activo/{id}/`
  - `DELETE /api/estados-activo/{id}/`

### Lógica de "Oro" (Snippets a Rescatar)

Ninguna especial - CRUD simple.

### Patrones "Tóxicos" (A NO Imitar)

❌ **`page_size: 1000`** - Carga todos los estados (línea 303)
❌ **Filtrado en cliente** - Búsqueda se aplica localmente

### Estructura del Formulario

**Campos:**
- `nombre_estado` (text, requerido)

**Validaciones:**
- Nombre: requerido

---

## RESUMEN EJECUTIVO

### ✅ Patrones Híbridos Encontrados (Transformación Objeto → ID)

1. **GestionActivos.vue** (Líneas 740-755)
   - Formulario usa objetos en `v-select` con `item-value="id"`
   - Al guardar transforma: `tipo` → `tipo_id`, `estado` → `estado_id`, `ubicacion_actual` → `ubicacion_actual_id`
   - Al editar extrae IDs: `registro.tipo?.id || null`

2. **GestionUbicaciones.vue** (Líneas 555-565)
   - Formulario usa `departamento_id` directamente
   - Al editar extrae: `registro.departamento?.id || null`

3. **GestionUsuarios.vue** (Líneas 722-787)
   - Formulario usa `rol_id` directamente
   - No requiere transformación adicional

### ❌ Patrones Tóxicos Recurrentes

1. **`page_size: 1000`** - Presente en TODAS las vistas de gestión
2. **Filtrado en cliente** - Todas las búsquedas y filtros se aplican localmente
3. **Carga de todas las páginas** - Múltiples vistas iteran sobre paginación
4. **Tablas HTML nativas** - `AssetListView.vue` usa `<table>` en vez de `v-data-table-server`
5. **Bugs en filtros** - `GestionDepartamentos`, `GestionRoles`, `GestionTipoEquipo` filtran por campo incorrecto

### 📋 Estructura de Formularios Rescatable

- **GestionUsuarios:** Formulario completo con validaciones robustas
- **GestionActivos:** Formulario con transformación híbrida (modelo a seguir)
- **GestionUbicaciones:** Formulario simple con relación a departamento

---

**FIN DEL REPORTE**


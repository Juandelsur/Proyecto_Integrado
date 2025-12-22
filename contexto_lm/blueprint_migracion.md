# 🔄 BLUEPRINT DE MIGRACIÓN: MAESTRO DE ACTIVOS

## 📋 ÍNDICE

1. [Reglas Violadas](#1-reglas-violadas)
2. [Rutas a Conectar](#2-rutas-a-conectar)
3. [Plan de Reutilización QR](#3-plan-de-reutilización-qr)
4. [Análisis de Código Legacy](#4-análisis-de-código-legacy)
5. [Estrategia de Migración](#5-estrategia-de-migración)

---

## 1. REGLAS VIOLADAS

### ❌ **REGLA 1: Composition API Estricta**

**ESTADO:** ✅ **NO HAY VIOLACIONES**

- Todas las vistas analizadas utilizan `<script setup>` correctamente.
- No se encontró uso de Options API (`data()`, `methods: {}`, `mounted()`).

**ARCHIVOS VERIFICADOS:**
- ✅ `frontend/src/views/admin/HomeView.vue` - Composition API correcta
- ✅ `frontend/src/views/admin/GestionView.vue` - Composition API correcta
- ✅ `frontend/src/views/admin/gestion/GestionActivos.vue` - Composition API correcta
- ✅ `frontend/src/layouts/LayoutAdministrador.vue` - Composition API correcta

---

### ❌ **REGLA 2: Data Tables Server-Side (Sinergia Django)**

**ESTADO:** ⚠️ **VIOLACIONES CRÍTICAS ENCONTRADAS**

#### **VIOLACIÓN 1: `GestionActivos.vue` - Paginación Manual Local**

**Archivo:** `frontend/src/views/admin/gestion/GestionActivos.vue`

**Problema:**
- ❌ NO usa `<v-data-table-server>`
- ❌ Carga TODOS los registros con `page_size: 1000` (línea 659)
- ❌ Filtra y pagina localmente en el cliente (líneas 600-646)
- ❌ Implementa "Cargar más" manualmente (líneas 918-920)

**Código Problemático:**
```javascript
// LÍNEA 655-677: Carga todos los registros
async function cargarRegistros() {
  loading.value = true
  try {
    const response = await apiClient.get('/api/activos/', {
      params: { page_size: 1000 }  // ❌ VIOLACIÓN: Carga masiva
    })
    
    registros.value = Array.isArray(response.data) 
      ? response.data 
      : response.data.results || []

    // Si hay paginación, obtener todas las páginas
    if (response.data.next) {
      await cargarTodasLasPaginas(response.data.next)  // ❌ VIOLACIÓN: Carga todas las páginas
    }
  }
}

// LÍNEA 643-646: Paginación local
const registrosMostrados = computed(() => {
  const limite = paginaActual.value * registrosPorPagina.value
  return registrosFiltrados.value.slice(0, limite)  // ❌ VIOLACIÓN: Paginación en cliente
})
```

**Impacto:**
- ⚠️ Rendimiento degradado con grandes volúmenes de datos
- ⚠️ Consumo excesivo de memoria en el navegador
- ⚠️ No aprovecha la paginación server-side de Django REST Framework

---

#### **VIOLACIÓN 2: `AssetListView.vue` - Tabla HTML Personalizada**

**Archivo:** `frontend/src/views/admin/AssetListView.vue`

**Problema:**
- ❌ NO usa `<v-data-table-server>`
- ❌ Usa tabla HTML personalizada (`<table>`) sin paginación server-side
- ❌ Carga todos los registros sin paginación (línea 181)

**Código Problemático:**
```javascript
// LÍNEA 178-189: Carga sin paginación
async function loadActivos() {
  try {
    isLoading.value = true
    const response = await apiClient.get('/api/activos/')
    activos.value = Array.isArray(response.data) ? response.data : response.data.results || []
    // ❌ VIOLACIÓN: No maneja paginación, solo toma la primera página
  }
}
```

**Impacto:**
- ⚠️ Solo muestra los primeros 20 registros (paginación por defecto de DRF)
- ⚠️ No permite navegar entre páginas
- ⚠️ No permite ordenamiento server-side

---

#### **VIOLACIÓN 3: `ScannerView.vue` - `v-data-table` (NO Server-Side)**

**Archivo:** `frontend/src/views/technician/ScannerView.vue`

**Problema:**
- ❌ Usa `<v-data-table>` en lugar de `<v-data-table-server>` (línea 298)
- ❌ Carga todos los activos de la ubicación en memoria (línea 817-823)
- ❌ Filtra localmente (líneas 631-648)

**Código Problemático:**
```vue
<!-- LÍNEA 298: Tabla NO server-side -->
<v-data-table
  :headers="headersInventario"
  :items="activosFiltrados"  <!-- ❌ VIOLACIÓN: Items locales, no server-side -->
  :loading="loadingActivos"
  :items-per-page="10"
  class="elevation-1"
  @click:row="handleActivoClick"
>
```

**Impacto:**
- ⚠️ No escala con ubicaciones con muchos activos
- ⚠️ Filtrado y ordenamiento en cliente

---

#### **VIOLACIÓN 4: Otras Vistas de Gestión**

**Archivos afectados:**
- `frontend/src/views/admin/gestion/GestionUbicaciones.vue` (línea 501: `page_size: 1000`)
- `frontend/src/views/admin/gestion/GestionUsuarios.vue` (probablemente mismo patrón)
- `frontend/src/views/admin/gestion/GestionTipoEquipo.vue` (probablemente mismo patrón)
- `frontend/src/views/admin/gestion/GestionEstadoActivo.vue` (probablemente mismo patrón)
- `frontend/src/views/admin/gestion/GestionDepartamentos.vue` (probablemente mismo patrón)
- `frontend/src/views/admin/gestion/GestionRoles.vue` (probablemente mismo patrón)

**Patrón común:**
```javascript
// Todas cargan con page_size: 1000 y filtran localmente
const response = await apiClient.get('/api/entidad/', {
  params: { page_size: 1000 }  // ❌ VIOLACIÓN: Carga masiva
})
```

---

### ✅ **REGLA 3: Patrón Híbrido de Serializers**

**ESTADO:** ✅ **IMPLEMENTACIÓN CORRECTA EN `GestionActivos.vue`**

**Archivo:** `frontend/src/views/admin/gestion/GestionActivos.vue`

**Implementación Correcta (Líneas 740-755):**
```javascript
async function guardar() {
  // Preparar payload con los nombres correctos que espera el backend
  const payload = {
    tipo_id: formulario.value.tipo,           // ✅ CORRECTO: ID en lugar de objeto
    marca: formulario.value.marca?.trim(),
    modelo: formulario.value.modelo?.trim(),
    numero_serie: formulario.value.numero_serie?.trim() || null,
    estado_id: formulario.value.estado,       // ✅ CORRECTO: ID en lugar de objeto
    ubicacion_actual_id: formulario.value.ubicacion_actual,  // ✅ CORRECTO: ID en lugar de objeto
    notas: formulario.value.notas?.trim() || ''
  }

  // ✅ CORRECTO: No envía codigo_inventario en POST (se genera automáticamente)
  if (modoEdicion.value) {
    await apiClient.put(`/api/activos/${formulario.value.id}/`, payload)
  } else {
    await apiClient.post('/api/activos/', payload)
  }
}
```

**Lectura Correcta (Líneas 873-886):**
```javascript
function abrirModalEditar(registro) {
  modoEdicion.value = true
  formulario.value = {
    id: registro.id,
    codigo_inventario: registro.codigo_inventario,
    tipo: registro.tipo?.id || null,              // ✅ CORRECTO: Extrae ID del objeto
    marca: registro.marca,
    modelo: registro.modelo,
    numero_serie: registro.numero_serie,
    estado: registro.estado?.id || null,          // ✅ CORRECTO: Extrae ID del objeto
    ubicacion_actual: registro.ubicacion_actual?.id || null,  // ✅ CORRECTO: Extrae ID del objeto
    notas: registro.notas || ''
  }
  showModal.value = true
}
```

**✅ PATRÓN A REPLICAR:**
- **Lectura (GET):** Usa objetos anidados con Optional Chaining (`registro.tipo?.id`)
- **Escritura (POST/PUT):** Transforma objetos a IDs (`tipo_id`, `estado_id`, `ubicacion_actual_id`)
- **NO envía `codigo_inventario` en POST** (se genera automáticamente)

---

## 2. RUTAS A CONECTAR

### 📍 **Navegación en Layouts y Vistas Home**

**ESTADO:** ⚠️ **MEJORABLE (No es crítico)**

#### **Análisis Actual:**

**Archivo:** `frontend/src/layouts/LayoutAdministrador.vue`

**Código Actual (Líneas 34-47):**
```vue
<v-bottom-navigation v-model="activeTab" grow color="primary" class="bottom-nav">
  <v-btn value="home" @click="navigateTo('/admin/home')">
    <v-icon>mdi-home</v-icon>
    <span>Inicio</span>
  </v-btn>

  <v-btn value="history" @click="navigateTo('/admin/gestion')">
    <v-icon>mdi-folder</v-icon>
    <span>Gestion</span>
  </v-btn>

  <v-btn value="print" @click="navigateTo('/admin/otros')">
    <v-icon>mdi-application-cog</v-icon>
    <span>Otros</span>
  </v-btn>
</v-bottom-navigation>
```

**Función `navigateTo` (Líneas 89-91):**
```javascript
function navigateTo(path) {
  router.push(path)  // ✅ CORRECTO: Usa router.push() internamente
}
```

**✅ CONCLUSIÓN:**
- La función `navigateTo()` ya usa `router.push()` internamente, por lo que **NO es una violación crítica**.
- Sin embargo, se puede simplificar usando directamente `router.push()` en los `@click`.

**Recomendación (Opcional):**
```vue
<!-- MEJOR: Usar router.push() directamente -->
<v-btn value="home" @click="router.push('/admin/home')">
```

---

#### **Navegación en Vistas Home:**

**Archivo:** `frontend/src/views/admin/HomeView.vue`

**Código Actual (Línea 328):**
```javascript
function navigateTo(path) {
  router.push(path)  // ✅ CORRECTO
}
```

**Archivo:** `frontend/src/views/admin/GestionView.vue`

**Código Actual (Líneas 224-226):**
```javascript
function navigateTo(route) {
  router.push(route)  // ✅ CORRECTO
}
```

**✅ CONCLUSIÓN:**
- Todas las funciones `navigateTo()` ya usan `router.push()` correctamente.
- **NO requiere cambios urgentes**, pero se puede simplificar.

---

### 🔗 **Rutas Definidas en Router:**

**Archivo:** `frontend/src/router/index.js`

**Rutas de Administrador (Líneas 214-327):**
```javascript
{
  path: '/admin',
  component: () => import('../layouts/LayoutAdministrador.vue'),
  children: [
    { path: 'home', name: 'admin-home', component: () => import('../views/admin/HomeView.vue') },
    { path: 'gestion', name: 'admin-gestion', component: () => import('../views/admin/GestionView.vue') },
    { path: 'activos', name: 'admin-activos', component: () => import('../views/admin/gestion/GestionActivos.vue') },
    { path: 'usuarios', name: 'admin-usuarios', component: () => import('../views/admin/gestion/GestionUsuarios.vue') },
    // ... más rutas
  ]
}
```

**✅ CONCLUSIÓN:**
- Las rutas `/admin/activos` y `/admin/usuarios` ya están definidas y conectadas.
- `GestionView.vue` navega correctamente a estas rutas (líneas 157, 211).

---

## 3. PLAN DE REUTILIZACIÓN QR

### 📦 **Componente QRScanner Existente**

**Archivo Principal:** `frontend/src/components/QRScanner.vue`

**Estado:** ✅ **IMPLEMENTACIÓN CORRECTA**

**Características:**
- ✅ Usa Composition API (`<script setup>`)
- ✅ Patrón "Overlay Manual" para móviles (User Gesture)
- ✅ Manejo de errores robusto
- ✅ Limpieza correcta en `onBeforeUnmount`
- ✅ Emite eventos: `@scan-success` y `@scan-error`

**Estructura del Componente:**
```vue
<template>
  <div class="qr-scanner-wrapper">
    <div :id="readerId" class="qr-reader-element"></div>
    
    <!-- Overlay con botón ACTIVAR CÁMARA -->
    <div v-if="!isCameraReady" class="overlay-manual">
      <v-btn @click="iniciarCamara">ACTIVAR CÁMARA</v-btn>
    </div>
  </div>
</template>

<script setup>
import { Html5Qrcode } from 'html5-qrcode'

const emit = defineEmits(['scan-success', 'scan-error'])

// Estado y funciones de escaneo
async function iniciarCamara() { /* ... */ }
function onQRCodeSuccess(decodedText, decodedResult) {
  emit('scan-success', { decodedText, decodedResult })
}
</script>
```

---

### 🔄 **Reutilización en `tecnico/ScannerView.vue`**

**Archivo:** `frontend/src/views/technician/ScannerView.vue`

**Estado Actual:** ✅ **YA REUTILIZA EL COMPONENTE CORRECTAMENTE**

**Código Actual (Líneas 47-51):**
```vue
<QRScanner
  @scan-success="handleQRScanSuccess"
  @scan-error="handleQRScanError"
  class="mb-4"
/>
```

**Manejo de Eventos (Líneas 718-731):**
```javascript
function handleQRScanSuccess({ decodedText }) {
  const code = decodedText.trim().toUpperCase()
  
  if (code.startsWith('INV-')) {
    transitionToAsset(code)
  } else if (code.startsWith('LOC-')) {
    transitionToLocation(code)
  } else {
    showErrorMessage('Código QR inválido...')
  }
}
```

**✅ CONCLUSIÓN:**
- El componente `QRScanner.vue` ya se reutiliza correctamente en `ScannerView.vue`.
- **NO requiere cambios** para la nueva vista `admin/ActivosView.vue`.

---

### 📁 **Carpeta `_QR_SAFEZONE`**

**Análisis:**
- `_QR_SAFEZONE/components/QRScanner.vue` es **idéntico** a `frontend/src/components/QRScanner.vue`
- Parece ser una copia de seguridad o versión legacy.
- **NO se debe usar** para nuevas implementaciones.

**Recomendación:**
- ✅ Usar siempre `frontend/src/components/QRScanner.vue` (versión actualizada)
- ⚠️ Considerar eliminar `_QR_SAFEZONE/` después de confirmar que no se usa

---

## 4. ANÁLISIS DE CÓDIGO LEGACY

### 🔍 **Patrones a Desechar**

#### **PATRÓN 1: Carga Masiva con `page_size: 1000`**

**❌ NO REPLICAR:**
```javascript
// ❌ MAL: Carga todos los registros
async function cargarRegistros() {
  const response = await apiClient.get('/api/activos/', {
    params: { page_size: 1000 }
  })
  registros.value = response.data.results || []
  
  // Cargar todas las páginas
  if (response.data.next) {
    await cargarTodasLasPaginas(response.data.next)
  }
}
```

**✅ CORRECTO (Usar `v-data-table-server`):**
```vue
<v-data-table-server
  v-model:items-per-page="options.itemsPerPage"
  v-model:page="options.page"
  :items="items"
  :items-length="totalItems"
  :loading="loading"
  @update:options="loadItems"
>
```

```javascript
async function loadItems({ page, itemsPerPage, sortBy }) {
  loading.value = true
  try {
    const params = {
      page: page,
      page_size: itemsPerPage  // ✅ Mapeo correcto
    }
    
    // Mapeo de ordenamiento
    if (sortBy.length > 0) {
      const sort = sortBy[0]
      params.ordering = sort.order === 'desc' ? `-${sort.key}` : sort.key
    }
    
    const response = await apiClient.get('/api/activos/', { params })
    items.value = response.data.results
    totalItems.value = response.data.count
  } finally {
    loading.value = false
  }
}
```

---

#### **PATRÓN 2: Tablas HTML Personalizadas**

**❌ NO REPLICAR:**
```vue
<!-- ❌ MAL: Tabla HTML sin paginación server-side -->
<table class="assets-table">
  <thead>
    <tr>
      <th>Código</th>
      <th>Marca/Modelo</th>
    </tr>
  </thead>
  <tbody>
    <tr v-for="activo in activos" :key="activo.id">
      <td>{{ activo.codigo_inventario }}</td>
      <td>{{ activo.marca }} {{ activo.modelo }}</td>
    </tr>
  </tbody>
</table>
```

**✅ CORRECTO (Usar `v-data-table-server`):**
```vue
<v-data-table-server
  :headers="headers"
  :items="items"
  :items-length="totalItems"
  :loading="loading"
  @update:options="loadItems"
>
  <template v-slot:item.codigo_inventario="{ item }">
    {{ item.codigo_inventario }}
  </template>
  <template v-slot:item.tipo="{ item }">
    {{ item.tipo?.nombre_tipo }}
  </template>
</v-data-table-server>
```

---

#### **PATRÓN 3: Filtrado Local**

**❌ NO REPLICAR:**
```javascript
// ❌ MAL: Filtra en el cliente
const registrosFiltrados = computed(() => {
  let resultado = registros.value
  
  if (busqueda.value) {
    resultado = resultado.filter(r => 
      r.marca?.toLowerCase().includes(busqueda.value.toLowerCase())
    )
  }
  
  if (filtroTipo.value) {
    resultado = resultado.filter(r => r.tipo?.id === filtroTipo.value)
  }
  
  return resultado
})
```

**✅ CORRECTO (Filtrado server-side):**
```javascript
async function loadItems({ page, itemsPerPage, sortBy }) {
  const params = {
    page: page,
    page_size: itemsPerPage,
    search: busqueda.value || undefined,  // ✅ Búsqueda en backend
    tipo: filtroTipo.value || undefined   // ✅ Filtro en backend
  }
  
  const response = await apiClient.get('/api/activos/', { params })
  items.value = response.data.results
  totalItems.value = response.data.count
}
```

---

### ✅ **Patrones a Replicar**

#### **PATRÓN 1: Patrón Híbrido de Serializers (✅ CORRECTO)**

**Archivo de Referencia:** `frontend/src/views/admin/gestion/GestionActivos.vue`

**Lectura (Líneas 873-886):**
```javascript
function abrirModalEditar(registro) {
  formulario.value = {
    tipo: registro.tipo?.id || null,              // ✅ Extrae ID del objeto
    estado: registro.estado?.id || null,         // ✅ Extrae ID del objeto
    ubicacion_actual: registro.ubicacion_actual?.id || null
  }
}
```

**Escritura (Líneas 747-755):**
```javascript
const payload = {
  tipo_id: formulario.value.tipo,           // ✅ Envía ID, no objeto
  estado_id: formulario.value.estado,       // ✅ Envía ID, no objeto
  ubicacion_actual_id: formulario.value.ubicacion_actual,
  // ✅ NO envía codigo_inventario en POST
}
```

---

#### **PATRÓN 2: Manejo de Relaciones con Optional Chaining**

**✅ CORRECTO:**
```vue
<template>
  <v-data-table-server :items="items">
    <template v-slot:item.tipo="{ item }">
      {{ item.tipo?.nombre_tipo || 'N/A' }}  <!-- ✅ Optional Chaining -->
    </template>
    <template v-slot:item.estado="{ item }">
      {{ item.estado?.nombre_estado || 'N/A' }}
    </template>
    <template v-slot:item.ubicacion_actual="{ item }">
      {{ item.ubicacion_actual?.nombre_ubicacion || 'N/A' }}
    </template>
  </v-data-table-server>
</template>
```

---

## 5. ESTRATEGIA DE MIGRACIÓN

### 🎯 **Objetivo: Crear `admin/ActivosView.vue`**

**Requisitos del Borrador:**
1. ✅ Tabla server-side con `<v-data-table-server>`
2. ✅ Mapeo correcto de parámetros (Vuetify → Django)
3. ✅ Formulario modal CRUD
4. ✅ Patrón híbrido de serializers
5. ✅ Carga de opciones para selects (tipos, estados, ubicaciones)

---

### 📝 **Checklist de Implementación**

#### **FASE 1: Estructura Base**

- [ ] Crear archivo `frontend/src/views/admin/ActivosView.vue`
- [ ] Usar `<script setup>` (Composition API)
- [ ] Usar layout con `<v-container fluid>`
- [ ] Importar `apiClient` y `useRouter`

---

#### **FASE 2: Tabla Server-Side**

- [ ] Implementar `<v-data-table-server>`
- [ ] Crear función `loadItems(options)` que:
  - [ ] Mapee `options.page` → `page` (Django)
  - [ ] Mapee `options.itemsPerPage` → `page_size` (Django)
  - [ ] Mapee `options.sortBy` → `ordering` (String con prefijo `-` para desc)
- [ ] Mapear `response.data.count` → `items-length`
- [ ] Usar Optional Chaining para relaciones (`item.tipo?.nombre_tipo`)

**Headers de Ejemplo:**
```javascript
const headers = [
  { title: 'Código Inventario', key: 'codigo_inventario', sortable: true },
  { title: 'Marca', key: 'marca', sortable: true },
  { title: 'Modelo', key: 'modelo', sortable: true },
  { title: 'Tipo', key: 'tipo', sortable: false },  // FK - no sortable
  { title: 'Estado', key: 'estado', sortable: false },  // FK - no sortable
  { title: 'Ubicación', key: 'ubicacion_actual', sortable: false },  // FK - no sortable
  { title: 'Acciones', key: 'actions', sortable: false }
]
```

---

#### **FASE 3: Formulario Modal CRUD**

- [ ] Crear `<v-dialog>` para crear/editar
- [ ] Usar `<v-form>` con validación
- [ ] Implementar campos:
  - [ ] `tipo` (v-select con `GET /api/tipos-equipo/`)
  - [ ] `marca` (v-text-field)
  - [ ] `modelo` (v-text-field)
  - [ ] `numero_serie` (v-text-field, opcional)
  - [ ] `estado` (v-select con `GET /api/estados-activo/`)
  - [ ] `ubicacion_actual` (v-select con `GET /api/ubicaciones/`)
  - [ ] `notas` (v-textarea, opcional)
- [ ] **NO incluir** `codigo_inventario` en formulario de creación

---

#### **FASE 4: Patrón Híbrido de Serializers**

- [ ] **Lectura (GET):** Usar objetos anidados con Optional Chaining
- [ ] **Escritura (POST/PUT):** Transformar objetos a IDs antes de enviar:
  ```javascript
  const payload = {
    tipo_id: formulario.value.tipo,           // ID, no objeto
    estado_id: formulario.value.estado,       // ID, no objeto
    ubicacion_actual_id: formulario.value.ubicacion_actual,  // ID, no objeto
    marca: formulario.value.marca,
    modelo: formulario.value.modelo,
    numero_serie: formulario.value.numero_serie || null,
    notas: formulario.value.notas || ''
  }
  ```
- [ ] **NO enviar** `codigo_inventario` en POST (solo en PUT si es necesario)

---

#### **FASE 5: Carga de Opciones para Selects**

- [ ] Crear función `cargarTiposEquipo()` que llame a `GET /api/tipos-equipo/`
- [ ] Crear función `cargarEstados()` que llame a `GET /api/estados-activo/`
- [ ] Crear función `cargarUbicaciones()` que llame a `GET /api/ubicaciones/`
- [ ] Cargar estas opciones en `onMounted()` o al abrir el modal

---

#### **FASE 6: Integración con Router**

- [ ] Verificar que la ruta `/admin/activos` ya existe en `router/index.js`
- [ ] Si no existe, agregarla:
  ```javascript
  {
    path: 'activos',
    name: 'admin-activos',
    component: () => import('../views/admin/ActivosView.vue'),
    meta: { title: 'Maestro de Activos' }
  }
  ```

---

### 🚫 **Errores a Evitar**

1. ❌ **NO usar** `page_size: 1000` para cargar todos los registros
2. ❌ **NO usar** tablas HTML personalizadas (`<table>`)
3. ❌ **NO usar** `<v-data-table>` (usar `<v-data-table-server>`)
4. ❌ **NO filtrar** localmente en el cliente
5. ❌ **NO enviar** objetos anidados en POST/PUT (solo IDs)
6. ❌ **NO enviar** `codigo_inventario` en POST (se genera automáticamente)
7. ❌ **NO usar** Options API (`data()`, `methods: {}`)

---

### ✅ **Buenas Prácticas a Seguir**

1. ✅ Usar `<script setup>` (Composition API)
2. ✅ Usar `<v-data-table-server>` para listados paginados
3. ✅ Mapear parámetros correctamente (Vuetify → Django)
4. ✅ Usar Optional Chaining para relaciones (`item.tipo?.nombre_tipo`)
5. ✅ Transformar objetos a IDs antes de enviar (POST/PUT)
6. ✅ Cargar opciones de selects desde la API
7. ✅ Manejar estados de carga (`loading`, `error`)
8. ✅ Usar `variant="outlined"` y `density="compact"` en inputs

---

## 📚 **REFERENCIAS**

### **Archivos de Referencia (Código Correcto):**

1. **Patrón Híbrido de Serializers:**
   - `frontend/src/views/admin/gestion/GestionActivos.vue` (Líneas 740-755, 873-886)

2. **Composition API:**
   - `frontend/src/views/admin/HomeView.vue`
   - `frontend/src/views/admin/GestionView.vue`

3. **Componente QRScanner:**
   - `frontend/src/components/QRScanner.vue` (✅ Usar este, NO `_QR_SAFEZONE`)

---

### **Archivos a NO Replicar (Código Legacy):**

1. ❌ `frontend/src/views/admin/gestion/GestionActivos.vue` (paginación manual)
2. ❌ `frontend/src/views/admin/AssetListView.vue` (tabla HTML personalizada)
3. ❌ `frontend/src/views/technician/ScannerView.vue` (v-data-table NO server-side)

---

## 🎯 **RESUMEN EJECUTIVO**

### **Violaciones Críticas Encontradas:**

1. ⚠️ **REGLA 2 (Data Tables Server-Side):** 
   - `GestionActivos.vue` carga todos los registros con `page_size: 1000`
   - `AssetListView.vue` usa tabla HTML sin paginación server-side
   - `ScannerView.vue` usa `v-data-table` en lugar de `v-data-table-server`

### **Patrones Correctos a Replicar:**

1. ✅ **Patrón Híbrido de Serializers:** `GestionActivos.vue` lo implementa correctamente
2. ✅ **Composition API:** Todas las vistas usan `<script setup>` correctamente
3. ✅ **Componente QRScanner:** Ya está bien implementado y reutilizable

### **Acciones Inmediatas:**

1. ✅ Crear `admin/ActivosView.vue` usando `<v-data-table-server>`
2. ✅ Implementar mapeo correcto de parámetros (Vuetify → Django)
3. ✅ Replicar patrón híbrido de serializers de `GestionActivos.vue`
4. ✅ NO replicar patrones de carga masiva o filtrado local

---

**FIN DEL BLUEPRINT**



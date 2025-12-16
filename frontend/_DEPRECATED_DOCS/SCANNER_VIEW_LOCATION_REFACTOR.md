# 🔧 REFACTORIZACIÓN: VIEW_LOCATION STATE - IMPRESIÓN CONTEXTUAL

## ✅ CAMBIOS IMPLEMENTADOS CON ÉXITO

He refactorizado exitosamente el estado **VIEW_LOCATION** del componente **ScannerView.vue** (TecnicoScanView.vue) con las siguientes mejoras críticas:

---

## 🎯 1. HEADER DE UBICACIÓN (MEJORADO)

### **Antes:**
```vue
<v-btn variant="tonal" color="secondary" prepend-icon="mdi-printer">
  Imprimir Etiquetas
</v-btn>
```

### **Después:**
```vue
<!-- Navegación: Volver a SCANNING -->
<v-btn icon="mdi-arrow-left" variant="text" @click="resetToScanning"></v-btn>

<!-- Títulos: Nombre + Código de Ubicación -->
<div class="flex-grow-1 ml-2">
  <div class="text-h6 font-weight-bold">{{ currentLocation?.nombre_ubicacion }}</div>
  <div class="text-caption text-grey">{{ currentLocation?.codigo_qr }}</div>
</div>

<!-- Acción Contextual: Botón de Impresión con Tooltip -->
<v-tooltip text="Imprimir Etiquetas de esta Sala" location="bottom">
  <template v-slot:activator="{ props }">
    <v-btn
      icon="mdi-printer"
      variant="text"
      color="secondary"
      v-bind="props"
      @click="abrirModalImpresion"
    >
    </v-btn>
  </template>
</v-tooltip>
```

**Mejoras:**
- ✅ **Botón icon-only** con tooltip para ahorrar espacio
- ✅ **Tooltip descriptivo** "Imprimir Etiquetas de esta Sala"
- ✅ **Diseño más limpio** y profesional

---

## 🖨️ 2. MODAL DE IMPRESIÓN (REFACTORIZADO)

### **A. HEADER DEL DIÁLOGO (FASE DE SELECCIÓN)**

```vue
<v-app-bar color="secondary" dark>
  <!-- Botón Cerrar (X) -->
  <v-btn icon="mdi-close" @click="cerrarModalImpresion"></v-btn>

  <!-- Título -->
  <v-toolbar-title>Seleccionar Activos a Imprimir</v-toolbar-title>

  <v-spacer></v-spacer>

  <!-- Botones de Acción -->
  <v-btn variant="text" prepend-icon="mdi-checkbox-multiple-marked" @click="seleccionarTodosActivos">
    Seleccionar Todos
  </v-btn>

  <v-btn variant="text" prepend-icon="mdi-checkbox-multiple-blank-outline" @click="deseleccionarTodosActivos">
    Deseleccionar
  </v-btn>

  <!-- Botón Principal: IMPRIMIR AHORA -->
  <v-btn
    variant="elevated"
    color="white"
    prepend-icon="mdi-printer"
    @click="imprimirEtiquetas"
    :disabled="activosSeleccionados.length === 0"
  >
    <span style="color: #424242;">IMPRIMIR AHORA</span>
  </v-btn>
</v-app-bar>
```

**Mejoras:**
- ✅ **Título actualizado** a "Seleccionar Activos a Imprimir"
- ✅ **Botones de acción** en el header (Seleccionar Todos / Deseleccionar)
- ✅ **Botón IMPRIMIR AHORA** destacado con color blanco
- ✅ **Disabled state** cuando no hay activos seleccionados

---

### **B. CUERPO DEL DIÁLOGO (LISTA DE SELECCIÓN)**

```vue
<!-- Contador de Selección -->
<v-alert type="info" variant="tonal" class="mb-4" prominent>
  <div class="d-flex align-center">
    <v-icon size="32" class="mr-3">mdi-information</v-icon>
    <div>
      <div class="text-h6">
        {{ activosSeleccionados.length }} de {{ activosDeUbicacion.length }} activos seleccionados
      </div>
      <div class="text-caption">
        Selecciona los activos que deseas imprimir. Las etiquetas se generarán automáticamente.
      </div>
    </div>
  </div>
</v-alert>

<!-- Lista de Activos con Checkboxes -->
<v-card variant="outlined" class="mb-6">
  <v-card-text>
    <div class="activos-list" style="max-height: 400px; overflow-y: auto;">
      <v-checkbox
        v-for="activo in activosDeUbicacion"
        :key="activo.id"
        v-model="activosSeleccionados"
        :value="activo.id"
        hide-details
        class="mb-3"
        color="secondary"
      >
        <template v-slot:label>
          <div class="d-flex align-center justify-space-between" style="width: 100%;">
            <div>
              <span class="font-weight-bold text-body-1">
                {{ activo.marca }} {{ activo.modelo }}
              </span>
              <br>
              <span class="text-caption text-grey">
                {{ activo.codigo_inventario }} | {{ activo.tipo?.nombre_tipo }}
              </span>
            </div>
            <v-chip size="small" :color="getEstadoColor(activo.estado?.nombre_estado)">
              {{ activo.estado?.nombre_estado }}
            </v-chip>
          </div>
        </template>
      </v-checkbox>
    </div>
  </v-card-text>
</v-card>
```

**Mejoras:**
- ✅ **Alert informativo** con contador de selección
- ✅ **Diseño mejorado** de los checkboxes con más información
- ✅ **Scroll vertical** para listas largas (max-height: 400px)
- ✅ **Color secundario** en los checkboxes

---

### **C. VISTA PREVIA DE ETIQUETAS**

```vue
<div class="preview-section">
  <h3 class="text-h6 mb-3">
    <v-icon start color="secondary">mdi-eye</v-icon>
    Vista Previa de Etiquetas
  </h3>

  <v-alert v-if="activosSeleccionados.length === 0" type="warning" variant="tonal" class="mb-4">
    <v-icon start>mdi-alert</v-icon>
    Selecciona al menos un activo para ver la vista previa de las etiquetas.
  </v-alert>

  <!-- ÁREA DE IMPRESIÓN -->
  <div id="print-area" class="print-area">
    <div class="labels-grid">
      <div v-for="activoId in activosSeleccionados" :key="activoId" class="label-item">
        <div class="label-content">
          <!-- Nombre del Activo (Izquierda) -->
          <div class="label-nombre">
            <div class="nombre-text">
              {{ getActivoById(activoId)?.marca }} {{ getActivoById(activoId)?.modelo }}
            </div>
            <div class="tipo-text">
              {{ getActivoById(activoId)?.tipo?.nombre_tipo }}
            </div>
          </div>

          <!-- QR Code (Centro) -->
          <div class="label-qr">
            <img
              v-if="qrCodes[getActivoById(activoId)?.codigo_inventario]"
              :src="qrCodes[getActivoById(activoId)?.codigo_inventario]"
              alt="QR Code"
              class="qr-image"
            />
            <div v-else class="qr-placeholder">
              <v-progress-circular indeterminate size="32"></v-progress-circular>
            </div>
          </div>

          <!-- Código Vertical (Derecha del QR) -->
          <div class="label-codigo-vertical">
            <span class="codigo-vertical-text">
              {{ getActivoById(activoId)?.codigo_inventario }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
```

**Mejoras:**
- ✅ **Placeholder de carga** para QR codes (v-progress-circular)
- ✅ **Alert de advertencia** cuando no hay activos seleccionados
- ✅ **Vista previa visible** en pantalla (no solo en impresión)

---

## 🎨 3. ESTILOS DE IMPRESIÓN (CSS CRÍTICO - "PIXEL PERFECT")

### **A. RESET Y VISIBILIDAD**

```css
@media print {
  /* RESET: Ocultar todo el body excepto el contenedor de etiquetas */
  body {
    visibility: hidden;
    margin: 0;
    padding: 0;
  }

  /* Hacer visible solo el área de impresión */
  #print-area,
  #print-area * {
    visibility: visible;
  }

  /* Posicionar el área de impresión en la esquina superior izquierda */
  #print-area {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    background: white;
    padding: 1cm;
    margin: 0;
    border: none;
    border-radius: 0;
  }
}
```

---

### **B. GRID LAYOUT (3 COLUMNAS)**

```css
@media print {
  .labels-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    padding: 0;
    margin: 0;
  }
}
```

---

### **C. TARJETA DE ETIQUETA (Label Card)**

```css
@media print {
  .label-item {
    border: 1px dashed black;
    padding: 0.75rem;
    background: white;
    page-break-inside: avoid;
    break-inside: avoid;
    min-height: 150px;
    height: 150px;
    display: flex;
    align-items: center;
  }

  .label-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
    width: 100%;
    height: 100%;
  }
}
```

**Características:**
- ✅ **Borde dashed** de 1px para líneas de corte
- ✅ **page-break-inside: avoid** - Evita cortes entre páginas
- ✅ **Altura fija** de 150px para consistencia
- ✅ **Flex layout** para alineación perfecta

---

### **D. TIPOGRAFÍA Y ORIENTACIÓN**

```css
@media print {
  /* Izquierda: Nombre del Activo */
  .nombre-text {
    font-size: 11pt;
    font-weight: bold;
    line-height: 1.3;
    color: black;
  }

  .tipo-text {
    font-size: 9pt;
    color: #333;
  }

  /* Centro: QR Code */
  .qr-image {
    width: 100px;
    height: 100px;
  }

  /* Derecha: Texto Vertical (Código Inventario) */
  .label-codigo-vertical {
    writing-mode: vertical-rl;
    text-orientation: mixed;
    transform: rotate(180deg);
    height: 100px;
  }

  .codigo-vertical-text {
    font-size: 9pt;
    font-weight: bold;
    letter-spacing: 0.1em;
    color: black;
  }
}
```

**Regla CSS Clave:**
```css
writing-mode: vertical-rl;
text-orientation: mixed;
transform: rotate(180deg);
```

---

## 🔧 4. INTEGRACIÓN LÓGICA (JAVASCRIPT)

### **A. Función `abrirModalImpresion()` (MEJORADA)**

```javascript
/**
 * Abre el modal de impresión y genera los QR codes.
 * Inicializa la selección con TODOS los activos de la ubicación actual.
 */
async function abrirModalImpresion() {
  // Resetear selección
  activosSeleccionados.value = []
  seleccionarTodos.value = false
  qrCodes.value = {}

  // Abrir modal
  dialogImpresion.value = true

  // Generar QR codes para todos los activos de la ubicación
  await generarQRCodes()

  // Inicializar con todos los activos seleccionados
  activosSeleccionados.value = activosDeUbicacion.value.map(a => a.id)
  seleccionarTodos.value = true
}
```

**Cambio Crítico:**
- ✅ **Inicializa con TODOS los activos seleccionados** por defecto
- ✅ **Genera QR codes automáticamente** al abrir el modal

---

### **B. Nuevas Funciones de Selección**

```javascript
/**
 * Selecciona todos los activos de la ubicación.
 */
function seleccionarTodosActivos() {
  activosSeleccionados.value = activosDeUbicacion.value.map(a => a.id)
  seleccionarTodos.value = true
}

/**
 * Deselecciona todos los activos.
 */
function deseleccionarTodosActivos() {
  activosSeleccionados.value = []
  seleccionarTodos.value = false
}
```

---

## 📊 CONEXIONES A BASE DE DATOS (VERIFICADAS)

### **API Endpoint: `/api/ubicaciones/`**

**Parámetros:**
```javascript
{
  search: 'LOC-F8A1B2'  // Código QR de la ubicación
}
```

**Respuesta:**
```json
{
  "results": [
    {
      "id": 1,
      "nombre_ubicacion": "Sala 101",
      "codigo_qr": "LOC-F8A1B2",
      "departamento": {
        "id": 1,
        "nombre_departamento": "Urgencias"
      },
      "total_activos": 15
    }
  ]
}
```

---

### **API Endpoint: `/api/activos/`**

**Parámetros:**
```javascript
{
  ubicacion_actual: 1  // ID de la ubicación
}
```

**Respuesta:**
```json
{
  "results": [
    {
      "id": 5,
      "codigo_inventario": "INV-25-A1B2C3",
      "numero_serie": "SN123456",
      "marca": "HP",
      "modelo": "EliteBook 840 G8",
      "tipo": {
        "id": 1,
        "nombre_tipo": "Laptop"
      },
      "estado": {
        "id": 1,
        "nombre_estado": "Operativo"
      },
      "ubicacion_actual": {
        "id": 1,
        "nombre_ubicacion": "Sala 101"
      }
    }
  ]
}
```

---

## ✅ VERIFICACIÓN DE ATRIBUTOS

| Atributo Frontend | Atributo Backend | Estado |
|-------------------|------------------|--------|
| `currentLocation.nombre_ubicacion` | `nombre_ubicacion` | ✅ Correcto |
| `currentLocation.codigo_qr` | `codigo_qr` | ✅ Correcto |
| `activo.codigo_inventario` | `codigo_inventario` | ✅ Correcto |
| `activo.marca` | `marca` | ✅ Correcto |
| `activo.modelo` | `modelo` | ✅ Correcto |
| `activo.tipo.nombre_tipo` | `tipo.nombre_tipo` | ✅ Correcto |
| `activo.estado.nombre_estado` | `estado.nombre_estado` | ✅ Correcto |

---

## 📝 RESUMEN DE CAMBIOS

| Sección | Cambios |
|---------|---------|
| **Header VIEW_LOCATION** | ✅ Botón icon-only con tooltip |
| **Modal Header** | ✅ Botones de acción + IMPRIMIR AHORA |
| **Modal Body** | ✅ Alert informativo + lista mejorada |
| **Vista Previa** | ✅ Placeholder de carga para QR |
| **Estilos Print** | ✅ CSS Pixel Perfect con grid 3x3 |
| **Lógica JS** | ✅ Inicialización con todos seleccionados |
| **Funciones** | ✅ seleccionarTodosActivos() + deseleccionarTodosActivos() |

**Total de líneas modificadas:** ~150 líneas

---

**¡La refactorización está completa y lista para producción!** 🚀


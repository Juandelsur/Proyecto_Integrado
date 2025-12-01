<template>
  <div class="print-labels-view">
    <!-- TABS DE SELECCIÓN DE ACTIVOS -->
    <v-card class="mb-4">
      <v-tabs v-model="activeTab" bg-color="primary" dark>
        <v-tab value="activos">
          <v-icon start>mdi-checkbox-multiple-marked</v-icon>
          Por Activos
        </v-tab>
        <v-tab value="ubicaciones">
          <v-icon start>mdi-map-marker-multiple</v-icon>
          Por Ubicaciones
        </v-tab>
        <v-tab value="manual">
          <v-icon start>mdi-keyboard</v-icon>
          Manual
        </v-tab>
      </v-tabs>

      <v-window v-model="activeTab">
        <!-- TAB 1: POR ACTIVOS -->
        <v-window-item value="activos">
          <v-card-text>
            <!-- Filtros -->
            <v-row class="mb-4">
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="filtros.busqueda"
                  label="Buscar activo"
                  prepend-inner-icon="mdi-magnify"
                  variant="outlined"
                  density="comfortable"
                  clearable
                  hint="Buscar por código, marca, modelo o número de serie"
                  persistent-hint
                ></v-text-field>
              </v-col>

              <v-col cols="12" sm="6" md="3">
                <v-select
                  v-model="filtros.marca"
                  :items="marcasDisponibles"
                  label="Marca"
                  variant="outlined"
                  density="comfortable"
                  clearable
                ></v-select>
              </v-col>

              <v-col cols="12" sm="6" md="3">
                <v-select
                  v-model="filtros.tipoEquipo"
                  :items="tiposEquipo"
                  item-title="nombre_tipo"
                  item-value="id"
                  label="Tipo de Equipo"
                  variant="outlined"
                  density="comfortable"
                  clearable
                ></v-select>
              </v-col>

              <v-col cols="12" md="6">
                <v-select
                  v-model="filtros.ubicacion"
                  :items="ubicaciones"
                  item-title="nombre_ubicacion"
                  item-value="id"
                  label="Ubicación Actual"
                  variant="outlined"
                  density="comfortable"
                  clearable
                ></v-select>
              </v-col>

              <v-col cols="12" md="6">
                <v-btn
                  color="secondary"
                  variant="outlined"
                  block
                  @click="limpiarFiltros"
                >
                  <v-icon start>mdi-filter-off</v-icon>
                  Limpiar Filtros
                </v-btn>
              </v-col>
            </v-row>

            <!-- Tabla de Activos -->
            <v-data-table
              v-model="activosSeleccionados"
              :headers="headersActivos"
              :items="activosFiltrados"
              :loading="loadingActivos"
              show-select
              item-value="id"
              class="elevation-1"
              :items-per-page="10"
            >
              <template v-slot:loading>
                <v-skeleton-loader type="table-row@10"></v-skeleton-loader>
              </template>

              <template v-slot:no-data>
                <div class="text-center py-8">
                  <v-icon size="64" color="grey">mdi-package-variant</v-icon>
                  <p class="text-h6 mt-4">No hay activos disponibles</p>
                </div>
              </template>

              <template v-slot:item.nombre="{ item }">
                <span class="font-weight-medium">{{ item.marca }} {{ item.modelo }}</span>
              </template>

              <template v-slot:item.ubicacion="{ item }">
                <v-chip size="small" color="info" variant="tonal">
                  {{ item.ubicacion_actual?.nombre_ubicacion || 'Sin ubicación' }}
                </v-chip>
              </template>
            </v-data-table>

            <v-card-actions class="mt-4">
              <v-spacer></v-spacer>
              <v-btn
                color="primary"
                size="large"
                :disabled="activosSeleccionados.length === 0"
                @click="agregarSeleccionadosACola"
              >
                <v-icon start>mdi-plus-circle</v-icon>
                Agregar {{ activosSeleccionados.length }} Seleccionados a Cola
              </v-btn>
            </v-card-actions>
          </v-card-text>
        </v-window-item>

        <!-- TAB 2: POR UBICACIONES -->
        <v-window-item value="ubicaciones">
          <v-card-text>
            <v-row class="mb-4">
              <v-col cols="12" md="6">
                <v-select
                  v-model="filtros.departamento"
                  :items="departamentos"
                  item-title="nombre_departamento"
                  item-value="id"
                  label="Departamento"
                  variant="outlined"
                  density="comfortable"
                  clearable
                ></v-select>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="filtros.busquedaUbicacion"
                  label="Buscar ubicación"
                  prepend-inner-icon="mdi-magnify"
                  variant="outlined"
                  density="comfortable"
                  clearable
                ></v-text-field>
              </v-col>
            </v-row>

            <!-- Tabla de Ubicaciones -->
            <v-data-table
              v-model="ubicacionesSeleccionadas"
              :headers="headersUbicaciones"
              :items="ubicacionesFiltradas"
              :loading="loadingUbicaciones"
              show-select
              item-value="id"
              class="elevation-1"
              :items-per-page="10"
            >
              <template v-slot:loading>
                <v-skeleton-loader type="table-row@10"></v-skeleton-loader>
              </template>

              <template v-slot:no-data>
                <div class="text-center py-8">
                  <v-icon size="64" color="grey">mdi-map-marker-off</v-icon>
                  <p class="text-h6 mt-4">No hay ubicaciones disponibles</p>
                </div>
              </template>

              <template v-slot:item.departamento="{ item }">
                <v-chip size="small" color="primary" variant="tonal">
                  {{ item.departamento?.nombre_departamento || 'Sin departamento' }}
                </v-chip>
              </template>

              <template v-slot:item.total_activos="{ item }">
                <v-chip size="small" color="success" variant="outlined">
                  {{ item.total_activos || 0 }} activos
                </v-chip>
              </template>
            </v-data-table>

            <v-card-actions class="mt-4">
              <v-spacer></v-spacer>
              <v-btn
                color="primary"
                size="large"
                :disabled="ubicacionesSeleccionadas.length === 0"
                @click="agregarActivosPorUbicacion"
              >
                <v-icon start>mdi-plus-circle</v-icon>
                Agregar Activos de {{ ubicacionesSeleccionadas.length }} Ubicaciones
              </v-btn>
            </v-card-actions>
          </v-card-text>
        </v-window-item>

        <!-- TAB 3: MANUAL -->
        <v-window-item value="manual">
          <v-card-text>
            <v-alert type="info" variant="tonal" class="mb-4">
              <v-icon start>mdi-information</v-icon>
              Ingresa los códigos de inventario manualmente. Presiona Enter después de cada código.
            </v-alert>

            <v-combobox
              v-model="codigosManuales"
              label="Códigos de Inventario"
              prepend-inner-icon="mdi-barcode"
              variant="outlined"
              chips
              multiple
              closable-chips
              hint="Escribe un código y presiona Enter. Ejemplo: INV-25-A1B2C3"
              persistent-hint
            ></v-combobox>

            <v-card-actions class="mt-4">
              <v-spacer></v-spacer>
              <v-btn
                color="error"
                variant="outlined"
                @click="codigosManuales = []"
                :disabled="codigosManuales.length === 0"
              >
                <v-icon start>mdi-delete</v-icon>
                Limpiar
              </v-btn>
              <v-btn
                color="primary"
                size="large"
                :disabled="codigosManuales.length === 0"
                @click="agregarCodigosManuales"
              >
                <v-icon start>mdi-plus-circle</v-icon>
                Agregar {{ codigosManuales.length }} Códigos
              </v-btn>
            </v-card-actions>
          </v-card-text>
        </v-window-item>
      </v-window>
    </v-card>

    <!-- COLA DE IMPRESIÓN -->
    <v-card v-if="colaImpresion.length > 0" class="mb-4">
      <v-card-title class="d-flex align-center">
        <v-icon start color="success">mdi-printer-check</v-icon>
        Cola de Impresión ({{ colaImpresion.length }} activos)
        <v-spacer></v-spacer>
        <v-btn
          color="error"
          variant="text"
          size="small"
          @click="limpiarCola"
        >
          <v-icon start>mdi-delete-sweep</v-icon>
          Limpiar Cola
        </v-btn>
      </v-card-title>

      <v-card-text>
        <v-chip-group column>
          <v-chip
            v-for="activo in colaImpresion"
            :key="activo.id"
            closable
            @click:close="removerDeCola(activo.id)"
            color="primary"
            variant="outlined"
          >
            {{ activo.codigo_inventario }} - {{ activo.marca }} {{ activo.modelo }}
          </v-chip>
        </v-chip-group>
      </v-card-text>
    </v-card>

    <!-- BOTÓN FLOTANTE DE VISTA PREVIA -->
    <v-btn
      v-if="colaImpresion.length > 0"
      class="fab-preview"
      color="success"
      size="x-large"
      elevation="8"
      @click="abrirVistaPrevia"
    >
      <v-icon start>mdi-printer-eye</v-icon>
      Vista Previa / Imprimir ({{ colaImpresion.length }})
    </v-btn>

    <!-- DIÁLOGO DE VISTA PREVIA E IMPRESIÓN -->
    <v-dialog
      v-model="dialogVistaPrevia"
      fullscreen
      transition="dialog-bottom-transition"
    >
      <v-card>
        <v-toolbar color="primary" dark>
          <v-btn icon @click="cerrarVistaPrevia">
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-toolbar-title>Vista Previa de Etiquetas ({{ colaImpresion.length }} activos)</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="imprimirEtiquetas">
            <v-icon start>mdi-printer</v-icon>
            Imprimir Ahora
          </v-btn>
        </v-toolbar>

        <v-card-text class="pa-4">
          <!-- Área de Impresión -->
          <div id="print-area" class="print-container">
            <div
              v-for="activo in colaImpresion"
              :key="activo.id"
              class="etiqueta-card"
            >
              <!-- Contenido de la Etiqueta -->
              <div class="etiqueta-content">
                <!-- Izquierda: Nombre del Activo (70%) -->
                <div class="etiqueta-nombre">
                  <span class="nombre-text">{{ activo.marca }} {{ activo.modelo }}</span>
                </div>

                <!-- Derecha: QR + Código Vertical (30%) -->
                <div class="etiqueta-qr-section">
                  <!-- QR Code -->
                  <div class="qr-container">
                    <img
                      :src="activo.qrDataUrl"
                      alt="QR Code"
                      class="qr-image"
                    />
                  </div>

                  <!-- Código Vertical -->
                  <div class="codigo-vertical">
                    <span>{{ activo.codigo_inventario }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
/**
 * ============================================================================
 * PRINT LABELS VIEW - IMPRESIÓN DE ETIQUETAS QR
 * ============================================================================
 *
 * Vista crítica de gestión para imprimir etiquetas de activos con QR codes.
 * Tres modos de selección: Por Activos, Por Ubicaciones, Manual.
 * Genera etiquetas con diseño industrial (3 por fila) listas para impresión.
 */

import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/services/api'
import QRCode from 'qrcode'

// ============================================================================
// COMPOSABLES
// ============================================================================

const router = useRouter()

// ============================================================================
// STATE - TABS Y FILTROS
// ============================================================================

const activeTab = ref('activos')

const filtros = ref({
  busqueda: '',
  marca: null,
  tipoEquipo: null,
  ubicacion: null,
  departamento: null,
  busquedaUbicacion: ''
})

// ============================================================================
// STATE - DATOS DE LA API
// ============================================================================

const activos = ref([])
const ubicaciones = ref([])
const departamentos = ref([])
const tiposEquipo = ref([])

const loadingActivos = ref(false)
const loadingUbicaciones = ref(false)

// ============================================================================
// STATE - SELECCIÓN Y COLA
// ============================================================================

const activosSeleccionados = ref([])
const ubicacionesSeleccionadas = ref([])
const codigosManuales = ref([])
const colaImpresion = ref([])

// ============================================================================
// STATE - VISTA PREVIA
// ============================================================================

const dialogVistaPrevia = ref(false)

// ============================================================================
// COMPUTED - HEADERS DE TABLAS
// ============================================================================

const headersActivos = computed(() => [
  { title: 'Nombre', key: 'nombre', sortable: true },
  { title: 'Código', key: 'codigo_inventario', sortable: true },
  { title: 'Marca', key: 'marca', sortable: true },
  { title: 'Ubicación', key: 'ubicacion', sortable: false }
])

const headersUbicaciones = computed(() => [
  { title: 'Ubicación', key: 'nombre_ubicacion', sortable: true },
  { title: 'Departamento', key: 'departamento', sortable: false },
  { title: 'Total Activos', key: 'total_activos', sortable: true }
])

// ============================================================================
// COMPUTED - FILTROS
// ============================================================================

const activosFiltrados = computed(() => {
  let resultado = activos.value

  if (filtros.value.marca) {
    resultado = resultado.filter(a => a.marca === filtros.value.marca)
  }

  if (filtros.value.tipoEquipo) {
    resultado = resultado.filter(a => a.tipo?.id === filtros.value.tipoEquipo)
  }

  if (filtros.value.ubicacion) {
    resultado = resultado.filter(a => a.ubicacion_actual?.id === filtros.value.ubicacion)
  }

  return resultado
})

const ubicacionesFiltradas = computed(() => {
  let resultado = ubicaciones.value

  if (filtros.value.departamento) {
    resultado = resultado.filter(u => u.departamento?.id === filtros.value.departamento)
  }

  if (filtros.value.busquedaUbicacion) {
    const busqueda = filtros.value.busquedaUbicacion.toLowerCase()
    resultado = resultado.filter(u =>
      u.nombre_ubicacion.toLowerCase().includes(busqueda)
    )
  }

  return resultado
})

const marcasDisponibles = computed(() => {
  const marcas = [...new Set(activos.value.map(a => a.marca))]
  return marcas.sort()
})

// ============================================================================
// MÉTODOS - API
// ============================================================================

async function fetchActivos() {
  loadingActivos.value = true
  try {
    const response = await apiClient.get('/api/activos/')
    activos.value = response.data.results || response.data
  } catch (error) {
    console.error('Error al cargar activos:', error)
  } finally {
    loadingActivos.value = false
  }
}

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

async function fetchDepartamentos() {
  try {
    const response = await apiClient.get('/api/departamentos/')
    departamentos.value = response.data.results || response.data
  } catch (error) {
    console.error('Error al cargar departamentos:', error)
  }
}

async function fetchTiposEquipo() {
  try {
    const response = await apiClient.get('/api/tipos-equipo/')
    tiposEquipo.value = response.data.results || response.data
  } catch (error) {
    console.error('Error al cargar tipos de equipo:', error)
  }
}

// ============================================================================
// MÉTODOS - GESTIÓN DE COLA
// ============================================================================

function agregarSeleccionadosACola() {
  const nuevosActivos = activos.value.filter(a =>
    activosSeleccionados.value.includes(a.id) &&
    !colaImpresion.value.some(c => c.id === a.id)
  )

  colaImpresion.value.push(...nuevosActivos)
  activosSeleccionados.value = []
}

async function agregarActivosPorUbicacion() {
  for (const ubicacionId of ubicacionesSeleccionadas.value) {
    const activosDeUbicacion = activos.value.filter(a =>
      a.ubicacion_actual?.id === ubicacionId &&
      !colaImpresion.value.some(c => c.id === a.id)
    )

    colaImpresion.value.push(...activosDeUbicacion)
  }

  ubicacionesSeleccionadas.value = []
}

async function agregarCodigosManuales() {
  for (const codigo of codigosManuales.value) {
    const activo = activos.value.find(a =>
      a.codigo_inventario === codigo &&
      !colaImpresion.value.some(c => c.id === a.id)
    )

    if (activo) {
      colaImpresion.value.push(activo)
    }
  }

  codigosManuales.value = []
}

function removerDeCola(activoId) {
  colaImpresion.value = colaImpresion.value.filter(a => a.id !== activoId)
}

function limpiarCola() {
  colaImpresion.value = []
}

function limpiarFiltros() {
  filtros.value = {
    busqueda: '',
    marca: null,
    tipoEquipo: null,
    ubicacion: null,
    departamento: null,
    busquedaUbicacion: ''
  }
}

// ============================================================================
// MÉTODOS - GENERACIÓN DE QR CODES
// ============================================================================

async function generarQRCode(codigo) {
  try {
    const qrDataUrl = await QRCode.toDataURL(codigo, {
      width: 120,
      margin: 1,
      color: {
        dark: '#000000',
        light: '#FFFFFF'
      }
    })
    return qrDataUrl
  } catch (error) {
    console.error('Error al generar QR:', error)
    return ''
  }
}

async function generarQRsParaCola() {
  for (const activo of colaImpresion.value) {
    if (!activo.qrDataUrl) {
      activo.qrDataUrl = await generarQRCode(activo.codigo_inventario)
    }
  }
}

// ============================================================================
// MÉTODOS - VISTA PREVIA E IMPRESIÓN
// ============================================================================

async function abrirVistaPrevia() {
  await generarQRsParaCola()
  dialogVistaPrevia.value = true
}

function cerrarVistaPrevia() {
  dialogVistaPrevia.value = false
}

function imprimirEtiquetas() {
  window.print()
}

// ============================================================================
// LIFECYCLE HOOKS
// ============================================================================

onMounted(async () => {
  await Promise.all([
    fetchActivos(),
    fetchUbicaciones(),
    fetchDepartamentos(),
    fetchTiposEquipo()
  ])
})
</script>

<style scoped>
/* ============================================================================
   CONTENEDOR PRINCIPAL
   ============================================================================ */

.print-labels-view {
  min-height: calc(100vh - 112px);
  background: #f5f7fa;
  padding: 1rem;
  padding-bottom: 100px; /* Espacio para el FAB */
}

/* ============================================================================
   BOTÓN FLOTANTE DE VISTA PREVIA
   ============================================================================ */

.fab-preview {
  position: fixed !important;
  bottom: 80px !important;
  right: 24px !important;
  z-index: 1000 !important;
}

/* ============================================================================
   CONTENEDOR DE ETIQUETAS (GRID 3 COLUMNAS)
   ============================================================================ */

.print-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  padding: 20px;
  background: white;
}

/* ============================================================================
   TARJETA DE ETIQUETA INDIVIDUAL
   ============================================================================ */

.etiqueta-card {
  border: 1px dashed #000;
  padding: 8px;
  page-break-inside: avoid;
  min-height: 80px;
  display: flex;
  align-items: center;
}

.etiqueta-content {
  display: flex;
  width: 100%;
  align-items: center;
  gap: 8px;
}

/* ============================================================================
   NOMBRE DEL ACTIVO (IZQUIERDA - 70%)
   ============================================================================ */

.etiqueta-nombre {
  flex: 0 0 70%;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  padding-left: 8px;
}

.nombre-text {
  font-size: 14px;
  font-weight: bold;
  line-height: 1.2;
  text-align: left;
  word-wrap: break-word;
}

/* ============================================================================
   SECCIÓN QR + CÓDIGO (DERECHA - 30%)
   ============================================================================ */

.etiqueta-qr-section {
  flex: 0 0 30%;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 4px;
}

.qr-container {
  flex-shrink: 0;
}

.qr-image {
  width: 60px;
  height: 60px;
  display: block;
}

/* ============================================================================
   CÓDIGO VERTICAL (ROTADO 90 GRADOS)
   ============================================================================ */

.codigo-vertical {
  writing-mode: vertical-rl;
  text-orientation: mixed;
  font-size: 10px;
  font-weight: bold;
  letter-spacing: 1px;
  white-space: nowrap;
  padding: 4px 0;
}

/* ============================================================================
   RESPONSIVE - TABLETS Y MÓVILES
   ============================================================================ */

@media (max-width: 960px) {
  .print-container {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 600px) {
  .print-container {
    grid-template-columns: 1fr;
  }

  .fab-preview {
    bottom: 70px !important;
    right: 16px !important;
  }
}

/* ============================================================================
   ESTILOS DE IMPRESIÓN (@media print)
   ============================================================================ */

@media print {
  /* Ocultar todo excepto el área de impresión */
  body * {
    visibility: hidden;
  }

  #print-area,
  #print-area * {
    visibility: visible;
  }

  #print-area {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
  }

  /* Ajustar márgenes de página */
  @page {
    margin: 10mm;
    size: A4;
  }

  /* Asegurar que las etiquetas no se corten */
  .etiqueta-card {
    page-break-inside: avoid;
    break-inside: avoid;
  }

  /* Mantener el grid de 3 columnas en impresión */
  .print-container {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
  }
}
</style>


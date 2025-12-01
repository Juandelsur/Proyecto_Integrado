<!--
  ============================================================================
  TECNICO SCAN VIEW - CENTRO DE DECISIÓN CON STATE MACHINE + IMPRESIÓN QR
  ============================================================================

  DESCRIPCIÓN:
  Vista crítica que actúa como un Centro de Decisión para el técnico.
  Implementa un patrón de State Machine con 3 estados visuales internos
  sin navegación entre rutas, eliminando tiempos de carga.

  PATRÓN DE DISEÑO: SINGLE PAGE STATE MACHINE

  ESTADOS:
  1. SCANNING - Interfaz de captura (estado inicial)
  2. VIEW_ASSET - Detalle de un activo (prefijo INV-)
  3. VIEW_LOCATION - Inventario de una ubicación (prefijo LOC-)

  CARACTERÍSTICAS:
  - Transiciones instantáneas entre estados
  - Sin navegación entre rutas (mejor UX móvil)
  - Tabla móvil optimizada con diseño de 2 líneas
  - Modal de impresión con generación de QR del lado del cliente
  - Generación de QR en Base64 usando librería 'qrcode'
  - Diseño de etiquetas con CSS Grid (3 columnas)
  - Código vertical rotado 90 grados
  - Flujo circular (desde ubicación → activo → ubicación)

  DEPENDENCIAS:
  - Vue 3 Composition API
  - Vuetify 3
  - Vue Router
  - API Client
  - qrcode (para generación de QR en Base64)

  AUTOR: Senior Frontend Developer
  FECHA: 2025-12-01
  ============================================================================
-->

<template>
  <div class="scanner-view">
    <!-- ========================================================================
         ESTADO 1: SCANNING (Interfaz de Captura)
         ======================================================================== -->
    <div v-if="uiState === 'SCANNING'" class="scanning-state">
      <!-- Simulación de Cámara -->
      <v-card color="black" height="300" class="mb-4 d-flex align-center justify-center">
        <div class="text-center">
          <v-icon size="80" color="white">mdi-camera</v-icon>
          <p class="text-white mt-4 text-h6">Escáner Activo</p>
          <p class="text-grey-lighten-1">Apunta al código QR</p>
        </div>
      </v-card>

      <!-- Input Manual -->
      <v-text-field
        v-model="manualCode"
        label="Ingresar código manualmente"
        prepend-inner-icon="mdi-barcode-scan"
        variant="outlined"
        density="comfortable"
        hint="Ingresa INV-XX-XXXXXX (Activo) o LOC-XXXXXX (Ubicación)"
        persistent-hint
        @keyup.enter="handleManualSubmit"
      >
        <template v-slot:append>
          <v-btn
            color="primary"
            variant="flat"
            @click="handleManualSubmit"
            :disabled="!manualCode"
          >
            Buscar
          </v-btn>
        </template>
      </v-text-field>

      <!-- Contexto Rápido: Últimos 5 Movimientos Personales -->
      <v-card class="mt-6" variant="outlined">
        <v-card-title class="text-subtitle-1">
          <v-icon start>mdi-history</v-icon>
          Mis Últimos Movimientos
        </v-card-title>

        <v-card-text>
          <v-list v-if="!loadingMovimientos && ultimosMovimientos.length > 0" density="compact">
            <v-list-item
              v-for="mov in ultimosMovimientos.slice(0, 5)"
              :key="mov.id"
              :title="`${mov.activo?.marca || ''} ${mov.activo?.modelo || ''}`"
              :subtitle="`${mov.tipo_movimiento} • ${formatTimeAgo(mov.fecha_movimiento)}`"
            >
              <template v-slot:prepend>
                <v-avatar :color="getMovementColor(mov.tipo_movimiento)" size="small">
                  <v-icon size="small">{{ getMovementIcon(mov.tipo_movimiento) }}</v-icon>
                </v-avatar>
              </template>
            </v-list-item>
          </v-list>

          <div v-else-if="loadingMovimientos" class="text-center py-4">
            <v-progress-circular indeterminate color="primary"></v-progress-circular>
          </div>

          <div v-else class="text-center py-4 text-grey">
            <v-icon size="48">mdi-inbox</v-icon>
            <p class="mt-2">No hay movimientos recientes</p>
          </div>
        </v-card-text>
      </v-card>
    </div>

    <!-- ========================================================================
         ESTADO 2: VIEW_ASSET (Detalle de Activo)
         ======================================================================== -->
    <div v-else-if="uiState === 'VIEW_ASSET'" class="view-asset-state">
      <!-- Navegación -->
      <v-btn
        variant="text"
        prepend-icon="mdi-arrow-left"
        class="mb-4"
        @click="resetToScanning"
      >
        Volver al Escáner
      </v-btn>

      <!-- Info Card del Activo -->
      <v-card v-if="currentAsset" class="mb-4">
        <v-card-title class="bg-primary text-white">
          <v-icon start>mdi-package-variant</v-icon>
          Información del Activo
        </v-card-title>

        <v-card-text class="pt-4">
          <v-row dense>
            <v-col cols="12">
              <div class="text-h6 font-weight-bold">
                {{ currentAsset.marca }} {{ currentAsset.modelo }}
              </div>
            </v-col>

            <v-col cols="12" sm="6">
              <div class="text-caption text-grey">Código de Inventario</div>
              <div class="font-weight-medium">{{ currentAsset.codigo_inventario }}</div>
            </v-col>

            <v-col cols="12" sm="6">
              <div class="text-caption text-grey">Número de Serie</div>
              <div class="font-weight-medium">{{ currentAsset.numero_serie || 'N/A' }}</div>
            </v-col>

            <v-col cols="12" sm="6">
              <div class="text-caption text-grey">Tipo de Equipo</div>
              <div class="font-weight-medium">{{ currentAsset.tipo?.nombre_tipo || 'N/A' }}</div>
            </v-col>

            <v-col cols="12" sm="6">
              <div class="text-caption text-grey">Estado</div>
              <v-chip size="small" :color="getEstadoColor(currentAsset.estado?.nombre_estado)">
                {{ currentAsset.estado?.nombre_estado || 'N/A' }}
              </v-chip>
            </v-col>

            <v-col cols="12">
              <div class="text-caption text-grey">Ubicación Actual</div>
              <div class="font-weight-medium">
                {{ currentAsset.ubicacion_actual?.nombre_ubicacion || 'N/A' }}
                <span v-if="currentAsset.ubicacion_actual?.departamento" class="text-grey">
                  ({{ currentAsset.ubicacion_actual.departamento.nombre_departamento }})
                </span>
              </div>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>

      <!-- Acciones Críticas -->
      <v-row dense>
        <v-col cols="12">
          <v-btn
            color="primary"
            variant="flat"
            block
            size="large"
            prepend-icon="mdi-swap-horizontal"
            @click="generarMovimiento"
          >
            Generar Movimiento
          </v-btn>
        </v-col>

        <v-col cols="12">
          <v-btn
            color="secondary"
            variant="flat"
            block
            size="large"
            prepend-icon="mdi-pencil"
            @click="actualizarActivo"
          >
            Actualizar Activo
          </v-btn>
        </v-col>

        <v-col cols="12">
          <v-btn
            color="info"
            variant="outlined"
            block
            size="large"
            prepend-icon="mdi-history"
            @click="verHistorial"
          >
            Ver Historial
          </v-btn>
        </v-col>
      </v-row>
    </div>

    <!-- ========================================================================
         ESTADO 3: VIEW_LOCATION (Inventario de Ubicación)
         ======================================================================== -->
    <div v-else-if="uiState === 'VIEW_LOCATION'" class="view-location-state">
      <!-- Cabecera con Botón de Impresión -->
      <div class="d-flex align-center mb-4">
        <v-btn
          variant="text"
          icon
          @click="resetToScanning"
        >
          <v-icon>mdi-arrow-left</v-icon>
        </v-btn>

        <div class="flex-grow-1 ml-2">
          <div class="text-h6 font-weight-bold">{{ currentLocation?.nombre_ubicacion }}</div>
          <div class="text-caption text-grey">{{ currentLocation?.codigo_qr }}</div>
        </div>

        <v-btn
          variant="tonal"
          color="secondary"
          prepend-icon="mdi-printer"
          @click="abrirModalImpresion"
        >
          Imprimir Etiquetas
        </v-btn>
      </div>

      <!-- Tabs: Inventario y Movimientos -->
      <v-tabs v-model="locationTab" bg-color="primary" dark class="mb-4">
        <v-tab value="inventario">
          <v-icon start>mdi-package-variant-closed</v-icon>
          Inventario ({{ activosDeUbicacion.length }})
        </v-tab>
        <v-tab value="movimientos">
          <v-icon start>mdi-swap-horizontal</v-icon>
          Movimientos
        </v-tab>
      </v-tabs>

      <v-window v-model="locationTab">
        <!-- TAB 1: INVENTARIO (Tabla Móvil) -->
        <v-window-item value="inventario">
          <!-- Filtros -->
          <v-row dense class="mb-4">
            <v-col cols="12" md="8">
              <v-text-field
                v-model="filtroInventario.busqueda"
                label="Buscar activo"
                prepend-inner-icon="mdi-magnify"
                variant="outlined"
                density="compact"
                clearable
              ></v-text-field>
            </v-col>

            <v-col cols="12" md="4">
              <v-select
                v-model="filtroInventario.tipo"
                :items="tiposEquipo"
                item-title="nombre_tipo"
                item-value="id"
                label="Tipo de Equipo"
                variant="outlined"
                density="compact"
                clearable
              ></v-select>
            </v-col>
          </v-row>

          <!-- Tabla Móvil con Diseño de 2 Líneas -->
          <v-data-table
            :headers="headersInventario"
            :items="activosFiltrados"
            :loading="loadingActivos"
            :items-per-page="10"
            class="elevation-1"
            @click:row="handleActivoClick"
          >
            <template v-slot:loading>
              <v-skeleton-loader type="table-row@10"></v-skeleton-loader>
            </template>

            <template v-slot:no-data>
              <div class="text-center py-8">
                <v-icon size="64" color="grey">mdi-package-variant-closed-remove</v-icon>
                <p class="text-h6 mt-4">No hay activos en esta ubicación</p>
              </div>
            </template>

            <!-- Diseño Móvil de 2 Líneas -->
            <template v-slot:item="{ item }">
              <tr @click="handleActivoClick(null, { item })" style="cursor: pointer;">
                <td colspan="4" class="pa-3">
                  <div class="mobile-row">
                    <!-- Línea 1: Nombre + Estado -->
                    <div class="d-flex align-center justify-space-between mb-1">
                      <span class="font-weight-bold">{{ item.marca }} {{ item.modelo }}</span>
                      <v-chip size="x-small" :color="getEstadoColor(item.estado?.nombre_estado)">
                        {{ item.estado?.nombre_estado }}
                      </v-chip>
                    </div>

                    <!-- Línea 2: Código | Marca | Tipo -->
                    <div class="text-caption text-grey">
                      {{ item.codigo_inventario }} | {{ item.marca }} | {{ item.tipo?.nombre_tipo }}
                    </div>
                  </div>
                </td>
              </tr>
            </template>
          </v-data-table>
        </v-window-item>

        <!-- TAB 2: MOVIMIENTOS -->
        <v-window-item value="movimientos">
          <v-card variant="outlined">
            <v-card-text class="text-center py-8">
              <v-icon size="64" color="grey">mdi-swap-horizontal</v-icon>
              <p class="text-h6 mt-4">Historial de Movimientos</p>
              <p class="text-grey">Funcionalidad en desarrollo</p>
            </v-card-text>
          </v-card>
        </v-window-item>
      </v-window>
    </div>

    <!-- Snackbar para Errores -->
    <v-snackbar
      v-model="showError"
      color="error"
      :timeout="3000"
      location="top"
    >
      {{ errorMessage }}
      <template v-slot:actions>
        <v-btn variant="text" @click="showError = false">Cerrar</v-btn>
      </template>
    </v-snackbar>

    <!-- ========================================================================
         MODAL DE IMPRESIÓN - GENERACIÓN DE QR DEL LADO DEL CLIENTE
         ======================================================================== -->
    <v-dialog v-model="dialogImpresion" fullscreen transition="dialog-bottom-transition">
      <v-card>
        <!-- App Bar del Modal -->
        <v-app-bar color="secondary" dark>
          <v-btn icon @click="cerrarModalImpresion">
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-toolbar-title>Imprimir Etiquetas QR</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="imprimirEtiquetas">
            <v-icon start>mdi-printer</v-icon>
            Imprimir Ahora
          </v-btn>
        </v-app-bar>

        <!-- Contenido del Modal -->
        <v-card-text class="pa-4">
          <!-- Sección de Selección -->
          <div class="selection-section mb-6">
            <h3 class="text-h6 mb-3">
              <v-icon start color="primary">mdi-checkbox-multiple-marked</v-icon>
              Seleccionar Activos para Imprimir
            </h3>

            <v-card variant="outlined" class="mb-4">
              <v-card-text>
                <div class="d-flex align-center justify-space-between mb-3">
                  <div>
                    <v-checkbox
                      v-model="seleccionarTodos"
                      label="Seleccionar Todos"
                      hide-details
                      @change="toggleSeleccionarTodos"
                    ></v-checkbox>
                  </div>
                  <v-chip color="primary" variant="tonal">
                    {{ activosSeleccionados.length }} de {{ activosDeUbicacion.length }} seleccionados
                  </v-chip>
                </div>

                <v-divider class="mb-3"></v-divider>

                <!-- Lista de Activos con Checkboxes -->
                <div class="activos-list" style="max-height: 300px; overflow-y: auto;">
                  <v-checkbox
                    v-for="activo in activosDeUbicacion"
                    :key="activo.id"
                    v-model="activosSeleccionados"
                    :value="activo.id"
                    hide-details
                    class="mb-2"
                  >
                    <template v-slot:label>
                      <div class="d-flex align-center justify-space-between" style="width: 100%;">
                        <div>
                          <span class="font-weight-bold">{{ activo.marca }} {{ activo.modelo }}</span>
                          <br>
                          <span class="text-caption text-grey">{{ activo.codigo_inventario }}</span>
                        </div>
                        <v-chip size="x-small" :color="getEstadoColor(activo.estado?.nombre_estado)">
                          {{ activo.estado?.nombre_estado }}
                        </v-chip>
                      </div>
                    </template>
                  </v-checkbox>
                </div>
              </v-card-text>
            </v-card>
          </div>

          <!-- Sección de Vista Previa -->
          <div class="preview-section">
            <h3 class="text-h6 mb-3">
              <v-icon start color="secondary">mdi-eye</v-icon>
              Vista Previa de Etiquetas
            </h3>

            <v-alert v-if="activosSeleccionados.length === 0" type="info" variant="tonal" class="mb-4">
              <v-icon start>mdi-information</v-icon>
              Selecciona al menos un activo para ver la vista previa.
            </v-alert>

            <!-- Área de Impresión (Oculta en pantalla, visible en impresión) -->
            <div id="print-area" class="print-area">
              <div class="labels-grid">
                <div
                  v-for="activoId in activosSeleccionados"
                  :key="activoId"
                  class="label-item"
                >
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
                    </div>

                    <!-- Código Vertical (Derecha) -->
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
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
/**
 * ============================================================================
 * SCANNER VIEW - STATE MACHINE IMPLEMENTATION
 * ============================================================================
 *
 * Implementa un patrón de State Machine con 3 estados:
 * - SCANNING: Interfaz de captura
 * - VIEW_ASSET: Detalle de activo
 * - VIEW_LOCATION: Inventario de ubicación
 *
 * Sin navegación entre rutas para mejor UX móvil.
 */

import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import apiClient from '@/services/api'
import QRCode from 'qrcode'

// ============================================================================
// COMPOSABLES
// ============================================================================

const router = useRouter()
const authStore = useAuthStore()

// ============================================================================
// STATE MACHINE - ESTADOS
// ============================================================================

const uiState = ref('SCANNING') // 'SCANNING' | 'VIEW_ASSET' | 'VIEW_LOCATION'

// ============================================================================
// STATE - SCANNING
// ============================================================================

const manualCode = ref('')
const ultimosMovimientos = ref([])
const loadingMovimientos = ref(false)

// ============================================================================
// STATE - VIEW_ASSET
// ============================================================================

const currentAsset = ref(null)

// ============================================================================
// STATE - VIEW_LOCATION
// ============================================================================

const currentLocation = ref(null)
const activosDeUbicacion = ref([])
const locationTab = ref('inventario')
const loadingActivos = ref(false)
const tiposEquipo = ref([])

const filtroInventario = ref({
  busqueda: '',
  tipo: null
})

// ============================================================================
// STATE - GENERAL
// ============================================================================

const showError = ref(false)
const errorMessage = ref('')
const dialogImpresion = ref(false)

// ============================================================================
// STATE - MODAL DE IMPRESIÓN
// ============================================================================

const activosSeleccionados = ref([])
const seleccionarTodos = ref(false)
const qrCodes = ref({}) // { 'A-001': 'data:image/png;base64,...', ... }

// ============================================================================
// COMPUTED - TABLA INVENTARIO
// ============================================================================

const headersInventario = computed(() => [
  { title: 'Activo', key: 'nombre', sortable: true },
  { title: 'Código', key: 'codigo_inventario', sortable: true },
  { title: 'Marca', key: 'marca', sortable: true },
  { title: 'Tipo', key: 'tipo', sortable: false }
])

const activosFiltrados = computed(() => {
  let resultado = activosDeUbicacion.value

  if (filtroInventario.value.busqueda) {
    const busqueda = filtroInventario.value.busqueda.toLowerCase()
    resultado = resultado.filter(a =>
      a.marca?.toLowerCase().includes(busqueda) ||
      a.modelo?.toLowerCase().includes(busqueda) ||
      a.codigo_inventario?.toLowerCase().includes(busqueda)
    )
  }

  if (filtroInventario.value.tipo) {
    resultado = resultado.filter(a => a.tipo?.id === filtroInventario.value.tipo)
  }

  return resultado
})

// ============================================================================
// MÉTODOS - STATE MACHINE TRANSITIONS
// ============================================================================

function resetToScanning() {
  uiState.value = 'SCANNING'
  currentAsset.value = null
  currentLocation.value = null
  activosDeUbicacion.value = []
  manualCode.value = ''
}

async function transitionToAsset(code) {
  try {
    // Buscar activo por código
    const response = await apiClient.get('/api/activos/', {
      params: { search: code }
    })

    const activos = response.data.results || response.data

    if (activos.length === 0) {
      showErrorMessage(`No se encontró el activo con código: ${code}`)
      return
    }

    currentAsset.value = activos[0]
    uiState.value = 'VIEW_ASSET'
  } catch (error) {
    console.error('Error al cargar activo:', error)
    showErrorMessage('Error al cargar la información del activo')
  }
}

async function transitionToLocation(code) {
  try {
    // Buscar ubicación por código QR
    const response = await apiClient.get('/api/ubicaciones/', {
      params: { search: code }
    })

    const ubicaciones = response.data.results || response.data

    if (ubicaciones.length === 0) {
      showErrorMessage(`No se encontró la ubicación con código: ${code}`)
      return
    }

    currentLocation.value = ubicaciones[0]

    // Cargar activos de la ubicación
    await loadActivosDeUbicacion(currentLocation.value.id)

    uiState.value = 'VIEW_LOCATION'
  } catch (error) {
    console.error('Error al cargar ubicación:', error)
    showErrorMessage('Error al cargar la información de la ubicación')
  }
}

// ============================================================================
// MÉTODOS - SCANNING STATE
// ============================================================================

function handleManualSubmit() {
  const code = manualCode.value.trim().toUpperCase()

  if (!code) {
    showErrorMessage('Por favor ingresa un código')
    return
  }

  // Evaluar prefijo según formato del backend
  if (code.startsWith('INV-')) {
    transitionToAsset(code)
  } else if (code.startsWith('LOC-')) {
    transitionToLocation(code)
  } else {
    showErrorMessage('Código inválido. Debe comenzar con INV- (Activo) o LOC- (Ubicación)')
  }
}

async function fetchUltimosMovimientos() {
  loadingMovimientos.value = true
  try {
    const response = await apiClient.get('/api/historial-movimientos/', {
      params: {
        ordering: '-fecha_movimiento',
        page_size: 5,
        usuario_registra: authStore.user?.id
      }
    })

    ultimosMovimientos.value = response.data.results || response.data
  } catch (error) {
    console.error('Error al cargar movimientos:', error)
  } finally {
    loadingMovimientos.value = false
  }
}

// ============================================================================
// MÉTODOS - VIEW_ASSET STATE
// ============================================================================

function generarMovimiento() {
  if (!currentAsset.value) return

  router.push({
    name: 'confirm-asset',
    params: { id: currentAsset.value.id }
  })
}

function actualizarActivo() {
  if (!currentAsset.value) return

  router.push({
    name: 'technician-edit-search',
    query: { codigo: currentAsset.value.codigo_inventario }
  })
}

function verHistorial() {
  if (!currentAsset.value) return

  router.push({
    name: 'technician-history',
    query: { activo: currentAsset.value.id }
  })
}

// ============================================================================
// MÉTODOS - VIEW_LOCATION STATE
// ============================================================================

async function loadActivosDeUbicacion(ubicacionId) {
  loadingActivos.value = true
  try {
    const response = await apiClient.get('/api/activos/', {
      params: {
        ubicacion_actual: ubicacionId
      }
    })

    activosDeUbicacion.value = response.data.results || response.data
  } catch (error) {
    console.error('Error al cargar activos de ubicación:', error)
    showErrorMessage('Error al cargar los activos de la ubicación')
  } finally {
    loadingActivos.value = false
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

function handleActivoClick(event, { item }) {
  // Flujo circular: desde ubicación → activo
  currentAsset.value = item
  uiState.value = 'VIEW_ASSET'
}

async function abrirModalImpresion() {
  // Resetear selección
  activosSeleccionados.value = []
  seleccionarTodos.value = false
  qrCodes.value = {}

  // Abrir modal
  dialogImpresion.value = true

  // Generar QR codes para todos los activos de la ubicación
  await generarQRCodes()
}

function cerrarModalImpresion() {
  dialogImpresion.value = false
  activosSeleccionados.value = []
  seleccionarTodos.value = false
  qrCodes.value = {}
}

function toggleSeleccionarTodos() {
  if (seleccionarTodos.value) {
    activosSeleccionados.value = activosDeUbicacion.value.map(a => a.id)
  } else {
    activosSeleccionados.value = []
  }
}

function getActivoById(id) {
  return activosDeUbicacion.value.find(a => a.id === id)
}

async function generarQRCodes() {
  // Generar QR codes para todos los activos
  for (const activo of activosDeUbicacion.value) {
    try {
      const qrDataUrl = await QRCode.toDataURL(activo.codigo_inventario, {
        width: 200,
        margin: 1,
        color: {
          dark: '#000000',
          light: '#FFFFFF'
        }
      })
      qrCodes.value[activo.codigo_inventario] = qrDataUrl
    } catch (error) {
      console.error(`Error generando QR para ${activo.codigo_inventario}:`, error)
    }
  }
}

function imprimirEtiquetas() {
  if (activosSeleccionados.value.length === 0) {
    showErrorMessage('Debes seleccionar al menos un activo para imprimir')
    return
  }

  // Ejecutar impresión
  window.print()
}

// ============================================================================
// MÉTODOS - UTILIDADES
// ============================================================================

function showErrorMessage(message) {
  errorMessage.value = message
  showError.value = true
}

function formatTimeAgo(fecha) {
  if (!fecha) return ''

  const ahora = new Date()
  const fechaMovimiento = new Date(fecha)
  const diffMs = ahora - fechaMovimiento
  const diffMinutos = Math.floor(diffMs / 60000)

  if (diffMinutos < 1) return 'Hace un momento'
  if (diffMinutos < 60) return `Hace ${diffMinutos} min`

  const diffHoras = Math.floor(diffMinutos / 60)
  if (diffHoras < 24) return `Hace ${diffHoras} h`

  const diffDias = Math.floor(diffHoras / 24)
  return `Hace ${diffDias} día${diffDias > 1 ? 's' : ''}`
}

function getMovementColor(tipo) {
  const colores = {
    'TRASLADO': 'blue',
    'ASIGNACION': 'green',
    'DEVOLUCION': 'orange',
    'MANTENIMIENTO': 'purple',
    'BAJA': 'red'
  }
  return colores[tipo] || 'grey'
}

function getMovementIcon(tipo) {
  const iconos = {
    'TRASLADO': 'mdi-swap-horizontal',
    'ASIGNACION': 'mdi-account-arrow-right',
    'DEVOLUCION': 'mdi-arrow-u-left-top',
    'MANTENIMIENTO': 'mdi-wrench',
    'BAJA': 'mdi-delete'
  }
  return iconos[tipo] || 'mdi-help-circle'
}

function getEstadoColor(estado) {
  const colores = {
    'Operativo': 'success',
    'En Mantenimiento': 'warning',
    'Fuera de Servicio': 'error',
    'En Reparación': 'orange',
    'Dado de Baja': 'grey'
  }
  return colores[estado] || 'info'
}

// ============================================================================
// WATCHERS
// ============================================================================

// Sincronizar checkbox "Seleccionar Todos" con la selección real
watch(activosSeleccionados, (newVal) => {
  if (newVal.length === activosDeUbicacion.value.length && activosDeUbicacion.value.length > 0) {
    seleccionarTodos.value = true
  } else {
    seleccionarTodos.value = false
  }
})

// ============================================================================
// LIFECYCLE HOOKS
// ============================================================================

onMounted(async () => {
  await Promise.all([
    fetchUltimosMovimientos(),
    fetchTiposEquipo()
  ])
})
</script>

<style scoped>
/* ============================================================================
   CONTENEDOR PRINCIPAL
   ============================================================================ */

.scanner-view {
  min-height: calc(100vh - 112px);
  background: #f5f7fa;
  padding: 1rem;
  padding-bottom: 80px; /* Espacio para bottom navigation */
}

/* ============================================================================
   ESTADO: SCANNING
   ============================================================================ */

.scanning-state {
  max-width: 600px;
  margin: 0 auto;
}

/* ============================================================================
   ESTADO: VIEW_ASSET
   ============================================================================ */

.view-asset-state {
  max-width: 800px;
  margin: 0 auto;
}

/* ============================================================================
   ESTADO: VIEW_LOCATION
   ============================================================================ */

.view-location-state {
  max-width: 1200px;
  margin: 0 auto;
}

/* ============================================================================
   TABLA MÓVIL - DISEÑO DE 2 LÍNEAS
   ============================================================================ */

.mobile-row {
  width: 100%;
}

/* ============================================================================
   MODAL DE IMPRESIÓN - SECCIÓN DE SELECCIÓN
   ============================================================================ */

.selection-section {
  /* Estilos para la sección de selección */
}

.activos-list {
  /* Estilos para la lista de activos */
}

/* ============================================================================
   MODAL DE IMPRESIÓN - ÁREA DE IMPRESIÓN
   ============================================================================ */

.print-area {
  background: #ffffff;
  padding: 1rem;
  border: 2px dashed #ccc;
  border-radius: 8px;
}

.labels-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  padding: 1rem;
}

.label-item {
  border: 2px dashed #333;
  padding: 0.5rem;
  background: #ffffff;
  page-break-inside: avoid;
  break-inside: avoid;
}

.label-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  min-height: 80px;
}

.label-nombre {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.nombre-text {
  font-size: 0.9rem;
  font-weight: bold;
  line-height: 1.2;
  margin-bottom: 0.25rem;
}

.tipo-text {
  font-size: 0.75rem;
  color: #666;
}

.label-qr {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.qr-image {
  width: 80px;
  height: 80px;
  display: block;
}

.label-codigo-vertical {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  writing-mode: vertical-rl;
  text-orientation: mixed;
  transform: rotate(180deg);
  padding: 0.25rem;
}

.codigo-vertical-text {
  font-size: 0.7rem;
  font-weight: bold;
  letter-spacing: 0.05em;
  white-space: nowrap;
}

/* ============================================================================
   ESTILOS DE IMPRESIÓN - @media print
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
    background: white;
    padding: 0;
    border: none;
  }

  .labels-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.5rem;
    padding: 0.5rem;
  }

  .label-item {
    border: 2px dashed #333;
    padding: 0.5rem;
    background: white;
    page-break-inside: avoid;
    break-inside: avoid;
  }

  /* Ajustar márgenes de página */
  @page {
    margin: 0.5cm;
    size: A4;
  }
}

/* ============================================================================
   RESPONSIVE
   ============================================================================ */

@media (max-width: 600px) {
  .scanner-view {
    padding: 0.5rem;
  }

  .labels-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 400px) {
  .labels-grid {
    grid-template-columns: 1fr;
  }
}
</style>


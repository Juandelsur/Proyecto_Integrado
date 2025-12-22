<!--
  ============================================================================
  TECNICO SCAN VIEW - DISEÑO MEJORADO CON GLASSMORPHISM Y ANIMACIONES
  ============================================================================
-->

<template>
  <div class="scanner-view">
    <!-- ========================================================================
         ESTADO 1: SCANNING (Interfaz de Captura) - MEJORADO
         ======================================================================== -->
    <div v-if="uiState === 'SCANNING'" class="scanning-state">
      <!-- Hero Section con Glassmorphism -->
      <div class="hero-section">
        <div class="hero-content">
          <v-icon size="64" color="primary" class="mb-4">mdi-qrcode-scan</v-icon>
          <h1 class="text-h4 font-weight-bold mb-2">Escanear Activo</h1>
          <p class="text-body-1 text-medium-emphasis">
            Apunta la cámara al código QR o ingresa el código manualmente
          </p>
        </div>
      </div>

      <!-- Escáner QR con Card Mejorado -->
      <v-card class="scanner-card glass-card mb-6" elevation="0">
        <v-card-text class="pa-6">
          <QRScanner
            @scan-success="handleQRScanSuccess"
            @scan-error="handleQRScanError"
          />
        </v-card-text>
      </v-card>

      <!-- Input Manual Mejorado -->
      <v-card class="glass-card mb-6" elevation="0">
        <v-card-text class="pa-6">
          <div class="text-subtitle-2 mb-3 d-flex align-center">
            <v-icon start color="primary">mdi-keyboard</v-icon>
            Ingreso Manual
          </div>
          
          <v-text-field
            v-model="manualCode"
            label="Código de activo o ubicación"
            prepend-inner-icon="mdi-barcode-scan"
            variant="outlined"
            density="comfortable"
            hint="Formato: INV-XX-XXXXXX o LOC-XXXXXX"
            persistent-hint
            @keyup.enter="handleManualSubmit"
            class="mb-2"
          >
            <template v-slot:append-inner>
              <v-fade-transition>
                <v-btn
                  v-if="manualCode"
                  icon="mdi-close-circle"
                  variant="text"
                  size="small"
                  @click="manualCode = ''"
                ></v-btn>
              </v-fade-transition>
            </template>
          </v-text-field>

          <v-btn
            color="primary"
            variant="elevated"
            block
            size="large"
            prepend-icon="mdi-magnify"
            @click="handleManualSubmit"
            :disabled="!manualCode"
            class="mt-2"
          >
            Buscar
          </v-btn>
        </v-card-text>
      </v-card>

      <!-- Últimos Movimientos con Diseño Mejorado -->
      <v-card class="glass-card" elevation="0">
        <v-card-title class="d-flex align-center pa-6 pb-4">
          <v-icon start color="primary">mdi-history</v-icon>
          <span class="text-h6">Actividad Reciente</span>
          <v-spacer></v-spacer>
          <v-chip size="small" color="primary" variant="tonal">
            {{ ultimosMovimientos.length }}
          </v-chip>
        </v-card-title>

        <v-card-text class="pa-0">
          <v-list v-if="!loadingMovimientos && ultimosMovimientos.length > 0" class="bg-transparent">
            <v-list-item
              v-for="(mov, index) in ultimosMovimientos.slice(0, 5)"
              :key="mov.id"
              class="movement-item"
              :class="{ 'border-t': index > 0 }"
            >
              <template v-slot:prepend>
                <v-avatar 
                  :color="getMovementColor(mov.tipo_movimiento)" 
                  size="48"
                  class="movement-avatar"
                >
                  <v-icon size="24" color="white">
                    {{ getMovementIcon(mov.tipo_movimiento) }}
                  </v-icon>
                </v-avatar>
              </template>

              <v-list-item-title class="font-weight-medium mb-1">
                {{ mov.activo?.marca || '' }} {{ mov.activo?.modelo || '' }}
              </v-list-item-title>

              <v-list-item-subtitle class="d-flex align-center gap-2">
                <v-chip size="x-small" :color="getMovementColor(mov.tipo_movimiento)" variant="tonal">
                  {{ mov.tipo_movimiento }}
                </v-chip>
                <span class="text-caption">{{ formatTimeAgo(mov.fecha_movimiento) }}</span>
              </v-list-item-subtitle>
            </v-list-item>
          </v-list>

          <div v-else-if="loadingMovimientos" class="text-center py-12">
            <v-progress-circular indeterminate color="primary" size="48"></v-progress-circular>
            <p class="text-body-2 mt-4 text-medium-emphasis">Cargando actividad...</p>
          </div>

          <div v-else class="text-center py-12">
            <v-icon size="64" color="grey-lighten-1">mdi-inbox-outline</v-icon>
            <p class="text-body-1 mt-4 text-medium-emphasis">No hay movimientos recientes</p>
          </div>
        </v-card-text>
      </v-card>
    </div>

    <!-- ========================================================================
         ESTADO 2: VIEW_ASSET (Detalle de Activo) - MEJORADO
         ======================================================================== -->
    <div v-else-if="uiState === 'VIEW_ASSET'" class="view-asset-state">
      <!-- Header con Navegación -->
      <div class="d-flex align-center mb-6">
        <v-btn
          icon="mdi-arrow-left"
          variant="text"
          size="large"
          @click="resetToScanning"
        ></v-btn>
        <div class="ml-3">
          <div class="text-overline text-primary">Detalle del Activo</div>
          <div class="text-h6 font-weight-bold">{{ currentAsset?.codigo_inventario }}</div>
        </div>
      </div>

      <!-- Card Principal del Activo con Gradiente -->
      <v-card v-if="currentAsset" class="asset-card mb-6" elevation="0">
        <div class="asset-header">
          <div class="asset-header-content pa-6">
            <v-icon size="48" color="white" class="mb-3">mdi-package-variant</v-icon>
            <h2 class="text-h5 font-weight-bold mb-1">
              {{ currentAsset.marca }} {{ currentAsset.modelo }}
            </h2>
            <div class="text-body-2 opacity-90">
              {{ currentAsset.tipo?.nombre_tipo || 'Sin tipo' }}
            </div>
          </div>
        </div>

        <v-card-text class="pa-6">
          <v-row dense>
            <v-col cols="6" sm="4">
              <div class="info-block">
                <v-icon size="20" class="mb-2" color="primary">mdi-barcode</v-icon>
                <div class="text-caption text-medium-emphasis">Código</div>
                <div class="text-body-1 font-weight-bold">{{ currentAsset.codigo_inventario }}</div>
              </div>
            </v-col>

            <v-col cols="6" sm="4">
              <div class="info-block">
                <v-icon size="20" class="mb-2" color="primary">mdi-identifier</v-icon>
                <div class="text-caption text-medium-emphasis">Serie</div>
                <div class="text-body-1 font-weight-bold">{{ currentAsset.numero_serie || 'N/A' }}</div>
              </div>
            </v-col>

            <v-col cols="6" sm="4">
              <div class="info-block">
                <v-icon size="20" class="mb-2" color="primary">mdi-state-machine</v-icon>
                <div class="text-caption text-medium-emphasis">Estado</div>
                <v-chip 
                  size="small" 
                  :color="getEstadoColor(currentAsset.estado?.nombre_estado)"
                  class="mt-1"
                >
                  {{ currentAsset.estado?.nombre_estado || 'N/A' }}
                </v-chip>
              </div>
            </v-col>

            <v-col cols="12">
              <v-divider class="my-4"></v-divider>
              <div class="info-block">
                <v-icon size="20" class="mb-2" color="primary">mdi-map-marker</v-icon>
                <div class="text-caption text-medium-emphasis">Ubicación Actual</div>
                <div class="text-body-1 font-weight-bold">
                  {{ currentAsset.ubicacion_actual?.nombre_ubicacion || 'N/A' }}
                </div>
                <div v-if="currentAsset.ubicacion_actual?.departamento" class="text-caption text-medium-emphasis mt-1">
                  {{ currentAsset.ubicacion_actual.departamento.nombre_departamento }}
                </div>
              </div>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>

      <!-- Acciones con Diseño Mejorado -->
      <div class="actions-grid">
        <v-card class="action-card" @click="generarMovimiento" elevation="0">
          <v-card-text class="text-center pa-6">
            <div class="action-icon-wrapper mb-3">
              <v-icon size="32" color="primary">mdi-swap-horizontal</v-icon>
            </div>
            <div class="text-subtitle-1 font-weight-bold">Generar Movimiento</div>
            <div class="text-caption text-medium-emphasis">Trasladar o asignar</div>
          </v-card-text>
        </v-card>

        <v-card class="action-card" @click="actualizarActivo" elevation="0">
          <v-card-text class="text-center pa-6">
            <div class="action-icon-wrapper mb-3">
              <v-icon size="32" color="secondary">mdi-pencil</v-icon>
            </div>
            <div class="text-subtitle-1 font-weight-bold">Actualizar</div>
            <div class="text-caption text-medium-emphasis">Editar información</div>
          </v-card-text>
        </v-card>

        <v-card class="action-card" @click="verHistorial" elevation="0">
          <v-card-text class="text-center pa-6">
            <div class="action-icon-wrapper mb-3">
              <v-icon size="32" color="info">mdi-history</v-icon>
            </div>
            <div class="text-subtitle-1 font-weight-bold">Historial</div>
            <div class="text-caption text-medium-emphasis">Ver movimientos</div>
          </v-card-text>
        </v-card>
      </div>
    </div>

    <!-- ========================================================================
         ESTADO 3: VIEW_LOCATION (Inventario de Ubicación) - MEJORADO
         ======================================================================== -->
    <div v-else-if="uiState === 'VIEW_LOCATION'" class="view-location-state">
      <!-- Header Mejorado -->
      <div class="location-header glass-card mb-6">
        <div class="d-flex align-center pa-6">
          <v-btn
            icon="mdi-arrow-left"
            variant="text"
            size="large"
            @click="resetToScanning"
          ></v-btn>

          <div class="flex-grow-1 ml-3">
            <div class="text-overline text-primary">Ubicación</div>
            <div class="text-h6 font-weight-bold">{{ currentLocation?.nombre_ubicacion }}</div>
            <div class="text-caption text-medium-emphasis">{{ currentLocation?.codigo_qr }}</div>
          </div>

          <v-btn
            icon="mdi-printer"
            variant="tonal"
            color="primary"
            size="large"
            @click="abrirModalImpresion"
          ></v-btn>
        </div>
      </div>

      <!-- Tabs Mejorados -->
      <v-tabs v-model="locationTab" class="mb-6" color="primary" density="compact">
        <v-tab value="inventario" class="text-none">
          <v-icon start size="20">mdi-package-variant-closed</v-icon>
          Inventario
          <v-chip size="x-small" class="ml-2" color="primary" variant="tonal">
            {{ activosDeUbicacion.length }}
          </v-chip>
        </v-tab>
        <v-tab value="movimientos" class="text-none">
          <v-icon start size="20">mdi-swap-horizontal</v-icon>
          Movimientos
        </v-tab>
      </v-tabs>

      <v-window v-model="locationTab">
        <!-- TAB 1: INVENTARIO -->
        <v-window-item value="inventario">
          <v-card class="glass-card mb-4" elevation="0">
            <v-card-text class="pa-4">
              <v-row dense>
                <v-col cols="12" md="8">
                  <v-text-field
                    v-model="filtroInventario.busqueda"
                    label="Buscar activo"
                    prepend-inner-icon="mdi-magnify"
                    variant="outlined"
                    density="compact"
                    clearable
                    hide-details
                  ></v-text-field>
                </v-col>

                <v-col cols="12" md="4">
                  <v-select
                    v-model="filtroInventario.tipo"
                    :items="tiposEquipo"
                    item-title="nombre_tipo"
                    item-value="id"
                    label="Tipo"
                    variant="outlined"
                    density="compact"
                    clearable
                    hide-details
                  ></v-select>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>

          <!-- Lista de Activos Mejorada -->
          <div v-if="loadingActivos" class="text-center py-12">
            <v-progress-circular indeterminate color="primary" size="48"></v-progress-circular>
          </div>

          <div v-else-if="activosFiltrados.length === 0" class="text-center py-12">
            <v-icon size="64" color="grey-lighten-1">mdi-package-variant-closed-remove</v-icon>
            <p class="text-body-1 mt-4 text-medium-emphasis">No hay activos en esta ubicación</p>
          </div>

          <v-card 
            v-else
            v-for="activo in activosFiltrados" 
            :key="activo.id"
            class="asset-list-item glass-card mb-3"
            @click="handleActivoClick(null, { item: activo })"
            elevation="0"
          >
            <v-card-text class="pa-4">
              <div class="d-flex align-center">
                <v-avatar 
                  :color="getEstadoColor(activo.estado?.nombre_estado)" 
                  size="48"
                  class="mr-4"
                >
                  <v-icon color="white">mdi-package-variant</v-icon>
                </v-avatar>

                <div class="flex-grow-1">
                  <div class="text-subtitle-1 font-weight-bold mb-1">
                    {{ activo.marca }} {{ activo.modelo }}
                  </div>
                  <div class="text-caption text-medium-emphasis">
                    {{ activo.codigo_inventario }} • {{ activo.tipo?.nombre_tipo }}
                  </div>
                </div>

                <div class="text-right">
                  <v-chip 
                    size="small" 
                    :color="getEstadoColor(activo.estado?.nombre_estado)"
                  >
                    {{ activo.estado?.nombre_estado }}
                  </v-chip>
                </div>
              </div>
            </v-card-text>
          </v-card>
        </v-window-item>

        <!-- TAB 2: MOVIMIENTOS -->
        <v-window-item value="movimientos">
          <v-card class="glass-card" elevation="0">
            <v-card-text class="text-center py-12">
              <v-icon size="64" color="grey-lighten-1">mdi-swap-horizontal</v-icon>
              <p class="text-h6 mt-4">Historial de Movimientos</p>
              <p class="text-body-2 text-medium-emphasis">Próximamente</p>
            </v-card-text>
          </v-card>
        </v-window-item>
      </v-window>
    </div>

    <!-- Snackbar Mejorado -->
    <v-snackbar
      v-model="showError"
      :color="snackbarColor"
      :timeout="3000"
      location="top"
      variant="elevated"
    >
      <div class="d-flex align-center">
        <v-icon start>{{ snackbarIcon }}</v-icon>
        {{ errorMessage }}
      </div>
      <template v-slot:actions>
        <v-btn variant="text" @click="showError = false">Cerrar</v-btn>
      </template>
    </v-snackbar>

    <!-- Modal de Impresión Mejorado -->
    <v-dialog v-model="dialogImpresion" fullscreen transition="dialog-bottom-transition">
      <v-card>
        <v-app-bar color="primary" density="comfortable">
          <v-btn icon="mdi-close" @click="cerrarModalImpresion"></v-btn>
          <v-toolbar-title>Imprimir Etiquetas</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn
            variant="text"
            prepend-icon="mdi-checkbox-multiple-marked"
            @click="seleccionarTodosActivos"
          >
            Todos
          </v-btn>
          <v-btn
            variant="text"
            prepend-icon="mdi-checkbox-blank-outline"
            @click="deseleccionarTodosActivos"
          >
            Ninguno
          </v-btn>
          <v-btn
            variant="elevated"
            color="white"
            prepend-icon="mdi-printer"
            @click="imprimirEtiquetas"
            :disabled="activosSeleccionados.length === 0"
            class="ml-2"
          >
            <span class="text-primary">Imprimir</span>
          </v-btn>
        </v-app-bar>

        <v-card-text class="pa-6">
          <v-alert type="info" variant="tonal" class="mb-6" prominent>
            <div class="d-flex align-center">
              <v-icon size="32" class="mr-3">mdi-information</v-icon>
              <div>
                <div class="text-h6">
                  {{ activosSeleccionados.length }} de {{ activosDeUbicacion.length }} seleccionados
                </div>
                <div class="text-caption">
                  Selecciona los activos para generar etiquetas con código QR
                </div>
              </div>
            </div>
          </v-alert>

          <v-card variant="outlined" class="mb-6">
            <v-card-text>
              <div style="max-height: 400px; overflow-y: auto;">
                <v-checkbox
                  v-for="activo in activosDeUbicacion"
                  :key="activo.id"
                  v-model="activosSeleccionados"
                  :value="activo.id"
                  hide-details
                  class="mb-3"
                  color="primary"
                >
                  <template v-slot:label>
                    <div class="d-flex align-center justify-space-between w-100">
                      <div>
                        <div class="font-weight-bold">
                          {{ activo.marca }} {{ activo.modelo }}
                        </div>
                        <div class="text-caption text-medium-emphasis">
                          {{ activo.codigo_inventario }} • {{ activo.tipo?.nombre_tipo }}
                        </div>
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

          <div class="preview-section">
            <h3 class="text-h6 mb-4">
              <v-icon start color="primary">mdi-eye</v-icon>
              Vista Previa
            </h3>

            <v-alert v-if="activosSeleccionados.length === 0" type="warning" variant="tonal">
              Selecciona activos para ver la vista previa
            </v-alert>

            <div id="print-area" class="print-area">
              <div class="labels-grid">
                <div
                  v-for="activoId in activosSeleccionados"
                  :key="activoId"
                  class="label-item"
                >
                  <div class="label-content">
                    <div class="label-nombre">
                      <div class="nombre-text">
                        {{ getActivoById(activoId)?.marca }} {{ getActivoById(activoId)?.modelo }}
                      </div>
                      <div class="tipo-text">
                        {{ getActivoById(activoId)?.tipo?.nombre_tipo }}
                      </div>
                    </div>

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
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import apiClient from '@/services/api'
import QRCode from 'qrcode'
import QRScanner from '@/components/QRScanner.vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

// State Machine
const uiState = ref('SCANNING')

// Scanning State
const manualCode = ref('')
const ultimosMovimientos = ref([])
const loadingMovimientos = ref(false)

// Asset State
const currentAsset = ref(null)

// Location State
const currentLocation = ref(null)
const activosDeUbicacion = ref([])
const locationTab = ref('inventario')
const loadingActivos = ref(false)
const tiposEquipo = ref([])

const filtroInventario = ref({
  busqueda: '',
  tipo: null
})

// General
const showError = ref(false)
const errorMessage = ref('')
const snackbarColor = ref('error')
const snackbarIcon = ref('mdi-alert-circle')
const dialogImpresion = ref(false)

// Impresión
const activosSeleccionados = ref([])
const seleccionarTodos = ref(false)
const qrCodes = ref({})

// Computed
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

// State Machine Transitions
function resetToScanning() {
  uiState.value = 'SCANNING'
  currentAsset.value = null
  currentLocation.value = null
  activosDeUbicacion.value = []
  manualCode.value = ''
}

async function transitionToAsset(code) {
  try {
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
    const response = await apiClient.get('/api/ubicaciones/', {
      params: { search: code }
    })

    const ubicaciones = response.data.results || response.data

    if (ubicaciones.length === 0) {
      showErrorMessage(`No se encontró la ubicación con código: ${code}`)
      return
    }

    currentLocation.value = ubicaciones[0]
    await loadActivosDeUbicacion(currentLocation.value.id)
    uiState.value = 'VIEW_LOCATION'
  } catch (error) {
    console.error('Error al cargar ubicación:', error)
    showErrorMessage('Error al cargar la información de la ubicación')
  }
}

// Scanning Methods
function handleQRScanSuccess({ decodedText }) {
  const code = decodedText.trim().toUpperCase()

  if (code.startsWith('INV-')) {
    transitionToAsset(code)
  } else if (code.startsWith('LOC-')) {
    transitionToLocation(code)
  } else {
    showErrorMessage('Código QR inválido')
  }
}

function handleQRScanError({ error, details }) {
  console.error('Error en escáner:', error, details)
}

function handleManualSubmit() {
  const code = manualCode.value.trim().toUpperCase()

  if (!code) {
    showErrorMessage('Por favor ingresa un código')
    return
  }

  if (code.startsWith('INV-')) {
    transitionToAsset(code)
  } else if (code.startsWith('LOC-')) {
    transitionToLocation(code)
  } else {
    showErrorMessage('Código inválido')
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

// Asset Methods
function generarMovimiento() {
  if (!currentAsset.value) return
  router.push({
    name: 'movimiento-tecnico-create',
    params: { id: currentAsset.value.id },
  })
}

function actualizarActivo() {
  if (!currentAsset.value) return
  router.push({
    name: 'technician-edit-activo',
    params: { id: currentAsset.value.id },
  })
}

function verHistorial() {
  if (!currentAsset.value) return
  router.push({
    name: 'technician-history',
    query: { activo: currentAsset.value.id }
  })
}

// Location Methods
async function loadActivosDeUbicacion(ubicacionId) {
  loadingActivos.value = true
  try {
    const response = await apiClient.get('/api/activos/', {
      params: { ubicacion_actual: ubicacionId }
    })

    activosDeUbicacion.value = response.data.results || response.data
  } catch (error) {
    console.error('Error al cargar activos:', error)
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
    console.error('Error al cargar tipos:', error)
  }
}

function handleActivoClick(event, { item }) {
  currentAsset.value = item
  uiState.value = 'VIEW_ASSET'
}

// Print Methods
async function abrirModalImpresion() {
  activosSeleccionados.value = []
  qrCodes.value = {}
  dialogImpresion.value = true
  await generarQRCodes()
  activosSeleccionados.value = activosDeUbicacion.value.map(a => a.id)
}

function cerrarModalImpresion() {
  dialogImpresion.value = false
  activosSeleccionados.value = []
  qrCodes.value = {}
}

function seleccionarTodosActivos() {
  activosSeleccionados.value = activosDeUbicacion.value.map(a => a.id)
}

function deseleccionarTodosActivos() {
  activosSeleccionados.value = []
}

function getActivoById(id) {
  return activosDeUbicacion.value.find(a => a.id === id)
}

async function generarQRCodes() {
  for (const activo of activosDeUbicacion.value) {
    try {
      const qrDataUrl = await QRCode.toDataURL(activo.codigo_inventario, {
        width: 200,
        margin: 1,
        color: { dark: '#000000', light: '#FFFFFF' }
      })
      qrCodes.value[activo.codigo_inventario] = qrDataUrl
    } catch (error) {
      console.error(`Error generando QR:`, error)
    }
  }
}

function imprimirEtiquetas() {
  if (activosSeleccionados.value.length === 0) {
    showErrorMessage('Selecciona al menos un activo')
    return
  }
  window.print()
}

// Utilities
function showErrorMessage(message) {
  errorMessage.value = message
  snackbarColor.value = 'error'
  snackbarIcon.value = 'mdi-alert-circle'
  showError.value = true
}

function formatTimeAgo(fecha) {
  if (!fecha) return ''
  const ahora = new Date()
  const fechaMov = new Date(fecha)
  const diffMs = ahora - fechaMov
  const diffMin = Math.floor(diffMs / 60000)

  if (diffMin < 1) return 'Ahora'
  if (diffMin < 60) return `${diffMin}m`
  const diffHoras = Math.floor(diffMin / 60)
  if (diffHoras < 24) return `${diffHoras}h`
  const diffDias = Math.floor(diffHoras / 24)
  return `${diffDias}d`
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

// Lifecycle
onMounted(async () => {
  await Promise.all([fetchUltimosMovimientos(), fetchTiposEquipo()])

  const ubicacionCode = route.query.ubicacion
  const activoCode = route.query.activo

  if (ubicacionCode) {
    await transitionToLocation(ubicacionCode)
  } else if (activoCode) {
    await transitionToAsset(activoCode)
  }
})

</script>

<style scoped>
/* ============================================================================
   VARIABLES Y CONFIGURACIÓN BASE
   ============================================================================ */
.scanner-view {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1rem;
  min-height: calc(100vh - 112px);
  background: #f5f7fa;
  padding-bottom: 80px;
}

/* ============================================================================
   GLASSMORPHISM CARDS
   ============================================================================ */
.glass-card {
  background: white !important;
  border-radius: 12px !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08) !important;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid rgba(0, 0, 0, 0.06);
}

.glass-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.12) !important;
}

/* ============================================================================
   HERO SECTION
   ============================================================================ */
.hero-section {
  background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%);
  border-radius: 16px;
  padding: 48px 32px;
  margin-bottom: 24px;
  text-align: center;
  box-shadow: 0 8px 24px rgba(25, 118, 210, 0.3);
  position: relative;
  overflow: hidden;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 30% 50%, rgba(255, 255, 255, 0.15) 0%, transparent 50%);
  pointer-events: none;
}

.hero-content {
  position: relative;
  z-index: 1;
  color: white;
}

.hero-content h1,
.hero-content p {
  color: white !important;
}

/* ============================================================================
   SCANNER CARD
   ============================================================================ */
.scanner-card {
  border-radius: 12px !important;
  overflow: hidden;
}

/* ============================================================================
   MOVEMENT ITEMS
   ============================================================================ */
.movement-item {
  padding: 16px 24px !important;
  transition: all 0.2s ease;
  cursor: pointer;
  position: relative;
  border-radius: 8px;
}

.movement-item:hover {
  background: rgba(25, 118, 210, 0.04);
}

.movement-item.border-t {
  border-top: 1px solid rgba(0, 0, 0, 0.08);
}

.movement-avatar {
  transition: transform 0.2s ease;
}

.movement-item:hover .movement-avatar {
  transform: scale(1.05);
}

/* ============================================================================
   ASSET CARD
   ============================================================================ */
.asset-card {
  border-radius: 12px !important;
  overflow: hidden;
  background: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08) !important;
  border: 1px solid rgba(0, 0, 0, 0.06);
}

.asset-header {
  background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%);
  position: relative;
  overflow: hidden;
}

.asset-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 70% 30%, rgba(255, 255, 255, 0.2) 0%, transparent 60%);
  pointer-events: none;
}

.asset-header-content {
  position: relative;
  z-index: 1;
  color: white;
}

.asset-header-content h2,
.asset-header-content div {
  color: white !important;
}

.info-block {
  padding: 12px;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.info-block:hover {
  background: #f5f7fa;
}

/* ============================================================================
   ACTION CARDS
   ============================================================================ */
.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-top: 24px;
}

.action-card {
  background: white !important;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 12px !important;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06) !important;
  height: 100%;
}

.action-card:hover {
  transform: translateY(-8px);
  border-color: rgba(25, 118, 210, 0.3);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15) !important;
}

.action-card:active {
  transform: translateY(-4px);
}

.action-icon-wrapper {
  width: 64px;
  height: 64px;
  margin: 0 auto;
  border-radius: 12px;
  background: #f5f7fa;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.action-card:hover .action-icon-wrapper {
  transform: scale(1.1);
  background: rgba(25, 118, 210, 0.08);
}

/* ============================================================================
   LOCATION HEADER
   ============================================================================ */
.location-header {
  border-radius: 12px !important;
  background: white !important;
  border: 1px solid rgba(0, 0, 0, 0.06);
}

/* ============================================================================
   ASSET LIST ITEMS
   ============================================================================ */
.asset-list-item {
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid rgba(0, 0, 0, 0.06);
  height: 100%;
}

.asset-list-item:hover {
  transform: translateY(-4px);
  border-color: rgba(25, 118, 210, 0.3);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.12) !important;
}

.asset-list-item:active {
  transform: translateY(-2px);
}

/* ============================================================================
   PRINT STYLES
   ============================================================================ */
.preview-section {
  margin-top: 32px;
  padding: 24px;
  background: #f5f7fa;
  border-radius: 12px;
}

.print-area {
  background: white;
  padding: 20mm;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.labels-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10mm;
}

.label-item {
  width: 90mm;
  height: 50mm;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  page-break-inside: avoid;
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.2s ease;
}

.label-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: scale(1.02);
}

.label-content {
  display: flex;
  height: 100%;
  padding: 5mm;
  gap: 3mm;
  position: relative;
}

.label-nombre {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding-right: 2mm;
}

.nombre-text {
  font-size: 14pt;
  font-weight: bold;
  line-height: 1.2;
  color: #1a1a1a;
  margin-bottom: 2mm;
}

.tipo-text {
  font-size: 10pt;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.label-qr {
  width: 35mm;
  height: 35mm;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  flex-shrink: 0;
}

.qr-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.qr-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
}

.label-codigo-vertical {
  position: absolute;
  right: 2mm;
  top: 50%;
  transform: translateY(-50%) rotate(90deg);
  transform-origin: center;
  white-space: nowrap;
}

.codigo-vertical-text {
  font-size: 8pt;
  font-weight: 600;
  color: #666;
  letter-spacing: 1px;
}

/* ============================================================================
   RESPONSIVE
   ============================================================================ */
@media (max-width: 600px) {
  .scanner-view {
    padding: 0.75rem;
  }

  .hero-section {
    padding: 32px 24px;
    border-radius: 12px;
  }

  .actions-grid {
    grid-template-columns: 1fr;
  }

  .labels-grid {
    grid-template-columns: 1fr;
  }

  .glass-card,
  .asset-card,
  .location-header {
    border-radius: 8px !important;
  }
}

@media (min-width: 960px) {
  .scanner-view {
    padding: 1.5rem;
  }
}

/* ============================================================================
   PRINT MEDIA QUERY
   ============================================================================ */
@media print {
  @page {
    size: A4;
    margin: 10mm;
  }

  .scanner-view {
    background: white;
    padding: 0;
  }

  .v-app-bar,
  .v-btn,
  .preview-section > h3,
  .v-alert {
    display: none !important;
  }

  .print-area {
    box-shadow: none;
    padding: 0;
  }

  .labels-grid {
    gap: 5mm;
  }

  .label-item {
    box-shadow: none;
    border: 1px solid #000;
  }

  .label-item:hover {
    transform: none;
  }
}

/* ============================================================================
   ANIMATIONS
   ============================================================================ */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.scanning-state > *,
.view-asset-state > *,
.view-location-state > * {
  animation: fadeIn 0.4s ease-out;
}

.movement-item,
.asset-list-item,
.action-card {
  animation: fadeIn 0.3s ease-out backwards;
}

.movement-item:nth-child(1) { animation-delay: 0.05s; }
.movement-item:nth-child(2) { animation-delay: 0.1s; }
.movement-item:nth-child(3) { animation-delay: 0.15s; }
.movement-item:nth-child(4) { animation-delay: 0.2s; }
.movement-item:nth-child(5) { animation-delay: 0.25s; }

/* ============================================================================
   UTILITY CLASSES
   ============================================================================ */
.gap-2 {
  gap: 8px;
}

.w-100 {
  width: 100%;
}

.opacity-90 {
  opacity: 0.9;
}
</style>
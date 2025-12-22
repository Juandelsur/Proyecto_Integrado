<template>
  <div class="scanner-view">
    <!-- ========================================================================
         ESTADO 1: SCANNING (Interfaz de Captura)
         ======================================================================== -->
    <div v-if="uiState === 'SCANNING'" class="scanning-state">
      <!-- Hero Section -->
      <div class="hero-section">
        <div class="hero-content">
          <v-icon size="64" color="primary" class="mb-4">mdi-qrcode-scan</v-icon>
          <h1 class="text-h4 font-weight-bold mb-2">Auditoría de Activos</h1>
          <p class="text-body-1 text-medium-emphasis">
            Escanea un activo o ubicación para ver su información
          </p>
        </div>
      </div>

      <!-- Escáner QR -->
      <v-card class="scanner-card glass-card mb-6" elevation="0">
        <v-card-text class="pa-6">
          <QRScanner
            @scan-success="handleQRScanSuccess"
            @scan-error="handleQRScanError"
          />
        </v-card-text>
      </v-card>

      <!-- Entrada Manual -->
      <v-card class="glass-card mb-6" elevation="0">
        <v-card-text class="pa-6">
          <h3 class="text-h6 font-weight-bold mb-4">
            <v-icon class="mr-2">mdi-keyboard</v-icon>
            Ingreso Manual
          </h3>
          <v-form @submit.prevent="handleManualSubmit">
            <v-text-field
              v-model="manualCode"
              label="Código de Activo o Ubicación"
              placeholder="INV-25-A1B2C3 o LOC-F8A1B2"
              variant="outlined"
              prepend-inner-icon="mdi-barcode"
              clearable
              autofocus
              class="mb-4"
            ></v-text-field>
            <v-btn
              type="submit"
              block
              size="large"
              color="primary"
              prepend-icon="mdi-magnify"
            >
              Buscar
            </v-btn>
          </v-form>
        </v-card-text>
      </v-card>
    </div>

    <!-- ========================================================================
         ESTADO 2: VIEW_ASSET (Detalle de Activo) - SOLO LECTURA
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

      <!-- Información del Activo -->
      <v-card class="asset-card glass-card mb-6" elevation="0">
        <v-card-text class="pa-6">
          <div class="asset-header mb-6">
            <div class="d-flex align-center mb-4">
              <v-avatar size="56" color="primary" class="mr-4">
                <v-icon size="32">mdi-desktop-classic</v-icon>
              </v-avatar>
              <div>
                <div class="text-h5 font-weight-bold">
                  {{ currentAsset?.marca }} {{ currentAsset?.modelo }}
                </div>
                <div class="text-body-2 text-medium-emphasis">
                  {{ currentAsset?.tipo?.nombre_tipo }}
                </div>
              </div>
            </div>

            <!-- Estado Badge -->
            <v-chip
              :color="getEstadoColor(currentAsset?.estado?.nombre_estado)"
              variant="flat"
              size="large"
              class="mb-4"
            >
              <v-icon start>{{ getEstadoIcon(currentAsset?.estado?.nombre_estado) }}</v-icon>
              {{ currentAsset?.estado?.nombre_estado }}
            </v-chip>
          </div>

          <!-- Detalles en Grid -->
          <v-row dense>
            <v-col cols="12" md="6">
              <div class="detail-item">
                <div class="detail-label">Código de Inventario</div>
                <div class="detail-value">{{ currentAsset?.codigo_inventario }}</div>
              </div>
            </v-col>
            <v-col cols="12" md="6">
              <div class="detail-item">
                <div class="detail-label">Número de Serie</div>
                <div class="detail-value">{{ currentAsset?.numero_serie || 'N/A' }}</div>
              </div>
            </v-col>
            <v-col cols="12" md="6">
              <div class="detail-item">
                <div class="detail-label">Ubicación Actual</div>
                <div class="detail-value">
                  {{ currentAsset?.ubicacion_actual?.nombre_ubicacion }}
                  <span class="text-medium-emphasis">
                    ({{ currentAsset?.ubicacion_actual?.departamento?.nombre_departamento }})
                  </span>
                </div>
              </div>
            </v-col>
            <v-col cols="12" md="6">
              <div class="detail-item">
                <div class="detail-label">Fecha de Alta</div>
                <div class="detail-value">{{ formatDate(currentAsset?.fecha_alta) }}</div>
              </div>
            </v-col>
          </v-row>

          <!-- Notas (si existen) -->
          <div v-if="currentAsset?.notas" class="mt-4">
            <div class="detail-label">Notas</div>
            <div class="detail-value">{{ currentAsset.notas }}</div>
          </div>
        </v-card-text>
      </v-card>

      <!-- Mensaje de Solo Lectura -->
      <v-alert
        type="info"
        variant="tonal"
        class="mb-4"
      >
        <v-icon start>mdi-information</v-icon>
        Modo auditoría: Solo puedes visualizar la información del activo.
      </v-alert>
    </div>

    <!-- ========================================================================
         ESTADO 3: VIEW_LOCATION (Auditoría de Ubicación)
         ======================================================================== -->
    <div v-else-if="uiState === 'VIEW_LOCATION'" class="view-location-state">
      <!-- Header con Navegación -->
      <div class="d-flex align-center mb-6">
        <v-btn
          icon="mdi-arrow-left"
          variant="text"
          size="large"
          @click="resetToScanning"
        ></v-btn>
        <div class="ml-3">
          <div class="text-overline text-primary">Auditoría de Ubicación</div>
          <div class="text-h6 font-weight-bold">{{ currentLocation?.nombre_ubicacion }}</div>
        </div>
      </div>

      <!-- Información de la Ubicación -->
      <v-card class="location-header glass-card mb-6" elevation="0">
        <v-card-text class="pa-6">
          <div class="d-flex align-center mb-4">
            <v-avatar size="56" color="success" class="mr-4">
              <v-icon size="32">mdi-map-marker</v-icon>
            </v-avatar>
            <div>
              <div class="text-h5 font-weight-bold">
                {{ currentLocation?.nombre_ubicacion }}
              </div>
              <div class="text-body-2 text-medium-emphasis">
                {{ currentLocation?.departamento?.nombre_departamento }}
              </div>
            </div>
          </div>

          <!-- Estadísticas de la Ubicación -->
          <v-row dense>
            <v-col cols="6" md="3">
              <v-card variant="tonal" color="primary">
                <v-card-text class="text-center">
                  <div class="text-h4 font-weight-bold">{{ activosDeUbicacion.length }}</div>
                  <div class="text-caption">Total Activos</div>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="6" md="3">
              <v-card variant="tonal" color="success">
                <v-card-text class="text-center">
                  <div class="text-h4 font-weight-bold">{{ contarPorEstado('Operativo') }}</div>
                  <div class="text-caption">Operativos</div>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="6" md="3">
              <v-card variant="tonal" color="warning">
                <v-card-text class="text-center">
                  <div class="text-h4 font-weight-bold">{{ contarPorEstado('Reparación') }}</div>
                  <div class="text-caption">En Reparación</div>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="6" md="3">
              <v-card variant="tonal" color="error">
                <v-card-text class="text-center">
                  <div class="text-h4 font-weight-bold">{{ contarPorEstado('De Baja') }}</div>
                  <div class="text-caption">De Baja</div>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>

      <!-- Lista de Activos en la Ubicación -->
      <v-card class="glass-card" elevation="0">
        <v-card-title class="text-h6 font-weight-bold">
          <v-icon class="mr-2">mdi-package-variant-closed</v-icon>
          Inventario de la Sala
        </v-card-title>
        <v-card-text class="pa-4">
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
                hide-details
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="4">
              <v-select
                v-model="filtroInventario.estado"
                :items="estadosDisponibles"
                label="Estado"
                variant="outlined"
                density="compact"
                clearable
                hide-details
              ></v-select>
            </v-col>
          </v-row>

          <!-- Tabla de Activos -->
          <v-data-table
            :headers="headers"
            :items="activosFiltrados"
            :items-per-page="10"
            class="elevation-0"
            @click:row="handleActivoClick"
          >
            <template #item.estado="{ item }">
              <v-chip
                :color="getEstadoColor(item.estado?.nombre_estado)"
                size="small"
                variant="flat"
              >
                {{ item.estado?.nombre_estado }}
              </v-chip>
            </template>
          </v-data-table>
        </v-card-text>
      </v-card>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import apiClient from '@/services/api'
import QRScanner from '@/components/QRScanner.vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

// ============================================================================
// STATE MACHINE
// ============================================================================
const uiState = ref('SCANNING') // 'SCANNING' | 'VIEW_ASSET' | 'VIEW_LOCATION'

// ============================================================================
// SCANNING STATE
// ============================================================================
const manualCode = ref('')

// ============================================================================
// ASSET STATE
// ============================================================================
const currentAsset = ref(null)

// ============================================================================
// LOCATION STATE
// ============================================================================
const currentLocation = ref(null)
const activosDeUbicacion = ref([])
const filtroInventario = ref({
  busqueda: '',
  estado: null
})

// ============================================================================
// DATA TABLE HEADERS
// ============================================================================
const headers = [
  { title: 'Código', key: 'codigo_inventario', sortable: true },
  { title: 'Tipo', key: 'tipo.nombre_tipo', sortable: true },
  { title: 'Marca', key: 'marca', sortable: true },
  { title: 'Modelo', key: 'modelo', sortable: true },
  { title: 'Estado', key: 'estado', sortable: true }
]

// ============================================================================
// COMPUTED
// ============================================================================

/**
 * Estados disponibles para el filtro
 */
const estadosDisponibles = computed(() => {
  const estados = new Set()
  activosDeUbicacion.value.forEach(activo => {
    if (activo.estado?.nombre_estado) {
      estados.add(activo.estado.nombre_estado)
    }
  })
  return Array.from(estados)
})

/**
 * Activos filtrados según búsqueda y estado
 */
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

  if (filtroInventario.value.estado) {
    resultado = resultado.filter(a => a.estado?.nombre_estado === filtroInventario.value.estado)
  }

  return resultado
})

// ============================================================================
// STATE MACHINE TRANSITIONS
// ============================================================================

/**
 * Resetear al estado de escaneo
 */
function resetToScanning() {
  uiState.value = 'SCANNING'
  currentAsset.value = null
  currentLocation.value = null
  activosDeUbicacion.value = []
  manualCode.value = ''
  filtroInventario.value = { busqueda: '', estado: null }
}

/**
 * Transición a vista de activo
 */
async function transitionToAsset(code) {
  try {
    console.log('🔍 Buscando activo:', code)

    const response = await apiClient.get('/api/activos/', {
      params: { search: code }
    })

    const activos = response.data.results || response.data

    if (activos.length === 0) {
      alert(`No se encontró el activo con código: ${code}`)
      return
    }

    currentAsset.value = activos[0]
    uiState.value = 'VIEW_ASSET'

    console.log('✅ Activo cargado:', currentAsset.value)
  } catch (error) {
    console.error('❌ Error al cargar activo:', error)
    alert('Error al cargar la información del activo')
  }
}

/**
 * Transición a vista de ubicación (Auditoría de Sala)
 */
async function transitionToLocation(code) {
  try {
    console.log('🔍 Buscando ubicación:', code)

    const response = await apiClient.get('/api/ubicaciones/', {
      params: { search: code }
    })

    const ubicaciones = response.data.results || response.data

    if (ubicaciones.length === 0) {
      alert(`No se encontró la ubicación con código: ${code}`)
      return
    }

    currentLocation.value = ubicaciones[0]
    await loadActivosDeUbicacion(currentLocation.value.id)
    uiState.value = 'VIEW_LOCATION'

    console.log('✅ Ubicación cargada:', currentLocation.value)
    console.log('📦 Activos encontrados:', activosDeUbicacion.value.length)
  } catch (error) {
    console.error('❌ Error al cargar ubicación:', error)
    alert('Error al cargar la información de la ubicación')
  }
}


// ============================================================================
// SCANNING METHODS
// ============================================================================

/**
 * Maneja el escaneo exitoso de un código QR
 */
function handleQRScanSuccess({ decodedText }) {
  const code = decodedText.trim().toUpperCase()
  console.log('📷 Código QR escaneado:', code)

  if (code.startsWith('INV-')) {
    transitionToAsset(code)
  } else if (code.startsWith('LOC-')) {
    transitionToLocation(code)
  } else {
    alert('Código QR inválido. Debe comenzar con INV- (Activo) o LOC- (Ubicación)')
  }
}

/**
 * Maneja errores del escáner
 */
function handleQRScanError({ error, details }) {
  console.error('Error en escáner:', error, details)
}

/**
 * Maneja el envío manual de código
 */
function handleManualSubmit() {
  const code = manualCode.value.trim().toUpperCase()

  if (!code) {
    alert('Por favor ingresa un código')
    return
  }

  if (code.startsWith('INV-')) {
    transitionToAsset(code)
  } else if (code.startsWith('LOC-')) {
    transitionToLocation(code)
  } else {
    alert('Código inválido. Debe comenzar con INV- (Activo) o LOC- (Ubicación)')
  }
}

// ============================================================================
// LOCATION METHODS
// ============================================================================

/**
 * Carga los activos de una ubicación específica
 */
async function loadActivosDeUbicacion(ubicacionId) {
  try {
    console.log('📦 Cargando activos de ubicación:', ubicacionId)

    const response = await apiClient.get('/api/activos/', {
      params: { ubicacion: ubicacionId }
    })

    activosDeUbicacion.value = response.data.results || response.data

    console.log('✅ Activos cargados:', activosDeUbicacion.value.length)
  } catch (error) {
    console.error('❌ Error al cargar activos de ubicación:', error)
    alert('Error al cargar los activos de la ubicación')
  }
}

/**
 * Cuenta activos por estado
 */
function contarPorEstado(estadoNombre) {
  return activosDeUbicacion.value.filter(activo =>
    activo.estado?.nombre_estado?.includes(estadoNombre)
  ).length
}

/**
 * Maneja el clic en un activo de la tabla
 */
function handleActivoClick(event, { item }) {
  currentAsset.value = item
  uiState.value = 'VIEW_ASSET'
}

// ============================================================================
// UTILITY METHODS
// ============================================================================

/**
 * Obtiene el color según el estado
 */
function getEstadoColor(estado) {
  if (!estado) return 'grey'

  const estadoLower = estado.toLowerCase()

  if (estadoLower.includes('operativo')) return 'success'
  if (estadoLower.includes('reparación') || estadoLower.includes('mantención')) return 'warning'
  if (estadoLower.includes('baja')) return 'error'

  return 'info'
}

/**
 * Obtiene el icono según el estado
 */
function getEstadoIcon(estado) {
  if (!estado) return 'mdi-help-circle'

  const estadoLower = estado.toLowerCase()

  if (estadoLower.includes('operativo')) return 'mdi-check-circle'
  if (estadoLower.includes('reparación') || estadoLower.includes('mantención')) return 'mdi-wrench'
  if (estadoLower.includes('baja')) return 'mdi-close-circle'

  return 'mdi-information'
}

/**
 * Formatea una fecha
 */
function formatDate(dateString) {
  if (!dateString) return 'N/A'

  const date = new Date(dateString)
  return date.toLocaleDateString('es-CL', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// ============================================================================
// LIFECYCLE
// ============================================================================

onMounted(async () => {
  console.log('🚀 ScannerView Jefe - Modo Auditoría')

  // Verificar si viene con un código en la URL
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
   CONFIGURACIÓN BASE
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
   HERO SECTION
   ============================================================================ */
.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  padding: 48px 32px;
  margin-bottom: 24px;
  box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
}

.hero-content {
  text-align: center;
  color: white;
}

/* ============================================================================
   GLASS CARD EFFECT
   ============================================================================ */
.glass-card {
  background: rgba(255, 255, 255, 0.95) !important;
  backdrop-filter: blur(10px);
  border-radius: 16px !important;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08) !important;
}

.scanner-card {
  overflow: hidden;
}

/* ============================================================================
   ASSET & LOCATION CARDS
   ============================================================================ */
.asset-card,
.location-header {
  background: rgba(255, 255, 255, 0.98) !important;
  border-radius: 16px !important;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08) !important;
}

.asset-header {
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
}

/* ============================================================================
   DETAIL ITEMS
   ============================================================================ */
.detail-item {
  padding: 12px 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.detail-item:last-child {
  border-bottom: none;
}

.detail-label {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: rgba(0, 0, 0, 0.6);
  margin-bottom: 4px;
}

.detail-value {
  font-size: 1rem;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.87);
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
</style>


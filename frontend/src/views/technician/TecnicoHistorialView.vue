<template>
  <div class="tecnico-historial-view pa-4">
    <!-- ========================================================================
         CABECERA
         ======================================================================== -->
    <div class="mb-4">
      <h1 class="text-h5 font-weight-bold mb-2">
        <v-icon start color="primary">mdi-history</v-icon>
        Historial de Movimientos
      </h1>
      <p class="text-body-2 text-grey">Consulta el historial completo de movimientos de activos</p>
    </div>

    <!-- ========================================================================
         PANEL DE FILTROS (EXPANSION PANEL PARA AHORRAR ESPACIO)
         ======================================================================== -->
    <v-expansion-panels class="mb-4">
      <v-expansion-panel>
        <v-expansion-panel-title>
          <div class="d-flex align-center">
            <v-icon start>mdi-filter-variant</v-icon>
            <span class="font-weight-medium">Filtros de Búsqueda</span>
            <v-chip v-if="filtrosActivos > 0" size="small" color="primary" class="ml-2">
              {{ filtrosActivos }}
            </v-chip>
          </div>
        </v-expansion-panel-title>

        <v-expansion-panel-text>
          <v-row dense>
            <!-- Buscador -->
            <v-col cols="12" md="4">
              <v-text-field
                v-model="filtros.busqueda"
                label="Buscar"
                placeholder="Nombre activo, usuario o código"
                prepend-inner-icon="mdi-magnify"
                variant="outlined"
                density="compact"
                clearable
                hide-details
              ></v-text-field>
            </v-col>

            <!-- Tipo de Movimiento -->
            <v-col cols="12" md="3">
              <v-select
                v-model="filtros.tipoMovimiento"
                :items="tiposMovimiento"
                label="Tipo de Acción"
                prepend-inner-icon="mdi-swap-horizontal"
                variant="outlined"
                density="compact"
                hide-details
              ></v-select>
            </v-col>

            <!-- Rango de Fecha -->
            <v-col cols="12" md="3">
              <v-select
                v-model="filtros.rango"
                :items="rangos"
                label="Rango de Fecha"
                prepend-inner-icon="mdi-calendar-range"
                variant="outlined"
                density="compact"
                hide-details
              ></v-select>
            </v-col>

            <!-- Botón Aplicar -->
            <v-col cols="12" md="2">
              <v-btn
                color="primary"
                variant="flat"
                block
                @click="aplicarFiltros"
                :loading="loading"
              >
                <v-icon start>mdi-check</v-icon>
                Aplicar
              </v-btn>
            </v-col>
          </v-row>

          <!-- Botón Limpiar Filtros -->
          <v-row v-if="filtrosActivos > 0" dense class="mt-2">
            <v-col cols="12">
              <v-btn
                variant="text"
                size="small"
                color="grey"
                @click="limpiarFiltros"
              >
                <v-icon start>mdi-filter-off</v-icon>
                Limpiar Filtros
              </v-btn>
            </v-col>
          </v-row>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>

    <!-- ========================================================================
         INFORMACIÓN DE RESULTADOS
         ======================================================================== -->
    <div v-if="!loading && movimientosFiltrados.length > 0" class="mb-3">
      <v-chip size="small" variant="outlined" prepend-icon="mdi-information-outline">
        {{ totalResultados }} movimiento{{ totalResultados !== 1 ? 's' : '' }} encontrado{{ totalResultados !== 1 ? 's' : '' }}
      </v-chip>
    </div>

    <!-- ========================================================================
         TABLA DE RESULTADOS (DISEÑO MÓVIL CON TARJETAS DE FILA)
         ======================================================================== -->
    <v-data-table
      :headers="headers"
      :items="movimientosFiltrados"
      :loading="loading"
      :items-per-page="itemsPerPage"
      :page="currentPage"
      class="elevation-1"
      @update:page="currentPage = $event"
    >
      <!-- Loading State -->
      <template v-slot:loading>
        <v-skeleton-loader type="table-row@15"></v-skeleton-loader>
      </template>

      <!-- No Data State -->
      <template v-slot:no-data>
        <div class="text-center py-8">
          <v-icon size="64" color="grey">mdi-history</v-icon>
          <p class="text-h6 mt-4">No hay movimientos registrados</p>
          <p class="text-grey">Intenta ajustar los filtros de búsqueda</p>
        </div>
      </template>

      <!-- DISEÑO MÓVIL: TARJETA DE FILA PERSONALIZADA -->
      <template v-slot:item="{ item }">
        <tr class="custom-row">
          <td colspan="5" class="pa-3" style="border-bottom: 1px solid #e0e0e0;">
            <div class="mobile-card">
              <!-- Línea 1: Icono + Nombre del Activo + Tipo -->
              <div class="d-flex align-center mb-2">
                <v-avatar :color="getTipoColor(item.tipo_movimiento)" size="32" class="mr-3">
                  <v-icon size="18" color="white">{{ getTipoIcon(item.tipo_movimiento) }}</v-icon>
                </v-avatar>

                <div class="flex-grow-1">
                  <div class="font-weight-bold text-body-1">
                    {{ item.activo?.marca }} {{ item.activo?.modelo }}
                  </div>
                  <div class="text-caption text-grey">
                    {{ item.codigo_activo }}
                  </div>
                </div>

                <v-chip size="small" :color="getTipoColor(item.tipo_movimiento)" variant="tonal">
                  {{ item.tipo_movimiento }}
                </v-chip>
              </div>

              <!-- Línea 2: El Cambio (Ubicación Origen -> Destino) -->
              <div class="d-flex align-center mb-2 ml-11">
                <div class="change-display">
                  <!-- Ubicación Origen -->
                  <span class="text-decoration-line-through text-grey">
                    {{ item.ubicacion_origen?.nombre_ubicacion }}
                  </span>

                  <!-- Flecha -->
                  <v-icon size="20" class="mx-2" color="primary">mdi-arrow-right</v-icon>

                  <!-- Ubicación Destino -->
                  <span class="font-weight-medium">
                    {{ item.ubicacion_destino?.nombre_ubicacion }}
                  </span>
                </div>
              </div>

              <!-- Línea 3: Metadatos (Usuario + Fecha) -->
              <div class="d-flex align-center text-caption text-grey ml-11">
                <v-icon size="16" class="mr-1">mdi-account</v-icon>
                <span class="mr-3">{{ item.nombre_usuario }}</span>

                <v-icon size="16" class="mr-1">mdi-clock-outline</v-icon>
                <span>{{ formatFecha(item.fecha_movimiento) }}</span>
              </div>

              <!-- Comentarios (Si existen) -->
              <div v-if="item.comentarios" class="mt-2 ml-11">
                <v-chip size="x-small" variant="outlined" prepend-icon="mdi-comment-text-outline">
                  {{ item.comentarios }}
                </v-chip>
              </div>
            </div>
          </td>
        </tr>
      </template>
    </v-data-table>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import apiClient from '@/services/api'

// ============================================================================
// STORES
// ============================================================================

const authStore = useAuthStore()

// ============================================================================
// STATE
// ============================================================================

const loading = ref(false)
const movimientos = ref([])

// Paginación
const currentPage = ref(1)
const itemsPerPage = ref(15)

const filtros = ref({
  busqueda: '',
  tipoMovimiento: 'Todos',
  rango: 'todo'
})

// ============================================================================
// OPCIONES DE FILTROS
// ============================================================================

const tiposMovimiento = [
  { title: 'Todos', value: 'Todos' },
  { title: 'Traslado', value: 'TRASLADO' },
  { title: 'Asignación', value: 'ASIGNACION' },
  { title: 'Devolución', value: 'DEVOLUCION' },
  { title: 'Mantenimiento', value: 'MANTENIMIENTO' },
  { title: 'Retorno', value: 'RETORNO' },
  { title: 'Baja', value: 'BAJA' }
]

const rangos = [
  { title: 'Hoy', value: 'hoy' },
  { title: '7 Días', value: '7dias' },
  { title: '30 Días', value: '30dias' },
  { title: 'Todo', value: 'todo' }
]

// ============================================================================
// HEADERS (NO SE MUESTRAN PERO SON NECESARIOS PARA v-data-table)
// ============================================================================

const headers = [
  { title: 'Activo', key: 'activo', sortable: false },
  { title: 'Tipo', key: 'tipo_movimiento', sortable: false },
  { title: 'Origen', key: 'ubicacion_origen', sortable: false },
  { title: 'Destino', key: 'ubicacion_destino', sortable: false },
  { title: 'Fecha', key: 'fecha_movimiento', sortable: false }
]

// ============================================================================
// COMPUTED
// ============================================================================

const filtrosActivos = computed(() => {
  let count = 0
  if (filtros.value.busqueda) count++
  if (filtros.value.tipoMovimiento !== 'Todos') count++
  if (filtros.value.rango !== 'todo') count++
  return count
})

const totalResultados = computed(() => {
  return movimientosFiltrados.value.length
})

const movimientosFiltrados = computed(() => {
  let resultado = [...movimientos.value]

  // Filtro de búsqueda
  if (filtros.value.busqueda) {
    const busqueda = filtros.value.busqueda.toLowerCase()
    resultado = resultado.filter(m =>
      m.activo?.marca?.toLowerCase().includes(busqueda) ||
      m.activo?.modelo?.toLowerCase().includes(busqueda) ||
      m.codigo_activo?.toLowerCase().includes(busqueda) ||
      m.nombre_usuario?.toLowerCase().includes(busqueda)
    )
  }

  // Filtro de tipo de movimiento
  if (filtros.value.tipoMovimiento !== 'Todos') {
    resultado = resultado.filter(m => m.tipo_movimiento === filtros.value.tipoMovimiento)
  }

  // Filtro de rango de fecha
  if (filtros.value.rango !== 'todo') {
    const ahora = new Date()
    const fechaLimite = new Date()

    if (filtros.value.rango === 'hoy') {
      fechaLimite.setHours(0, 0, 0, 0)
    } else if (filtros.value.rango === '7dias') {
      fechaLimite.setDate(ahora.getDate() - 7)
    } else if (filtros.value.rango === '30dias') {
      fechaLimite.setDate(ahora.getDate() - 30)
    }

    resultado = resultado.filter(m => new Date(m.fecha_movimiento) >= fechaLimite)
  }

  return resultado
})

// ============================================================================
// MÉTODOS - API
// ============================================================================

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

// ============================================================================
// MÉTODOS - FILTROS
// ============================================================================

function aplicarFiltros() {
  // Resetear a la primera página al aplicar filtros
  currentPage.value = 1

  // Simular carga
  loading.value = true
  setTimeout(() => {
    loading.value = false
  }, 500)
}

function limpiarFiltros() {
  filtros.value = {
    busqueda: '',
    tipoMovimiento: 'Todos',
    rango: 'todo'
  }

  // Resetear a la primera página al limpiar filtros
  currentPage.value = 1
}

// ============================================================================
// MÉTODOS - UTILIDADES
// ============================================================================

function getTipoColor(tipo) {
  const colores = {
    'TRASLADO': 'blue',
    'ASIGNACION': 'green',
    'DEVOLUCION': 'orange',
    'MANTENIMIENTO': 'purple',
    'RETORNO': 'teal',
    'BAJA': 'red'
  }
  return colores[tipo] || 'grey'
}

function getTipoIcon(tipo) {
  const iconos = {
    'TRASLADO': 'mdi-swap-horizontal',
    'ASIGNACION': 'mdi-account-arrow-right',
    'DEVOLUCION': 'mdi-arrow-u-left-top',
    'MANTENIMIENTO': 'mdi-wrench',
    'RETORNO': 'mdi-arrow-u-right-top',
    'BAJA': 'mdi-delete'
  }
  return iconos[tipo] || 'mdi-help-circle'
}

function formatFecha(fecha) {
  if (!fecha) return ''

  const date = new Date(fecha)
  const ahora = new Date()
  const diff = ahora - date

  // Menos de 1 minuto
  if (diff < 60000) {
    return 'Hace un momento'
  }

  // Menos de 1 hora
  if (diff < 3600000) {
    const minutos = Math.floor(diff / 60000)
    return `Hace ${minutos} min`
  }

  // Menos de 24 horas
  if (diff < 86400000) {
    const horas = Math.floor(diff / 3600000)
    return `Hace ${horas}h`
  }

  // Menos de 7 días
  if (diff < 604800000) {
    const dias = Math.floor(diff / 86400000)
    return `Hace ${dias}d`
  }

  // Formato completo
  const dia = date.getDate().toString().padStart(2, '0')
  const mes = (date.getMonth() + 1).toString().padStart(2, '0')
  const año = date.getFullYear()
  const hora = date.getHours().toString().padStart(2, '0')
  const minuto = date.getMinutes().toString().padStart(2, '0')

  return `${dia}/${mes}/${año} ${hora}:${minuto}`
}

// ============================================================================
// LIFECYCLE
// ============================================================================

onMounted(() => {
  fetchMovimientos()
})
</script>

<style scoped>
.tecnico-historial-view {
  max-width: 1200px;
  margin: 0 auto;
}

.custom-row {
  cursor: default;
}

.mobile-card {
  width: 100%;
}

.change-display {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
}

/* Responsive: En pantallas grandes, mejorar el espaciado */
@media (min-width: 960px) {
  .mobile-card {
    padding: 0.5rem 0;
  }
}
</style>

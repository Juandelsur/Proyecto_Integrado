<template>
  <div class="historial-content">
    <!-- ====================================================================
         HEADER
         ==================================================================== -->
    <v-card variant="tonal" color="primary" class="mb-4">
      <v-card-text>
        <h2 class="text-h5 font-weight-bold mb-1">Historial de Movimientos</h2>
        <p class="text-subtitle-1 mb-0">Registro completo de cambios y movimientos</p>
      </v-card-text>
    </v-card>

    <!-- ====================================================================
         PANEL DE FILTROS
         ==================================================================== -->
    <v-card class="mb-4">
      <v-card-title class="d-flex justify-space-between align-center">
        <span class="text-h6 font-weight-bold">Filtros</span>
        <v-btn
          variant="text"
          size="small"
          @click="limpiarFiltros"
        >
          Limpiar filtros
        </v-btn>
      </v-card-title>
      <v-card-text>
        <v-row>
          <!-- Búsqueda por texto -->
          <v-col cols="12" md="6">
            <v-text-field
              v-model="filtros.busqueda"
              label="Buscar por código o activo"
              prepend-inner-icon="mdi-magnify"
              variant="outlined"
              density="comfortable"
              clearable
              @input="aplicarFiltros"
            ></v-text-field>
          </v-col>

          <!-- Filtro por tipo de movimiento -->
          <v-col cols="12" sm="6" md="3">
            <v-select
              v-model="filtros.tipoMovimiento"
              :items="tiposMovimiento"
              label="Tipo de Movimiento"
              prepend-inner-icon="mdi-swap-horizontal"
              variant="outlined"
              density="comfortable"
              clearable
              @update:model-value="aplicarFiltros"
            ></v-select>
          </v-col>

          <!-- Filtro por usuario -->
          <v-col cols="12" sm="6" md="3">
            <v-select
              v-model="filtros.usuario"
              :items="usuarios"
              item-title="nombre_completo"
              item-value="id"
              label="Usuario"
              prepend-inner-icon="mdi-account"
              variant="outlined"
              density="comfortable"
              clearable
              @update:model-value="aplicarFiltros"
            ></v-select>
          </v-col>

          <!-- Filtro por rango de fechas -->
          <v-col cols="12" sm="6" md="3">
            <v-text-field
              v-model="filtros.fechaDesde"
              label="Fecha desde"
              type="date"
              prepend-inner-icon="mdi-calendar"
              variant="outlined"
              density="comfortable"
              clearable
              @update:model-value="aplicarFiltros"
            ></v-text-field>
          </v-col>

          <v-col cols="12" sm="6" md="3">
            <v-text-field
              v-model="filtros.fechaHasta"
              label="Fecha hasta"
              type="date"
              prepend-inner-icon="mdi-calendar"
              variant="outlined"
              density="comfortable"
              clearable
              @update:model-value="aplicarFiltros"
            ></v-text-field>
          </v-col>
        </v-row>

        <!-- Resumen de filtros activos -->
        <v-chip-group v-if="filtrosActivos.length > 0" class="mt-2">
          <v-chip
            v-for="(filtro, index) in filtrosActivos"
            :key="index"
            closable
            @click:close="removerFiltro(filtro.key)"
          >
            {{ filtro.label }}: {{ filtro.value }}
          </v-chip>
        </v-chip-group>
      </v-card-text>
    </v-card>

    <!-- ====================================================================
         ESTADÍSTICAS RÁPIDAS
         ==================================================================== -->
    <v-row class="mb-4">
      <v-col cols="12" sm="6" md="3">
        <v-card color="blue-lighten-5">
          <v-card-text class="text-center">
            <div class="text-h4 font-weight-bold text-blue">{{ totalRegistros }}</div>
            <div class="text-caption">Total de Registros</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card color="green-lighten-5">
          <v-card-text class="text-center">
            <div class="text-h4 font-weight-bold text-green">{{ registrosFiltrados.length }}</div>
            <div class="text-caption">Registros Filtrados</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card color="orange-lighten-5">
          <v-card-text class="text-center">
            <div class="text-h4 font-weight-bold text-orange">{{ paginaActual }}/{{ totalPaginas }}</div>
            <div class="text-caption">Página Actual</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card color="purple-lighten-5">
          <v-card-text class="text-center">
            <div class="text-h4 font-weight-bold text-purple">20</div>
            <div class="text-caption">Registros por Página</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- ====================================================================
         LOADING STATE
         ==================================================================== -->
    <div v-if="loading" class="loading-container">
      <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
      <p class="mt-3 text-h6">Cargando historial...</p>
    </div>

    <!-- ====================================================================
         LISTA DE MOVIMIENTOS
         ==================================================================== -->
    <v-card v-else>
      <v-card-text class="pa-0">
        <!-- Timeline de movimientos -->
        <v-timeline side="end" align="start" class="pa-4">
          <v-timeline-item
            v-for="(movimiento, index) in registrosPaginados"
            :key="index"
            :dot-color="getColorByTipo(movimiento.tipo_movimiento)"
            size="small"
          >
            <template v-slot:icon>
              <v-icon size="small">
                {{ getIconByTipo(movimiento.tipo_movimiento) }}
              </v-icon>
            </template>

            <v-card elevation="2" class="mb-2">
              <v-card-title class="text-subtitle-1 font-weight-bold pa-3 pb-2">
                <v-icon :color="getColorByTipo(movimiento.tipo_movimiento)" class="mr-2">
                  {{ getIconByTipo(movimiento.tipo_movimiento) }}
                </v-icon>
                {{ getTipoMovimientoTexto(movimiento.tipo_movimiento) }}
              </v-card-title>
              
              <v-card-text class="pa-3 pt-0">
                <v-row dense>
                  <v-col cols="12" sm="6">
                    <div class="text-caption text-grey">Activo</div>
                    <div class="font-weight-medium">
                      {{ getActivoNombre(movimiento) }}
                    </div>
                  </v-col>
                  
                  <v-col cols="12" sm="6">
                    <div class="text-caption text-grey">Código</div>
                    <div class="font-weight-medium">
                      {{ movimiento.activo?.codigo_inventario || 'N/A' }}
                    </div>
                  </v-col>

                  <v-col cols="12" sm="6">
                    <div class="text-caption text-grey">Origen</div>
                    <div>{{ movimiento.ubicacion_origen?.nombre_ubicacion || 'N/A' }}</div>
                  </v-col>

                  <v-col cols="12" sm="6">
                    <div class="text-caption text-grey">Destino</div>
                    <div>{{ movimiento.ubicacion_destino?.nombre_ubicacion || 'N/A' }}</div>
                  </v-col>

                  <v-col cols="12" sm="6">
                    <div class="text-caption text-grey">Usuario</div>
                    <div>
                      <v-icon size="small" class="mr-1">mdi-account</v-icon>
                      {{ movimiento.usuario_registra?.nombre_completo || 'Sistema' }}
                    </div>
                  </v-col>

                  <v-col cols="12" sm="6">
                    <div class="text-caption text-grey">Fecha</div>
                    <div>
                      <v-icon size="small" class="mr-1">mdi-clock</v-icon>
                      {{ formatearFecha(movimiento.fecha_movimiento) }}
                    </div>
                  </v-col>

                  <v-col v-if="movimiento.observaciones" cols="12">
                    <div class="text-caption text-grey">Observaciones</div>
                    <div class="text-body-2">{{ movimiento.observaciones }}</div>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-timeline-item>
        </v-timeline>

        <!-- Empty State -->
        <div v-if="registrosPaginados.length === 0" class="empty-state py-8">
          <v-icon size="64" color="grey-lighten-1">mdi-inbox</v-icon>
          <p class="text-h6 mt-4">No se encontraron registros</p>
          <p class="text-body-2 text-grey">Intenta ajustar los filtros de búsqueda</p>
        </div>
      </v-card-text>

      <!-- ====================================================================
           PAGINACIÓN
           ==================================================================== -->
      <v-card-actions v-if="totalPaginas > 1" class="justify-center pa-4">
        <v-pagination
          v-model="paginaActual"
          :length="totalPaginas"
          :total-visible="5"
          @update:model-value="cambiarPagina"
        ></v-pagination>
      </v-card-actions>
    </v-card>

    <!-- ====================================================================
         BOTÓN EXPORTAR
         ==================================================================== -->
    <v-row class="mt-4">
      <v-col>
        <v-btn
          color="success"
          variant="tonal"
          size="large"
          prepend-icon="mdi-download"
          @click="exportarHistorial"
        >
          Exportar a Excel
        </v-btn>
      </v-col>
    </v-row>

    <!-- ====================================================================
         BOTÓN VOLVER
         ==================================================================== -->
    <div class="footer-section">
      <v-btn
        variant="outlined"
        size="large"
        prepend-icon="mdi-arrow-left"
        class="btn-volver"
        @click="volver"
      >
        Volver
      </v-btn>
    </div>

    <!-- ====================================================================
         SNACKBAR
         ==================================================================== -->
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="3000"
    >
      {{ snackbar.text }}
    </v-snackbar>
  </div>
</template>

<script setup>
/**
 * ============================================================================
 * HISTORIAL DE MOVIMIENTOS
 * ============================================================================
 *
 * Vista completa del historial con:
 * - Filtros avanzados (búsqueda, tipo, usuario, fechas)
 * - Paginación (20 registros por página)
 * - Timeline visual de movimientos
 * - Exportación a Excel
 */

import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/services/api'

// ============================================================================
// COMPOSABLES
// ============================================================================

const router = useRouter()

// ============================================================================
// STATE
// ============================================================================

const movimientos = ref([])
const usuarios = ref([])
const loading = ref(false)
const paginaActual = ref(1)
const registrosPorPagina = 20

const filtros = ref({
  busqueda: '',
  tipoMovimiento: null,
  usuario: null,
  fechaDesde: null,
  fechaHasta: null
})

const tiposMovimiento = [
  { title: 'Todo', value: '' },
  { title: 'Traslado', value: 'TRASLADO' },
  { title: 'Asignación', value: 'ASIGNACION' },
  { title: 'Devolución', value: 'DEVOLUCION' },
  { title: 'Envío a Mantenimiento', value: 'MANTENIMIENTO' },
  { title: 'Retorno de Mantenimiento', value: 'RETORNO' },
  { title: 'Baja de Activo', value: 'BAJA_ACTIVO' }
]

const snackbar = ref({
  show: false,
  text: '',
  color: 'success'
})

// ============================================================================
// COMPUTED
// ============================================================================

/**
 * Total de registros cargados
 */
const totalRegistros = computed(() => movimientos.value.length)

/**
 * Registros filtrados según los criterios
 */
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
    fechaHasta.setHours(23, 59, 59, 999) // Incluir todo el día
    resultado = resultado.filter(mov => new Date(mov.fecha_movimiento) <= fechaHasta)
  }

  return resultado
})

/**
 * Registros para la página actual
 */
const registrosPaginados = computed(() => {
  const inicio = (paginaActual.value - 1) * registrosPorPagina
  const fin = inicio + registrosPorPagina
  return registrosFiltrados.value.slice(inicio, fin)
})

/**
 * Total de páginas según los registros filtrados
 */
const totalPaginas = computed(() => {
  return Math.ceil(registrosFiltrados.value.length / registrosPorPagina)
})

/**
 * Lista de filtros activos para mostrar chips
 */
const filtrosActivos = computed(() => {
  const activos = []

  if (filtros.value.busqueda) {
    activos.push({ key: 'busqueda', label: 'Búsqueda', value: filtros.value.busqueda })
  }

  if (filtros.value.tipoMovimiento) {
    const tipo = tiposMovimiento.find(t => t.value === filtros.value.tipoMovimiento)
    activos.push({ key: 'tipoMovimiento', label: 'Tipo', value: tipo?.title })
  }

  if (filtros.value.usuario) {
    const usuario = usuarios.value.find(u => u.id === filtros.value.usuario)
    activos.push({ key: 'usuario', label: 'Usuario', value: usuario?.nombre_completo })
  }

  if (filtros.value.fechaDesde) {
    activos.push({ key: 'fechaDesde', label: 'Desde', value: filtros.value.fechaDesde })
  }

  if (filtros.value.fechaHasta) {
    activos.push({ key: 'fechaHasta', label: 'Hasta', value: filtros.value.fechaHasta })
  }

  return activos
})

// ============================================================================
// MÉTODOS - API
// ============================================================================

/**
 * Carga todos los movimientos desde la API
 */
async function cargarMovimientos() {
  loading.value = true
  try {
    const response = await apiClient.get('/api/historial-movimientos/', {
      params: {
        ordering: '-fecha_movimiento',
        page_size: 1000
      }
    })

    movimientos.value = Array.isArray(response.data)
      ? response.data
      : response.data.results || []

    // Si hay paginación, obtener todas las páginas
    if (response.data.next) {
      await cargarTodasLasPaginas(response.data.next)
    }

  } catch (error) {
    console.error('Error al cargar movimientos:', error)
    mostrarNotificacion('Error al cargar el historial', 'error')
  } finally {
    loading.value = false
  }
}

/**
 * Carga todas las páginas si la API está paginada
 */
async function cargarTodasLasPaginas(nextUrl) {
  try {
    while (nextUrl) {
      const response = await apiClient.get(nextUrl)
      const nuevosMovimientos = Array.isArray(response.data) ? response.data : response.data.results || []
      movimientos.value = [...movimientos.value, ...nuevosMovimientos]
      nextUrl = response.data.next || null
    }
  } catch (error) {
    console.error('Error al cargar páginas adicionales:', error)
  }
}

/**
 * Carga los usuarios para el filtro
 */
async function cargarUsuarios() {
  try {
    const response = await apiClient.get('/api/usuarios/', {
      params: { page_size: 1000 }
    })
    usuarios.value = Array.isArray(response.data) ? response.data : response.data.results || []
  } catch (error) {
    console.error('Error al cargar usuarios:', error)
  }
}

// ============================================================================
// MÉTODOS - FILTROS Y PAGINACIÓN
// ============================================================================

/**
 * Aplica los filtros y resetea a la primera página
 */
function aplicarFiltros() {
  paginaActual.value = 1
}

/**
 * Limpia todos los filtros
 */
function limpiarFiltros() {
  filtros.value = {
    busqueda: '',
    tipoMovimiento: null,
    usuario: null,
    fechaDesde: null,
    fechaHasta: null
  }
  paginaActual.value = 1
}

/**
 * Remueve un filtro específico
 */
function removerFiltro(key) {
  filtros.value[key] = key === 'busqueda' ? '' : null
  aplicarFiltros()
}

/**
 * Cambia de página
 */
function cambiarPagina(pagina) {
  paginaActual.value = pagina
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// ============================================================================
// MÉTODOS - HELPERS
// ============================================================================

/**
 * Retorna el color según el tipo de movimiento
 */
function getColorByTipo(tipo) {
  const colores = {
    'TRASLADO': 'primary',
    'ASIGNACION': 'success',
    'DEVOLUCION': 'info',
    'MANTENIMIENTO': 'warning',
    'RETORNO': 'success',
    'BAJA': 'error'
  }
  return colores[tipo] || 'grey'
}

/**
 * Retorna el icono según el tipo de movimiento
 */
function getIconByTipo(tipo) {
  const iconos = {
    'TRASLADO': 'mdi-swap-horizontal',
    'ASIGNACION': 'mdi-account-check',
    'DEVOLUCION': 'mdi-keyboard-return',
    'MANTENIMIENTO': 'mdi-wrench',
    'RETORNO': 'mdi-check-circle',
    'BAJA': 'mdi-delete'
  }
  return iconos[tipo] || 'mdi-help-circle'
}

/**
 * Convierte el tipo de movimiento a texto legible
 */
function getTipoMovimientoTexto(tipo) {
  const textos = {
    'TRASLADO': 'Traslado',
    'ASIGNACION': 'Asignación',
    'DEVOLUCION': 'Devolución',
    'MANTENIMIENTO': 'Mantenimiento',
    'RETORNO': 'Retorno',
    'BAJA': 'Baja'
  }
  return textos[tipo] || tipo
}

/**
 * Obtiene el nombre del activo
 */
function getActivoNombre(movimiento) {
  if (movimiento.activo) {
    return `${movimiento.activo.marca} ${movimiento.activo.modelo}` || movimiento.activo.codigo_inventario
  }
  return 'Activo desconocido'
}

/**
 * Formatea la fecha a formato legible
 */
function formatearFecha(fechaISO) {
  const fecha = new Date(fechaISO)
  return fecha.toLocaleString('es-ES', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

/**
 * Exporta el historial a Excel
 */
function exportarHistorial() {
  // TODO: Implementar exportación a Excel
  mostrarNotificacion('Función de exportación en desarrollo', 'info')
  console.log('Exportando', registrosFiltrados.value.length, 'registros')
}

/**
 * Muestra una notificación
 */
function mostrarNotificacion(text, color = 'success') {
  snackbar.value = {
    show: true,
    text,
    color
  }
}

function volver() {
  router.back()
}

// ============================================================================
// LIFECYCLE HOOKS
// ============================================================================

onMounted(async () => {
  await Promise.all([
    cargarMovimientos(),
    cargarUsuarios()
  ])
})

</script>

<style scoped>
/* ============================================================================
   CONTENEDOR PRINCIPAL
   ============================================================================ */

.historial-content {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 1rem;
  padding-bottom: 2rem;
}

/* ============================================================================
   LOADING STATE
   ============================================================================ */

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 1rem;
  color: #666;
}

/* ============================================================================
   EMPTY STATE
   ============================================================================ */

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: #999;
}

/* ============================================================================
   RESPONSIVE
   ============================================================================ */

@media (max-width: 600px) {
  .historial-content {
    padding: 0.75rem;
  }
}

@media (min-width: 960px) {
  .historial-content {
    max-width: 1200px;
    margin: 0 auto;
  }
}
</style>
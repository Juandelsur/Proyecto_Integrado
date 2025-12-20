<template>
  <div class="technician-home-content">
    <!-- ====================================================================
         1. TARJETA DE BIENVENIDA (Header)
         ==================================================================== -->
    <v-card variant="tonal" color="primary" class="mb-4">
      <v-card-text>
        <h2 class="text-h5 font-weight-bold mb-1">Hola, desde Admin {{ userName }}</h2>
        <p class="text-subtitle-1 mb-0">{{ fechaActual }}</p>
      </v-card-text>
    </v-card>

    <!-- ====================================================================
         2. DASHBOARD DE ESTADO DE ACTIVOS
         ==================================================================== -->
    <v-card class="mb-4">
      <v-card-title class="text-h6 font-weight-bold">
        Estado de Activos
      </v-card-title>
      <v-card-subtitle class="pb-2">
        Total de activos: <strong>{{ totalActivos }}</strong>
      </v-card-subtitle>
      <v-card-text>
        <!-- Grid de tarjetas de estado -->
        <v-row>
          <v-col
            v-for="(activo, index) in activos"
            :key="index"
            cols="12"
            sm="6"
            md="3"
          >
            <v-card
              :color="activo.color"
              dark
              class="status-card"
              elevation="4"
            >
              <v-card-text>
                <div class="d-flex justify-space-between align-start mb-3">
                  <v-icon size="48" class="status-icon">
                    {{ activo.icon }}
                  </v-icon>
                  <div class="text-right">
                    <div class="text-h3 font-weight-bold">
                      {{ activo.cantidad }}
                    </div>
                  </div>
                </div>
                <div class="text-h6 font-weight-medium mb-2">
                  {{ activo.estado }}
                </div>
                <v-divider class="my-2 border-opacity-25"></v-divider>
                <div class="text-caption">
                  {{ calcularPorcentaje(activo.cantidad) }}% del total
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <!-- Resumen compacto CON FILTRO POR DEPARTAMENTO -->
        <v-card variant="tonal" class="mt-4">
          <v-card-title class="text-subtitle-1 font-weight-bold d-flex justify-space-between align-center">
            <span>Resumen por Ubicación</span>
          </v-card-title>
          <v-card-text>
            <!-- Filtro de Departamento -->
            <v-select
              v-model="filtroDepartamento"
              :items="departamentosDisponibles"
              item-title="nombre_ubicacion"
              item-value="id"
              label="Filtrar por Departamento"
              variant="outlined"
              density="comfortable"
              clearable
              prepend-inner-icon="mdi-office-building"
              class="mb-3"
              @update:model-value="filtrarActivosPorDepartamento"
            ></v-select>

            <!-- Lista de resumen filtrada -->
            <v-list density="compact" class="bg-transparent">
              <v-list-item
                v-for="(activo, index) in activosFiltrados"
                :key="index"
                class="px-0"
              >
                <template v-slot:prepend>
                  <v-avatar :color="activo.color" size="16" class="mr-3"></v-avatar>
                </template>
                <v-list-item-title>{{ activo.estado }}</v-list-item-title>
                <template v-slot:append>
                  <strong>{{ activo.cantidad }}</strong>
                </template>
              </v-list-item>
            </v-list>

            <!-- Mensaje si no hay resultados -->
            <div v-if="activosFiltrados.every(a => a.cantidad === 0)" class="text-center py-4">
              <v-icon size="48" color="grey-lighten-1">mdi-filter-off</v-icon>
              <p class="text-body-2 text-grey mt-2">No hay activos en este departamento</p>
            </div>
          </v-card-text>
        </v-card>
      </v-card-text>
    </v-card>

    <!-- ====================================================================
         3. FEED DE ACTIVIDAD DEL EQUIPO (COLAPSABLE)
         ==================================================================== -->
    <v-card>
      <v-card-title class="text-h6 font-weight-bold d-flex justify-space-between align-center">
        <span>Últimos Movimientos del Equipo</span>
        <v-btn
          :icon="movimientosExpandido ? 'mdi-chevron-up' : 'mdi-chevron-down'"
          variant="text"
          @click="movimientosExpandido = !movimientosExpandido"
        ></v-btn>
      </v-card-title>

      <!-- Contenido colapsable -->
      <v-expand-transition>
        <v-card-text v-show="movimientosExpandido">
          <!-- Estado de carga -->
          <div v-if="loading" class="text-center py-8">
            <v-progress-circular indeterminate color="primary"></v-progress-circular>
            <p class="mt-4 text-body-2">Cargando movimientos...</p>
          </div>

          <!-- Error -->
          <v-alert v-else-if="error" type="error" variant="tonal" class="mb-4">
            {{ error }}
          </v-alert>

          <!-- Lista de movimientos -->
          <v-list v-else-if="ultimosMovimientos.length > 0" lines="three">
            <v-list-item
              v-for="(movimiento, index) in ultimosMovimientos"
              :key="index"
              class="mb-2"
            >
              <template v-slot:prepend>
                <v-avatar :color="getColorByTipo(movimiento.tipo_movimiento)">
                  <v-icon>{{ getIconByTipo(movimiento.tipo_movimiento) }}</v-icon>
                </v-avatar>
              </template>

              <v-list-item-title class="font-weight-medium">
                {{ getActivoNombre(movimiento) }}
              </v-list-item-title>
              <v-list-item-subtitle>
                {{ getDescripcionMovimiento(movimiento) }}
              </v-list-item-subtitle>
            </v-list-item>
          </v-list>

          <!-- Sin datos -->
          <div v-else class="text-center py-8">
            <v-icon size="64" color="grey-lighten-1">mdi-inbox</v-icon>
            <p class="text-body-1 mt-2">No hay movimientos registrados</p>
          </div>
        </v-card-text>
      </v-expand-transition>

      <!-- Mini indicador cuando está colapsado -->
      <v-card-text v-if="!movimientosExpandido" class="py-2 text-center">
        <v-chip size="small" color="primary" variant="tonal">
          {{ ultimosMovimientos.length }} movimiento{{ ultimosMovimientos.length !== 1 ? 's' : '' }} registrado{{ ultimosMovimientos.length !== 1 ? 's' : '' }}
        </v-chip>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup>
/**
 * ============================================================================
 * TÉCNICO HOME VIEW - DASHBOARD OPERATIVO MEJORADO
 * ============================================================================
 *
 * Vista principal del técnico con:
 * 1. Tarjeta de bienvenida con fecha actual
 * 2. Dashboard de estado de activos (Operativos, En Reparación, En Bodega, De Baja)
 * 3. Resumen compacto CON FILTRO POR DEPARTAMENTO
 * 4. Feed de actividad COLAPSABLE con los últimos 15 movimientos del equipo
 *
 * RESTRICCIÓN: NO incluye barras de navegación (gestionadas por LayoutTecnico.vue)
 */

import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import apiClient from '@/services/api'

// ============================================================================
// COMPOSABLES
// ============================================================================

const router = useRouter()
const authStore = useAuthStore()

// ============================================================================
// STATE
// ============================================================================

const ultimosMovimientos = ref([])
const loading = ref(false)
const error = ref(null)
const movimientosExpandido = ref(true) // Por defecto expandido
const filtroDepartamento = ref(null)
const ubicaciones = ref([])

// Datos del dashboard de activos (se llenarán desde la API)
const activos = ref([
  {
    estado: 'Operativos',
    cantidad: 0,
    color: 'green',
    icon: 'mdi-check-circle',
    estados_incluidos: ['activo', 'operativo', 'disponible']
  },
  {
    estado: 'En Reparación',
    cantidad: 0,
    color: 'amber',
    icon: 'mdi-wrench',
    estados_incluidos: ['mantenimiento', 'mantención', 'reparación', 'reparacion']
  },
  {
    estado: 'En Bodega',
    cantidad: 0,
    color: 'blue',
    icon: 'mdi-package-variant',
    estados_incluidos: ['bodega', 'almacén', 'almacen', 'stock']
  },
  {
    estado: 'De Baja',
    cantidad: 0,
    color: 'red',
    icon: 'mdi-close-circle',
    estados_incluidos: ['baja', 'inactivo', 'retirado', 'descartado']
  }
])

// Lista completa de activos desde la API
const activosCompletos = ref([])

// ============================================================================
// COMPUTED PROPERTIES
// ============================================================================

/**
 * Obtiene el nombre del usuario desde el store
 */
const userName = computed(() => {
  return authStore.user?.nombre_completo || authStore.user?.username || 'Usuario'
})

/**
 * Genera la fecha actual formateada en español
 * Ejemplo: "Lunes, 25 de Noviembre de 2024"
 */
const fechaActual = computed(() => {
  const fecha = new Date()
  const opciones = {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }

  return fecha.toLocaleDateString('es-ES', opciones)
    .split(' ')
    .map((palabra, index) => index === 0 ? palabra.charAt(0).toUpperCase() + palabra.slice(1) : palabra)
    .join(' ')
})

/**
 * Calcula el total de activos
 */
const totalActivos = computed(() => {
  return activos.value.reduce((sum, item) => sum + item.cantidad, 0)
})

/**
 * Obtiene los departamentos únicos disponibles
 */
const departamentosDisponibles = computed(() => {
  return ubicaciones.value
})

/**
 * Activos filtrados por departamento seleccionado
 */
const activosFiltrados = computed(() => {
  if (!filtroDepartamento.value) {
    return activos.value
  }

  // Crear una copia de activos con cantidades filtradas
  return activos.value.map(categoria => {
    const activosFiltradosPorDepartamento = activosCompletos.value.filter(activo => {
      const estadoNombre = activo.estado?.nombre_estado?.toLowerCase() || ''
      const perteneceCategoria = categoria.estados_incluidos.some(estado => 
        estadoNombre.includes(estado)
      )
      const perteneceUbicacion = activo.ubicacion_actual?.id === filtroDepartamento.value

      return perteneceCategoria && perteneceUbicacion
    })

    return {
      ...categoria,
      cantidad: activosFiltradosPorDepartamento.length
    }
  })
})

// ============================================================================
// MÉTODOS - NAVEGACIÓN
// ============================================================================

/**
 * Navega a una ruta específica
 */
function navigateTo(path) {
  router.push(path)
}

// ============================================================================
// MÉTODOS - CÁLCULOS DEL DASHBOARD
// ============================================================================

/**
 * Calcula el porcentaje que representa cada categoría
 */
function calcularPorcentaje(cantidad) {
  if (totalActivos.value === 0) return '0.0'
  return ((cantidad / totalActivos.value) * 100).toFixed(1)
}

/**
 * Filtra los activos cuando cambia el departamento
 */
function filtrarActivosPorDepartamento() {
  // El computed activosFiltrados se encarga automáticamente
  console.log('Filtrando por departamento:', filtroDepartamento.value)
}

// ============================================================================
// MÉTODOS - API
// ============================================================================

/**
 * Carga las ubicaciones/departamentos desde la API
 */
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

/**
 * Obtiene todos los activos desde la API y los agrupa por estado
 */
async function fetchActivos() {
  try {
    // Opción 1: Intentar obtener todos los registros con page_size grande
    const response = await apiClient.get('/api/activos/', {
      params: {
        page_size: 1000 // Ajusta este número según tu necesidad
      }
    })
    
    activosCompletos.value = Array.isArray(response.data) ? response.data : response.data.results || []
    
    // Si la respuesta está paginada y hay más páginas, obtenerlas todas
    if (response.data.next) {
      await fetchTodasLasPaginas(response.data.next)
    }
    
    // Agrupar activos por estado
    agruparActivosPorEstado()
  } catch (err) {
    console.error('Error al cargar activos:', err)
    error.value = 'No se pudieron cargar los activos. Verifica tu conexión.'
  }
}

/**
 * Función auxiliar para obtener todas las páginas si la API está paginada
 */
async function fetchTodasLasPaginas(nextUrl) {
  try {
    while (nextUrl) {
      const response = await apiClient.get(nextUrl)
      const nuevosActivos = Array.isArray(response.data) ? response.data : response.data.results || []
      activosCompletos.value = [...activosCompletos.value, ...nuevosActivos]
      nextUrl = response.data.next || null
    }
  } catch (err) {
    console.error('Error al cargar páginas adicionales:', err)
  }
}

/**
 * Agrupa los activos en las categorías del dashboard según su estado
 */
function agruparActivosPorEstado() {
  // Resetear contadores
  activos.value.forEach(categoria => {
    categoria.cantidad = 0
  })

  // Contar activos por estado
  activosCompletos.value.forEach(activo => {
    const estadoNombre = activo.estado?.nombre_estado?.toLowerCase() || ''
    
    // Buscar en qué categoría encaja este estado
    const categoria = activos.value.find(cat => 
      cat.estados_incluidos.some(estado => estadoNombre.includes(estado))
    )
    
    if (categoria) {
      categoria.cantidad++
    }
  })
}

/**
 * Obtiene los últimos 15 movimientos del historial
 */
async function fetchMovimientos() {
  loading.value = true
  error.value = null

  try {
    // GET /api/historial-movimientos/?ordering=-fecha_movimiento&limit=15
    const response = await apiClient.get('/api/historial-movimientos/', {
      params: {
        ordering: '-fecha_movimiento',
        page_size: 15
      }
    })

    ultimosMovimientos.value = response.data.results || response.data

  } catch (err) {
    console.error('Error al cargar movimientos:', err)
    error.value = 'No se pudieron cargar los movimientos. Verifica tu conexión.'
  } finally {
    loading.value = false
  }
}

// ============================================================================
// MÉTODOS - HELPERS DE VISUALIZACIÓN
// ============================================================================

/**
 * Retorna el color del avatar según el tipo de movimiento
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
 * Obtiene el nombre del activo desde el objeto movimiento
 */
function getActivoNombre(movimiento) {
  if (movimiento.activo) {
    return `${movimiento.activo.marca} ${movimiento.activo.modelo}` || movimiento.activo.codigo_inventario
  }

  return movimiento.codigo_activo || 'Activo desconocido'
}

/**
 * Genera la descripción del movimiento
 */
function getDescripcionMovimiento(movimiento) {
  const accion = getTipoMovimientoTexto(movimiento.tipo_movimiento)
  const destino = movimiento.ubicacion_destino?.nombre_ubicacion || 'Ubicación desconocida'
  const usuario = movimiento.usuario_registra?.nombre_completo || movimiento.nombre_usuario || 'Usuario'
  const tiempo = getTimeAgo(movimiento.fecha_movimiento)

  return `${accion} a ${destino} por ${usuario} • ${tiempo}`
}

/**
 * Convierte el tipo de movimiento a texto legible
 */
function getTipoMovimientoTexto(tipo) {
  const textos = {
    'TRASLADO': 'Trasladado',
    'ASIGNACION': 'Asignado',
    'DEVOLUCION': 'Devuelto',
    'MANTENIMIENTO': 'Enviado a mantenimiento',
    'RETORNO': 'Retornado',
    'BAJA': 'Dado de baja'
  }

  return textos[tipo] || tipo
}

/**
 * Calcula el tiempo transcurrido desde una fecha
 */
function getTimeAgo(fechaISO) {
  const fecha = new Date(fechaISO)
  const ahora = new Date()
  const diffMs = ahora - fecha
  const diffMinutos = Math.floor(diffMs / 60000)

  if (diffMinutos < 1) return 'Ahora'
  if (diffMinutos < 60) return `Hace ${diffMinutos} min`

  const diffHoras = Math.floor(diffMinutos / 60)
  if (diffHoras < 24) return `Hace ${diffHoras} h`

  const diffDias = Math.floor(diffHoras / 24)
  if (diffDias === 1) return 'Ayer'
  if (diffDias < 7) return `Hace ${diffDias} días`

  return fecha.toLocaleDateString('es-ES', { day: 'numeric', month: 'short' })
}

// ============================================================================
// LIFECYCLE HOOKS
// ============================================================================

/**
 * Al montar el componente, cargar los activos y movimientos
 */
onMounted(async () => {
  // Cargar ubicaciones para el filtro
  await fetchUbicaciones()
  // Cargar activos primero para el dashboard
  await fetchActivos()
  // Luego cargar los movimientos
  await fetchMovimientos()
})

</script>

<style scoped>
/* ============================================================================
   CONTENEDOR PRINCIPAL
   ============================================================================ */

.technician-home-content {
  min-height: calc(100vh - 112px);
  background: #f5f7fa;
  padding: 1rem;
  padding-bottom: 80px;
}

/* ============================================================================
   TARJETAS DE ESTADO
   ============================================================================ */

.status-card {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  height: 100%;
  cursor: pointer;
}

.status-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.25) !important;
}

.status-card:active {
  transform: translateY(-2px);
}

.status-icon {
  opacity: 0.8;
}

/* ============================================================================
   RESPONSIVE ADJUSTMENTS
   ============================================================================ */

@media (max-width: 600px) {
  .technician-home-content {
    padding: 0.75rem;
  }
}

@media (min-width: 960px) {
  .technician-home-content {
    max-width: 1200px;
    margin: 0 auto;
  }
}
</style>
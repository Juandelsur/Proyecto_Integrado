<template>
  <div class="technician-home-content">
    <!-- ====================================================================
         1. TARJETA DE BIENVENIDA (Header)
         ==================================================================== -->
    <v-card variant="tonal" color="primary" class="mb-4">
      <v-card-text>
        <h2 class="text-h5 font-weight-bold mb-1">Hola, {{ userName }}</h2>
        <p class="text-subtitle-1 mb-0">{{ fechaActual }}</p>
      </v-card-text>
    </v-card>

    <!-- ====================================================================
         2. ACCESOS RÁPIDOS DE GESTIÓN (Grid)
         ==================================================================== -->
    <v-row class="mb-4">
      <!-- Botón 1: Crear Activo -->
      <v-col cols="6">
        <v-card
          class="action-card"
          hover
          ripple
          @click="navigateTo('/tecnico/crear')"
        >
          <v-card-text class="text-center pa-4">
            <v-icon size="64" color="primary" class="mb-2">mdi-plus-box</v-icon>
            <p class="text-subtitle-1 font-weight-medium mb-0">Crear Activo</p>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Botón 2: Editar Activos -->
      <v-col cols="6">
        <v-card
          class="action-card"
          hover
          ripple
          @click="navigateTo('/tecnico/editar-buscar')"
        >
          <v-card-text class="text-center pa-4">
            <v-icon size="64" color="info" class="mb-2">mdi-pencil-box-multiple</v-icon>
            <p class="text-subtitle-1 font-weight-medium mb-0">Editar Activos</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- ====================================================================
         3. FEED DE ACTIVIDAD DEL EQUIPO (Listado)
         ==================================================================== -->
    <v-card>
      <v-card-title class="text-h6 font-weight-bold">
        Últimos Movimientos del Equipo
      </v-card-title>

      <!-- Loading State -->
      <v-card-text v-if="loading" class="text-center py-8">
        <v-progress-circular indeterminate color="primary"></v-progress-circular>
        <p class="text-body-2 mt-4">Cargando movimientos...</p>
      </v-card-text>

      <!-- Error State -->
      <v-card-text v-else-if="error" class="text-center py-8">
        <v-icon size="48" color="error" class="mb-2">mdi-alert-circle</v-icon>
        <p class="text-body-1 text-error">{{ error }}</p>
        <v-btn color="primary" variant="text" @click="fetchMovimientos">
          Reintentar
        </v-btn>
      </v-card-text>

      <!-- Empty State -->
      <v-card-text v-else-if="ultimosMovimientos.length === 0" class="text-center py-8">
        <v-icon size="48" color="grey" class="mb-2">mdi-inbox</v-icon>
        <p class="text-body-1 text-grey">No hay movimientos registrados</p>
      </v-card-text>

      <!-- Lista de Movimientos -->
      <v-list v-else lines="two">
        <v-list-item
          v-for="movimiento in ultimosMovimientos"
          :key="movimiento.id"
        >
          <!-- Avatar con color semántico según tipo de acción -->
          <template v-slot:prepend>
            <v-avatar :color="getColorByTipo(movimiento.tipo_movimiento)">
              <v-icon color="white">{{ getIconByTipo(movimiento.tipo_movimiento) }}</v-icon>
            </v-avatar>
          </template>

          <!-- Contenido del ítem -->
          <v-list-item-title class="font-weight-medium">
            {{ getActivoNombre(movimiento) }}
          </v-list-item-title>
          <v-list-item-subtitle>
            {{ getDescripcionMovimiento(movimiento) }}
          </v-list-item-subtitle>
        </v-list-item>
      </v-list>

      <!-- Footer: Botón Ver Historial Completo -->
      <v-card-actions v-if="ultimosMovimientos.length > 0">
        <v-btn
          variant="text"
          color="primary"
          block
          @click="navigateTo('/tecnico/history')"
        >
          Ver Historial Completo
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script setup>
/**
 * ============================================================================
 * TÉCNICO HOME VIEW - DASHBOARD OPERATIVO
 * ============================================================================
 *
 * Vista principal del técnico con:
 * 1. Tarjeta de bienvenida con fecha actual
 * 2. Accesos rápidos a Crear y Editar activos
 * 3. Feed de actividad con los últimos 15 movimientos del equipo
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
// MÉTODOS - API
// ============================================================================

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
        ordering: '-fecha_movimiento', // Ordenar por fecha descendente
        page_size: 15 // Limitar a 15 resultados
      }
    })

    // La respuesta puede ser paginada o un array directo
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
    'TRASLADO': 'primary',      // Azul
    'ASIGNACION': 'success',     // Verde
    'DEVOLUCION': 'info',        // Azul claro
    'MANTENIMIENTO': 'warning',  // Naranja
    'RETORNO': 'success',        // Verde
    'BAJA': 'error'              // Rojo
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
  // El serializer devuelve el objeto activo completo
  if (movimiento.activo) {
    return `${movimiento.activo.marca} ${movimiento.activo.modelo}` || movimiento.activo.codigo_inventario
  }

  return movimiento.codigo_activo || 'Activo desconocido'
}

/**
 * Genera la descripción del movimiento
 * Formato: "Acción por Usuario • Tiempo"
 * Ejemplo: "Movido a Bodega por Juan • Hace 10 min"
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
 * Retorna: "Hace X minutos/horas/días"
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

  // Si es más de una semana, mostrar la fecha
  return fecha.toLocaleDateString('es-ES', { day: 'numeric', month: 'short' })
}

// ============================================================================
// LIFECYCLE HOOKS
// ============================================================================

/**
 * Al montar el componente, cargar los movimientos
 */
onMounted(() => {
  fetchMovimientos()
})
</script>

<style scoped>
/* ============================================================================
   CONTENEDOR PRINCIPAL (ADAPTADO PARA LAYOUT)
   ============================================================================ */

.technician-home-content {
  min-height: calc(100vh - 112px); /* Altura total - app bar - bottom nav */
  background: #f5f7fa;
  padding: 1rem;
  padding-bottom: 80px; /* Espacio para el FAB flotante */
}

/* ============================================================================
   TARJETAS DE ACCIÓN RÁPIDA
   ============================================================================ */

.action-card {
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  height: 100%;
}

.action-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15) !important;
}

.action-card:active {
  transform: translateY(-2px);
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
    max-width: 800px;
    margin: 0 auto;
  }
}
</style>


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
         2. ACCESOS RÁPIDOS DE GESTIÓN (Grid de 3 columnas)
         ==================================================================== -->
    <v-row class="mb-4">
      <!-- Escanear QR -->
      <v-col cols="12" sm="4">
        <v-card
          class="action-card"
          hover
          ripple
          @click="navigateTo('/tecnico/scan')"
        >
          <v-card-text class="text-center pa-6">
            <v-avatar size="80" color="success" class="mb-3">
              <v-icon size="48">mdi-qrcode-scan</v-icon>
            </v-avatar>
            <p class="text-h6 font-weight-bold mb-1">Escanear QR</p>
            <p class="text-caption text-grey">Registrar movimientos</p>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Crear Activo -->
      <v-col cols="12" sm="4">
        <v-card
          class="action-card"
          hover
          ripple
          @click="navigateTo('/tecnico/activos/crear')"
        >
          <v-card-text class="text-center pa-6">
            <v-avatar size="80" color="primary" class="mb-3">
              <v-icon size="48">mdi-plus-circle</v-icon>
            </v-avatar>
            <p class="text-h6 font-weight-bold mb-1">Crear Activo</p>
            <p class="text-caption text-grey">Registrar nuevo equipo</p>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Editar Activo -->
      <v-col cols="12" sm="4">
        <v-card
          class="action-card"
          hover
          ripple
          @click="navigateTo('/tecnico/activos/actualizar-activo')"
        >
          <v-card-text class="text-center pa-6">
            <v-avatar size="80" color="warning" class="mb-3">
              <v-icon size="48">mdi-pencil</v-icon>
            </v-avatar>
            <p class="text-h6 font-weight-bold mb-1">Editar Activo</p>
            <p class="text-caption text-grey">Modificar información</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- ====================================================================
         3. FEED DE ACTIVIDAD DEL EQUIPO (COLAPSABLE)
         ==================================================================== -->
    <v-card>
      <v-card-title class="d-flex justify-space-between align-center flex-wrap">
        <span class="text-h6 font-weight-bold">Últimos Movimientos del Equipo</span>
        <div class="d-flex align-center gap-2">
          <v-btn
            variant="tonal"
            color="primary"
            size="small"
            prepend-icon="mdi-history"
            @click="navigateTo('/tecnico/historial')"
          >
            Ver Historial
          </v-btn>
          <v-btn
            :icon="movimientosExpandido ? 'mdi-chevron-up' : 'mdi-chevron-down'"
            variant="text"
            size="small"
            @click="movimientosExpandido = !movimientosExpandido"
          ></v-btn>
        </div>
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
 * TÉCNICO HOME VIEW - DASHBOARD OPERATIVO
 * ============================================================================
 *
 * Vista principal del técnico con:
 * 1. Tarjeta de bienvenida con fecha actual
 * 2. Tres accesos rápidos: Escanear QR, Crear Activo, Editar Activo
 * 3. Feed de actividad con los últimos 15 movimientos del equipo
 * 4. Botón para ver el historial completo
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
const movimientosExpandido = ref(true) // Por defecto expandido
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
  max-width: 9000px;
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
  border: 2px solid transparent;
}

.action-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15) !important;
  border-color: rgba(25, 118, 210, 0.3);
}

.action-card:active {
  transform: translateY(-2px);
}

/* ============================================================================
   UTILIDADES
   ============================================================================ */

.gap-2 {
  gap: 0.5rem;
}

/* ============================================================================
   RESPONSIVE ADJUSTMENTS
   ============================================================================ */

@media (max-width: 600px) {
  .technician-home-content {
    padding: 0.75rem;
  }

  .action-card .text-h6 {
    font-size: 1rem !important;
  }

  .action-card v-avatar {
    width: 64px !important;
    height: 64px !important;
  }

  .action-card .v-icon {
    font-size: 36px !important;
  }
}

@media (min-width: 960px) {
  .technician-home-content {
    max-width: 1000px;
    margin: 0 auto;
  }
}
</style>
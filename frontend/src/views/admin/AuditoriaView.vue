<template>
  <div class="crud-entidad-content">
    <!-- ====================================================================
         HEADER CON TÍTULO
         ==================================================================== -->
    <div class="header-section">
      <h1 class="entity-title">Auditoría del Sistema</h1>
    </div>

    <!-- ====================================================================
         BARRA DE BÚSQUEDA Y FILTROS
         ==================================================================== -->
    <div class="filters-section">
      <v-text-field
        v-model="busqueda"
        prepend-inner-icon="mdi-magnify"
        label="Buscar por usuario, acción o detalle"
        variant="outlined"
        density="comfortable"
        clearable
        @input="buscarLogs"
      ></v-text-field>

      <v-select
        v-model="ordenamiento"
        :items="opcionesOrdenamiento"
        label="Ordenar por"
        variant="outlined"
        density="comfortable"
        prepend-inner-icon="mdi-sort"
        @update:model-value="cargarLogs"
      ></v-select>

      <v-btn
        color="blue"
        size="large"
        prepend-icon="mdi-refresh"
        @click="cargarLogs"
      >
        Actualizar
      </v-btn>
    </div>

    <!-- ====================================================================
         LOADING STATE
         ==================================================================== -->
    <div v-if="loading" class="loading-container">
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
      <p class="mt-3">Cargando logs de auditoría...</p>
    </div>

    <!-- ====================================================================
         LISTA DE LOGS
         ==================================================================== -->
    <div v-else class="registros-lista">
      <div
        v-for="log in logs"
        :key="log.id"
        class="registro-item"
      >
        <div class="log-badge-container">
          <v-chip
            :color="getAccionColor(log.accion)"
            size="small"
            label
          >
            {{ getAccionLabel(log.accion) }}
          </v-chip>
        </div>

        <div class="registro-info">
          <div class="registro-nombre">
            {{ log.usuario_nombre_completo }}
            <span class="usuario-username">@{{ log.usuario_username }}</span>
          </div>
          <div class="registro-detalles">
            <span class="detalle-accion">{{ log.detalle_accion }}</span>
          </div>
          <div class="registro-timestamp">
            <v-icon size="small" class="mr-1">mdi-clock-outline</v-icon>
            {{ formatTimestamp(log.timestamp) }}
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="logs.length === 0" class="empty-state">
        <v-icon size="64" color="grey-lighten-1">mdi-history</v-icon>
        <p>No hay logs de auditoría disponibles</p>
      </div>
    </div>

    <!-- ====================================================================
         PAGINACIÓN
         ==================================================================== -->
    <div v-if="totalPaginas > 1" class="pagination-section">
      <v-btn
        :disabled="paginaActual === 1"
        variant="outlined"
        prepend-icon="mdi-chevron-left"
        @click="cambiarPagina(paginaActual - 1)"
      >
        Anterior
      </v-btn>

      <span class="pagination-info">
        Página {{ paginaActual }} de {{ totalPaginas }}
      </span>

      <v-btn
        :disabled="paginaActual === totalPaginas"
        variant="outlined"
        append-icon="mdi-chevron-right"
        @click="cambiarPagina(paginaActual + 1)"
      >
        Siguiente
      </v-btn>
    </div>

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
         SNACKBAR NOTIFICACIONES
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
 * AUDITORÍA DEL SISTEMA - REGISTRO DE ACCIONES DE USUARIOS
 * ============================================================================
 *
 * Funcionalidades:
 * - Listar logs de auditoría
 * - Buscar logs
 * - Ordenar logs
 * - Paginación
 */

import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/services/api'

// ============================================================================
// COMPOSABLES
// ============================================================================

const router = useRouter()

// ============================================================================
// STATE
// ============================================================================

const logs = ref([])
const loading = ref(false)
const busqueda = ref('')
const ordenamiento = ref('-timestamp')
const paginaActual = ref(1)
const totalPaginas = ref(1)
const totalRegistros = ref(0)

const snackbar = ref({
  show: false,
  text: '',
  color: 'success'
})

const opcionesOrdenamiento = [
  { title: 'Más recientes', value: '-timestamp' },
  { title: 'Más antiguos', value: 'timestamp' },
  { title: 'Usuario A-Z', value: 'usuario_username' },
  { title: 'Usuario Z-A', value: '-usuario_username' },
  { title: 'Acción A-Z', value: 'accion' }
]

// ============================================================================
// MÉTODOS - API
// ============================================================================

/**
 * Carga los logs de auditoría desde la API
 */
async function cargarLogs() {
  loading.value = true
  try {
    const params = {
      page: paginaActual.value,
      ordering: ordenamiento.value
    }

    if (busqueda.value) {
      params.search = busqueda.value
    }

    const response = await apiClient.get('/api/auditoria-logs/', { params })
    
    logs.value = response.data.results || []
    totalRegistros.value = response.data.count || 0
    
    // Calcular total de páginas (asumiendo 10 registros por página)
    totalPaginas.value = Math.ceil(totalRegistros.value / 10)
      
  } catch (error) {
    console.error('Error al cargar logs de auditoría:', error)
    mostrarNotificacion('Error al cargar los logs de auditoría', 'error')
  } finally {
    loading.value = false
  }
}

// ============================================================================
// MÉTODOS - UI
// ============================================================================

/**
 * Realiza la búsqueda de logs
 */
function buscarLogs() {
  paginaActual.value = 1
  cargarLogs()
}

/**
 * Cambia de página en la paginación
 */
function cambiarPagina(pagina) {
  if (pagina >= 1 && pagina <= totalPaginas.value) {
    paginaActual.value = pagina
    cargarLogs()
  }
}

/**
 * Obtiene el color del chip según la acción
 */
function getAccionColor(accion) {
  const colores = {
    CREATE: 'green',
    UPDATE: 'blue',
    DELETE: 'red',
    VIEW: 'grey',
    LOGIN: 'purple',
    LOGOUT: 'orange'
  }
  return colores[accion] || 'grey'
}

/**
 * Obtiene la etiqueta traducida de la acción
 */
function getAccionLabel(accion) {
  const etiquetas = {
    CREATE: 'Crear',
    UPDATE: 'Actualizar',
    DELETE: 'Eliminar',
    VIEW: 'Ver',
    LOGIN: 'Inicio Sesión',
    LOGOUT: 'Cierre Sesión'
  }
  return etiquetas[accion] || accion
}

/**
 * Formatea el timestamp a formato legible
 */
function formatTimestamp(timestamp) {
  const date = new Date(timestamp)
  return new Intl.DateTimeFormat('es-CL', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  }).format(date)
}

/**
 * Muestra una notificación snackbar
 */
function mostrarNotificacion(text, color = 'success') {
  snackbar.value = {
    show: true,
    text,
    color
  }
}

/**
 * Vuelve a la página anterior
 */
function volver() {
  router.back()
}

// ============================================================================
// LIFECYCLE HOOKS
// ============================================================================

onMounted(async () => {
  await cargarLogs()
})

</script>

<style scoped>
/* ============================================================================
   CONTENEDOR PRINCIPAL
   ============================================================================ */

.crud-entidad-content {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 1rem;
  max-width: 9000px;
  margin: 0 auto;
  padding-bottom: 2rem;
}

/* ============================================================================
   HEADER
   ============================================================================ */

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  gap: 1rem;
}

.entity-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #333;
  margin: 0;
}

/* ============================================================================
   FILTROS Y BÚSQUEDA
   ============================================================================ */

.filters-section {
  display: grid;
  grid-template-columns: 1fr auto auto;
  gap: 1rem;
  margin-bottom: 1.5rem;
  align-items: start;
}

/* ============================================================================
   LISTA DE LOGS
   ============================================================================ */

.registros-lista {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 2rem;
}

.registro-item {
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  padding: 1rem;
  display: flex;
  gap: 1rem;
  transition: all 0.2s ease;
}

.registro-item:hover {
  border-color: #1976d2;
  box-shadow: 0 2px 8px rgba(25, 118, 210, 0.15);
}

.log-badge-container {
  flex-shrink: 0;
  display: flex;
  align-items: flex-start;
  padding-top: 0.25rem;
}

.registro-info {
  flex: 1;
  min-width: 0;
}

.registro-nombre {
  font-size: 1rem;
  color: #333;
  font-weight: 600;
  margin-bottom: 0.25rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.usuario-username {
  font-weight: 400;
  color: #666;
  font-size: 0.875rem;
  margin-left: 0.5rem;
}

.registro-detalles {
  font-size: 0.875rem;
  color: #555;
  margin-bottom: 0.5rem;
  line-height: 1.4;
}

.detalle-accion {
  display: block;
}

.registro-timestamp {
  font-size: 0.75rem;
  color: #999;
  display: flex;
  align-items: center;
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
  padding: 3rem 1rem;
  color: #999;
  gap: 1rem;
}

.empty-state p {
  font-size: 1rem;
  font-weight: 500;
}

/* ============================================================================
   PAGINACIÓN
   ============================================================================ */

.pagination-section {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.pagination-info {
  font-size: 0.875rem;
  color: #666;
  font-weight: 500;
}

/* ============================================================================
   FOOTER
   ============================================================================ */

.footer-section {
  display: flex;
  justify-content: flex-start;
  margin-top: 2rem;
}

.btn-volver {
  min-width: 120px;
  font-weight: 600;
}

/* ============================================================================
   RESPONSIVE
   ============================================================================ */

@media (max-width: 768px) {
  .filters-section {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 600px) {
  .crud-entidad-content {
    padding: 0.75rem;
  }

  .header-section {
    flex-direction: column;
    align-items: stretch;
  }

  .registro-item {
    flex-direction: column;
  }

  .log-badge-container {
    align-self: flex-start;
  }

  .pagination-section {
    flex-direction: column;
    gap: 0.5rem;
  }
}
</style>
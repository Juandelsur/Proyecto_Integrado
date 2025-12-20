<template>
  <div class="crud-entidad-content">
    <!-- ====================================================================
         HEADER CON TÍTULO Y BOTÓN NUEVO
         ==================================================================== -->
    <div class="header-section">
      <h1 class="entity-title">Gestión Ubicaciones</h1>
      <v-btn
        color="blue"
        size="large"
        class="btn-nuevo"
        prepend-icon="mdi-plus"
        @click="abrirModalCrear"
      >
        Nuevo
      </v-btn>
    </div>

    <!-- ====================================================================
         BARRA DE BÚSQUEDA Y FILTROS
         ==================================================================== -->
    <div class="search-section">
      <v-text-field
        v-model="busqueda"
        prepend-inner-icon="mdi-magnify"
        label="Buscar por nombre o código QR"
        variant="outlined"
        density="comfortable"
        clearable
        @input="filtrarRegistros"
        class="mb-3"
      ></v-text-field>

      <!-- Filtros Desplegables -->
      <v-row dense>
        <v-col cols="12" sm="6">
          <v-select
            v-model="filtroDepartamento"
            :items="departamentosDisponibles"
            item-title="nombre_departamento"
            item-value="id"
            label="Filtrar por Departamento"
            variant="outlined"
            density="comfortable"
            clearable
            prepend-inner-icon="mdi-office-building"
            @update:model-value="filtrarRegistros"
          ></v-select>
        </v-col>
      </v-row>

      <!-- Contador de resultados -->
      <div class="text-caption text-grey mt-2">
        Mostrando {{ registrosMostrados.length }} de {{ registrosFiltrados.length }} ubicaciones
      </div>
    </div>

    <!-- ====================================================================
         LOADING STATE
         ==================================================================== -->
    <div v-if="loading" class="loading-container">
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
      <p class="mt-3">Cargando ubicaciones...</p>
    </div>

    <!-- ====================================================================
         LISTA DE REGISTROS
         ==================================================================== -->
    <div v-else class="registros-lista">
      <div
        v-for="registro in registrosMostrados"
        :key="registro.id"
        class="registro-item"
      >
        <div class="registro-info">
          <div class="registro-nombre">
            {{ registro.nombre_ubicacion }}
          </div>
          <div class="registro-detalles">
            <span class="detalle-codigo">{{ registro.codigo_qr }}</span>
            <span class="detalle-separador">•</span>
            <span class="detalle-departamento">{{ registro.departamento?.nombre_departamento || 'N/A' }}</span>
            <span class="detalle-separador">•</span>
            <span class="detalle-activos">{{ registro.total_activos || 0 }} activos</span>
          </div>
        </div>
        <div class="registro-acciones">
          <v-btn
            color="blue-grey-lighten-1"
            size="small"
            icon="mdi-eye"
            class="btn-accion"
            @click="abrirModalVer(registro)"
          ></v-btn>
          <v-btn
            color="yellow-darken-2"
            size="small"
            icon="mdi-pencil"
            class="btn-accion"
            @click="abrirModalEditar(registro)"
          ></v-btn>
          <v-btn
            color="red-lighten-1"
            size="small"
            icon="mdi-delete"
            class="btn-accion"
            @click="confirmarEliminar(registro)"
          ></v-btn>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="registrosMostrados.length === 0" class="empty-state">
        <v-icon size="64" color="grey-lighten-1">mdi-inbox</v-icon>
        <p>No hay ubicaciones disponibles</p>
      </div>

      <!-- Botón Cargar Más -->
      <div v-if="registrosFiltrados.length > registrosMostrados.length" class="load-more-section">
        <v-btn
          variant="outlined"
          color="primary"
          size="large"
          prepend-icon="mdi-refresh"
          @click="cargarMasRegistros"
        >
          Cargar más ({{ registrosFiltrados.length - registrosMostrados.length }} restantes)
        </v-btn>
      </div>
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
         MODAL VER DETALLES (SOLO LECTURA)
         ==================================================================== -->
    <v-dialog v-model="showViewModal" max-width="600px" scrollable>
      <v-card>
        <v-card-title class="text-h5 pa-4 bg-blue-grey-lighten-1 text-white">
          <v-icon start>mdi-information</v-icon>
          Detalles de la Ubicación
        </v-card-title>
        
        <v-card-text class="pa-4">
          <v-list lines="two" class="py-0">
            <v-list-item>
              <template v-slot:prepend>
                <v-icon color="primary">mdi-map-marker</v-icon>
              </template>
              <v-list-item-title class="text-subtitle-2 text-grey-darken-1">
                Nombre de la Ubicación
              </v-list-item-title>
              <v-list-item-subtitle class="text-body-1 text-black mt-1">
                {{ registroVer?.nombre_ubicacion || 'N/A' }}
              </v-list-item-subtitle>
            </v-list-item>

            <v-divider class="my-2"></v-divider>

            <v-list-item>
              <template v-slot:prepend>
                <v-icon color="primary">mdi-qrcode</v-icon>
              </template>
              <v-list-item-title class="text-subtitle-2 text-grey-darken-1">
                Código QR
              </v-list-item-title>
              <v-list-item-subtitle class="text-body-1 text-black mt-1">
                {{ registroVer?.codigo_qr || 'N/A' }}
              </v-list-item-subtitle>
            </v-list-item>

            <v-divider class="my-2"></v-divider>

            <v-list-item>
              <template v-slot:prepend>
                <v-icon color="primary">mdi-office-building</v-icon>
              </template>
              <v-list-item-title class="text-subtitle-2 text-grey-darken-1">
                Departamento
              </v-list-item-title>
              <v-list-item-subtitle class="text-body-1 text-black mt-1">
                {{ registroVer?.departamento?.nombre_departamento || 'N/A' }}
              </v-list-item-subtitle>
            </v-list-item>

            <v-divider class="my-2"></v-divider>

            <v-list-item>
              <template v-slot:prepend>
                <v-icon color="primary">mdi-laptop</v-icon>
              </template>
              <v-list-item-title class="text-subtitle-2 text-grey-darken-1">
                Total de Activos
              </v-list-item-title>
              <v-list-item-subtitle class="text-body-1 text-black mt-1">
                {{ registroVer?.total_activos || 0 }} activos asignados
              </v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </v-card-text>

        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            @click="showViewModal = false"
          >
            Cerrar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- ====================================================================
         MODAL CREAR/EDITAR
         ==================================================================== -->
    <v-dialog v-model="showModal" max-width="600px" scrollable>
      <v-card>
        <v-card-title class="text-h5 pa-4 bg-primary text-white">
          <v-icon start>mdi-map-marker</v-icon>
          {{ modoEdicion ? 'Editar Ubicación' : 'Nueva Ubicación' }}
        </v-card-title>
        
        <v-card-text class="pa-4">
          <v-form ref="formRef">
            <!-- Código QR (solo lectura si está editando) -->
            <v-text-field
              v-if="modoEdicion"
              v-model="formulario.codigo_qr"
              label="Código QR"
              variant="outlined"
              density="comfortable"
              prepend-inner-icon="mdi-qrcode"
              readonly
              class="mb-2"
              hint="Generado automáticamente"
              persistent-hint
            ></v-text-field>
            
            <v-alert
              v-else
              type="info"
              variant="tonal"
              density="compact"
              class="mb-4"
            >
              <template v-slot:prepend>
                <v-icon>mdi-information</v-icon>
              </template>
              El código QR se generará automáticamente
            </v-alert>

            <!-- Nombre de la Ubicación -->
            <v-text-field
              v-model="formulario.nombre_ubicacion"
              label="Nombre de la Ubicación *"
              variant="outlined"
              density="comfortable"
              prepend-inner-icon="mdi-map-marker"
              :rules="[v => !!v || 'Campo requerido']"
              class="mb-2"
              placeholder="Ej: Sala 101, Box 3, Oficina Principal"
            ></v-text-field>

            <!-- Departamento -->
            <v-select
              v-model="formulario.departamento_id"
              :items="departamentos"
              item-title="nombre_departamento"
              item-value="id"
              label="Departamento *"
              variant="outlined"
              density="comfortable"
              prepend-inner-icon="mdi-office-building"
              :rules="[v => !!v || 'Campo requerido']"
              class="mb-2"
            ></v-select>

            <!-- Información adicional en modo edición -->
            <v-alert
              v-if="modoEdicion && formulario.total_activos !== undefined"
              type="info"
              variant="tonal"
              density="compact"
              class="mt-4"
            >
              <template v-slot:prepend>
                <v-icon>mdi-laptop</v-icon>
              </template>
              Esta ubicación tiene {{ formulario.total_activos }} activos asignados
            </v-alert>
          </v-form>
        </v-card-text>

        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn
            variant="text"
            @click="cerrarModal"
          >
            Cancelar
          </v-btn>
          <v-btn
            color="primary"
            @click="guardar"
          >
            {{ modoEdicion ? 'Actualizar' : 'Crear' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- ====================================================================
         MODAL CONFIRMAR ELIMINACIÓN
         ==================================================================== -->
    <v-dialog v-model="showDeleteDialog" max-width="400px">
      <v-card>
        <v-card-title class="text-h5 pa-4">
          <v-icon start color="error">mdi-alert-circle</v-icon>
          Confirmar Eliminación
        </v-card-title>
        
        <v-card-text class="pa-4">
          ¿Estás seguro de que deseas eliminar esta ubicación?
          <br><br>
          <strong>{{ registroAEliminar?.nombre_ubicacion }}</strong>
          <br>
          <span class="text-grey">{{ registroAEliminar?.codigo_qr }}</span>
          <br><br>
          <v-alert
            v-if="registroAEliminar?.total_activos > 0"
            type="warning"
            variant="tonal"
            density="compact"
          >
            Esta ubicación tiene {{ registroAEliminar.total_activos }} activos asignados
          </v-alert>
        </v-card-text>

        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn
            variant="text"
            @click="showDeleteDialog = false"
          >
            Cancelar
          </v-btn>
          <v-btn
            color="red"
            @click="eliminar"
          >
            Eliminar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

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
 * GESTIÓN DE UBICACIONES - CRUD COMPLETO CON FILTROS
 * ============================================================================
 *
 * Funcionalidades:
 * - Listar ubicaciones con paginación (20 por página)
 * - Filtros desplegables (Departamento)
 * - Búsqueda por texto (nombre, código QR)
 * - Ver detalles (modal solo lectura)
 * - Crear nueva ubicación
 * - Editar ubicación existente
 * - Eliminar ubicación
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

const registros = ref([])
const departamentos = ref([])
const loading = ref(false)
const showModal = ref(false)
const showViewModal = ref(false)
const showDeleteDialog = ref(false)
const modoEdicion = ref(false)
const registroAEliminar = ref(null)
const registroVer = ref(null)
const busqueda = ref('')
const formRef = ref(null)
const registrosPorPagina = ref(20)
const paginaActual = ref(1)

// Filtros
const filtroDepartamento = ref(null)

const snackbar = ref({
  show: false,
  text: '',
  color: 'success'
})

const formulario = ref({
  id: null,
  nombre_ubicacion: '',
  departamento_id: null,
  codigo_qr: '',
  total_activos: 0
})

// ============================================================================
// COMPUTED
// ============================================================================

/**
 * Obtiene los departamentos disponibles para el filtro
 */
const departamentosDisponibles = computed(() => {
  return departamentos.value
})

/**
 * Filtra los registros según la búsqueda y los filtros desplegables
 */
const registrosFiltrados = computed(() => {
  let resultado = registros.value

  // Filtro de búsqueda de texto
  if (busqueda.value) {
    const termino = busqueda.value.toLowerCase()
    resultado = resultado.filter(registro => {
      return (
        registro.nombre_ubicacion?.toLowerCase().includes(termino) ||
        registro.codigo_qr?.toLowerCase().includes(termino)
      )
    })
  }

  // Filtro por departamento
  if (filtroDepartamento.value) {
    resultado = resultado.filter(registro => 
      registro.departamento?.id === filtroDepartamento.value
    )
  }

  return resultado
})

/**
 * Registros a mostrar con paginación (20 por defecto)
 */
const registrosMostrados = computed(() => {
  const limite = paginaActual.value * registrosPorPagina.value
  return registrosFiltrados.value.slice(0, limite)
})

// ============================================================================
// MÉTODOS - API
// ============================================================================

/**
 * Carga todas las ubicaciones desde la API
 */
async function cargarRegistros() {
  loading.value = true
  try {
    const response = await apiClient.get('/api/ubicaciones/', {
      params: { page_size: 1000 }
    })
    
    registros.value = Array.isArray(response.data) 
      ? response.data 
      : response.data.results || []

    // Si hay paginación, obtener todas las páginas
    if (response.data.next) {
      await cargarTodasLasPaginas(response.data.next)
    }
      
  } catch (error) {
    console.error('Error al cargar ubicaciones:', error)
    mostrarNotificacion('Error al cargar las ubicaciones', 'error')
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
      const nuevosRegistros = Array.isArray(response.data) ? response.data : response.data.results || []
      registros.value = [...registros.value, ...nuevosRegistros]
      nextUrl = response.data.next || null
    }
  } catch (error) {
    console.error('Error al cargar páginas adicionales:', error)
  }
}

/**
 * Carga los departamentos para el select
 */
async function cargarDepartamentos() {
  try {
    const response = await apiClient.get('/api/departamentos/', {
      params: { page_size: 1000 }
    })
    departamentos.value = Array.isArray(response.data) ? response.data : response.data.results || []
  } catch (error) {
    console.error('Error al cargar departamentos:', error)
  }
}

/**
 * Guarda una nueva ubicación o actualiza una existente
 */
async function guardar() {
  // Validar formulario
  const { valid } = await formRef.value.validate()
  if (!valid) return

  try {
    // Preparar payload
    const payload = {
      nombre_ubicacion: formulario.value.nombre_ubicacion?.trim(),
      departamento_id: formulario.value.departamento_id
    }

    console.log('📤 Enviando payload:', payload)

    if (modoEdicion.value) {
      // Actualizar ubicación existente
      await apiClient.put(
        `/api/ubicaciones/${formulario.value.id}/`,
        payload
      )
      mostrarNotificacion('Ubicación actualizada correctamente', 'success')
    } else {
      // Crear nueva ubicación
      await apiClient.post('/api/ubicaciones/', payload)
      mostrarNotificacion('Ubicación creada correctamente', 'success')
    }
    
    cerrarModal()
    await cargarRegistros()
    
  } catch (error) {
    console.error('❌ Error al guardar:', error)
    
    // Mostrar error detallado del servidor
    if (error.response?.data) {
      console.error('📥 Detalle del error:', error.response.data)
      
      // Crear mensaje de error más descriptivo
      let mensajeError = 'Error al guardar la ubicación'
      
      if (typeof error.response.data === 'object') {
        const errores = []
        for (const [campo, mensajes] of Object.entries(error.response.data)) {
          if (Array.isArray(mensajes)) {
            errores.push(`${campo}: ${mensajes.join(', ')}`)
          } else {
            errores.push(`${campo}: ${mensajes}`)
          }
        }
        mensajeError = errores.join(' | ')
      }
      
      mostrarNotificacion(mensajeError, 'error')
    } else {
      mostrarNotificacion('Error al guardar la ubicación', 'error')
    }
  }
}

/**
 * Elimina una ubicación
 */
async function eliminar() {
  try {
    await apiClient.delete(`/api/ubicaciones/${registroAEliminar.value.id}/`)
    
    mostrarNotificacion('Ubicación eliminada correctamente', 'success')
    showDeleteDialog.value = false
    registroAEliminar.value = null
    await cargarRegistros()
    
  } catch (error) {
    console.error('❌ Error al eliminar:', error)
    
    // Manejar error de protección de integridad referencial
    if (error.response?.status === 500 || error.response?.status === 400) {
      const errorMsg = error.response?.data
      
      if (errorMsg && typeof errorMsg === 'string' && errorMsg.includes('ProtectedError')) {
        mostrarNotificacion(
          'No se puede eliminar esta ubicación porque tiene activos asignados', 
          'error'
        )
      } else {
        mostrarNotificacion('Error al eliminar la ubicación', 'error')
      }
    } else {
      mostrarNotificacion('Error al eliminar la ubicación', 'error')
    }
    
    showDeleteDialog.value = false
    registroAEliminar.value = null
  }
}

// ============================================================================
// MÉTODOS - UI
// ============================================================================

/**
 * Abre el modal para ver los detalles de una ubicación (solo lectura)
 */
function abrirModalVer(registro) {
  registroVer.value = registro
  showViewModal.value = true
}

/**
 * Abre el modal para crear una nueva ubicación
 */
function abrirModalCrear() {
  modoEdicion.value = false
  formulario.value = {
    id: null,
    nombre_ubicacion: '',
    departamento_id: null,
    codigo_qr: '',
    total_activos: 0
  }
  showModal.value = true
}

/**
 * Abre el modal para editar una ubicación existente
 */
function abrirModalEditar(registro) {
  modoEdicion.value = true
  formulario.value = {
    id: registro.id,
    nombre_ubicacion: registro.nombre_ubicacion,
    departamento_id: registro.departamento?.id || null,
    codigo_qr: registro.codigo_qr,
    total_activos: registro.total_activos || 0
  }
  showModal.value = true
}

/**
 * Cierra el modal de crear/editar
 */
function cerrarModal() {
  showModal.value = false
  if (formRef.value) {
    formRef.value.reset()
  }
}

/**
 * Abre el diálogo de confirmación para eliminar
 */
function confirmarEliminar(registro) {
  registroAEliminar.value = registro
  showDeleteDialog.value = true
}

/**
 * Filtra los registros (método auxiliar)
 */
function filtrarRegistros() {
  // Reiniciar la paginación cuando se aplica un filtro
  paginaActual.value = 1
}

/**
 * Carga más registros (incrementa la paginación)
 */
function cargarMasRegistros() {
  paginaActual.value++
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
  await Promise.all([
    cargarRegistros(),
    cargarDepartamentos()
  ])
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

.btn-nuevo {
  min-width: 120px;
  font-weight: 600;
}

/* ============================================================================
   BÚSQUEDA Y FILTROS
   ============================================================================ */

.search-section {
  margin-bottom: 1.5rem;
}

/* ============================================================================
   LISTA DE REGISTROS
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
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  transition: all 0.2s ease;
}

.registro-item:hover {
  border-color: #1976d2;
  box-shadow: 0 2px 8px rgba(25, 118, 210, 0.15);
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

.registro-detalles {
  font-size: 0.875rem;
  color: #666;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.detalle-codigo {
  font-family: monospace;
  background: #f5f5f5;
  padding: 0.125rem 0.5rem;
  border-radius: 4px;
}

.detalle-separador {
  color: #ccc;
}

.detalle-departamento {
  color: #1976d2;
}

.detalle-activos {
  color: #4caf50;
  font-weight: 500;
}

.registro-acciones {
  display: flex;
  gap: 0.5rem;
  flex-shrink: 0;
}

.btn-accion {
  min-width: 40px;
  height: 40px;
}

/* ============================================================================
   LOAD MORE
   ============================================================================ */

.load-more-section {
  display: flex;
  justify-content: center;
  margin-top: 1.5rem;
  padding: 1rem 0;
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

@media (max-width: 600px) {
  .crud-entidad-content {
    padding: 0.75rem;
  }

  .header-section {
    flex-direction: column;
    align-items: stretch;
  }

  .btn-nuevo {
    width: 100%;
  }

  .registro-item {
    flex-direction: column;
    align-items: stretch;
  }

  .registro-info {
    margin-bottom: 0.5rem;
  }

  .registro-acciones {
    justify-content: flex-end;
  }
}
</style>
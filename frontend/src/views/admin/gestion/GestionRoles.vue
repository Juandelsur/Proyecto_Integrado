<template>
  <div class="crud-entidad-content">
    <!-- ====================================================================
         HEADER CON TÍTULO Y BOTÓN NUEVO
         ==================================================================== -->
    <div class="header-section">
      <h1 class="entity-title">Gestión De Roles</h1>
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
         BARRA DE BÚSQUEDA
         ==================================================================== -->
    <div class="search-section">
      <v-text-field
        v-model="busqueda"
        prepend-inner-icon="mdi-magnify"
        label="Buscar por nombre del Rol"
        variant="outlined"
        density="comfortable"
        clearable
        @input="filtrarRegistros"
        class="mb-3"
      ></v-text-field>

      <!-- Contador de resultados -->
      <div class="text-caption text-grey mt-2">
        Mostrando {{ registrosMostrados.length }} de {{ registrosFiltrados.length }} estados
      </div>
    </div>

    <!-- ====================================================================
         LOADING STATE
         ==================================================================== -->
    <div v-if="loading" class="loading-container">
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
      <p class="mt-3">Cargando Roles...</p>
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
            {{ registro.nombre_rol }}
          </div>
        </div>
        <div class="registro-acciones">
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
        <p>No hay Roles disponibles</p>
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
         MODAL CREAR/EDITAR
         ==================================================================== -->
    <v-dialog v-model="showModal" max-width="500px">
      <v-card>
        <v-card-title class="text-h5 pa-4 bg-primary text-white">
          <v-icon start>mdi-state-machine</v-icon>
          {{ modoEdicion ? 'Editar Rol' : 'Nuevo Rol' }}
        </v-card-title>
        
        <v-card-text class="pa-4">
          <v-form ref="formRef">
            <!-- Nombre del Rol -->
            <v-text-field
              v-model="formulario.nombre_rol"
              label="Nombre del Rol *"
              variant="outlined"
              density="comfortable"
              prepend-inner-icon="mdi-label-outline"
              :rules="[v => !!v || 'Campo requerido']"
              autofocus
              hint="Ejemplo: Administrador, Tecnico, etc."
              persistent-hint
            ></v-text-field>
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
          ¿Estás seguro de que deseas eliminar este Rol?
          <br><br>
          <strong>{{ registroAEliminar?.nombre_rol }}</strong>
          <br>
          <span class="text-grey">ID: {{ registroAEliminar?.id }}</span>
          <br><br>
          <v-alert type="warning" density="compact" class="mt-2">
            Los activos que usen este Rol quedarán sin Rol asignado.
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
 * GESTIÓN ROLES - CRUD COMPLETO
 * ============================================================================
 *
 * Funcionalidades:
 * - Listar Roles con paginación (20 por página)
 * - Búsqueda por nombre
 * - Crear nuevo Rol
 * - Editar Rol existente
 * - Eliminar Rol
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
const loading = ref(false)
const showModal = ref(false)
const showDeleteDialog = ref(false)
const modoEdicion = ref(false)
const registroAEliminar = ref(null)
const busqueda = ref('')
const formRef = ref(null)
const registrosPorPagina = ref(20)
const paginaActual = ref(1)

const snackbar = ref({
  show: false,
  text: '',
  color: 'success'
})

const formulario = ref({
  id: null,
  nombre_estado: ''
})

// ============================================================================
// COMPUTED
// ============================================================================

/**
 * Filtra los registros según la búsqueda
 */
const registrosFiltrados = computed(() => {
  let resultado = registros.value

  // Filtro de búsqueda de texto
  if (busqueda.value) {
    const termino = busqueda.value.toLowerCase()
    resultado = resultado.filter(registro => {
      return registro.nombre_estado?.toLowerCase().includes(termino)
    })
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
 * Carga todos los estados desde la API
 */
async function cargarRegistros() {
  loading.value = true
  try {
    const response = await apiClient.get('/api/roles/', {
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
    console.error('Error al cargar Roles:', error)
    mostrarNotificacion('Error al cargar los Roles', 'error')
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
 * Guarda un nuevo Rol o actualiza uno existente
 */
async function guardar() {
  // Validar formulario
  const { valid } = await formRef.value.validate()
  if (!valid) return

  try {
    const payload = {
      nombre_rol: formulario.value.nombre_rol?.trim()
    }

    console.log('📤 Enviando payload:', payload)

    if (modoEdicion.value) {
      // Actualizar Rol existente
      await apiClient.put(
        `/api/roles/${formulario.value.id}/`,
        payload
      )
      mostrarNotificacion('Rol actualizado correctamente', 'success')
    } else {
      // Crear nuevo Rol
      await apiClient.post('/api/roles/', payload)
      mostrarNotificacion('Rol creado correctamente', 'success')
    }
    
    cerrarModal()
    await cargarRegistros()
    
  } catch (error) {
    console.error('❌ Error al guardar:', error)
    
    // Mostrar error detallado del servidor
    if (error.response?.data) {
      console.error('📥 Detalle del error:', error.response.data)
      
      let mensajeError = 'Error al guardar el Rol'
      
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
      mostrarNotificacion('Error al guardar el Rol', 'error')
    }
  }
}

/**
 * Elimina un Rol
 */
async function eliminar() {
  try {
    await apiClient.delete(`/api/roles/${registroAEliminar.value.id}/`)
    
    mostrarNotificacion('Rol eliminado correctamente', 'success')
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
          'No se puede eliminar este Rol porque está siendo usado por uno o más activos', 
          'error'
        )
      } else {
        mostrarNotificacion('Error al eliminar el Rol. Puede estar en uso por otros registros.', 'error')
      }
    } else {
      mostrarNotificacion('Error al eliminar el Rol', 'error')
    }
    
    showDeleteDialog.value = false
    registroAEliminar.value = null
  }
}

// ============================================================================
// MÉTODOS - UI
// ============================================================================

/**
 * Abre el modal para crear un nuevo Rol
 */
function abrirModalCrear() {
  modoEdicion.value = false
  formulario.value = {
    id: null,
    nombre_rol: ''
  }
  showModal.value = true
}

/**
 * Abre el modal para editar un Rol existente
 */
function abrirModalEditar(registro) {
  modoEdicion.value = true
  formulario.value = {
    id: registro.id,
    nombre_rol: registro.nombre_rol
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
  await cargarRegistros()
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
   BÚSQUEDA
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
}

.detalle-codigo {
  font-family: monospace;
  background: #f5f5f5;
  padding: 0.125rem 0.5rem;
  border-radius: 4px;
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
<template>
  <div class="crud-entidad-content">
    <!-- ====================================================================
         HEADER CON TÍTULO Y BOTÓN NUEVO
         ==================================================================== -->
    <div class="header-section">
      <h1 class="entity-title">Gestión Activos</h1>
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
        label="Buscar por código, número de serie o modelo"
        variant="outlined"
        density="comfortable"
        clearable
        @input="filtrarRegistros"
        class="mb-3"
      ></v-text-field>

      <!-- Filtros Desplegables -->
      <v-row dense>
        <v-col cols="12" sm="4">
          <v-select
            v-model="filtroMarca"
            :items="marcasDisponibles"
            label="Filtrar por Marca"
            variant="outlined"
            density="comfortable"
            clearable
            prepend-inner-icon="mdi-tag"
            @update:model-value="filtrarRegistros"
          ></v-select>
        </v-col>
        <v-col cols="12" sm="4">
          <v-select
            v-model="filtroTipo"
            :items="tiposDisponibles"
            item-title="nombre_tipo"
            item-value="id"
            label="Filtrar por Tipo de Equipo"
            variant="outlined"
            density="comfortable"
            clearable
            prepend-inner-icon="mdi-devices"
            @update:model-value="filtrarRegistros"
          ></v-select>
        </v-col>
        <v-col cols="12" sm="4">
          <v-select
            v-model="filtroUbicacion"
            :items="ubicacionesDisponibles"
            item-title="nombre_ubicacion"
            item-value="id"
            label="Filtrar por Ubicación"
            variant="outlined"
            density="comfortable"
            clearable
            prepend-inner-icon="mdi-map-marker"
            @update:model-value="filtrarRegistros"
          ></v-select>
        </v-col>
      </v-row>

      <!-- Contador de resultados -->
      <div class="text-caption text-grey mt-2">
        Mostrando {{ registrosMostrados.length }} de {{ registrosFiltrados.length }} activos
      </div>
    </div>

    <!-- ====================================================================
         LOADING STATE
         ==================================================================== -->
    <div v-if="loading" class="loading-container">
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
      <p class="mt-3">Cargando activos...</p>
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
            {{ registro.marca }} {{ registro.modelo }}
          </div>
          <div class="registro-detalles">
            <span class="detalle-codigo">{{ registro.codigo_inventario }}</span>
            <span class="detalle-separador">•</span>
            <span class="detalle-estado">{{ registro.estado?.nombre_estado || 'N/A' }}</span>
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
        <p>No hay activos disponibles</p>
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
          Detalles del Activo
        </v-card-title>
        
        <v-card-text class="pa-4">
          <v-list lines="two" class="py-0">
            <v-list-item>
              <template v-slot:prepend>
                <v-icon color="primary">mdi-barcode</v-icon>
              </template>
              <v-list-item-title class="text-subtitle-2 text-grey-darken-1">
                Código de Inventario
              </v-list-item-title>
              <v-list-item-subtitle class="text-body-1 text-black mt-1">
                {{ registroVer?.codigo_inventario || 'N/A' }}
              </v-list-item-subtitle>
            </v-list-item>

            <v-divider class="my-2"></v-divider>

            <v-list-item>
              <template v-slot:prepend>
                <v-icon color="primary">mdi-devices</v-icon>
              </template>
              <v-list-item-title class="text-subtitle-2 text-grey-darken-1">
                Tipo de Equipo
              </v-list-item-title>
              <v-list-item-subtitle class="text-body-1 text-black mt-1">
                {{ registroVer?.tipo?.nombre_tipo || 'N/A' }}
              </v-list-item-subtitle>
            </v-list-item>

            <v-divider class="my-2"></v-divider>

            <v-list-item>
              <template v-slot:prepend>
                <v-icon color="primary">mdi-tag</v-icon>
              </template>
              <v-list-item-title class="text-subtitle-2 text-grey-darken-1">
                Marca
              </v-list-item-title>
              <v-list-item-subtitle class="text-body-1 text-black mt-1">
                {{ registroVer?.marca || 'N/A' }}
              </v-list-item-subtitle>
            </v-list-item>

            <v-divider class="my-2"></v-divider>

            <v-list-item>
              <template v-slot:prepend>
                <v-icon color="primary">mdi-label</v-icon>
              </template>
              <v-list-item-title class="text-subtitle-2 text-grey-darken-1">
                Modelo
              </v-list-item-title>
              <v-list-item-subtitle class="text-body-1 text-black mt-1">
                {{ registroVer?.modelo || 'N/A' }}
              </v-list-item-subtitle>
            </v-list-item>

            <v-divider class="my-2"></v-divider>

            <v-list-item>
              <template v-slot:prepend>
                <v-icon color="primary">mdi-numeric</v-icon>
              </template>
              <v-list-item-title class="text-subtitle-2 text-grey-darken-1">
                Número de Serie
              </v-list-item-title>
              <v-list-item-subtitle class="text-body-1 text-black mt-1">
                {{ registroVer?.numero_serie || 'N/A' }}
              </v-list-item-subtitle>
            </v-list-item>

            <v-divider class="my-2"></v-divider>

            <v-list-item>
              <template v-slot:prepend>
                <v-icon color="primary">mdi-state-machine</v-icon>
              </template>
              <v-list-item-title class="text-subtitle-2 text-grey-darken-1">
                Estado
              </v-list-item-title>
              <v-list-item-subtitle class="text-body-1 text-black mt-1">
                {{ registroVer?.estado?.nombre_estado || 'N/A' }}
              </v-list-item-subtitle>
            </v-list-item>

            <v-divider class="my-2"></v-divider>

            <v-list-item>
              <template v-slot:prepend>
                <v-icon color="primary">mdi-map-marker</v-icon>
              </template>
              <v-list-item-title class="text-subtitle-2 text-grey-darken-1">
                Ubicación Actual
              </v-list-item-title>
              <v-list-item-subtitle class="text-body-1 text-black mt-1">
                {{ registroVer?.ubicacion_actual?.nombre_ubicacion || 'N/A' }}
              </v-list-item-subtitle>
            </v-list-item>

            <v-divider class="my-2"></v-divider>

            <v-list-item>
              <template v-slot:prepend>
                <v-icon color="primary">mdi-note-text</v-icon>
              </template>
              <v-list-item-title class="text-subtitle-2 text-grey-darken-1">
                Notas
              </v-list-item-title>
              <v-list-item-subtitle class="text-body-1 text-black mt-1" style="white-space: pre-wrap;">
                {{ registroVer?.notas || 'Sin notas' }}
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
          <v-icon start>mdi-laptop</v-icon>
          {{ modoEdicion ? 'Editar Activo' : 'Nuevo Activo' }}
        </v-card-title>
        
        <v-card-text class="pa-4">
          <v-form ref="formRef">
            <!-- Código de Inventario (solo lectura si está editando) -->
            <v-text-field
              v-if="modoEdicion"
              v-model="formulario.codigo_inventario"
              label="Código de Inventario"
              variant="outlined"
              density="comfortable"
              prepend-inner-icon="mdi-barcode"
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
              El código de inventario se generará automáticamente
            </v-alert>

            <!-- Tipo de Equipo -->
            <v-select
              v-model="formulario.tipo"
              :items="tiposEquipo"
              item-title="nombre_tipo"
              item-value="id"
              label="Tipo de Equipo *"
              variant="outlined"
              density="comfortable"
              prepend-inner-icon="mdi-devices"
              :rules="[v => !!v || 'Campo requerido']"
              class="mb-2"
            ></v-select>

            <!-- Marca y Modelo -->
            <v-row>
              <v-col cols="6">
                <v-text-field
                  v-model="formulario.marca"
                  label="Marca *"
                  variant="outlined"
                  density="comfortable"
                  prepend-inner-icon="mdi-tag"
                  :rules="[v => !!v || 'Campo requerido']"
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  v-model="formulario.modelo"
                  label="Modelo *"
                  variant="outlined"
                  density="comfortable"
                  prepend-inner-icon="mdi-label"
                  :rules="[v => !!v || 'Campo requerido']"
                ></v-text-field>
              </v-col>
            </v-row>

            <!-- Número de Serie -->
            <v-text-field
              v-model="formulario.numero_serie"
              label="Número de Serie"
              variant="outlined"
              density="comfortable"
              prepend-inner-icon="mdi-numeric"
              class="mb-2"
            ></v-text-field>

            <!-- Estado -->
            <v-select
              v-model="formulario.estado"
              :items="estados"
              item-title="nombre_estado"
              item-value="id"
              label="Estado *"
              variant="outlined"
              density="comfortable"
              prepend-inner-icon="mdi-state-machine"
              :rules="[v => !!v || 'Campo requerido']"
              class="mb-2"
            ></v-select>

            <!-- Ubicación Actual -->
            <v-select
              v-model="formulario.ubicacion_actual"
              :items="ubicaciones"
              item-title="nombre_ubicacion"
              item-value="id"
              label="Ubicación Actual *"
              variant="outlined"
              density="comfortable"
              prepend-inner-icon="mdi-map-marker"
              :rules="[v => !!v || 'Campo requerido']"
              class="mb-2"
            ></v-select>

            <!-- Notas -->
            <v-textarea
              v-model="formulario.notas"
              label="Notas"
              variant="outlined"
              density="comfortable"
              rows="3"
              prepend-inner-icon="mdi-note-text"
            ></v-textarea>
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
          ¿Estás seguro de que deseas eliminar este activo?
          <br><br>
          <strong>{{ registroAEliminar?.marca }} {{ registroAEliminar?.modelo }}</strong>
          <br>
          <span class="text-grey">{{ registroAEliminar?.codigo_inventario }}</span>
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
 * GESTIÓN DE ACTIVOS - CRUD COMPLETO CON FILTROS MEJORADOS
 * ============================================================================
 *
 * Funcionalidades:
 * - Listar activos con paginación (20 por página)
 * - Filtros desplegables (Marca, Tipo, Ubicación)
 * - Búsqueda por texto
 * - Ver detalles (modal solo lectura)
 * - Crear nuevo activo
 * - Editar activo existente
 * - Eliminar activo
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
const tiposEquipo = ref([])
const estados = ref([])
const ubicaciones = ref([])
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
const filtroMarca = ref(null)
const filtroTipo = ref(null)
const filtroUbicacion = ref(null)

const snackbar = ref({
  show: false,
  text: '',
  color: 'success'
})

const formulario = ref({
  id: null,
  tipo: null,
  marca: '',
  modelo: '',
  numero_serie: '',
  estado: null,
  ubicacion_actual: null,
  notas: ''
})

// ============================================================================
// COMPUTED
// ============================================================================

/**
 * Obtiene las marcas únicas disponibles para el filtro
 */
const marcasDisponibles = computed(() => {
  const marcas = [...new Set(registros.value
    .map(r => r.marca)
    .filter(Boolean))]
  return marcas.sort()
})

/**
 * Obtiene los tipos únicos disponibles para el filtro
 */
const tiposDisponibles = computed(() => {
  return tiposEquipo.value
})

/**
 * Obtiene las ubicaciones únicas disponibles para el filtro
 */
const ubicacionesDisponibles = computed(() => {
  return ubicaciones.value
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
        registro.codigo_inventario?.toLowerCase().includes(termino) ||
        registro.marca?.toLowerCase().includes(termino) ||
        registro.modelo?.toLowerCase().includes(termino) ||
        registro.numero_serie?.toLowerCase().includes(termino)
      )
    })
  }

  // Filtro por marca
  if (filtroMarca.value) {
    resultado = resultado.filter(registro => 
      registro.marca === filtroMarca.value
    )
  }

  // Filtro por tipo de equipo
  if (filtroTipo.value) {
    resultado = resultado.filter(registro => 
      registro.tipo?.id === filtroTipo.value
    )
  }

  // Filtro por ubicación
  if (filtroUbicacion.value) {
    resultado = resultado.filter(registro => 
      registro.ubicacion_actual?.id === filtroUbicacion.value
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
 * Carga todos los activos desde la API
 */
async function cargarRegistros() {
  loading.value = true
  try {
    const response = await apiClient.get('/api/activos/', {
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
    console.error('Error al cargar activos:', error)
    mostrarNotificacion('Error al cargar los activos', 'error')
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
 * Carga los tipos de equipo para el select
 */
async function cargarTiposEquipo() {
  try {
    const response = await apiClient.get('/api/tipos-equipo/', {
      params: { page_size: 1000 }
    })
    tiposEquipo.value = Array.isArray(response.data) ? response.data : response.data.results || []
  } catch (error) {
    console.error('Error al cargar tipos de equipo:', error)
  }
}

/**
 * Carga los estados para el select
 */
async function cargarEstados() {
  try {
    const response = await apiClient.get('/api/estados-activo/', {
      params: { page_size: 1000 }
    })
    estados.value = Array.isArray(response.data) ? response.data : response.data.results || []
  } catch (error) {
    console.error('Error al cargar estados:', error)
  }
}

/**
 * Carga las ubicaciones para el select
 */
async function cargarUbicaciones() {
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
 * Guarda un nuevo activo o actualiza uno existente
 */
async function guardar() {
  // Validar formulario
  const { valid } = await formRef.value.validate()
  if (!valid) return

  try {
    // Preparar payload con los nombres correctos que espera el backend
    const payload = {
      tipo_id: formulario.value.tipo,
      marca: formulario.value.marca?.trim(),
      modelo: formulario.value.modelo?.trim(),
      numero_serie: formulario.value.numero_serie?.trim() || null,
      estado_id: formulario.value.estado,
      ubicacion_actual_id: formulario.value.ubicacion_actual,
      notas: formulario.value.notas?.trim() || ''
    }

    console.log('📤 Enviando payload:', payload)

    if (modoEdicion.value) {
      // Actualizar activo existente
      await apiClient.put(
        `/api/activos/${formulario.value.id}/`,
        payload
      )
      mostrarNotificacion('Activo actualizado correctamente', 'success')
    } else {
      // Crear nuevo activo
      await apiClient.post('/api/activos/', payload)
      mostrarNotificacion('Activo creado correctamente', 'success')
    }
    
    cerrarModal()
    await cargarRegistros()
    
  } catch (error) {
    console.error('❌ Error al guardar:', error)
    
    // Mostrar error detallado del servidor
    if (error.response?.data) {
      console.error('📥 Detalle del error:', error.response.data)
      
      // Crear mensaje de error más descriptivo
      let mensajeError = 'Error al guardar el activo'
      
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
      mostrarNotificacion('Error al guardar el activo', 'error')
    }
  }
}

/**
 * Elimina un activo
 */
async function eliminar() {
  try {
    await apiClient.delete(`/api/activos/${registroAEliminar.value.id}/`)
    
    mostrarNotificacion('Activo eliminado correctamente', 'success')
    showDeleteDialog.value = false
    registroAEliminar.value = null
    await cargarRegistros()
    
  } catch (error) {
    console.error('❌ Error al eliminar:', error)
    
    // Manejar error de protección de integridad referencial
    if (error.response?.status === 500) {
      const errorMsg = error.response?.data
      
      if (errorMsg && typeof errorMsg === 'string' && errorMsg.includes('ProtectedError')) {
        mostrarNotificacion(
          'No se puede eliminar este activo porque tiene movimientos registrados en el historial', 
          'error'
        )
      } else {
        mostrarNotificacion('Error al eliminar el activo', 'error')
      }
    } else {
      mostrarNotificacion('Error al eliminar el activo', 'error')
    }
    
    showDeleteDialog.value = false
    registroAEliminar.value = null
  }
}

// ============================================================================
// MÉTODOS - UI
// ============================================================================

/**
 * Abre el modal para ver los detalles de un activo (solo lectura)
 */
function abrirModalVer(registro) {
  registroVer.value = registro
  showViewModal.value = true
}

/**
 * Abre el modal para crear un nuevo activo
 */
function abrirModalCrear() {
  modoEdicion.value = false
  formulario.value = {
    id: null,
    tipo: null,
    marca: '',
    modelo: '',
    numero_serie: '',
    estado: null,
    ubicacion_actual: null,
    notas: ''
  }
  showModal.value = true
}

/**
 * Abre el modal para editar un activo existente
 */
function abrirModalEditar(registro) {
  modoEdicion.value = true
  formulario.value = {
    id: registro.id,
    codigo_inventario: registro.codigo_inventario,
    tipo: registro.tipo?.id || null,
    marca: registro.marca,
    modelo: registro.modelo,
    numero_serie: registro.numero_serie,
    estado: registro.estado?.id || null,
    ubicacion_actual: registro.ubicacion_actual?.id || null,
    notas: registro.notas || ''
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
    cargarTiposEquipo(),
    cargarEstados(),
    cargarUbicaciones()
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

.detalle-estado {
  color: #1976d2;
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
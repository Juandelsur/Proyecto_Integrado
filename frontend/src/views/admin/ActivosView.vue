<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="bg-primary text-white d-flex justify-space-between align-center">
            <div class="d-flex align-center">
              <v-icon start>mdi-cube-outline</v-icon>
              <span class="text-h6">Gestión de Activos</span>
            </div>
            <v-btn
              color="white"
              variant="elevated"
              prepend-icon="mdi-plus"
              @click="abrirModalCrear"
            >
              Nuevo Activo
            </v-btn>
          </v-card-title>

          <v-card-text class="pa-4">
            <!-- Buscador -->
            <v-row class="mb-4">
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="search"
                  label="Buscar activos..."
                  prepend-inner-icon="mdi-magnify"
                  variant="outlined"
                  density="compact"
                  hide-details
                  clearable
                  @update:model-value="handleSearchChange"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="3">
                <v-select
                  v-model="filtroTipo"
                  :items="tiposEquipo"
                  item-title="nombre_tipo"
                  item-value="id"
                  label="Filtrar por Tipo"
                  variant="outlined"
                  density="compact"
                  hide-details
                  clearable
                  @update:model-value="handleFiltroChange"
                ></v-select>
              </v-col>
              <v-col cols="12" md="3">
                <v-select
                  v-model="filtroEstado"
                  :items="estadosActivo"
                  item-title="nombre_estado"
                  item-value="id"
                  label="Filtrar por Estado"
                  variant="outlined"
                  density="compact"
                  hide-details
                  clearable
                  @update:model-value="handleFiltroChange"
                ></v-select>
              </v-col>
            </v-row>

            <!-- Tabla Server-Side -->
            <v-data-table-server
              v-model:items-per-page="itemsPerPage"
              v-model:page="page"
              :headers="headers"
              :items="items"
              :items-length="totalItems"
              :loading="loading"
              :search="search"
              item-value="id"
              class="elevation-1"
              @update:options="loadItems"
            >
              <!-- Slot para mostrar skeleton loader mientras carga -->
              <template v-slot:loading>
                <v-skeleton-loader type="table-row@10"></v-skeleton-loader>
              </template>

              <!-- Columna: Código Inventario -->
              <template v-slot:item.codigo_inventario="{ item }">
                <span class="font-weight-medium">{{ item.codigo_inventario || 'N/A' }}</span>
              </template>

              <!-- Columna: Serie -->
              <template v-slot:item.numero_serie="{ item }">
                {{ item.numero_serie || 'N/A' }}
              </template>

              <!-- Columna: Marca/Modelo -->
              <template v-slot:item.marca_modelo="{ item }">
                <div>
                  <div class="font-weight-medium">{{ item.marca || 'N/A' }}</div>
                  <div class="text-caption text-grey">{{ item.modelo || '' }}</div>
                </div>
              </template>

              <!-- Columna: Tipo -->
              <template v-slot:item.tipo="{ item }">
                <v-chip
                  v-if="item.tipo"
                  color="primary"
                  size="small"
                  variant="tonal"
                >
                  {{ item.tipo.nombre_tipo }}
                </v-chip>
                <span v-else class="text-grey">N/A</span>
              </template>

              <!-- Columna: Estado -->
              <template v-slot:item.estado="{ item }">
                <v-chip
                  v-if="item.estado"
                  :color="getEstadoColor(item.estado.nombre_estado)"
                  size="small"
                  variant="flat"
                >
                  {{ item.estado.nombre_estado }}
                </v-chip>
                <span v-else class="text-grey">N/A</span>
              </template>

              <!-- Columna: Ubicación -->
              <template v-slot:item.ubicacion_actual="{ item }">
                <div v-if="item.ubicacion_actual">
                  <div class="font-weight-medium">{{ item.ubicacion_actual.nombre_ubicacion }}</div>
                  <div v-if="item.ubicacion_actual.departamento" class="text-caption text-grey">
                    {{ item.ubicacion_actual.departamento.nombre_departamento }}
                  </div>
                </div>
                <span v-else class="text-grey">N/A</span>
              </template>

              <!-- Columna: Acciones -->
              <template v-slot:item.actions="{ item }">
                <v-btn
                  icon="mdi-pencil"
                  size="small"
                  variant="text"
                  color="primary"
                  @click="abrirModalEditar(item)"
                ></v-btn>
                <v-btn
                  icon="mdi-delete"
                  size="small"
                  variant="text"
                  color="error"
                  @click="confirmarEliminar(item)"
                ></v-btn>
              </template>
            </v-data-table-server>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Modal CRUD -->
    <v-dialog
      v-model="showModal"
      max-width="600"
      persistent
      scrollable
    >
      <v-card>
        <v-card-title class="bg-primary text-white">
          <span>{{ modoEdicion ? 'Editar Activo' : 'Nuevo Activo' }}</span>
          <v-spacer></v-spacer>
          <v-btn
            icon="mdi-close"
            variant="text"
            color="white"
            @click="cerrarModal"
          ></v-btn>
        </v-card-title>

        <v-card-text class="pa-4">
          <v-form ref="formRef" v-model="formValid">
            <!-- Código Inventario (Solo lectura en edición) -->
            <v-text-field
              v-if="modoEdicion"
              v-model="form.codigo_inventario"
              label="Código de Inventario"
              variant="outlined"
              density="compact"
              readonly
              class="mb-2"
            ></v-text-field>

            <!-- Tipo -->
            <v-select
              v-model="form.tipo_id"
              :items="tiposEquipo"
              item-title="nombre_tipo"
              item-value="id"
              label="Tipo de Equipo"
              variant="outlined"
              density="compact"
              :rules="[rules.required]"
              class="mb-2"
            ></v-select>

            <!-- Marca -->
            <v-text-field
              v-model="form.marca"
              label="Marca"
              variant="outlined"
              density="compact"
              :rules="[rules.required]"
              class="mb-2"
            ></v-text-field>

            <!-- Modelo -->
            <v-text-field
              v-model="form.modelo"
              label="Modelo"
              variant="outlined"
              density="compact"
              :rules="[rules.required]"
              class="mb-2"
            ></v-text-field>

            <!-- Número de Serie -->
            <v-text-field
              v-model="form.numero_serie"
              label="Número de Serie"
              variant="outlined"
              density="compact"
              class="mb-2"
            ></v-text-field>

            <!-- Estado -->
            <v-select
              v-model="form.estado_id"
              :items="estadosActivo"
              item-title="nombre_estado"
              item-value="id"
              label="Estado"
              variant="outlined"
              density="compact"
              :rules="[rules.required]"
              class="mb-2"
            ></v-select>

            <!-- Ubicación Actual -->
            <v-select
              v-model="form.ubicacion_actual_id"
              :items="ubicaciones"
              item-title="nombre_ubicacion"
              item-value="id"
              label="Ubicación Actual"
              variant="outlined"
              density="compact"
              :rules="[rules.required]"
              class="mb-2"
            >
              <template v-slot:item="{ props, item }">
                <v-list-item v-bind="props">
                  <template v-slot:title>
                    {{ item.raw.nombre_ubicacion }}
                  </template>
                  <template v-slot:subtitle>
                    {{ item.raw.departamento?.nombre_departamento }}
                  </template>
                </v-list-item>
              </template>
            </v-select>

            <!-- Notas -->
            <v-textarea
              v-model="form.notas"
              label="Notas"
              variant="outlined"
              density="compact"
              rows="3"
              class="mb-2"
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
            variant="elevated"
            :loading="guardando"
            @click="guardar"
          >
            {{ modoEdicion ? 'Actualizar' : 'Crear' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Dialog de Confirmación de Eliminación -->
    <v-dialog
      v-model="showDialogEliminar"
      max-width="400"
    >
      <v-card>
        <v-card-title class="text-h6">
          Confirmar Eliminación
        </v-card-title>
        <v-card-text>
          ¿Está seguro de que desea eliminar el activo
          <strong>{{ activoAEliminar?.codigo_inventario || activoAEliminar?.marca }}</strong>?
          Esta acción no se puede deshacer.
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            variant="text"
            @click="showDialogEliminar = false"
          >
            Cancelar
          </v-btn>
          <v-btn
            color="error"
            variant="elevated"
            :loading="eliminando"
            @click="eliminarActivo"
          >
            Eliminar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Snackbar para Feedback -->
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="3000"
      location="top"
    >
      {{ snackbar.message }}
      <template v-slot:actions>
        <v-btn
          variant="text"
          @click="snackbar.show = false"
        >
          Cerrar
        </v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import apiClient from '@/services/api'
import { getActivos, createActivo, updateActivo, deleteActivo } from '@/services/activosService'

// ============================================================================
// ESTADO REACTIVO
// ============================================================================

// Tabla
const items = ref([])
const loading = ref(false)
const totalItems = ref(0)
const page = ref(1)
const itemsPerPage = ref(10)
const search = ref('')
const filtroTipo = ref(null)
const filtroEstado = ref(null)

// Headers de la tabla
const headers = [
  { title: 'Código Inventario', key: 'codigo_inventario', sortable: true, align: 'start' },
  { title: 'Serie', key: 'numero_serie', sortable: true, align: 'start' },
  { title: 'Marca/Modelo', key: 'marca_modelo', sortable: false, align: 'start' },
  { title: 'Tipo', key: 'tipo', sortable: false, align: 'start' },
  { title: 'Estado', key: 'estado', sortable: false, align: 'start' },
  { title: 'Ubicación', key: 'ubicacion_actual', sortable: false, align: 'start' },
  { title: 'Acciones', key: 'actions', sortable: false, align: 'end', width: '120' }
]

// Modal y Formulario
const showModal = ref(false)
const modoEdicion = ref(false)
const formValid = ref(false)
const guardando = ref(false)
const formRef = ref(null)

const form = reactive({
  id: null,
  codigo_inventario: '',
  tipo_id: null,
  marca: '',
  modelo: '',
  numero_serie: '',
  estado_id: null,
  ubicacion_actual_id: null,
  notas: ''
})

// Opciones para Selects
const tiposEquipo = ref([])
const estadosActivo = ref([])
const ubicaciones = ref([])

// Eliminación
const showDialogEliminar = ref(false)
const activoAEliminar = ref(null)
const eliminando = ref(false)

// Snackbar
const snackbar = reactive({
  show: false,
  message: '',
  color: 'success'
})

// Validaciones
const rules = {
  required: (v) => !!v || 'Este campo es requerido'
}

// ============================================================================
// MÉTODOS - CARGA DE DATOS
// ============================================================================

/**
 * Carga los items de la tabla desde el servidor
 * Mapea los parámetros de Vuetify a Django REST Framework
 */
async function loadItems({ page: pageNum, itemsPerPage: itemsPerPageNum, sortBy }) {
  loading.value = true

  try {
    const params = {
      page: pageNum,
      page_size: itemsPerPageNum
    }

    // Mapeo de ordenamiento: Vuetify array -> Django string
    if (sortBy && sortBy.length > 0) {
      const sort = sortBy[0]
      params.ordering = sort.order === 'desc' ? `-${sort.key}` : sort.key
    }

    // Búsqueda
    if (search.value) {
      params.search = search.value
    }

    // Filtros
    if (filtroTipo.value) {
      params.tipo = filtroTipo.value
    }

    if (filtroEstado.value) {
      params.estado = filtroEstado.value
    }

    const response = await getActivos(params)
    
    // Django REST Framework devuelve { results: [], count: number }
    items.value = response.results || response.data || []
    totalItems.value = response.count || 0
  } catch (error) {
    console.error('Error al cargar activos:', error)
    mostrarSnackbar('Error al cargar los activos', 'error')
  } finally {
    loading.value = false
  }
}

/**
 * Carga las opciones para los selects (tipos, estados, ubicaciones)
 */
async function cargarOpcionesSelects() {
  try {
    // Cargar Tipos de Equipo
    const tiposResponse = await apiClient.get('/api/tipos-equipo/', {
      params: { page_size: 100 } // Cantidad razonable para selects
    })
    tiposEquipo.value = Array.isArray(tiposResponse.data) 
      ? tiposResponse.data 
      : tiposResponse.data.results || []

    // Cargar Estados de Activo
    const estadosResponse = await apiClient.get('/api/estados-activo/', {
      params: { page_size: 100 }
    })
    estadosActivo.value = Array.isArray(estadosResponse.data)
      ? estadosResponse.data
      : estadosResponse.data.results || []

    // Cargar Ubicaciones
    const ubicacionesResponse = await apiClient.get('/api/ubicaciones/', {
      params: { page_size: 100 }
    })
    ubicaciones.value = Array.isArray(ubicacionesResponse.data)
      ? ubicacionesResponse.data
      : ubicacionesResponse.data.results || []
  } catch (error) {
    console.error('Error al cargar opciones para selects:', error)
    mostrarSnackbar('Error al cargar las opciones del formulario', 'error')
  }
}

// ============================================================================
// MÉTODOS - FORMULARIO CRUD
// ============================================================================

/**
 * Abre el modal para crear un nuevo activo
 */
function abrirModalCrear() {
  modoEdicion.value = false
  resetearFormulario()
  showModal.value = true
}

/**
 * Abre el modal para editar un activo existente
 * Implementa el patrón híbrido: extrae IDs de los objetos recibidos
 */
function abrirModalEditar(item) {
  modoEdicion.value = true
  
  // Patrón Híbrido: Extraer IDs de los objetos recibidos del backend
  form.id = item.id
  form.codigo_inventario = item.codigo_inventario || ''
  form.tipo_id = item.tipo?.id || null
  form.marca = item.marca || ''
  form.modelo = item.modelo || ''
  form.numero_serie = item.numero_serie || ''
  form.estado_id = item.estado?.id || null
  form.ubicacion_actual_id = item.ubicacion_actual?.id || null
  form.notas = item.notas || ''

  showModal.value = true
}

/**
 * Resetea el formulario a valores por defecto
 */
function resetearFormulario() {
  form.id = null
  form.codigo_inventario = ''
  form.tipo_id = null
  form.marca = ''
  form.modelo = ''
  form.numero_serie = ''
  form.estado_id = null
  form.ubicacion_actual_id = null
  form.notas = ''
  
  if (formRef.value) {
    formRef.value.resetValidation()
  }
}

/**
 * Cierra el modal y resetea el formulario
 */
function cerrarModal() {
  showModal.value = false
  resetearFormulario()
}

/**
 * Guarda el activo (crear o actualizar)
 * Implementa el patrón híbrido: envía solo IDs al backend
 */
async function guardar() {
  // Validar formulario
  const { valid } = await formRef.value.validate()
  if (!valid) {
    return
  }

  guardando.value = true

  try {
    // Patrón Híbrido: Preparar payload con IDs (no objetos)
    const payload = {
      tipo_id: form.tipo_id,
      marca: form.marca,
      modelo: form.modelo,
      numero_serie: form.numero_serie || null,
      estado_id: form.estado_id,
      ubicacion_actual_id: form.ubicacion_actual_id,
      notas: form.notas || null
    }

    if (modoEdicion.value) {
      // Actualizar
      await updateActivo(form.id, payload)
      mostrarSnackbar('Activo actualizado correctamente', 'success')
    } else {
      // Crear
      await createActivo(payload)
      mostrarSnackbar('Activo creado correctamente', 'success')
    }

    cerrarModal()
    
    // Recargar la tabla
    await loadItems({
      page: page.value,
      itemsPerPage: itemsPerPage.value,
      sortBy: []
    })
  } catch (error) {
    console.error('Error al guardar activo:', error)
    const mensaje = error.response?.data?.detail || error.response?.data?.message || 'Error al guardar el activo'
    mostrarSnackbar(mensaje, 'error')
  } finally {
    guardando.value = false
  }
}

// ============================================================================
// MÉTODOS - ELIMINACIÓN
// ============================================================================

/**
 * Abre el diálogo de confirmación para eliminar un activo
 */
function confirmarEliminar(item) {
  activoAEliminar.value = item
  showDialogEliminar.value = true
}

/**
 * Elimina el activo confirmado
 */
async function eliminarActivo() {
  if (!activoAEliminar.value) return

  eliminando.value = true

  try {
    await deleteActivo(activoAEliminar.value.id)
    mostrarSnackbar('Activo eliminado correctamente', 'success')
    showDialogEliminar.value = false
    activoAEliminar.value = null

    // Recargar la tabla
    await loadItems({
      page: page.value,
      itemsPerPage: itemsPerPage.value,
      sortBy: []
    })
  } catch (error) {
    console.error('Error al eliminar activo:', error)
    const mensaje = error.response?.data?.detail || error.response?.data?.message || 'Error al eliminar el activo'
    mostrarSnackbar(mensaje, 'error')
  } finally {
    eliminando.value = false
  }
}

// ============================================================================
// MÉTODOS - UTILIDADES
// ============================================================================

/**
 * Muestra un snackbar con un mensaje
 */
function mostrarSnackbar(mensaje, color = 'success') {
  snackbar.message = mensaje
  snackbar.color = color
  snackbar.show = true
}

/**
 * Obtiene el color del chip según el estado
 */
function getEstadoColor(nombreEstado) {
  const colores = {
    'Operativo': 'success',
    'En Mantenimiento': 'warning',
    'Fuera de Servicio': 'error',
    'Disponible': 'info',
    'Asignado': 'primary'
  }
  return colores[nombreEstado] || 'grey'
}

/**
 * Maneja el cambio en el buscador (con debounce implícito de Vuetify)
 */
function handleSearchChange() {
  // Resetear a página 1 cuando cambia la búsqueda
  page.value = 1
  loadItems({
    page: 1,
    itemsPerPage: itemsPerPage.value,
    sortBy: []
  })
}

/**
 * Maneja el cambio en los filtros
 */
function handleFiltroChange() {
  // Resetear a página 1 cuando cambian los filtros
  page.value = 1
  loadItems({
    page: 1,
    itemsPerPage: itemsPerPage.value,
    sortBy: []
  })
}

// ============================================================================
// LIFECYCLE HOOKS
// ============================================================================

onMounted(async () => {
  // Cargar opciones para los selects
  await cargarOpcionesSelects()
  
  // Cargar datos iniciales de la tabla
  await loadItems({
    page: 1,
    itemsPerPage: itemsPerPage.value,
    sortBy: []
  })
})
</script>

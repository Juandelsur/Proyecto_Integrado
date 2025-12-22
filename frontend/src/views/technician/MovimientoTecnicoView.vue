<template>
  <div class="movimiento-content">
    <!-- ====================================================================
         HEADER
         ==================================================================== -->
    <v-card variant="tonal" color="primary" class="mb-4">
      <v-card-text>
        <h2 class="text-h5 font-weight-bold mb-1">Registrar Movimiento</h2>
        <p class="text-subtitle-1 mb-0">Traslado y cambio de estado de activo</p>
      </v-card-text>
    </v-card>

    <!-- ====================================================================
         SELECCIÓN DE ACTIVO
         ==================================================================== -->
    <v-card class="mb-4">
      <v-card-title class="text-h6 font-weight-bold">
        <v-icon start>mdi-laptop</v-icon>
        Seleccionar Activo
      </v-card-title>
      
      <v-card-text>
        <v-autocomplete
          v-model="activoSeleccionadoId"
          :items="activos"
          :item-title="getActivoLabel"
          item-value="id"
          label="Buscar activo por código, marca o modelo"
          variant="outlined"
          density="comfortable"
          prepend-inner-icon="mdi-magnify"
          clearable
          :loading="loadingActivos"
          @update:model-value="onActivoChange"
        >
          <template v-slot:item="{ props, item }">
            <v-list-item v-bind="props">
              <template v-slot:prepend>
                <v-avatar color="primary" size="small">
                  <v-icon size="small">mdi-laptop</v-icon>
                </v-avatar>
              </template>
              <template v-slot:subtitle>
                <span class="text-caption">{{ item.raw.codigo_inventario }}</span>
              </template>
            </v-list-item>
          </template>
        </v-autocomplete>
      </v-card-text>
    </v-card>

    <!-- ====================================================================
         INFORMACIÓN DEL ACTIVO SELECCIONADO
         ==================================================================== -->
    <v-card v-if="activoSeleccionado" class="mb-4">
      <v-card-title class="text-h6 font-weight-bold bg-blue">
        <v-icon start>mdi-information</v-icon>
        Información del Activo
      </v-card-title>

      <v-card-text class="pa-4">
        <v-row>
          <v-col cols="12" md="6">
            <div class="info-field">
              <p class="text-caption text-grey mb-1">
                <v-icon size="small">mdi-barcode</v-icon>
                Código de Inventario
              </p>
              <p class="text-h6 font-weight-medium mb-3">
                {{ activoSeleccionado.codigo_inventario }}
              </p>
            </div>

            <div class="info-field">
              <p class="text-caption text-grey mb-1">
                <v-icon size="small">mdi-tag</v-icon>
                Marca y Modelo
              </p>
              <p class="text-body-1 font-weight-medium mb-3">
                {{ activoSeleccionado.marca }} {{ activoSeleccionado.modelo }}
              </p>
            </div>

            <div class="info-field">
              <p class="text-caption text-grey mb-1">
                <v-icon size="small">mdi-devices</v-icon>
                Tipo de Equipo
              </p>
              <p class="text-body-1 mb-3">
                {{ activoSeleccionado.tipo?.nombre_tipo || 'N/A' }}
              </p>
            </div>
          </v-col>

          <v-col cols="12" md="6">
            <div class="info-field">
              <p class="text-caption text-grey mb-1">
                <v-icon size="small">mdi-state-machine</v-icon>
                Estado Actual
              </p>
              <v-chip 
                :color="getEstadoColor(activoSeleccionado.estado?.nombre_estado)"
                variant="tonal"
                class="mb-3"
              >
                {{ activoSeleccionado.estado?.nombre_estado || 'Sin estado' }}
              </v-chip>
            </div>

            <div class="info-field">
              <p class="text-caption text-grey mb-1">
                <v-icon size="small">mdi-map-marker</v-icon>
                Ubicación Actual
              </p>
              <v-chip color="primary" variant="tonal" class="mb-3">
                {{ activoSeleccionado.ubicacion_actual?.nombre_ubicacion || 'Sin ubicación' }}
              </v-chip>
            </div>

            <div class="info-field" v-if="activoSeleccionado.numero_serie">
              <p class="text-caption text-grey mb-1">
                <v-icon size="small">mdi-numeric</v-icon>
                Número de Serie
              </p>
              <p class="text-body-1">
                {{ activoSeleccionado.numero_serie }}
              </p>
            </div>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- ====================================================================
         FORMULARIO DE MOVIMIENTO
         ==================================================================== -->
    <v-card v-if="activoSeleccionado" class="mb-4">
      <v-card-title class="text-h6 font-weight-bold bg-orange">
        <v-icon start>mdi-swap-horizontal</v-icon>
        Datos del Movimiento
      </v-card-title>

      <v-card-text class="pa-4">
        <v-form ref="formRef">
          <!-- Tipo de Movimiento -->
          <v-select
            v-model="formulario.tipo_movimiento"
            :items="tiposMovimiento"
            item-title="text"
            item-value="value"
            label="Tipo de Movimiento *"
            variant="outlined"
            density="comfortable"
            prepend-inner-icon="mdi-swap-horizontal"
            :rules="[v => !!v || 'Campo requerido']"
            class="mb-3"
          ></v-select>

          <v-row>
            <!-- Ubicación Origen (Solo lectura) -->
            <v-col cols="12" md="6">
              <v-text-field
                :model-value="activoSeleccionado.ubicacion_actual?.nombre_ubicacion || 'Sin ubicación'"
                label="Ubicación Origen"
                variant="outlined"
                density="comfortable"
                prepend-inner-icon="mdi-map-marker-outline"
                readonly
                class="mb-3"
              ></v-text-field>
            </v-col>

            <!-- Ubicación Destino -->
            <v-col cols="12" md="6">
              <v-select
                v-model="formulario.ubicacion_destino"
                :items="ubicaciones"
                item-title="nombre_ubicacion"
                item-value="id"
                label="Ubicación Destino *"
                variant="outlined"
                density="comfortable"
                prepend-inner-icon="mdi-map-marker"
                :rules="[v => !!v || 'Campo requerido']"
                class="mb-3"
              ></v-select>
            </v-col>
          </v-row>

          <!-- Cambiar Estado del Activo -->
          <v-row>
            <v-col cols="12">
              <v-checkbox
                v-model="cambiarEstado"
                label="Cambiar estado del activo"
                color="primary"
                hide-details
                class="mb-2"
              ></v-checkbox>
            </v-col>
          </v-row>

          <v-expand-transition>
            <v-row v-show="cambiarEstado">
              <v-col cols="12" md="6">
                <v-text-field
                  :model-value="activoSeleccionado.estado?.nombre_estado || 'Sin estado'"
                  label="Estado Actual"
                  variant="outlined"
                  density="comfortable"
                  prepend-inner-icon="mdi-state-machine"
                  readonly
                  class="mb-3"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-select
                  v-model="formulario.nuevo_estado"
                  :items="estados"
                  item-title="nombre_estado"
                  item-value="id"
                  label="Nuevo Estado *"
                  variant="outlined"
                  density="comfortable"
                  prepend-inner-icon="mdi-state-machine"
                  :rules="cambiarEstado ? [v => !!v || 'Campo requerido'] : []"
                  class="mb-3"
                ></v-select>
              </v-col>
            </v-row>
          </v-expand-transition>

          <!-- Observaciones -->
          <v-textarea
            v-model="formulario.observaciones"
            label="Observaciones (opcional)"
            variant="outlined"
            density="comfortable"
            rows="3"
            prepend-inner-icon="mdi-note-text"
            placeholder="Agrega notas o comentarios sobre este movimiento"
          ></v-textarea>
        </v-form>
      </v-card-text>
    </v-card>

    <!-- ====================================================================
         BOTONES DE ACCIÓN
         ==================================================================== -->
    <v-card v-if="activoSeleccionado">
      <v-card-actions class="pa-4">
        <v-btn
          variant="outlined"
          size="large"
          prepend-icon="mdi-arrow-left"
          @click="volver"
        >
          Volver
        </v-btn>

        <v-spacer></v-spacer>

        <v-btn
          color="primary"
          size="large"
          prepend-icon="mdi-content-save"
          :loading="guardando"
          @click="guardarMovimiento"
        >
          Guardar Movimiento
        </v-btn>
      </v-card-actions>
    </v-card>

    <!-- ====================================================================
         EMPTY STATE (Sin activo seleccionado)
         ==================================================================== -->
    <v-card v-else class="text-center pa-8">
      <v-icon size="64" color="grey-lighten-1">mdi-arrow-up</v-icon>
      <p class="text-h6 mt-4 mb-2">Selecciona un activo para comenzar</p>
      <p class="text-body-2 text-grey">
        Usa el buscador superior para encontrar el activo que deseas mover
      </p>
    </v-card>

    <!-- ====================================================================
         DIÁLOGO DE CONFIRMACIÓN
         ==================================================================== -->
    <v-dialog v-model="showConfirmDialog" max-width="500px">
      <v-card>
        <v-card-title class="text-h6 pa-4 bg-orange-lighten-5">
          <v-icon start color="warning">mdi-alert</v-icon>
          Confirmar Movimiento
        </v-card-title>

        <v-card-text class="pa-4">
          <p class="text-body-1 mb-3">
            ¿Estás seguro de que deseas registrar este movimiento?
          </p>

          <v-list density="compact" class="bg-grey-lighten-5 rounded">
            <v-list-item>
              <template v-slot:prepend>
                <v-icon size="small">mdi-laptop</v-icon>
              </template>
              <v-list-item-title class="text-body-2">
                <strong>Activo:</strong> {{ activoSeleccionado?.marca }} {{ activoSeleccionado?.modelo }}
              </v-list-item-title>
            </v-list-item>

            <v-list-item>
              <template v-slot:prepend>
                <v-icon size="small">mdi-swap-horizontal</v-icon>
              </template>
              <v-list-item-title class="text-body-2">
                <strong>Tipo:</strong> {{ getTipoMovimientoText(formulario.tipo_movimiento) }}
              </v-list-item-title>
            </v-list-item>

            <v-list-item>
              <template v-slot:prepend>
                <v-icon size="small">mdi-map-marker</v-icon>
              </template>
              <v-list-item-title class="text-body-2">
                <strong>Destino:</strong> {{ getUbicacionNombre(formulario.ubicacion_destino) }}
              </v-list-item-title>
            </v-list-item>

            <v-list-item v-if="cambiarEstado">
              <template v-slot:prepend>
                <v-icon size="small">mdi-state-machine</v-icon>
              </template>
              <v-list-item-title class="text-body-2">
                <strong>Nuevo Estado:</strong> {{ getEstadoNombre(formulario.nuevo_estado) }}
              </v-list-item-title>
            </v-list-item>
          </v-list>
        </v-card-text>

        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn
            variant="text"
            @click="showConfirmDialog = false"
          >
            Cancelar
          </v-btn>
          <v-btn
            color="primary"
            :loading="guardando"
            @click="confirmarGuardar"
          >
            Confirmar
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
      :timeout="4000"
      location="top"
    >
      <div class="d-flex align-items-center">
        <v-icon start>{{ snackbar.icon }}</v-icon>
        <span>{{ snackbar.text }}</span>
      </div>
    </v-snackbar>
  </div>
</template>

<script setup>
/**
 * ============================================================================
 * REGISTRAR MOVIMIENTO DE ACTIVO
 * ============================================================================
 *
 * Permite:
 * - Seleccionar un activo
 * - Ver su información completa
 * - Cambiar su ubicación
 * - Cambiar su estado (opcional)
 * - Agregar observaciones
 */

import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import apiClient from '@/services/api'

// ============================================================================
// COMPOSABLES
// ============================================================================

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

// ============================================================================
// STATE
// ============================================================================

const activos = ref([])
const ubicaciones = ref([])
const estados = ref([])
const activoSeleccionadoId = ref(null)
const activoSeleccionado = ref(null)
const cambiarEstado = ref(false)
const loadingActivos = ref(false)
const guardando = ref(false)
const showConfirmDialog = ref(false)
const formRef = ref(null)

const tiposMovimiento = [
  { text: 'Traslado', value: 'TRASLADO' },
  { text: 'Asignación', value: 'ASIGNACION' },
  { text: 'Devolución', value: 'DEVOLUCION' },
  { text: 'Envío a Mantenimiento', value: 'MANTENIMIENTO' },
  { text: 'Retorno de Mantenimiento', value: 'RETORNO' },
  { text: 'Baja de Activo', value: 'BAJA' }
]

const formulario = ref({
  tipo_movimiento: null,
  ubicacion_destino: null,
  nuevo_estado: null,
  observaciones: ''
})

const snackbar = ref({
  show: false,
  text: '',
  color: 'success',
  icon: 'mdi-check-circle'
})

// ============================================================================
// COMPUTED
// ============================================================================

/**
 * ID del usuario actual
 */
const usuarioActualId = computed(() => {
  return authStore.user?.id
})

// ============================================================================
// MÉTODOS - API
// ============================================================================

/**
 * Carga todos los activos
 */
async function cargarActivos() {
  loadingActivos.value = true
  try {
    const response = await apiClient.get('/api/activos/', {
      params: { page_size: 1000 }
    })
    
    activos.value = Array.isArray(response.data) 
      ? response.data 
      : response.data.results || []

    console.log(`✅ Cargados ${activos.value.length} activos`)

  } catch (error) {
    console.error('Error al cargar activos:', error)
    mostrarNotificacion('Error al cargar los activos', 'error', 'mdi-alert-circle')
  } finally {
    loadingActivos.value = false
  }
}

/**
 * Carga un activo específico por ID (desde escaneo QR)
 */
async function cargarActivoPorId(activoId) {
  loadingActivos.value = true
  try {
    console.log(`🔍 Cargando activo con ID: ${activoId}`)
    
    const response = await apiClient.get(`/api/activos/${activoId}/`)
    
    activoSeleccionado.value = response.data
    activoSeleccionadoId.value = activoId
    
    console.log('✅ Activo cargado desde URL:', activoSeleccionado.value)
    
    mostrarNotificacion(
      `Activo cargado: ${activoSeleccionado.value.marca} ${activoSeleccionado.value.modelo}`,
      'success',
      'mdi-check-circle'
    )

  } catch (error) {
    console.error('❌ Error al cargar activo por ID:', error)
    mostrarNotificacion(
      'No se pudo cargar el activo. Usa el buscador para seleccionarlo.',
      'error',
      'mdi-alert-circle'
    )
  } finally {
    loadingActivos.value = false
  }
}

/**
 * Carga las ubicaciones
 */
async function cargarUbicaciones() {
  try {
    const response = await apiClient.get('/api/ubicaciones/', {
      params: { page_size: 1000 }
    })
    ubicaciones.value = Array.isArray(response.data) 
      ? response.data 
      : response.data.results || []
  } catch (error) {
    console.error('Error al cargar ubicaciones:', error)
  }
}

/**
 * Carga los estados
 */
async function cargarEstados() {
  try {
    const response = await apiClient.get('/api/estados-activo/', {
      params: { page_size: 1000 }
    })
    estados.value = Array.isArray(response.data) 
      ? response.data 
      : response.data.results || []
  } catch (error) {
    console.error('Error al cargar estados:', error)
  }
}

/**
 * Guarda el movimiento
 */
async function confirmarGuardar() {
  try {
    guardando.value = true

    // Preparar payload del movimiento
    const payload = {
      activo_id: activoSeleccionado.value.id,
      tipo_movimiento: formulario.value.tipo_movimiento,
      ubicacion_origen_id: activoSeleccionado.value.ubicacion_actual?.id || null,
      ubicacion_destino_id: formulario.value.ubicacion_destino,
      observaciones: formulario.value.observaciones?.trim() || ''
    }

    console.log('📤 Enviando movimiento:', payload)

    // Registrar el movimiento
    await apiClient.post('/api/historial-movimientos/', payload)

    // Si se cambió el estado, actualizar el activo
    if (cambiarEstado.value && formulario.value.nuevo_estado) {
      const payloadActivo = {
        estado_id: formulario.value.nuevo_estado,
        ubicacion_actual_id: formulario.value.ubicacion_destino
      }

      console.log('📤 Actualizando activo:', payloadActivo)

      await apiClient.patch(
        `/api/activos/${activoSeleccionado.value.id}/`,
        payloadActivo
      )
    } else {
      // Solo actualizar ubicación
      const payloadActivo = {
        ubicacion_actual_id: formulario.value.ubicacion_destino
      }

      await apiClient.patch(
        `/api/activos/${activoSeleccionado.value.id}/`,
        payloadActivo
      )
    }

    mostrarNotificacion(
      'Movimiento registrado correctamente', 
      'success', 
      'mdi-check-circle'
    )

    showConfirmDialog.value = false

    // Limpiar formulario y recargar activo
    setTimeout(() => {
      limpiarFormulario()
      cargarActivos()
    }, 1500)

  } catch (error) {
    console.error('❌ Error al guardar movimiento:', error)
    
    let mensajeError = 'Error al registrar el movimiento'
    
    if (error.response?.data) {
      console.error('📥 Detalle del error:', error.response.data)
      
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
    }
    
    mostrarNotificacion(mensajeError, 'error', 'mdi-alert-circle')
    showConfirmDialog.value = false

  } finally {
    guardando.value = false
  }
}

// ============================================================================
// MÉTODOS - UI
// ============================================================================

/**
 * Maneja el cambio de activo seleccionado
 */
function onActivoChange() {
  if (!activoSeleccionadoId.value) {
    activoSeleccionado.value = null
    limpiarFormulario()
    return
  }

  activoSeleccionado.value = activos.value.find(
    a => a.id === activoSeleccionadoId.value
  )

  if (activoSeleccionado.value) {
    console.log('✅ Activo seleccionado:', activoSeleccionado.value)
    limpiarFormulario()
  }
}

/**
 * Valida y muestra confirmación
 */
async function guardarMovimiento() {
  // Validar formulario
  const { valid } = await formRef.value.validate()
  if (!valid) {
    mostrarNotificacion('Por favor completa todos los campos requeridos', 'warning', 'mdi-alert')
    return
  }

  // Validar que la ubicación destino sea diferente
  if (formulario.value.ubicacion_destino === activoSeleccionado.value.ubicacion_actual?.id) {
    mostrarNotificacion(
      'La ubicación destino debe ser diferente a la ubicación actual', 
      'warning', 
      'mdi-alert'
    )
    return
  }

  // Mostrar confirmación
  showConfirmDialog.value = true
}

/**
 * Limpia el formulario
 */
function limpiarFormulario() {
  formulario.value = {
    tipo_movimiento: null,
    ubicacion_destino: null,
    nuevo_estado: null,
    observaciones: ''
  }
  cambiarEstado.value = false

  if (formRef.value) {
    formRef.value.resetValidation()
  }
}

/**
 * Obtiene el label del activo para el autocomplete
 */
function getActivoLabel(activo) {
  return `${activo.marca} ${activo.modelo} - ${activo.codigo_inventario}`
}

/**
 * Obtiene el nombre del tipo de movimiento
 */
function getTipoMovimientoText(tipo) {
  const item = tiposMovimiento.find(t => t.value === tipo)
  return item?.text || tipo
}

/**
 * Obtiene el nombre de la ubicación
 */
function getUbicacionNombre(ubicacionId) {
  const ubicacion = ubicaciones.value.find(u => u.id === ubicacionId)
  return ubicacion?.nombre_ubicacion || 'N/A'
}

/**
 * Obtiene el nombre del estado
 */
function getEstadoNombre(estadoId) {
  const estado = estados.value.find(e => e.id === estadoId)
  return estado?.nombre_estado || 'N/A'
}

/**
 * Obtiene el color según el estado
 */
function getEstadoColor(estado) {
  const colores = {
    'Operativo': 'success',
    'En Reparación': 'warning',
    'En Bodega TI': 'info',
    'De Baja': 'error'
  }
  return colores[estado] || 'grey'
}

/**
 * Muestra notificación
 */
function mostrarNotificacion(text, color = 'success', icon = 'mdi-check-circle') {
  snackbar.value = {
    show: true,
    text,
    color,
    icon
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
  // Primero cargar los datos necesarios (ubicaciones y estados)
  await Promise.all([
    cargarActivos(), // Cargar activos para el autocomplete
    cargarUbicaciones(),
    cargarEstados()
  ])

  // Si viene un activo_id desde la URL (desde escaneo QR), cargarlo automáticamente
  const activoIdFromUrl = route.query.activo_id || route.params.activo_id
  
  if (activoIdFromUrl) {
    console.log('🎯 Detectado activo_id en URL:', activoIdFromUrl)
    await cargarActivoPorId(parseInt(activoIdFromUrl))
  }
})

</script>

<style scoped>
/* ============================================================================
   CONTENEDOR PRINCIPAL
   ============================================================================ */

.movimiento-content {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 1rem;
  padding-bottom: 2rem;
}

/* ============================================================================
   INFO FIELDS
   ============================================================================ */

.info-field {
  margin-bottom: 1rem;
}

/* ============================================================================
   RESPONSIVE
   ============================================================================ */

@media (max-width: 600px) {
  .movimiento-content {
    padding: 0.75rem;
  }
}

@media (min-width: 960px) {
  .movimiento-content {
    max-width: 1200px;
    margin: 0 auto;
  }
}
</style>
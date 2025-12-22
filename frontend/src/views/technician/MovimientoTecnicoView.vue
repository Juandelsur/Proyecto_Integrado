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
         LOADING INICIAL
         ==================================================================== -->
    <div v-if="loadingInicial" class="loading-container">
      <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
      <p class="mt-3 text-h6">Cargando información del activo...</p>
    </div>

    <!-- ====================================================================
         INFORMACIÓN DEL ACTIVO SELECCIONADO
         ==================================================================== -->
    <v-card v-else-if="activoSeleccionado" class="mb-4">
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
                v-model="formulario.ubicacion_destino_id"
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
                  v-model="formulario.nuevo_estado_id"
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

          <!-- Comentarios -->
          <v-textarea
            v-model="formulario.comentarios"
            label="Comentarios (opcional)"
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
         EMPTY STATE (Error al cargar)
         ==================================================================== -->
    <v-card v-else-if="!loadingInicial" class="text-center pa-8">
      <v-icon size="64" color="error">mdi-alert-circle</v-icon>
      <p class="text-h6 mt-4 mb-2">No se pudo cargar el activo</p>
      <p class="text-body-2 text-grey mb-4">
        El activo solicitado no existe o hubo un error al cargarlo
      </p>
      <v-btn
        variant="outlined"
        prepend-icon="mdi-arrow-left"
        @click="volver"
      >
        Volver
      </v-btn>
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
                <strong>Destino:</strong> {{ getUbicacionNombre(formulario.ubicacion_destino_id) }}
              </v-list-item-title>
            </v-list-item>

            <v-list-item v-if="cambiarEstado">
              <template v-slot:prepend>
                <v-icon size="small">mdi-state-machine</v-icon>
              </template>
              <v-list-item-title class="text-body-2">
                <strong>Nuevo Estado:</strong> {{ getEstadoNombre(formulario.nuevo_estado_id) }}
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
 * REGISTRAR MOVIMIENTO DE ACTIVO - TÉCNICO
 * ============================================================================
 *
 * Recibe el ID del activo desde la ruta: /confirmar-equipo/:id
 * Permite:
 * - Ver información completa del activo
 * - Cambiar su ubicación
 * - Cambiar su estado (opcional)
 * - Agregar comentarios
 */

import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import apiClient from '@/services/api'

// ============================================================================
// COMPOSABLES
// ============================================================================

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

// Obtener el ID desde los props (viene de la ruta)
const props = defineProps({
  id: {
    type: String,
    required: true
  }
})

// ============================================================================
// STATE
// ============================================================================

const ubicaciones = ref([])
const estados = ref([])
const activoSeleccionado = ref(null)
const cambiarEstado = ref(false)
const loadingInicial = ref(true)
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
  ubicacion_destino_id: null,
  nuevo_estado_id: null,
  comentarios: ''
})

const snackbar = ref({
  show: false,
  text: '',
  color: 'success',
  icon: 'mdi-check-circle'
})

// ============================================================================
// MÉTODOS - API
// ============================================================================

/**
 * Carga un activo específico por ID
 */
async function cargarActivo() {
  loadingInicial.value = true
  try {
    const activoId = parseInt(props.id)
    console.log(`🔍 Cargando activo con ID: ${activoId}`)
    
    const response = await apiClient.get(`/api/activos/${activoId}/`)
    
    activoSeleccionado.value = response.data
    
    console.log('✅ Activo cargado:', activoSeleccionado.value)
    
    mostrarNotificacion(
      `Activo cargado: ${activoSeleccionado.value.marca} ${activoSeleccionado.value.modelo}`,
      'success',
      'mdi-check-circle'
    )

  } catch (error) {
    console.error('❌ Error al cargar activo:', error)
    mostrarNotificacion(
      'No se pudo cargar el activo solicitado',
      'error',
      'mdi-alert-circle'
    )
    activoSeleccionado.value = null
  } finally {
    loadingInicial.value = false
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
    
    console.log(`✅ Cargadas ${ubicaciones.value.length} ubicaciones`)
  } catch (error) {
    console.error('Error al cargar ubicaciones:', error)
    mostrarNotificacion('Error al cargar ubicaciones', 'error', 'mdi-alert-circle')
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
    
    console.log(`✅ Cargados ${estados.value.length} estados`)
  } catch (error) {
    console.error('Error al cargar estados:', error)
    mostrarNotificacion('Error al cargar estados', 'error', 'mdi-alert-circle')
  }
}

/**
 * Guarda el movimiento
 */
async function confirmarGuardar() {
  try {
    guardando.value = true

    // Preparar payload del movimiento según la estructura de la API
    // MODO ESCRITURA: Enviar solo IDs (activo_id, usuario_registra_id, ubicacion_origen_id, ubicacion_destino_id)
    // La API devolverá objetos completos + códigos en modo lectura (GET)
    const payload = {
      activo_id: activoSeleccionado.value.id,
      usuario_registra_id: authStore.user?.id,
      ubicacion_origen_id: activoSeleccionado.value.ubicacion_actual?.id || null,
      ubicacion_destino_id: formulario.value.ubicacion_destino_id,
      tipo_movimiento: formulario.value.tipo_movimiento,
      comentarios: formulario.value.comentarios?.trim() || ''
    }

    console.log('📤 Enviando movimiento:', payload)

    // Registrar el movimiento
    const responseMovimiento = await apiClient.post('/api/historial-movimientos/', payload)
    console.log('✅ Movimiento registrado:', responseMovimiento.data)

    // Preparar payload para actualizar el activo
    const payloadActivo = {
      ubicacion_actual_id: formulario.value.ubicacion_destino_id
    }

    // Si se cambió el estado, incluirlo en la actualización
    if (cambiarEstado.value && formulario.value.nuevo_estado_id) {
      payloadActivo.estado_id = formulario.value.nuevo_estado_id
    }

    console.log('📤 Actualizando activo:', payloadActivo)

    // Actualizar el activo
    await apiClient.patch(
      `/api/activos/${activoSeleccionado.value.id}/`,
      payloadActivo
    )

    console.log('✅ Activo actualizado')

    mostrarNotificacion(
      'Movimiento registrado correctamente', 
      'success', 
      'mdi-check-circle'
    )

    showConfirmDialog.value = false

    // Redirigir después de 1.5 segundos
    setTimeout(() => {
      router.push('/tecnico/home')
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
      } else if (typeof error.response.data === 'string') {
        mensajeError = error.response.data
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
  if (formulario.value.ubicacion_destino_id === activoSeleccionado.value.ubicacion_actual?.id) {
    mostrarNotificacion(
      'La ubicación destino debe ser diferente a la ubicación actual', 
      'warning', 
      'mdi-alert'
    )
    return
  }

  // Validar que si está marcado "cambiar estado", se haya seleccionado uno
  if (cambiarEstado.value && !formulario.value.nuevo_estado_id) {
    mostrarNotificacion(
      'Por favor selecciona el nuevo estado del activo', 
      'warning', 
      'mdi-alert'
    )
    return
  }

  // Mostrar confirmación
  showConfirmDialog.value = true
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
  console.log('🎯 ID del activo desde ruta:', props.id)
  
  // Cargar datos en paralelo
  await Promise.all([
    cargarActivo(),
    cargarUbicaciones(),
    cargarEstados()
  ])
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
   LOADING STATE
   ============================================================================ */

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 1rem;
  min-height: 400px;
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
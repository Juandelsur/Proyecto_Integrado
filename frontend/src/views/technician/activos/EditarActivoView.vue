<template>
  <div class="editar-activo-content">
    <!-- ====================================================================
         HEADER CON TÍTULO
         ==================================================================== -->
    <div class="header-section">
      <h1 class="entity-title">Editar Activo</h1>
      <p v-if="!loading && activo.codigo_inventario" class="subtitle">
        Código: {{ activo.codigo_inventario }}
      </p>
    </div>

    <!-- ====================================================================
         LOADING STATE
         ==================================================================== -->
    <div v-if="loading" class="loading-container">
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
      <p class="mt-3">Cargando datos...</p>
    </div>

    <!-- ====================================================================
         FORMULARIO PRINCIPAL
         ==================================================================== -->
    <v-card v-else class="form-card" elevation="2">
      <v-card-text class="pa-6">
        <v-form ref="formRef">
          <!-- Código de inventario (solo lectura) -->
          <v-text-field
            v-model="activo.codigo_inventario"
            label="Código de Inventario"
            variant="outlined"
            density="comfortable"
            prepend-inner-icon="mdi-barcode"
            readonly
            class="mb-4"
            bg-color="grey-lighten-4"
          ></v-text-field>

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
            class="mb-4"
          ></v-select>

          <!-- Marca y Modelo -->
          <v-row class="mb-4">
            <v-col cols="12" sm="6">
              <v-text-field
                v-model="formulario.marca"
                label="Marca *"
                variant="outlined"
                density="comfortable"
                prepend-inner-icon="mdi-tag"
                :rules="[v => !!v || 'Campo requerido']"
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
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
            hint="Opcional"
            persistent-hint
            class="mb-4"
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
            class="mb-4"
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
            class="mb-4"
          ></v-select>

          <!-- Notas -->
          <v-textarea
            v-model="formulario.notas"
            label="Notas"
            variant="outlined"
            density="comfortable"
            rows="4"
            prepend-inner-icon="mdi-note-text"
            hint="Información adicional sobre el activo"
            persistent-hint
          ></v-textarea>
        </v-form>
      </v-card-text>

      <!-- ====================================================================
           ACCIONES DEL FORMULARIO
           ==================================================================== -->
      <v-card-actions class="pa-6 pt-0">
        <v-btn
          variant="outlined"
          size="large"
          prepend-icon="mdi-arrow-left"
          @click="volver"
          :disabled="guardando"
        >
          Volver
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn
          color="primary"
          size="large"
          prepend-icon="mdi-content-save"
          @click="guardar"
          :loading="guardando"
        >
          Guardar Cambios
        </v-btn>
      </v-card-actions>
    </v-card>

    <!-- ====================================================================
         SNACKBAR NOTIFICACIONES
         ==================================================================== -->
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="3000"
      location="top"
    >
      {{ snackbar.text }}
      <template v-slot:actions>
        <v-btn
          variant="text"
          @click="snackbar.show = false"
        >
          Cerrar
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script setup>
/**
 * ============================================================================
 * EDITAR ACTIVO
 * ============================================================================
 *
 * Funcionalidades:
 * - Formulario para editar un activo existente
 * - Carga de datos del activo por ID
 * - Validación de campos requeridos
 * - Actualización de datos del activo
 * - Notificaciones de éxito/error
 * - Navegación de retorno
 */

import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import apiClient from '@/services/api'

// ============================================================================
// COMPOSABLES
// ============================================================================

const router = useRouter()
const route = useRoute()

// ============================================================================
// STATE
// ============================================================================

const loading = ref(false)
const guardando = ref(false)
const tiposEquipo = ref([])
const estados = ref([])
const ubicaciones = ref([])
const formRef = ref(null)

const activo = ref({
  codigo_inventario: ''
})

const snackbar = ref({
  show: false,
  text: '',
  color: 'success'
})

const formulario = ref({
  tipo: null,
  marca: '',
  modelo: '',
  numero_serie: '',
  estado: null,
  ubicacion_actual: null,
  notas: ''
})

// ============================================================================
// MÉTODOS - API
// ============================================================================

/**
 * Carga los datos del activo a editar
 */
async function cargarActivo() {
  // Obtener el identificador de la ruta
  // Puede venir en params (:id) o en query (?codigo=XXX)
  const identificador = route.params.id || route.query.codigo
  
  console.log('🔍 Parámetros de la ruta:', route.params)
  console.log('🔍 Query de la ruta:', route.query)
  console.log('🔍 Identificador recibido:', identificador)
  console.log('🔍 Ruta completa:', route.path)
  
  if (!identificador) {
    console.error('❌ No se encontró identificador en route.params.id ni route.query.codigo')
    mostrarNotificacion('Identificador de activo no válido', 'error')
    volver()
    return
  }

  try {
    // Primero intentar cargar todos los activos y buscar por código o ID
    const response = await apiClient.get('/api/activos/', {
      params: { page_size: 1000 }
    })
    
    const activos = Array.isArray(response.data) 
      ? response.data 
      : response.data.results || []
    
    console.log('📦 Total de activos cargados:', activos.length)
    
    // Buscar el activo por ID o por código de inventario
    const activoEncontrado = activos.find(a => 
      a.id?.toString() === identificador || 
      a.codigo_inventario === identificador
    )
    
    console.log('🔎 Activo encontrado:', activoEncontrado)
    
    if (!activoEncontrado) {
      console.error('❌ No se encontró activo con identificador:', identificador)
      mostrarNotificacion('Activo no encontrado', 'error')
      volver()
      return
    }
    
    activo.value = activoEncontrado
    
    // Llenar el formulario con los datos del activo
    // Usar la misma estructura que el código de referencia
    formulario.value = {
      tipo: activoEncontrado.tipo?.id || null,
      marca: activoEncontrado.marca,
      modelo: activoEncontrado.modelo,
      numero_serie: activoEncontrado.numero_serie || '',
      estado: activoEncontrado.estado?.id || null,
      ubicacion_actual: activoEncontrado.ubicacion_actual?.id || null,
      notas: activoEncontrado.notas || ''
    }
    
    console.log('✅ Activo cargado:', activoEncontrado)
    console.log('📋 Formulario inicializado:', formulario.value)
    
  } catch (error) {
    console.error('Error al cargar el activo:', error)
    mostrarNotificacion('Error al cargar el activo', 'error')
    volver()
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
    tiposEquipo.value = Array.isArray(response.data) 
      ? response.data 
      : response.data.results || []
  } catch (error) {
    console.error('Error al cargar tipos de equipo:', error)
    mostrarNotificacion('Error al cargar tipos de equipo', 'error')
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
    estados.value = Array.isArray(response.data) 
      ? response.data 
      : response.data.results || []
  } catch (error) {
    console.error('Error al cargar estados:', error)
    mostrarNotificacion('Error al cargar estados', 'error')
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
    ubicaciones.value = Array.isArray(response.data) 
      ? response.data 
      : response.data.results || []
  } catch (error) {
    console.error('Error al cargar ubicaciones:', error)
    mostrarNotificacion('Error al cargar ubicaciones', 'error')
  }
}

/**
 * Guarda los cambios del activo
 */
async function guardar() {
  // Validar formulario
  const { valid } = await formRef.value.validate()
  if (!valid) {
    mostrarNotificacion('Por favor complete todos los campos requeridos', 'warning')
    return
  }

  guardando.value = true

  try {
    // Usar el ID del activo cargado, no el parámetro de la ruta
    const activoId = activo.value.id
    
    if (!activoId) {
      mostrarNotificacion('Error: ID de activo no disponible', 'error')
      return
    }
    
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
    console.log('📍 ID del activo:', activoId)

    // Actualizar activo
    const response = await apiClient.put(`/api/activos/${activoId}/`, payload)
    
    console.log('✅ Activo actualizado:', response.data)
    
    mostrarNotificacion('Activo actualizado exitosamente', 'success')
    
    // Esperar un momento para que el usuario vea la notificación
    setTimeout(() => {
      volver()
    }, 1500)
    
  } catch (error) {
    console.error('❌ Error al guardar:', error)
    
    // Mostrar error detallado del servidor
    if (error.response?.data) {
      console.error('📥 Detalle del error:', error.response.data)
      
      // Crear mensaje de error más descriptivo
      let mensajeError = 'Error al actualizar el activo'
      
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
      mostrarNotificacion('Error al actualizar el activo', 'error')
    }
  } finally {
    guardando.value = false
  }
}

// ============================================================================
// MÉTODOS - UI
// ============================================================================

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
  loading.value = true
  try {
    await Promise.all([
      cargarTiposEquipo(),
      cargarEstados(),
      cargarUbicaciones(),
      cargarActivo()
    ])
  } finally {
    loading.value = false
  }
})

</script>

<style scoped>
/* ============================================================================
   CONTENEDOR PRINCIPAL
   ============================================================================ */

.editar-activo-content {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 2rem 1rem;
  max-width: 800px;
  margin: 0 auto;
}

/* ============================================================================
   HEADER
   ============================================================================ */

.header-section {
  margin-bottom: 2rem;
  text-align: center;
}

.entity-title {
  font-size: 1.75rem;
  font-weight: 600;
  color: #333;
  margin: 0 0 0.5rem 0;
}

.subtitle {
  font-size: 0.95rem;
  color: #666;
  margin: 0;
}

/* ============================================================================
   CARD DEL FORMULARIO
   ============================================================================ */

.form-card {
  background: white;
  border-radius: 12px;
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
   RESPONSIVE
   ============================================================================ */

@media (max-width: 600px) {
  .editar-activo-content {
    padding: 1rem 0.75rem;
  }

  .entity-title {
    font-size: 1.5rem;
  }

  .subtitle {
    font-size: 0.875rem;
  }

  .form-card {
    border-radius: 8px;
  }

  .form-card .v-card-text {
    padding: 1.25rem !important;
  }

  .form-card .v-card-actions {
    padding: 1.25rem !important;
    padding-top: 0 !important;
    flex-direction: column-reverse;
    gap: 0.75rem;
  }

  .form-card .v-card-actions .v-btn {
    width: 100%;
  }
}
</style>
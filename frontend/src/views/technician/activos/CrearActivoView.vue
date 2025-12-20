<template>
  <div class="nuevo-activo-content">
    <!-- ====================================================================
         HEADER CON TÍTULO
         ==================================================================== -->
    <div class="header-section">
      <h1 class="entity-title">Registrar Nuevo Activo</h1>
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
          <!-- Información sobre código de inventario -->
          <v-alert
            type="info"
            variant="tonal"
            density="compact"
            class="mb-6"
          >
            <template v-slot:prepend>
              <v-icon>mdi-information</v-icon>
            </template>
            El código de inventario se generará automáticamente al crear el activo
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
          Guardar Activo
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
 * REGISTRAR NUEVO ACTIVO
 * ============================================================================
 *
 * Funcionalidades:
 * - Formulario para crear un nuevo activo
 * - Validación de campos requeridos
 * - Generación automática de código de inventario
 * - Notificaciones de éxito/error
 * - Navegación de retorno
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

const loading = ref(false)
const guardando = ref(false)
const tiposEquipo = ref([])
const estados = ref([])
const ubicaciones = ref([])
const formRef = ref(null)

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
 * Guarda el nuevo activo
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

    // Crear nuevo activo
    const response = await apiClient.post('/api/activos/', payload)
    
    console.log('✅ Activo creado:', response.data)
    
    mostrarNotificacion('Activo registrado exitosamente', 'success')
    
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
      cargarUbicaciones()
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

.nuevo-activo-content {
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
}

.entity-title {
  font-size: 1.75rem;
  font-weight: 600;
  color: #333;
  margin: 0;
  text-align: center;
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
  .nuevo-activo-content {
    padding: 1rem 0.75rem;
  }

  .entity-title {
    font-size: 1.5rem;
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
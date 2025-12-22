<template>
  <div class="editar-activo-content">

    <!-- ============================================================
         BUSCAR ACTIVO
         ============================================================ -->
    <v-card class="form-card mb-6" elevation="2">
      <v-card-text class="pa-6">
        <h2 class="entity-title mb-4">Buscar Activo</h2>

        <v-row dense>
          <v-col cols="8">
            <v-text-field
              v-model="codigoBusqueda"
              label="Código de Inventario"
              variant="outlined"
              density="comfortable"
              prepend-inner-icon="mdi-barcode-scan"
              hint="Ingrese o escanee el código"
              persistent-hint
              @keyup.enter="buscarActivo"
            />
          </v-col>

          <v-col cols="2" class="d-flex align-center">
            <v-btn
              color="primary"
              variant="tonal"
              block
              height="56"
              icon="mdi-qrcode-scan"
              @click="abrirCamara"
            />
          </v-col>

          <v-col cols="2" class="d-flex align-center">
            <v-btn
              color="primary"
              block
              height="56"
              prepend-icon="mdi-magnify"
              :loading="loading"
              @click="buscarActivo"
            >
              Buscar
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- ============================================================
         LOADING
         ============================================================ -->
    <div v-if="loading" class="loading-container">
      <v-progress-circular indeterminate color="primary" />
      <p class="mt-3">Buscando activo...</p>
    </div>

    <!-- ============================================================
         HEADER
         ============================================================ -->
    <div v-if="activo.id" class="header-section">
      <h1 class="entity-title">Editar Activo</h1>
      <p class="subtitle">Código: {{ activo.codigo_inventario }}</p>
    </div>

    <!-- ============================================================
         FORMULARIO
         ============================================================ -->
    <v-card v-if="activo.id" class="form-card" elevation="2">
      <v-card-text class="pa-6">
        <v-form ref="formRef">

          <v-text-field
            v-model="activo.codigo_inventario"
            label="Código de Inventario"
            variant="outlined"
            density="comfortable"
            prepend-inner-icon="mdi-barcode"
            readonly
            bg-color="grey-lighten-4"
            class="mb-4"
          />

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
          />

          <v-row class="mb-4">
            <v-col cols="12" sm="6">
              <v-text-field
                v-model="formulario.marca"
                label="Marca *"
                variant="outlined"
                density="comfortable"
                prepend-inner-icon="mdi-tag"
                :rules="[v => !!v || 'Campo requerido']"
              />
            </v-col>

            <v-col cols="12" sm="6">
              <v-text-field
                v-model="formulario.modelo"
                label="Modelo *"
                variant="outlined"
                density="comfortable"
                prepend-inner-icon="mdi-label"
                :rules="[v => !!v || 'Campo requerido']"
              />
            </v-col>
          </v-row>

          <v-text-field
            v-model="formulario.numero_serie"
            label="Número de Serie"
            variant="outlined"
            density="comfortable"
            prepend-inner-icon="mdi-numeric"
            class="mb-4"
          />

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
          />

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
          />

          <v-textarea
            v-model="formulario.notas"
            label="Notas"
            variant="outlined"
            density="comfortable"
            rows="4"
            prepend-inner-icon="mdi-note-text"
          />
        </v-form>
      </v-card-text>

      <v-card-actions class="pa-6 pt-0">
        <v-btn variant="outlined" prepend-icon="mdi-arrow-left" @click="volver">
          Volver
        </v-btn>

        <v-spacer />

        <v-btn
          color="primary"
          prepend-icon="mdi-content-save"
          :loading="guardando"
          @click="guardar"
        >
          Guardar Cambios
        </v-btn>
      </v-card-actions>
    </v-card>

    <!-- ============================================================
         DIALOG CÁMARA
         ============================================================ -->
    <v-dialog v-model="dialogCamara" max-width="500" persistent>
      <v-card>
        <v-card-title class="d-flex align-center">
          <v-icon start>mdi-qrcode-scan</v-icon>
          Escanear Código
          <v-spacer />
          <v-btn icon="mdi-close" variant="text" @click="dialogCamara = false" />
        </v-card-title>

        <v-card-text>
          <QRScanner
            @scan-success="onScanSuccess"
            @scan-error="onScanError"
          />
        </v-card-text>
      </v-card>
    </v-dialog>

    <!-- ============================================================
         SNACKBAR
         ============================================================ -->
    <v-snackbar v-model="snackbar.show" :color="snackbar.color" timeout="3000">
      {{ snackbar.text }}
    </v-snackbar>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/services/api'
import QRScanner from '@/components/QRScanner.vue'

const router = useRouter()

const codigoBusqueda = ref('')
const loading = ref(false)
const guardando = ref(false)
const dialogCamara = ref(false)
const formRef = ref(null)

const tiposEquipo = ref([])
const estados = ref([])
const ubicaciones = ref([])

const activo = ref({})
const formulario = ref({
  tipo: null,
  marca: '',
  modelo: '',
  numero_serie: '',
  estado: null,
  ubicacion_actual: null,
  notas: ''
})

const snackbar = ref({
  show: false,
  text: '',
  color: 'success'
})

function mostrarNotificacion(text, color = 'success') {
  snackbar.value = { show: true, text, color }
}

/* =======================
   CARGAS INICIALES
   ======================= */
onMounted(async () => {
  await Promise.all([
    cargarTiposEquipo(),
    cargarEstados(),
    cargarUbicaciones()
  ])
})

async function cargarTiposEquipo() {
  const res = await apiClient.get('/api/tipos-equipo/', { params: { page_size: 1000 } })
  tiposEquipo.value = res.data.results || res.data
}

async function cargarEstados() {
  const res = await apiClient.get('/api/estados-activo/', { params: { page_size: 1000 } })
  estados.value = res.data.results || res.data
}

async function cargarUbicaciones() {
  const res = await apiClient.get('/api/ubicaciones/', { params: { page_size: 1000 } })
  ubicaciones.value = res.data.results || res.data
}

/* =======================
   CÁMARA
   ======================= */
function abrirCamara() {
  dialogCamara.value = true
}

function onScanSuccess({ decodedText }) {
  dialogCamara.value = false
  codigoBusqueda.value = decodedText.trim()
  buscarActivo()
}

function onScanError() {
  mostrarNotificacion('Error al escanear', 'error')
}

/* =======================
   BUSCAR ACTIVO
   ======================= */
async function buscarActivo() {
  if (!codigoBusqueda.value.trim()) {
    mostrarNotificacion('Ingrese un código', 'warning')
    return
  }

  loading.value = true

  try {
    const res = await apiClient.get('/api/activos/', {
      params: { codigo_inventario: codigoBusqueda.value.trim() }
    })

    const data = res.data.results || res.data

    if (!data.length) {
      mostrarNotificacion('Activo no encontrado', 'error')
      activo.value = {}
      return
    }

    activo.value = data[0]

    formulario.value = {
      tipo: activo.value.tipo?.id || null,
      marca: activo.value.marca,
      modelo: activo.value.modelo,
      numero_serie: activo.value.numero_serie || '',
      estado: activo.value.estado?.id || null,
      ubicacion_actual: activo.value.ubicacion_actual?.id || null,
      notas: activo.value.notas || ''
    }

    mostrarNotificacion('Activo cargado correctamente')

  } catch {
    mostrarNotificacion('Error al buscar activo', 'error')
  } finally {
    loading.value = false
  }
}

/* =======================
   GUARDAR
   ======================= */
async function guardar() {
  const { valid } = await formRef.value.validate()
  if (!valid) return

  guardando.value = true

  try {
    const payload = {
      tipo_id: formulario.value.tipo,
      marca: formulario.value.marca,
      modelo: formulario.value.modelo,
      numero_serie: formulario.value.numero_serie || null,
      estado_id: formulario.value.estado,
      ubicacion_actual_id: formulario.value.ubicacion_actual,
      notas: formulario.value.notas || ''
    }

    await apiClient.put(`/api/activos/${activo.value.id}/`, payload)

    mostrarNotificacion('Activo actualizado exitosamente')

  } catch {
    mostrarNotificacion('Error al guardar cambios', 'error')
  } finally {
    guardando.value = false
  }
}

function volver() {
  router.back()
}
</script>

<style scoped>
/* ============================================================
   CONTENEDOR PRINCIPAL
   ============================================================ */
.editar-activo-content {
  max-width: 880px;
  margin: 0 auto;
  padding: 2.5rem 1.25rem;
  min-height: 100vh;
  background: linear-gradient(
    180deg,
    #f6f8fb 0%,
    #eef2f7 100%
  );
}

/* ============================================================
   TÍTULOS
   ============================================================ */
.entity-title {
  font-size: 1.7rem;
  font-weight: 600;
  text-align: center;
  color: #1f2937;
  letter-spacing: -0.3px;
}

.subtitle {
  text-align: center;
  font-size: 0.95rem;
  color: #6b7280;
  margin-top: 0.25rem;
  margin-bottom: 1.5rem;
}

/* ============================================================
   CARDS
   ============================================================ */
.form-card {
  border-radius: 16px;
  background: #ffffff;
  box-shadow:
    0 4px 12px rgba(0, 0, 0, 0.06),
    0 1px 3px rgba(0, 0, 0, 0.04);
  transition: box-shadow 0.25s ease, transform 0.25s ease;
}

.form-card:hover {
  box-shadow:
    0 8px 20px rgba(0, 0, 0, 0.08),
    0 3px 6px rgba(0, 0, 0, 0.06);
}

/* ============================================================
   BUSCADOR
   ============================================================ */
.form-card h2 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 1rem;
}

/* Input de búsqueda destacado */
.v-text-field input {
  font-size: 0.95rem;
}

/* ============================================================
   HEADER ACTIVO
   ============================================================ */
.header-section {
  margin-bottom: 1.25rem;
  padding: 0.75rem 1rem;
  border-radius: 12px;
  background: linear-gradient(
    135deg,
    #2563eb,
    #1d4ed8
  );
  color: #ffffff;
  box-shadow: 0 6px 16px rgba(37, 99, 235, 0.35);
}

.header-section .entity-title {
  color: #ffffff;
  margin-bottom: 0.25rem;
}

.header-section .subtitle {
  color: #dbeafe;
  margin-bottom: 0;
}

/* ============================================================
   FORMULARIO
   ============================================================ */
.v-field {
  border-radius: 12px;
}

/* Campos readonly más suaves */
.v-field--variant-outlined.v-field--disabled,
.v-field--variant-outlined.v-field--readonly {
  background-color: #f9fafb;
}

/* Textarea */
.v-textarea textarea {
  font-size: 0.95rem;
  line-height: 1.4;
}

/* ============================================================
   ACCIONES
   ============================================================ */
.v-card-actions {
  border-top: 1px solid #e5e7eb;
}

/* Botón primario */
.v-btn--variant-elevated,
.v-btn--variant-flat,
.v-btn--variant-tonal {
  border-radius: 10px;
  text-transform: none;
  font-weight: 500;
}

/* ============================================================
   LOADING
   ============================================================ */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 1rem;
  color: #4b5563;
}

/* ============================================================
   SNACKBAR
   ============================================================ */
.v-snackbar {
  border-radius: 12px;
}

/* ============================================================
   RESPONSIVE
   ============================================================ */
@media (max-width: 600px) {
  .editar-activo-content {
    padding: 1.5rem 0.75rem;
  }

  .entity-title {
    font-size: 1.45rem;
  }

  .form-card {
    border-radius: 14px;
  }

  .v-card-actions {
    flex-direction: column-reverse;
    gap: 0.75rem;
  }

  .v-card-actions .v-btn {
    width: 100%;
  }
}

</style>

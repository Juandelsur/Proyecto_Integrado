<template>
  <div class="asset-detail-view">
    <!-- Navegación -->
    <div class="breadcrumb">
      <button @click="goBack" class="btn-back">← Volver a Lista</button>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="loading">
      <p>⏳ Cargando información del activo...</p>
    </div>

    <!-- Contenido del Activo -->
    <div v-else-if="activo" class="asset-content">
      <!-- Encabezado -->
      <div class="header">
        <div class="title-section">
          <h1>{{ activo.marca }} {{ activo.modelo }}</h1>
          <span :class="['badge', `badge-${getEstadoClass(activo.estado)}`]">
            {{ activo.estado?.nombre_estado || 'Sin estado' }}
          </span>
        </div>
        
        <!-- Botones de Acción -->
        <div class="actions">
          <button
            v-if="canEditAssets"
            @click="editAsset"
            class="btn-action btn-edit"
          >
            ✏️ Editar
          </button>
          <button
            v-if="canMoveAssets"
            @click="moveAsset"
            class="btn-action btn-move"
          >
            🚚 Movilizar
          </button>
          <button
            v-if="canDeleteAssets"
            @click="deleteAsset"
            class="btn-action btn-delete"
          >
            🗑️ Eliminar
          </button>
        </div>
      </div>

      <!-- Grid Principal -->
      <div class="main-grid">
        <!-- Columna Izquierda: Información -->
        <div class="info-section">
          <div class="info-card">
            <h2>📋 Información General</h2>
            <div class="info-grid">
              <div class="info-item">
                <span class="label">ID Activo:</span>
                <span class="value">{{ activo.id_activo }}</span>
              </div>
              <div class="info-item">
                <span class="label">Marca:</span>
                <span class="value">{{ activo.marca }}</span>
              </div>
              <div class="info-item">
                <span class="label">Modelo:</span>
                <span class="value">{{ activo.modelo }}</span>
              </div>
              <div class="info-item">
                <span class="label">Número de Serie:</span>
                <span class="value">{{ activo.numero_serie }}</span>
              </div>
              <div class="info-item">
                <span class="label">Tipo:</span>
                <span class="value">{{ activo.tipo?.nombre_tipo || 'N/A' }}</span>
              </div>
              <div class="info-item">
                <span class="label">Estado:</span>
                <span class="value">{{ activo.estado?.nombre_estado || 'N/A' }}</span>
              </div>
            </div>
          </div>

          <div class="info-card">
            <h2>📍 Ubicación Actual</h2>
            <div class="info-grid">
              <div class="info-item">
                <span class="label">Ubicación:</span>
                <span class="value">{{ activo.ubicacion_actual?.nombre_ubicacion || 'Sin ubicación' }}</span>
              </div>
              <div class="info-item">
                <span class="label">Departamento:</span>
                <span class="value">{{ activo.ubicacion_actual?.departamento?.nombre_departamento || 'N/A' }}</span>
              </div>
            </div>
          </div>

          <div v-if="activo.descripcion" class="info-card">
            <h2>📝 Descripción</h2>
            <p class="description">{{ activo.descripcion }}</p>
          </div>

          <div class="info-card">
            <h2>📅 Fechas</h2>
            <div class="info-grid">
              <div class="info-item">
                <span class="label">Fecha de Adquisición:</span>
                <span class="value">{{ formatDate(activo.fecha_adquisicion) }}</span>
              </div>
              <div class="info-item">
                <span class="label">Fecha de Registro:</span>
                <span class="value">{{ formatDate(activo.fecha_registro) }}</span>
              </div>
              <div v-if="activo.fecha_ultima_actualizacion" class="info-item">
                <span class="label">Última Actualización:</span>
                <span class="value">{{ formatDate(activo.fecha_ultima_actualizacion) }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Columna Derecha: Código QR -->
        <div class="qr-section">
          <div class="qr-card">
            <h2>🔲 Código QR</h2>
            <div class="qr-image-container">
              <img
                v-if="activo.qr_url"
                :src="activo.qr_url"
                :alt="`QR del activo ${activo.id_activo}`"
                class="qr-image"
              />
              <div v-else class="qr-placeholder">
                <p>❌ Código QR no disponible</p>
              </div>
            </div>

            <!-- Botón de Descarga/Impresión (Solo Admin y Técnico) -->
            <button
              v-if="canPrintLabels && activo.qr_url"
              @click="downloadQR"
              class="btn-download"
            >
              ⬇️ Descargar / Imprimir QR
            </button>

            <div class="qr-info">
              <p class="qr-tip">
                💡 <strong>Tip:</strong> Escanea este código QR con tu dispositivo móvil
                para acceder rápidamente a la información del activo.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Error -->
    <div v-else class="error">
      <p>❌ No se pudo cargar la información del activo.</p>
      <button @click="goBack" class="btn-back">← Volver</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import activosService from '@/services/activosService'

// ============================================================================
// COMPOSABLES
// ============================================================================

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

// ============================================================================
// STATE
// ============================================================================

const activo = ref(null)
const loading = ref(false)

// ============================================================================
// COMPUTED (Permisos)
// ============================================================================

const canPrintLabels = computed(() => authStore.canPrintLabels)
const canEditAssets = computed(() => authStore.canEditAssets)
const canDeleteAssets = computed(() => authStore.canDeleteAssets)
const canMoveAssets = computed(() => authStore.canMoveAssets)

// ============================================================================
// METHODS
// ============================================================================

/**
 * Carga la información del activo
 */
async function loadActivo() {
  loading.value = true
  try {
    const id = route.params.id
    const response = await activosService.getById(id)
    activo.value = response
  } catch (error) {
    console.error('Error al cargar activo:', error)
    alert('Error al cargar la información del activo.')
  } finally {
    loading.value = false
  }
}

/**
 * Vuelve a la lista de activos
 */
function goBack() {
  router.push({ name: 'asset-list' })
}

/**
 * Navega a la edición del activo
 */
function editAsset() {
  router.push({ name: 'asset-edit', params: { id: activo.value.id_activo } })
}

/**
 * Navega a la movilización del activo
 */
function moveAsset() {
  router.push({ name: 'asset-move', params: { id: activo.value.id_activo } })
}

/**
 * Elimina el activo (con confirmación)
 */
async function deleteAsset() {
  const confirmed = confirm(
    `¿Estás seguro de que deseas eliminar el activo "${activo.value.marca} ${activo.value.modelo}"?\n\n` +
    'Esta acción no se puede deshacer.'
  )

  if (!confirmed) return

  try {
    await activosService.delete(activo.value.id_activo)
    alert('✅ Activo eliminado exitosamente.')
    goBack()
  } catch (error) {
    console.error('Error al eliminar activo:', error)
    alert('❌ Error al eliminar el activo. Por favor, intenta de nuevo.')
  }
}

/**
 * Descarga la imagen del QR
 */
function downloadQR() {
  if (!activo.value.qr_url) return

  // Crear un enlace temporal para descargar
  const link = document.createElement('a')
  link.href = activo.value.qr_url
  link.download = `QR_Activo_${activo.value.id_activo}.png`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

/**
 * Formatea una fecha en formato legible
 */
function formatDate(dateString) {
  if (!dateString) return 'N/A'

  const date = new Date(dateString)
  return date.toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

/**
 * Obtiene la clase CSS según el estado
 */
function getEstadoClass(estado) {
  const estadoNombre = estado?.nombre_estado?.toLowerCase() || ''
  if (estadoNombre.includes('operativo')) return 'success'
  if (estadoNombre.includes('mantenimiento')) return 'warning'
  if (estadoNombre.includes('fuera')) return 'danger'
  return 'default'
}

// ============================================================================
// LIFECYCLE
// ============================================================================

onMounted(() => {
  loadActivo()
})
</script>

<style scoped>
.asset-detail-view {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

.breadcrumb {
  margin-bottom: 2rem;
}

.btn-back {
  padding: 0.75rem 1.5rem;
  background: #95a5a6;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-back:hover {
  background: #7f8c8d;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.title-section {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.title-section h1 {
  font-size: 2rem;
  color: #2c3e50;
  margin: 0;
}

.badge {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
}

.badge-success {
  background: #d4edda;
  color: #155724;
}

.badge-warning {
  background: #fff3cd;
  color: #856404;
}

.badge-danger {
  background: #f8d7da;
  color: #721c24;
}

.badge-default {
  background: #e9ecef;
  color: #495057;
}

.actions {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.btn-action {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn-action:hover {
  transform: translateY(-2px);
}

.btn-edit {
  background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
  color: white;
}

.btn-edit:hover {
  box-shadow: 0 4px 12px rgba(243, 156, 18, 0.4);
}

.btn-move {
  background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
  color: white;
}

.btn-move:hover {
  box-shadow: 0 4px 12px rgba(52, 152, 219, 0.4);
}

.btn-delete {
  background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
  color: white;
}

.btn-delete:hover {
  box-shadow: 0 4px 12px rgba(231, 76, 60, 0.4);
}

.main-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
}

.info-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.info-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.info-card h2 {
  font-size: 1.3rem;
  color: #2c3e50;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #e0e0e0;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.label {
  font-size: 0.85rem;
  color: #7f8c8d;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.value {
  font-size: 1rem;
  color: #2c3e50;
  font-weight: 500;
}

.description {
  color: #2c3e50;
  line-height: 1.6;
  margin: 0;
}

.qr-section {
  position: sticky;
  top: 2rem;
  height: fit-content;
}

.qr-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.qr-card h2 {
  font-size: 1.3rem;
  color: #2c3e50;
  margin-bottom: 1rem;
}

.qr-image-container {
  width: 100%;
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8f9fa;
  border-radius: 12px;
  margin-bottom: 1.5rem;
  padding: 1rem;
}

.qr-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.qr-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #95a5a6;
  font-size: 1.1rem;
}

.btn-download {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  margin-bottom: 1rem;
}

.btn-download:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.qr-info {
  background: #e8f4f8;
  border-left: 4px solid #3498db;
  padding: 1rem;
  border-radius: 8px;
  text-align: left;
}

.qr-tip {
  margin: 0;
  color: #2c3e50;
  font-size: 0.9rem;
  line-height: 1.5;
}

.loading,
.error {
  padding: 3rem;
  text-align: center;
  color: #7f8c8d;
  font-size: 1.1rem;
}

.error {
  color: #e74c3c;
}

@media (max-width: 1024px) {
  .main-grid {
    grid-template-columns: 1fr;
  }

  .qr-section {
    position: static;
  }
}

@media (max-width: 768px) {
  .header {
    flex-direction: column;
    align-items: flex-start;
  }

  .actions {
    width: 100%;
  }

  .btn-action {
    flex: 1;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }
}
</style>



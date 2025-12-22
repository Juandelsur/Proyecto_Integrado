<template>
  <div class="asset-detail-view">
    <!-- Header -->
    <header class="detail-header">
      <button @click="goBack" class="btn-back">
        <i class="bi bi-arrow-left"></i>
        <span>Volver</span>
      </button>
      <h1 class="header-title">Detalle del Activo</h1>
    </header>

    <!-- Loading State -->
    <div v-if="isLoading" class="loading-container">
      <div class="spinner"></div>
      <p class="loading-text">Cargando activo...</p>
    </div>

    <!-- Contenido Principal -->
    <div v-else-if="activo" class="detail-content">
      <!-- Grid de 2 Columnas -->
      <div class="detail-grid">
        <!-- Columna Izquierda: Información -->
        <div class="info-section">
          <!-- Título y Estado -->
          <div class="asset-header">
            <h2 class="asset-title">{{ activo.marca }} {{ activo.modelo }}</h2>
            <span class="badge" :class="getEstadoClass(activo.estado?.nombre_estado)">
              {{ activo.estado?.nombre_estado || 'N/A' }}
            </span>
          </div>

          <!-- Información General -->
          <div class="info-card">
            <h3 class="card-title">
              <i class="bi bi-info-circle"></i>
              <span>Información General</span>
            </h3>
            <div class="info-list">
              <div class="info-item">
                <span class="info-label">Código de Inventario:</span>
                <span class="info-value">{{ activo.codigo_inventario }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Número de Serie:</span>
                <span class="info-value">{{ activo.numero_serie }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Tipo de Equipo:</span>
                <span class="info-value">{{ activo.tipo?.nombre_tipo || 'N/A' }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Marca:</span>
                <span class="info-value">{{ activo.marca }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Modelo:</span>
                <span class="info-value">{{ activo.modelo }}</span>
              </div>
            </div>
          </div>

          <!-- Ubicación -->
          <div class="info-card">
            <h3 class="card-title">
              <i class="bi bi-geo-alt"></i>
              <span>Ubicación Actual</span>
            </h3>
            <div class="info-list">
              <div class="info-item">
                <span class="info-label">Ubicación:</span>
                <span class="info-value">{{ activo.ubicacion_actual?.nombre_ubicacion || 'N/A' }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Departamento:</span>
                <span class="info-value">
                  {{ activo.ubicacion_actual?.departamento?.nombre_departamento || 'N/A' }}
                </span>
              </div>
            </div>
          </div>

          <!-- Notas -->
          <div v-if="activo.notas" class="info-card">
            <h3 class="card-title">
              <i class="bi bi-sticky"></i>
              <span>Notas</span>
            </h3>
            <p class="notes-text">{{ activo.notas }}</p>
          </div>
        </div>

        <!-- Columna Derecha: Código QR -->
        <div class="qr-section">
          <div class="qr-card">
            <h3 class="card-title">
              <i class="bi bi-qr-code"></i>
              <span>Código QR</span>
            </h3>

            <!-- Imagen QR -->
            <div class="qr-image-container">
              <canvas ref="qrCanvas" class="qr-canvas"></canvas>
            </div>

            <!-- Código de Texto -->
            <p class="qr-code-text">{{ activo.codigo_inventario }}</p>

            <!-- Botón de Descarga (Solo Admin/Técnico) -->
            <button
              v-if="authStore.canPrintLabels"
              @click="downloadQR"
              class="btn-download"
            >
              <i class="bi bi-download"></i>
              <span>Descargar PNG</span>
            </button>

            <p class="qr-tip">
              <i class="bi bi-lightbulb"></i>
              <span>Escanea este código QR para registrar movimientos del equipo</span>
            </p>
          </div>
        </div>
      </div>

      <!-- Botones de Acción -->
      <div class="action-buttons">
        <button
          v-if="authStore.canManageAssets"
          @click="editAsset"
          class="btn-action btn-edit"
        >
          <i class="bi bi-pencil"></i>
          <span>Editar Activo</span>
        </button>
        <button
          v-if="authStore.canMoveAssets"
          @click="moveAsset"
          class="btn-action btn-move"
        >
          <i class="bi bi-truck"></i>
          <span>Movilizar</span>
        </button>
      </div>
    </div>

    <!-- Error State -->
    <div v-else class="error-state">
      <i class="bi bi-exclamation-triangle error-icon"></i>
      <p class="error-text">No se pudo cargar el activo</p>
      <button @click="goBack" class="btn-back-error">Volver al Inventario</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import apiClient from '@/services/api'
import QRCode from 'qrcode'




const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

// Estado
const activo = ref(null)
const isLoading = ref(true)
const qrCanvas = ref(null)

/**
 * Carga el activo desde la API
 */
async function loadActivo() {
  try {
    isLoading.value = true
    const id = route.params.id
    const response = await apiClient.get(`/api/activos/${id}/`)
    activo.value = response.data

    // Generar QR code después de cargar el activo
    await generateQRCode()
  } catch (error) {
    console.error('Error al cargar activo:', error)
    alert('Error al cargar el activo')
  } finally {
    isLoading.value = false
  }
}

/**
 * Genera el código QR en el canvas
 */
async function generateQRCode() {
  if (!activo.value || !qrCanvas.value) return

  try {
    await QRCode.toCanvas(qrCanvas.value, activo.value.codigo_inventario, {
      width: 300,
      margin: 2,
      color: {
        dark: '#000000',
        light: '#FFFFFF'
      }
    })
  } catch (error) {
    console.error('Error al generar QR code:', error)
  }
}

/**
 * Descarga el QR code como imagen PNG
 */
function downloadQR() {
  if (!qrCanvas.value) return

  try {
    // Convertir canvas a blob y descargar
    qrCanvas.value.toBlob((blob) => {
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `QR_${activo.value.codigo_inventario}.png`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      URL.revokeObjectURL(url)
    })
  } catch (error) {
    console.error('Error al descargar QR:', error)
    alert('Error al descargar el código QR')
  }
}

/**
 * Retorna la clase CSS según el estado del activo
 */
function getEstadoClass(estado) {
  if (!estado) return 'badge-default'

  const estadoLower = estado.toLowerCase()

  if (estadoLower.includes('activo') || estadoLower.includes('operativo')) {
    return 'badge-success'
  } else if (estadoLower.includes('mantenimiento') || estadoLower.includes('mantención')) {
    return 'badge-warning'
  } else if (estadoLower.includes('baja') || estadoLower.includes('inactivo')) {
    return 'badge-danger'
  }

  return 'badge-default'
}

/**
 * Navega a la vista de edición
 */
function editAsset() {
  // TODO: Implementar vista de edición
  alert('Funcionalidad de edición en desarrollo')
}

/**
 * Navega a la vista de movilización
 */
function moveAsset() {
  // TODO: Implementar vista de movilización
  alert('Funcionalidad de movilización en desarrollo')
}

/**
 * Vuelve a la vista anterior
 */
function goBack() {
  router.back()
}

/**
 * Inicialización
 */
onMounted(() => {
  loadActivo()
})
</script>


<style scoped>
/* ============================================================================
   LAYOUT PRINCIPAL
   ============================================================================ */

.asset-detail-view {
  min-height: 100vh;
  background: #f5f7fa;
  padding-bottom: 2rem;
}

/* ============================================================================
   HEADER
   ============================================================================ */

.detail-header {
  background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%);
  color: white;
  padding: 1.5rem 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.btn-back {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
  transition: all 0.3s ease;
}

.btn-back:hover {
  background: rgba(255, 255, 255, 0.3);
}

.header-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
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
  gap: 1rem;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #e0e0e0;
  border-top-color: #1565c0;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loading-text {
  color: #666;
  font-size: 1rem;
}

/* ============================================================================
   CONTENIDO PRINCIPAL
   ============================================================================ */

.detail-content {
  padding: 1rem;
}

.detail-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

/* ============================================================================
   SECCIÓN DE INFORMACIÓN
   ============================================================================ */

.info-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.asset-header {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.asset-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #333;
  margin: 0;
}

.info-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.card-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #333;
  margin: 0 0 1rem 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.card-title i {
  color: #1565c0;
  font-size: 1.25rem;
}

.info-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #e0e0e0;
}

.info-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.info-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-value {
  font-size: 1rem;
  color: #333;
  font-weight: 500;
}


.notes-text {
  color: #666;
  font-size: 0.95rem;
  line-height: 1.6;
  margin: 0;
}

/* ============================================================================
   SECCIÓN DE QR
   ============================================================================ */

.qr-section {
  display: flex;
  flex-direction: column;
}

.qr-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.qr-image-container {
  margin: 1.5rem 0;
  padding: 1rem;
  background: #f5f7fa;
  border-radius: 12px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.qr-canvas {
  display: block;
  max-width: 100%;
  height: auto;
  border-radius: 8px;
}

.qr-code-text {
  font-size: 1.1rem;
  font-weight: 700;
  color: #1565c0;
  margin: 0 0 1.5rem 0;
  font-family: 'Courier New', monospace;
  letter-spacing: 1px;
}

.btn-download {
  background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%);
  border: none;
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(13, 71, 161, 0.3);
  width: 100%;
}

.btn-download:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(13, 71, 161, 0.4);
}

.btn-download i {
  font-size: 1.25rem;
}

.qr-tip {
  margin-top: 1.5rem;
  padding: 1rem;
  background: #e3f2fd;
  border-radius: 8px;
  color: #1565c0;
  font-size: 0.9rem;
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  text-align: left;
}

.qr-tip i {
  font-size: 1.1rem;
  flex-shrink: 0;
  margin-top: 0.1rem;
}

/* ============================================================================
   BOTONES DE ACCIÓN
   ============================================================================ */

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 0 1rem;
}

.btn-action {
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  transition: all 0.3s ease;
  border: none;
}

.btn-edit {
  background: #1565c0;
  color: white;
  box-shadow: 0 4px 12px rgba(21, 101, 192, 0.3);
}

.btn-edit:hover {
  background: #0d47a1;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(21, 101, 192, 0.4);
}

.btn-move {
  background: white;
  color: #1565c0;
  border: 2px solid #1565c0;
}

.btn-move:hover {
  background: #e3f2fd;
}

.btn-action i {
  font-size: 1.25rem;
}

/* ============================================================================
   BADGES DE ESTADO
   ============================================================================ */

.badge {
  display: inline-block;
  padding: 0.35rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
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
  background: #e0e0e0;
  color: #666;
}


/* ============================================================================
   ERROR STATE
   ============================================================================ */

.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 1rem;
  gap: 1rem;
}

.error-icon {
  font-size: 4rem;
  color: #dc3545;
}

.error-text {
  color: #666;
  font-size: 1.1rem;
  font-weight: 600;
}

.btn-back-error {
  background: #1565c0;
  border: none;
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-back-error:hover {
  background: #0d47a1;
}

/* ============================================================================
   RESPONSIVE
   ============================================================================ */

@media (min-width: 768px) {
  .detail-header {
    padding: 2rem;
  }

  .header-title {
    font-size: 2rem;
  }

  .detail-content {
    padding: 2rem;
  }

  .detail-grid {
    grid-template-columns: 1fr 1fr;
  }

  .asset-header {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }

  .info-item {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }

  .info-label {
    flex: 0 0 40%;
  }

  .info-value {
    flex: 1;
    text-align: right;
  }

  .action-buttons {
    flex-direction: row;
    padding: 0 2rem;
  }

  .btn-action {
    flex: 1;
  }

  .qr-section {
    position: sticky;
    top: 2rem;
    align-self: flex-start;
  }
}

@media (min-width: 1024px) {
  .detail-content {
    max-width: 1200px;
    margin: 0 auto;
  }
}
</style>
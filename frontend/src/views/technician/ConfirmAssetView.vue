<template>
  <div class="confirm-asset-view">
    <!-- Header -->
    <header class="confirm-header">
      <button @click="goBack" class="btn-back">
        <i class="bi bi-arrow-left"></i>
      </button>
      <h1 class="header-title">Confirmar Equipo</h1>
    </header>

    <!-- Contenido Principal -->
    <main class="confirm-content">
      <!-- Loading State -->
      <div v-if="isLoadingAsset" class="loading-container">
        <div class="spinner"></div>
        <p class="loading-text">Cargando información del equipo...</p>
      </div>

      <!-- Asset Information -->
      <div v-else-if="asset" class="asset-card">
        <h2 class="card-title">Confirmar Equipo</h2>

        <!-- Datos del Activo -->
        <div class="asset-info">
          <div class="info-row">
            <span class="info-label">Código:</span>
            <span class="info-value">{{ asset.codigo_inventario }}</span>
          </div>

          <div class="info-row">
            <span class="info-label">Tipo:</span>
            <span class="info-value">{{ asset.tipo?.nombre_tipo || 'N/A' }}</span>
          </div>

          <div class="info-row">
            <span class="info-label">Marca/Modelo:</span>
            <span class="info-value">{{ asset.marca }} {{ asset.modelo }}</span>
          </div>

          <div class="info-row">
            <span class="info-label">Serie:</span>
            <span class="info-value">{{ asset.numero_serie || 'N/A' }}</span>
          </div>

          <div class="info-row">
            <span class="info-label">Ubicación:</span>
            <span class="info-value">
              {{ asset.ubicacion_actual?.nombre_ubicacion || 'N/A' }}
              <span v-if="asset.ubicacion_actual?.departamento" class="departamento">
                - {{ asset.ubicacion_actual.departamento.nombre_departamento }}
              </span>
            </span>
          </div>

          <div class="info-row">
            <span class="info-label">Estado:</span>
            <span class="info-value">
              <span class="badge" :class="getEstadoClass(asset.estado?.nombre_estado)">
                {{ asset.estado?.nombre_estado || 'N/A' }}
              </span>
            </span>
          </div>
        </div>

        <!-- Campo de Observaciones -->
        <div class="observations-section">
          <label for="observaciones" class="observations-label">Observaciones (opcional)</label>
          <textarea
            id="observaciones"
            v-model="observaciones"
            placeholder="Estado físico, movimiento registrado, etc."
            class="observations-textarea"
            rows="4"
          ></textarea>
        </div>

        <!-- Botones de Acción -->
        <div class="action-buttons">
          <button
            @click="handleConfirm"
            class="btn-confirm"
            :disabled="isConfirming"
          >
            <span v-if="!isConfirming" class="btn-content">
              <i class="bi bi-check-circle"></i>
              <span>Confirmar Registro</span>
            </span>
            <span v-else class="btn-content">
              <div class="btn-spinner"></div>
              <span>Confirmando...</span>
            </span>
          </button>

          <button @click="scanAnother" class="btn-secondary" :disabled="isConfirming">
            <i class="bi bi-qr-code-scan"></i>
            <span>Escanear Otro</span>
          </button>
        </div>
      </div>

      <!-- Error State -->
      <div v-else class="error-container">
        <i class="bi bi-exclamation-triangle error-icon"></i>
        <p class="error-text">No se pudo cargar la información del equipo</p>
        <button @click="goBack" class="btn-retry">Volver</button>
      </div>

      <!-- Error Message Toast -->
      <div v-if="errorMessage" class="error-toast">
        <i class="bi bi-exclamation-triangle"></i>
        <p>{{ errorMessage }}</p>
        <button @click="clearError" class="btn-close-toast">×</button>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import apiClient from '@/services/api'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

// Estado
const asset = ref(null)
const observaciones = ref('')
const isLoadingAsset = ref(true)
const isConfirming = ref(false)
const errorMessage = ref('')

/**
 * Carga la información del activo
 */
onMounted(async () => {
  // Intentar obtener el activo desde el state de la navegación
  if (history.state && history.state.activo) {
    asset.value = history.state.activo
    isLoadingAsset.value = false
  } else {
    // Si no está en el state, cargar desde la API
    await loadAsset()
  }
})

/**
 * Carga el activo desde la API
 */
async function loadAsset() {
  try {
    const assetId = route.params.id
    const response = await apiClient.get(`/api/activos/${assetId}/`)
    asset.value = response.data
  } catch (error) {
    console.error('Error al cargar activo:', error)
    errorMessage.value = 'Error al cargar la información del equipo'
  } finally {
    isLoadingAsset.value = false
  }
}

/**
 * Maneja la confirmación del registro
 *
 * NOTA: Esta función registra el movimiento del activo.
 * Necesitarás ajustar la lógica según tu backend.
 * Por ahora, asumimos que se registra un movimiento a la misma ubicación
 * como una forma de "check-in" o verificación.
 */
async function handleConfirm() {
  if (isConfirming.value) return

  isConfirming.value = true
  errorMessage.value = ''

  try {
    // Opción 1: Si tienes un endpoint específico para registrar movimientos
    // await apiClient.post('/api/historial-movimientos/', {
    //   activo: asset.value.id,
    //   usuario_registra: authStore.user.id,
    //   ubicacion_origen: asset.value.ubicacion_actual.id,
    //   ubicacion_destino: asset.value.ubicacion_actual.id,
    //   tipo_movimiento: 'VERIFICACION',
    //   comentarios: observaciones.value
    // })

    // Opción 2: Usar el endpoint de movilizar (si aplica)
    // Por ahora, simulamos un registro exitoso

    // Simular delay de red
    await new Promise(resolve => setTimeout(resolve, 1500))

    // Redirigir a vista de éxito
    router.push({
      name: 'movement-success',
      state: {
        asset: asset.value,
        observaciones: observaciones.value
      }
    })
  } catch (error) {
    console.error('Error al confirmar registro:', error)
    errorMessage.value = error.response?.data?.detail || 'Error al confirmar el registro. Intenta nuevamente.'
    isConfirming.value = false
  }
}

/**
 * Vuelve al escáner para escanear otro equipo
 */
function scanAnother() {
  router.push({ name: 'scan-qr' })
}

/**
 * Vuelve a la vista anterior
 */
function goBack() {
  router.back()
}

/**
 * Limpia el mensaje de error
 */
function clearError() {
  errorMessage.value = ''
}

/**
 * Retorna la clase CSS según el estado del activo
 */
function getEstadoClass(estado) {
  if (!estado) return 'badge-default'

  const estadoLower = estado.toLowerCase()

  if (estadoLower.includes('activo') || estadoLower.includes('operativo')) {
    return 'badge-success'
  } else if (estadoLower.includes('mantenimiento')) {
    return 'badge-warning'
  } else if (estadoLower.includes('baja') || estadoLower.includes('inactivo')) {
    return 'badge-danger'
  }

  return 'badge-default'
}
</script>

<style scoped>
/* ============================================================================
   CONTENEDOR PRINCIPAL
   ============================================================================ */

.confirm-asset-view {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f7fa;
}

/* ============================================================================
   HEADER
   ============================================================================ */

.confirm-header {
  background: linear-gradient(135deg, #0d47a1 0%, #1565c0 50%, #1976d2 100%);
  color: white;
  padding: 1rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.btn-back {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-back:hover {
  background: rgba(255, 255, 255, 0.3);
}

.btn-back i {
  font-size: 1.25rem;
}

.header-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
}

/* ============================================================================
   CONTENIDO PRINCIPAL
   ============================================================================ */

.confirm-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem 1.5rem;
  position: relative;
}

/* ============================================================================
   LOADING STATE
   ============================================================================ */

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 3rem;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #e0e0e0;
  border-top-color: #0d47a1;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loading-text {
  font-size: 1rem;
  color: #666;
  font-weight: 500;
}

/* ============================================================================
   ASSET CARD
   ============================================================================ */

.asset-card {
  width: 100%;
  max-width: 600px;
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.card-title {
  font-size: 1.75rem;
  font-weight: 700;
  margin: 0 0 1.5rem 0;
  color: #0d47a1;
}

/* ============================================================================
   ASSET INFO
   ============================================================================ */

.asset-info {
  background: #f5f7fa;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 0.75rem 0;
  border-bottom: 1px solid #e0e0e0;
}

.info-row:last-child {
  border-bottom: none;
}

.info-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #666;
  flex-shrink: 0;
  margin-right: 1rem;
}

.info-value {
  font-size: 0.95rem;
  font-weight: 600;
  color: #333;
  text-align: right;
  word-break: break-word;
}

.departamento {
  font-size: 0.85rem;
  color: #666;
  font-weight: 400;
}

/* ============================================================================
   BADGES
   ============================================================================ */

.badge {
  display: inline-block;
  padding: 0.375rem 0.75rem;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: uppercase;
}

.badge-success {
  background: #e8f5e9;
  color: #2e7d32;
}

.badge-warning {
  background: #fff3e0;
  color: #f57c00;
}

.badge-danger {
  background: #ffebee;
  color: #c62828;
}

.badge-default {
  background: #e0e0e0;
  color: #666;
}

/* ============================================================================
   OBSERVATIONS SECTION
   ============================================================================ */

.observations-section {
  margin-bottom: 2rem;
}

.observations-label {
  display: block;
  font-size: 0.95rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 0.75rem;
}

.observations-textarea {
  width: 100%;
  padding: 0.875rem 1rem;
  font-size: 0.95rem;
  font-family: inherit;
  border: 2px solid #ddd;
  border-radius: 8px;
  resize: vertical;
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.observations-textarea:focus {
  outline: none;
  border-color: #0d47a1;
  box-shadow: 0 0 0 3px rgba(13, 71, 161, 0.1);
}

.observations-textarea::placeholder {
  color: #999;
}

/* ============================================================================
   ACTION BUTTONS
   ============================================================================ */

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.btn-confirm {
  background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%);
  border: none;
  color: white;
  padding: 1rem 1.5rem;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(13, 71, 161, 0.3);
}

.btn-confirm:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(13, 71, 161, 0.4);
}

.btn-confirm:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.btn-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
}

.btn-content i {
  font-size: 1.25rem;
}

.btn-spinner {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.btn-secondary {
  background: white;
  border: 2px solid #0d47a1;
  color: #0d47a1;
  padding: 1rem 1.5rem;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
}

.btn-secondary:hover:not(:disabled) {
  background: #f5f7fa;
}

.btn-secondary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary i {
  font-size: 1.25rem;
}

/* ============================================================================
   ERROR STATE
   ============================================================================ */

.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
  padding: 3rem;
  text-align: center;
}

.error-icon {
  font-size: 4rem;
  color: #f44336;
}

.error-text {
  font-size: 1.1rem;
  color: #666;
  margin: 0;
}

.btn-retry {
  background: #0d47a1;
  border: none;
  color: white;
  padding: 0.875rem 2rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-retry:hover {
  background: #1565c0;
  transform: translateY(-2px);
}

/* ============================================================================
   ERROR TOAST
   ============================================================================ */

.error-toast {
  position: fixed;
  bottom: 2rem;
  left: 1.5rem;
  right: 1.5rem;
  background: #f44336;
  color: white;
  padding: 1.25rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(244, 67, 54, 0.4);
  display: flex;
  align-items: center;
  gap: 1rem;
  z-index: 999;
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    transform: translateY(100%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.error-toast i {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.error-toast p {
  margin: 0;
  font-size: 0.95rem;
  flex: 1;
}

.btn-close-toast {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  font-size: 1.5rem;
  line-height: 1;
  cursor: pointer;
  transition: all 0.3s ease;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-close-toast:hover {
  background: rgba(255, 255, 255, 0.3);
}

/* ============================================================================
   RESPONSIVE
   ============================================================================ */

@media (min-width: 768px) {
  .confirm-content {
    padding: 3rem 2rem;
  }

  .header-title {
    font-size: 1.5rem;
  }

  .card-title {
    font-size: 2rem;
  }

  .action-buttons {
    flex-direction: row;
  }

  .btn-confirm,
  .btn-secondary {
    flex: 1;
  }

  .info-row {
    flex-direction: row;
  }

  .info-label {
    width: 140px;
  }

  .info-value {
    flex: 1;
  }
}

@media (min-width: 1024px) {
  .asset-card {
    max-width: 700px;
  }
}
</style>


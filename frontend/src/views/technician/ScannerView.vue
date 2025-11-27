<template>
  <div class="scanner-view">
    <!-- Header -->
    <header class="scanner-header">
      <button @click="goBack" class="btn-back">
        <i class="bi bi-arrow-left"></i>
      </button>
      <h1 class="header-title">Escanear Código QR</h1>
    </header>

    <!-- Contenido Principal -->
    <main class="scanner-content">
      <!-- Modo Escáner -->
      <div v-if="!showManualInput" class="scanner-container">
        <!-- Área de Cámara -->
        <div class="camera-area">
          <div id="qr-reader" class="qr-reader"></div>
          <p class="help-text">Apunta la cámara al código QR del equipo</p>
        </div>

        <!-- Botón para Ingreso Manual -->
        <button @click="toggleManualInput" class="btn-manual">
          <i class="bi bi-keyboard"></i>
          <span>¿Problemas con la cámara? Ingresar Manualmente</span>
        </button>
      </div>

      <!-- Modo Ingreso Manual -->
      <div v-else class="manual-input-container">
        <div class="manual-card">
          <h2 class="manual-title">Ingreso Manual</h2>
          <p class="manual-subtitle">Escribe el código del equipo</p>

          <div class="input-group">
            <label for="codigo-input" class="input-label">Código de Inventario</label>
            <input
              id="codigo-input"
              v-model="manualCode"
              type="text"
              placeholder="Ej: INV-001"
              class="input-field"
              @keyup.enter="handleManualSubmit"
              autofocus
            />
          </div>

          <div class="manual-actions">
            <button @click="handleManualSubmit" class="btn-submit" :disabled="!manualCode.trim()">
              <i class="bi bi-check-circle"></i>
              <span>Buscar Equipo</span>
            </button>

            <button @click="toggleManualInput" class="btn-cancel">
              <i class="bi bi-camera"></i>
              <span>Volver al Escáner</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="loading-overlay">
        <div class="spinner"></div>
        <p class="loading-text">Buscando equipo...</p>
      </div>

      <!-- Error Message -->
      <div v-if="errorMessage" class="error-message">
        <i class="bi bi-exclamation-triangle"></i>
        <p>{{ errorMessage }}</p>
        <button @click="clearError" class="btn-close-error">Cerrar</button>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { Html5Qrcode } from 'html5-qrcode'
import apiClient from '@/services/api'

const router = useRouter()

// Estado
const showManualInput = ref(false)
const manualCode = ref('')
const isLoading = ref(false)
const errorMessage = ref('')
let html5QrCode = null

/**
 * Inicializa el escáner QR
 */
onMounted(() => {
  if (!showManualInput.value) {
    initScanner()
  }
})

/**
 * Limpia el escáner al desmontar el componente
 */
onUnmounted(() => {
  stopScanner()
})

/**
 * Inicializa el escáner de QR
 */
async function initScanner() {
  try {
    html5QrCode = new Html5Qrcode('qr-reader')
    
    await html5QrCode.start(
      { facingMode: 'environment' }, // Cámara trasera
      {
        fps: 10,
        qrbox: { width: 250, height: 250 }
      },
      onScanSuccess,
      onScanError
    )
  } catch (err) {
    console.error('Error al iniciar escáner:', err)
    errorMessage.value = 'No se pudo acceder a la cámara. Intenta con ingreso manual.'
  }
}

/**
 * Detiene el escáner
 */
async function stopScanner() {
  if (html5QrCode && html5QrCode.isScanning) {
    try {
      await html5QrCode.stop()
      html5QrCode.clear()
    } catch (err) {
      console.error('Error al detener escáner:', err)
    }
  }
}

/**
 * Callback cuando se escanea un código exitosamente
 */
function onScanSuccess(decodedText) {
  console.log('Código escaneado:', decodedText)
  handleCodeDetected(decodedText)
}

/**
 * Callback cuando hay un error al escanear
 */
function onScanError(error) {
  // Ignorar errores de escaneo (son muy frecuentes)
  // console.warn('Error de escaneo:', error)
}

/**
 * Maneja el código detectado (escaneado o manual)
 */
async function handleCodeDetected(code) {
  if (isLoading.value) return // Evitar múltiples llamadas

  isLoading.value = true
  errorMessage.value = ''

  try {
    // Detener el escáner mientras se busca el activo
    await stopScanner()

    // Buscar el activo por código de inventario
    // Opción 1: Buscar en la lista completa (puede ser lento con muchos activos)
    const response = await apiClient.get(`/api/activos/`)

    // Filtrar por código de inventario en el frontend
    const activos = Array.isArray(response.data) ? response.data : response.data.results || []
    const activo = activos.find(a => a.codigo_inventario === code)

    // Verificar si se encontró el activo
    if (activo) {
      // Redirigir a la vista de confirmación con los datos del activo
      router.push({
        name: 'confirm-asset',
        params: { id: activo.id },
        state: { activo }
      })
    } else {
      errorMessage.value = `No se encontró ningún equipo con el código: ${code}`
      isLoading.value = false

      // Reiniciar el escáner si estaba activo
      if (!showManualInput.value) {
        setTimeout(() => initScanner(), 2000)
      }
    }
  } catch (error) {
    console.error('Error al buscar activo:', error)
    errorMessage.value = error.response?.data?.detail || 'Error al buscar el equipo. Intenta nuevamente.'
    isLoading.value = false

    // Reiniciar el escáner si estaba activo
    if (!showManualInput.value) {
      setTimeout(() => initScanner(), 2000)
    }
  }
}

/**
 * Alterna entre modo escáner y modo manual
 */
async function toggleManualInput() {
  showManualInput.value = !showManualInput.value

  if (showManualInput.value) {
    // Cambiar a modo manual: detener escáner
    await stopScanner()
    manualCode.value = ''
  } else {
    // Cambiar a modo escáner: iniciar escáner
    await initScanner()
  }
}

/**
 * Maneja el envío del código manual
 */
function handleManualSubmit() {
  const code = manualCode.value.trim()
  if (code) {
    handleCodeDetected(code)
  }
}

/**
 * Limpia el mensaje de error
 */
function clearError() {
  errorMessage.value = ''
}

/**
 * Vuelve a la vista anterior
 */
function goBack() {
  router.back()
}
</script>

<style scoped>
/* ============================================================================
   CONTENEDOR PRINCIPAL
   ============================================================================ */

.scanner-view {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f7fa;
}

/* ============================================================================
   HEADER
   ============================================================================ */

.scanner-header {
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

.scanner-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem 1.5rem;
  position: relative;
}

/* ============================================================================
   MODO ESCÁNER
   ============================================================================ */

.scanner-container {
  width: 100%;
  max-width: 500px;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.camera-area {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.qr-reader {
  width: 100%;
  max-width: 400px;
  margin: 0 auto;
  border-radius: 12px;
  overflow: hidden;
}

.help-text {
  margin-top: 1.5rem;
  font-size: 0.95rem;
  color: #666;
}

.btn-manual {
  background: white;
  border: 2px solid #0d47a1;
  color: #0d47a1;
  padding: 1rem 1.5rem;
  border-radius: 12px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.btn-manual:hover {
  background: #0d47a1;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(13, 71, 161, 0.2);
}

.btn-manual i {
  font-size: 1.25rem;
}

/* ============================================================================
   MODO INGRESO MANUAL
   ============================================================================ */

.manual-input-container {
  width: 100%;
  max-width: 500px;
}

.manual-card {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.manual-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0 0 0.5rem 0;
  color: #0d47a1;
}

.manual-subtitle {
  font-size: 0.95rem;
  color: #666;
  margin: 0 0 2rem 0;
}

.input-group {
  margin-bottom: 2rem;
}

.input-label {
  display: block;
  font-size: 0.9rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 0.5rem;
}

.input-field {
  width: 100%;
  padding: 0.875rem 1rem;
  font-size: 1rem;
  border: 2px solid #ddd;
  border-radius: 8px;
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.input-field:focus {
  outline: none;
  border-color: #0d47a1;
  box-shadow: 0 0 0 3px rgba(13, 71, 161, 0.1);
}

.manual-actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.btn-submit {
  background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%);
  border: none;
  color: white;
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
  box-shadow: 0 4px 12px rgba(13, 71, 161, 0.3);
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(13, 71, 161, 0.4);
}

.btn-submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-submit i {
  font-size: 1.25rem;
}

.btn-cancel {
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

.btn-cancel:hover {
  background: #f5f7fa;
}

.btn-cancel i {
  font-size: 1.25rem;
}

/* ============================================================================
   LOADING OVERLAY
   ============================================================================ */

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loading-text {
  color: white;
  font-size: 1.1rem;
  font-weight: 600;
  margin-top: 1rem;
}

/* ============================================================================
   ERROR MESSAGE
   ============================================================================ */

.error-message {
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
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
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

.error-message i {
  font-size: 1.5rem;
}

.error-message p {
  margin: 0;
  font-size: 0.95rem;
  text-align: center;
}

.btn-close-error {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 0.5rem 1.5rem;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-close-error:hover {
  background: rgba(255, 255, 255, 0.3);
}

/* ============================================================================
   RESPONSIVE
   ============================================================================ */

@media (min-width: 768px) {
  .scanner-content {
    padding: 3rem 2rem;
  }

  .header-title {
    font-size: 1.5rem;
  }

  .manual-actions {
    flex-direction: row;
  }

  .btn-submit,
  .btn-cancel {
    flex: 1;
  }
}
</style>



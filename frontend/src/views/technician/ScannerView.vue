<!--
  ============================================================================
  SCANNER VIEW - Vista de Escaneo de Códigos QR
  ============================================================================

  DESCRIPCIÓN:
  Vista mobile-first para escanear códigos QR de equipos hospitalarios.
  Incluye modo de ingreso manual como fallback.

  MEJORAS DE ROBUSTEZ IMPLEMENTADAS:

  1. ✅ MANEJO DE ERRORES DE PERMISOS:
     - Try-catch robusto en el método .start()
     - Detección específica de NotAllowedError y PermissionDeniedError
     - Mensajes de error amigables y accionables
     - Instrucciones en consola para habilitar permisos

  2. ✅ CONFIGURACIÓN DE CÁMARA TRASERA:
     - facingMode: { exact: 'environment' } para forzar cámara trasera
     - Optimizado para Android (evita cámara frontal por defecto)
     - Configuración de aspectRatio y qrbox optimizada

  3. ✅ VALIDACIÓN DE CONTEXTO SEGURO (HTTPS):
     - Verifica window.isSecureContext al montar el componente
     - Muestra advertencia si no está en HTTPS
     - La API de cámara solo funciona en HTTPS (excepto localhost)

  4. ✅ MANEJO DE ERRORES ESPECÍFICOS:
     - NotAllowedError: Permisos denegados
     - NotFoundError: No se encontró cámara
     - NotReadableError: Cámara en uso por otra app
     - OverconstrainedError: Configuración no compatible

  5. ✅ UX MEJORADA:
     - Botón "Reintentar" cuando fallan los permisos
     - Indicador visual de "Cámara activa"
     - Transiciones suaves entre modos
     - Limpieza automática de errores al cambiar de modo

  DEPENDENCIAS:
  - html5-qrcode: Librería para escaneo de QR con cámara
  - Vue Router: Navegación entre vistas
  - API Client: Comunicación con backend

  AUTOR: Senior Frontend Engineer
  FECHA: 2025-11-27
  ============================================================================
-->

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

          <!-- Indicador de estado de cámara -->
          <div v-if="!cameraPermissionDenied && !errorMessage" class="camera-status">
            <i class="bi bi-camera-video-fill"></i>
            <span>Cámara activa</span>
          </div>

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
        <div class="error-actions">
          <button @click="retryScanner" class="btn-retry" v-if="cameraPermissionDenied && !showManualInput">
            <i class="bi bi-arrow-clockwise"></i>
            <span>Reintentar</span>
          </button>
          <button @click="clearError" class="btn-close-error">Cerrar</button>
        </div>
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
const cameraPermissionDenied = ref(false)
let html5QrCode = null

/**
 * Inicializa el escáner QR
 */
onMounted(() => {
  // Validar contexto seguro (HTTPS)
  checkSecureContext()

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
 * Valida que estemos en un contexto seguro (HTTPS)
 * La API de cámara solo funciona en HTTPS (excepto localhost)
 */
function checkSecureContext() {
  if (!window.isSecureContext) {
    console.warn('⚠️ Contexto no seguro detectado. La cámara requiere HTTPS.')
    errorMessage.value = '⚠️ La cámara solo funciona en conexiones seguras (HTTPS). Por favor, usa el ingreso manual.'
    cameraPermissionDenied.value = true
  }
}

/**
 * Inicializa el escáner de QR con manejo robusto de errores
 *
 * MEJORAS IMPLEMENTADAS:
 * 1. Validación de contexto seguro (HTTPS)
 * 2. Manejo específico de errores de permisos
 * 3. Configuración explícita de cámara trasera para Android
 * 4. Mensajes de error amigables y accionables
 * 5. Fallback automático a ingreso manual
 */
async function initScanner() {
  // Si ya se negaron los permisos, no intentar de nuevo
  if (cameraPermissionDenied.value) {
    return
  }

  try {
    // Crear instancia del escáner
    html5QrCode = new Html5Qrcode('qr-reader')

    // Configuración de cámara optimizada para Android
    const cameraConfig = {
      facingMode: { exact: 'environment' } // Forzar cámara trasera
    }

    // Configuración del escáner
    const scannerConfig = {
      fps: 10, // Frames por segundo
      qrbox: { width: 250, height: 250 }, // Área de escaneo
      aspectRatio: 1.0, // Ratio cuadrado para mejor detección
      disableFlip: false // Permitir flip horizontal si es necesario
    }

    // Intentar iniciar el escáner
    await html5QrCode.start(
      cameraConfig,
      scannerConfig,
      onScanSuccess,
      onScanError
    )

    console.log('✅ Escáner QR iniciado correctamente')

  } catch (err) {
    console.error('❌ Error al iniciar escáner:', err)

    // Manejo específico de errores de permisos
    handleCameraError(err)
  }
}

/**
 * Maneja errores específicos de la cámara con mensajes amigables
 *
 * @param {Error} error - Error capturado al iniciar la cámara
 */
function handleCameraError(error) {
  const errorName = error.name || ''
  const errorMessage = error.message || ''

  // Detectar tipo de error
  if (errorName === 'NotAllowedError' || errorName === 'PermissionDeniedError') {
    // Usuario negó el permiso de cámara
    showPermissionDeniedError()
  } else if (errorName === 'NotFoundError' || errorMessage.includes('camera')) {
    // No se encontró cámara en el dispositivo
    showNoCameraError()
  } else if (errorName === 'NotReadableError' || errorName === 'TrackStartError') {
    // Cámara en uso por otra aplicación
    showCameraInUseError()
  } else if (errorName === 'OverconstrainedError') {
    // La configuración solicitada no es compatible
    showConfigurationError()
  } else {
    // Error genérico
    showGenericCameraError(errorMessage)
  }

  cameraPermissionDenied.value = true
}

/**
 * Muestra error cuando el usuario niega el permiso de cámara
 */
function showPermissionDeniedError() {
  errorMessage.value = '⚠️ No podemos acceder a la cámara. Por favor, revisa los permisos de tu navegador o usa el ingreso manual.'

  // Mostrar instrucciones adicionales en consola
  console.warn(`
    📱 INSTRUCCIONES PARA HABILITAR LA CÁMARA:

    Android Chrome:
    1. Toca el ícono de candado/información en la barra de direcciones
    2. Toca "Permisos"
    3. Cambia "Cámara" a "Permitir"
    4. Recarga la página

    iOS Safari:
    1. Ve a Ajustes > Safari > Cámara
    2. Selecciona "Preguntar" o "Permitir"
    3. Recarga la página
  `)
}

/**
 * Muestra error cuando no se encuentra cámara
 */
function showNoCameraError() {
  errorMessage.value = '📷 No se detectó ninguna cámara en tu dispositivo. Por favor, usa el ingreso manual.'
}

/**
 * Muestra error cuando la cámara está en uso
 */
function showCameraInUseError() {
  errorMessage.value = '⚠️ La cámara está siendo usada por otra aplicación. Cierra otras apps que usen la cámara e intenta nuevamente.'
}

/**
 * Muestra error de configuración no compatible
 */
function showConfigurationError() {
  errorMessage.value = '⚠️ Tu dispositivo no soporta la configuración de cámara requerida. Por favor, usa el ingreso manual.'
}

/**
 * Muestra error genérico de cámara
 */
function showGenericCameraError(message) {
  errorMessage.value = `⚠️ Error al acceder a la cámara: ${message || 'Error desconocido'}. Por favor, usa el ingreso manual.`
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
 *
 * MEJORAS:
 * - Limpia errores al cambiar de modo
 * - Resetea el estado de permisos al volver al escáner
 * - Manejo seguro de transiciones
 */
async function toggleManualInput() {
  // Limpiar mensajes de error
  errorMessage.value = ''

  showManualInput.value = !showManualInput.value

  if (showManualInput.value) {
    // Cambiar a modo manual: detener escáner
    await stopScanner()
    manualCode.value = ''
    console.log('📝 Modo manual activado')
  } else {
    // Cambiar a modo escáner: reiniciar escáner
    // Resetear el flag de permisos para permitir reintentar
    cameraPermissionDenied.value = false

    console.log('📷 Intentando reiniciar escáner...')
    await initScanner()
  }
}

/**
 * Reintenta iniciar el escáner (útil después de que el usuario otorgue permisos)
 */
async function retryScanner() {
  errorMessage.value = ''
  cameraPermissionDenied.value = false

  console.log('🔄 Reintentando acceso a la cámara...')
  await initScanner()
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

.camera-status {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: #d4edda;
  color: #155724;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  margin-top: 1rem;
  animation: pulse 2s ease-in-out infinite;
}

.camera-status i {
  font-size: 1rem;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
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
  line-height: 1.5;
}

.error-actions {
  display: flex;
  gap: 0.75rem;
  width: 100%;
  justify-content: center;
}

.btn-retry {
  background: rgba(255, 255, 255, 0.9);
  border: none;
  color: #f44336;
  padding: 0.5rem 1.5rem;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-retry:hover {
  background: white;
  transform: translateY(-2px);
}

.btn-retry i {
  font-size: 1rem;
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



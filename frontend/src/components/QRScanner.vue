<!--
  ============================================================================
  QR SCANNER COMPONENT - ESCÁNER DE CÓDIGOS QR CON CÁMARA REAL
  ============================================================================

  VERSIÓN: 2.0 - REFACTORIZADO PARA MÓVILES

  CAMBIOS CRÍTICOS:
  - Usa Html5Qrcode (clase pura) en lugar de Html5QrcodeScanner
  - Fuerza cámara trasera con facingMode: "environment"
  - Manejo robusto de errores con debug visible
  - Altura fija del contenedor para móviles
  - Logs detallados para troubleshooting

  EVENTOS:
  - @scan-success: Emitido cuando se detecta un código QR exitosamente
    Payload: { decodedText: string, decodedResult: object }

  - @scan-error: Emitido cuando hay un error al escanear
    Payload: { error: string }

  DEPENDENCIAS:
  - html5-qrcode: ^2.3.8

  USO:
  <QRScanner
    @scan-success="handleScanSuccess"
    @scan-error="handleScanError"
  />

  AUTOR: Senior Frontend Developer
  FECHA: 2025-12-01 (Refactorizado)
  ============================================================================
-->

<template>
  <div class="qr-scanner-container">
    <!-- Contenedor del Escáner (ALTURA FIJA CRÍTICA PARA MÓVILES) -->
    <div id="reader" class="qr-reader"></div>

    <!-- Estado: Inicializando -->
    <div v-if="isInitializing" class="scanner-overlay">
      <div class="scanner-message">
        <div class="spinner"></div>
        <p class="mt-4">Solicitando acceso a la cámara...</p>
        <p class="text-small">Por favor, permite el acceso cuando el navegador lo solicite</p>
      </div>
    </div>

    <!-- Estado: Error con Debug Visible -->
    <div v-if="error" class="scanner-overlay error">
      <div class="scanner-message">
        <div class="error-icon">⚠️</div>
        <p class="mt-4 font-weight-bold">Error al iniciar la cámara</p>
        <div class="error-log">
          <p class="error-title">Detalles técnicos:</p>
          <p class="error-detail">{{ error }}</p>
          <p class="error-detail" v-if="errorDetails">{{ errorDetails }}</p>
        </div>
        <button class="retry-button" @click="retryScanner">
          🔄 Reintentar
        </button>
        <button class="debug-button" @click="showDebugInfo">
          🔍 Ver Info de Debug
        </button>
      </div>
    </div>

    <!-- Debug Info (Visible en desarrollo) -->
    <div v-if="debugMode" class="debug-panel">
      <h4>🐛 Debug Info</h4>
      <p><strong>Estado:</strong> {{ scannerState }}</p>
      <p><strong>Navegador:</strong> {{ userAgent }}</p>
      <p><strong>HTTPS:</strong> {{ isHttps ? '✅' : '❌' }}</p>
      <p><strong>MediaDevices API:</strong> {{ hasMediaDevices ? '✅' : '❌' }}</p>
      <button @click="debugMode = false">Cerrar</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { Html5Qrcode } from 'html5-qrcode'

// ============================================================================
// PROPS Y EMITS
// ============================================================================

const emit = defineEmits(['scan-success', 'scan-error'])

// ============================================================================
// STATE
// ============================================================================

let html5QrCode = null // NO usar ref() para evitar problemas de reactividad
const isInitializing = ref(true)
const isScanning = ref(false)
const error = ref(null)
const errorDetails = ref(null)
const debugMode = ref(false)
const scannerState = ref('IDLE')

// ============================================================================
// COMPUTED - DEBUG INFO
// ============================================================================

const userAgent = computed(() => navigator.userAgent)
const isHttps = computed(() => window.location.protocol === 'https:')
const hasMediaDevices = computed(() => !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia))

// ============================================================================
// MÉTODOS
// ============================================================================

/**
 * Inicia el escáner de QR codes con configuración robusta para móviles
 */
async function startScanner() {
  console.log('🚀 [QRScanner] Iniciando escáner...')
  console.log('📱 User Agent:', navigator.userAgent)
  console.log('🔒 HTTPS:', window.location.protocol === 'https:')
  console.log('📷 MediaDevices API:', !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia))

  try {
    isInitializing.value = true
    error.value = null
    errorDetails.value = null
    scannerState.value = 'INITIALIZING'

    // VERIFICACIÓN CRÍTICA: MediaDevices API
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      throw new Error('MediaDevices API no disponible. Verifica que estés usando HTTPS.')
    }

    // VERIFICACIÓN CRÍTICA: Elemento DOM existe
    const readerElement = document.getElementById('reader')
    if (!readerElement) {
      throw new Error('Elemento #reader no encontrado en el DOM')
    }

    console.log('✅ [QRScanner] Verificaciones iniciales pasadas')

    // Crear instancia del escáner (clase pura Html5Qrcode)
    html5QrCode = new Html5Qrcode('reader')
    console.log('✅ [QRScanner] Instancia Html5Qrcode creada')

    // CONFIGURACIÓN CRÍTICA PARA MÓVILES
    const qrCodeConfig = {
      fps: 10, // Frames por segundo (10 es óptimo para móviles)
      qrbox: { width: 250, height: 250 }, // Área de escaneo
      aspectRatio: 1.0, // Relación de aspecto cuadrada
      disableFlip: false, // Permitir flip horizontal
      videoConstraints: {
        facingMode: { exact: 'environment' } // FORZAR cámara trasera
      }
    }

    // CONSTRAINTS DE CÁMARA - FORZAR CÁMARA TRASERA
    const cameraConstraints = {
      facingMode: { exact: 'environment' } // Cámara trasera (crítico para móviles)
    }

    console.log('📷 [QRScanner] Solicitando acceso a la cámara...')
    console.log('🔧 [QRScanner] Constraints:', cameraConstraints)
    console.log('🔧 [QRScanner] Config:', qrCodeConfig)

    scannerState.value = 'REQUESTING_CAMERA'

    // Callback cuando se detecta un código QR
    const onScanSuccess = (decodedText, decodedResult) => {
      console.log('✅ [QRScanner] QR Code detectado:', decodedText)

      // Detener el escáner inmediatamente para evitar lecturas múltiples
      stopScanner()

      // Emitir evento al componente padre
      emit('scan-success', { decodedText, decodedResult })
    }

    // Callback para errores de escaneo (NO críticos - ocurren mientras escanea)
    const onScanError = (errorMessage) => {
      // No hacer nada - estos son errores normales mientras busca QR codes
      // Solo descomentar para debugging extremo:
      // console.log('🔍 [QRScanner] Escaneando...', errorMessage)
    }

    // INICIAR EL ESCÁNER
    await html5QrCode.start(
      cameraConstraints,
      qrCodeConfig,
      onScanSuccess,
      onScanError
    )

    isScanning.value = true
    isInitializing.value = false
    scannerState.value = 'SCANNING'

    console.log('✅ [QRScanner] Escáner iniciado correctamente')
    console.log('📹 [QRScanner] Video stream activo')

  } catch (err) {
    console.error('❌ [QRScanner] Error al iniciar el escáner:', err)
    console.error('❌ [QRScanner] Error name:', err.name)
    console.error('❌ [QRScanner] Error message:', err.message)
    console.error('❌ [QRScanner] Error stack:', err.stack)

    isInitializing.value = false
    scannerState.value = 'ERROR'

    // MANEJO DETALLADO DE ERRORES
    if (err.name === 'NotAllowedError' || err.message.includes('Permission denied')) {
      error.value = 'Permiso de cámara denegado'
      errorDetails.value = 'Ve a Configuración del navegador → Permisos → Cámara y permite el acceso a este sitio.'
    } else if (err.name === 'NotFoundError' || err.message.includes('Requested device not found')) {
      error.value = 'No se encontró la cámara trasera'
      errorDetails.value = 'Intenta con facingMode: "user" (cámara frontal) o verifica que tu dispositivo tenga cámara.'
    } else if (err.name === 'NotReadableError' || err.message.includes('Could not start video source')) {
      error.value = 'La cámara está siendo usada por otra aplicación'
      errorDetails.value = 'Cierra otras apps que usen la cámara e intenta de nuevo.'
    } else if (err.message.includes('HTTPS') || err.message.includes('secure context')) {
      error.value = 'Se requiere HTTPS para acceder a la cámara'
      errorDetails.value = `Protocolo actual: ${window.location.protocol}. La API de cámara solo funciona en HTTPS.`
    } else if (err.message.includes('MediaDevices')) {
      error.value = 'API de MediaDevices no disponible'
      errorDetails.value = 'Tu navegador no soporta acceso a la cámara o no estás en HTTPS.'
    } else {
      error.value = 'Error desconocido al iniciar la cámara'
      errorDetails.value = `${err.name}: ${err.message}`
    }

    emit('scan-error', { error: error.value, details: errorDetails.value })

    // MOSTRAR ALERT PARA DEBUG EN PRODUCCIÓN
    if (typeof window !== 'undefined') {
      alert(`❌ ERROR DE CÁMARA:\n\n${error.value}\n\n${errorDetails.value}\n\nError técnico: ${err.message}`)
    }
  }
}

/**
 * Detiene el escáner y libera la cámara
 */
async function stopScanner() {
  console.log('🛑 [QRScanner] Deteniendo escáner...')

  if (html5QrCode && isScanning.value) {
    try {
      await html5QrCode.stop()
      await html5QrCode.clear()
      isScanning.value = false
      scannerState.value = 'STOPPED'
      console.log('✅ [QRScanner] Escáner detenido y cámara liberada')
    } catch (err) {
      console.error('❌ [QRScanner] Error al detener el escáner:', err)
    }
  } else {
    console.log('⚠️ [QRScanner] No hay escáner activo para detener')
  }
}

/**
 * Reintentar el escáner después de un error
 */
function retryScanner() {
  console.log('🔄 [QRScanner] Reintentando iniciar escáner...')
  error.value = null
  errorDetails.value = null
  debugMode.value = false
  startScanner()
}

/**
 * Mostrar información de debug
 */
function showDebugInfo() {
  debugMode.value = true
  console.log('🐛 [QRScanner] Modo debug activado')
  console.log('📊 Estado:', scannerState.value)
  console.log('📱 User Agent:', navigator.userAgent)
  console.log('🔒 HTTPS:', window.location.protocol === 'https:')
  console.log('📷 MediaDevices:', !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia))
}

// ============================================================================
// LIFECYCLE HOOKS
// ============================================================================

onMounted(() => {
  console.log('🎬 [QRScanner] Componente montado')
  console.log('🌐 [QRScanner] URL:', window.location.href)
  console.log('🔧 [QRScanner] Protocolo:', window.location.protocol)

  // Pequeño delay para asegurar que el DOM esté completamente renderizado
  setTimeout(() => {
    startScanner()
  }, 100)
})

onUnmounted(async () => {
  console.log('🧹 [QRScanner] Componente desmontado - Liberando recursos...')
  await stopScanner()
})


</script>

<style scoped>
/* ============================================================================
   CONTENEDOR PRINCIPAL
   ============================================================================ */

.qr-scanner-container {
  position: relative;
  width: 100%;
  max-width: 500px;
  margin: 0 auto;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* ============================================================================
   ÁREA DEL ESCÁNER - CRÍTICO PARA MÓVILES
   ============================================================================ */

.qr-reader {
  width: 100%;
  height: 400px; /* ALTURA FIJA - CRÍTICO PARA MÓVILES */
  min-height: 400px;
  max-height: 400px;
  background: #000;
  position: relative;
  overflow: hidden;
}

/* Estilos para el video de la cámara */
.qr-reader video {
  width: 100% !important;
  height: 100% !important;
  object-fit: cover; /* Cubrir todo el contenedor */
  display: block;
}

/* Estilos para el canvas de html5-qrcode */
.qr-reader canvas {
  width: 100% !important;
  height: 100% !important;
  object-fit: cover;
}

/* Contenedor interno de html5-qrcode */
#reader {
  width: 100%;
  height: 100%;
}

#reader > div {
  width: 100% !important;
  height: 100% !important;
}

/* ============================================================================
   OVERLAY DE ESTADOS
   ============================================================================ */

.scanner-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
}

.scanner-overlay.error {
  background: rgba(211, 47, 47, 0.9);
}

.scanner-message {
  text-align: center;
  padding: 2rem;
}

.scanner-message p {
  font-size: 1rem;
  margin: 0;
  color: white;
}

.text-small {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.8);
  margin-top: 0.5rem;
}

.mt-4 {
  margin-top: 1rem;
}

.font-weight-bold {
  font-weight: 700;
}

/* ============================================================================
   ERROR LOG
   ============================================================================ */

.error-log {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 8px;
  padding: 1rem;
  margin: 1rem 0;
  text-align: left;
  max-width: 90%;
  margin-left: auto;
  margin-right: auto;
}

.error-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 0.5rem;
}

.error-detail {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.8);
  font-family: monospace;
  line-height: 1.4;
  margin: 0.25rem 0;
  word-break: break-word;
}

/* ============================================================================
   SPINNER
   ============================================================================ */

.spinner {
  width: 64px;
  height: 64px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* ============================================================================
   ERROR ICON
   ============================================================================ */

.error-icon {
  font-size: 64px;
  margin: 0 auto;
}

/* ============================================================================
   RETRY BUTTON
   ============================================================================ */

.retry-button {
  margin-top: 1rem;
  padding: 0.75rem 1.5rem;
  background: white;
  color: #d32f2f;
  border: 2px solid white;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.retry-button:hover {
  background: rgba(255, 255, 255, 0.9);
  transform: translateY(-2px);
}

.retry-button:active {
  transform: translateY(0);
}

/* ============================================================================
   DEBUG BUTTON
   ============================================================================ */

.debug-button {
  margin-top: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.debug-button:hover {
  background: rgba(255, 255, 255, 0.3);
}

/* ============================================================================
   DEBUG PANEL
   ============================================================================ */

.debug-panel {
  position: absolute;
  top: 1rem;
  left: 1rem;
  right: 1rem;
  background: rgba(0, 0, 0, 0.95);
  color: white;
  padding: 1rem;
  border-radius: 8px;
  z-index: 1000;
  font-size: 0.875rem;
  max-height: 80%;
  overflow-y: auto;
}

.debug-panel h4 {
  margin: 0 0 1rem 0;
  font-size: 1rem;
}

.debug-panel p {
  margin: 0.5rem 0;
  font-family: monospace;
  word-break: break-word;
}

.debug-panel button {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background: white;
  color: black;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
}

/* ============================================================================
   RESPONSIVE
   ============================================================================ */

@media (max-width: 600px) {
  .qr-scanner-container {
    max-width: 100%;
    border-radius: 0;
  }

  .qr-reader {
    height: 350px; /* Altura ligeramente menor en móviles */
    min-height: 350px;
    max-height: 350px;
  }

  .error-log {
    font-size: 0.75rem;
    padding: 0.75rem;
  }

  .debug-panel {
    font-size: 0.75rem;
    padding: 0.75rem;
  }
}

/* ============================================================================
   LANDSCAPE MODE (MÓVILES EN HORIZONTAL)
   ============================================================================ */

@media (max-width: 900px) and (orientation: landscape) {
  .qr-reader {
    height: 300px;
    min-height: 300px;
    max-height: 300px;
  }
}
</style>



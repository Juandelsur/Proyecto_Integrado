<!--
  ============================================================================
  QR SCANNER COMPONENT - ESCÁNER DE CÓDIGOS QR CON CÁMARA REAL
  ============================================================================

  DESCRIPCIÓN:
  Componente reutilizable que implementa un escáner de códigos QR usando
  la librería html5-qrcode. Accede a la cámara del dispositivo y detecta
  códigos QR en tiempo real.

  CARACTERÍSTICAS:
  - Acceso a la cámara del dispositivo (móvil/desktop)
  - Detección automática de códigos QR
  - Detiene el escáner automáticamente al detectar un código
  - Manejo correcto del ciclo de vida (libera la cámara al desmontar)
  - Emite evento con el código escaneado
  - Manejo de errores (permisos, cámara no disponible)

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
  FECHA: 2025-12-01
  ============================================================================
-->

<template>
  <div class="qr-scanner-container">
    <!-- Contenedor del Escáner -->
    <div id="qr-reader" class="qr-reader"></div>

    <!-- Estado: Inicializando -->
    <div v-if="isInitializing" class="scanner-overlay">
      <div class="scanner-message">
        <div class="spinner"></div>
        <p class="mt-4">Iniciando cámara...</p>
      </div>
    </div>

    <!-- Estado: Error -->
    <div v-if="error" class="scanner-overlay error">
      <div class="scanner-message">
        <div class="error-icon">⚠️</div>
        <p class="mt-4 font-weight-bold">{{ error }}</p>
        <button class="retry-button" @click="retryScanner">
          Reintentar
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { Html5Qrcode } from 'html5-qrcode'

// ============================================================================
// PROPS Y EMITS
// ============================================================================

const emit = defineEmits(['scan-success', 'scan-error'])

// ============================================================================
// STATE
// ============================================================================

const html5QrCode = ref(null)
const isInitializing = ref(true)
const isScanning = ref(false)
const error = ref(null)

// ============================================================================
// MÉTODOS
// ============================================================================

/**
 * Inicia el escáner de QR codes
 */
async function startScanner() {
  try {
    isInitializing.value = true
    error.value = null

    // Crear instancia del escáner
    html5QrCode.value = new Html5Qrcode('qr-reader')

    // Configuración del escáner
    const config = {
      fps: 10, // Frames por segundo
      qrbox: { width: 250, height: 250 }, // Área de escaneo
      aspectRatio: 1.0 // Relación de aspecto
    }

    // Callback cuando se detecta un código QR
    const onScanSuccess = (decodedText, decodedResult) => {
      console.log('✅ QR Code detectado:', decodedText)

      // Detener el escáner inmediatamente
      stopScanner()

      // Emitir evento al componente padre
      emit('scan-success', { decodedText, decodedResult })
    }

    // Callback para errores de escaneo (no críticos)
    const onScanError = (errorMessage) => {
      // No hacer nada - errores normales durante el escaneo
      // Solo logueamos si es necesario para debugging
      // console.log('Escaneando...', errorMessage)
    }

    // Iniciar el escáner con la cámara trasera (preferida en móviles)
    await html5QrCode.value.start(
      { facingMode: 'environment' }, // Cámara trasera
      config,
      onScanSuccess,
      onScanError
    )

    isScanning.value = true
    isInitializing.value = false

    console.log('📷 Escáner iniciado correctamente')
  } catch (err) {
    console.error('❌ Error al iniciar el escáner:', err)
    isInitializing.value = false

    // Determinar el tipo de error
    if (err.name === 'NotAllowedError') {
      error.value = 'Permiso de cámara denegado. Por favor, permite el acceso a la cámara.'
    } else if (err.name === 'NotFoundError') {
      error.value = 'No se encontró ninguna cámara en este dispositivo.'
    } else {
      error.value = 'Error al iniciar la cámara. Por favor, intenta de nuevo.'
    }

    emit('scan-error', { error: error.value })
  }
}

/**
 * Detiene el escáner y libera la cámara
 */
async function stopScanner() {
  if (html5QrCode.value && isScanning.value) {
    try {
      await html5QrCode.value.stop()
      isScanning.value = false
      console.log('🛑 Escáner detenido')
    } catch (err) {
      console.error('Error al detener el escáner:', err)
    }
  }
}

/**
 * Reintentar el escáner después de un error
 */
function retryScanner() {
  error.value = null
  startScanner()
}

// ============================================================================
// LIFECYCLE HOOKS
// ============================================================================

onMounted(() => {
  console.log('🎬 QRScanner montado - Iniciando escáner...')
  startScanner()
})

onUnmounted(async () => {
  console.log('🧹 QRScanner desmontado - Liberando cámara...')
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
   ÁREA DEL ESCÁNER
   ============================================================================ */

.qr-reader {
  width: 100%;
  min-height: 300px;
  background: #000;
}

/* Estilos para el video de la cámara */
.qr-reader video {
  width: 100%;
  height: auto;
  display: block;
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

.mt-4 {
  margin-top: 1rem;
}

.font-weight-bold {
  font-weight: 700;
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
   RESPONSIVE
   ============================================================================ */

@media (max-width: 600px) {
  .qr-scanner-container {
    max-width: 100%;
    border-radius: 0;
  }

  .qr-reader {
    min-height: 250px;
  }
}
</style>



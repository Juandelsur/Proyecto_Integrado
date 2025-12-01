<!--
  ============================================================================
  QR SCANNER COMPONENT - ESCÁNER DE CÓDIGOS QR CON CÁMARA REAL
  ============================================================================

  VERSIÓN: 4.0 - ESTRATEGIA "ISLA HTML" 🏝️

  ARQUITECTURA:
  - Vuetify para UI (v-card, v-btn, v-icon, v-alert) → Marco visual profesional
  - HTML puro para área de cámara → Evita conflictos de CSS con Vuetify
  - "Click para Iniciar" → Resuelve permisos en móviles + problemas de renderizado

  CAMBIOS CRÍTICOS V4:
  ✅ Isla HTML: <div id="reader"> con estilos inline (height en px)
  ✅ Click para Iniciar: Botón grande que activa la cámara (User Interaction)
  ✅ Delay de 200ms: setTimeout antes de html5QrCode.start()
  ✅ Configuración robusta: fps=10, qrbox=250, aspectRatio=1.0
  ✅ Manejo de errores: v-alert detallado + console.error

  EVENTOS:
  - @scan-success: Emitido cuando se detecta un código QR exitosamente
    Payload: { decodedText: string, decodedResult: object }

  - @scan-error: Emitido cuando hay un error al escanear
    Payload: { error: string, details: string }

  DEPENDENCIAS:
  - html5-qrcode: ^2.3.8
  - Vuetify 3: v-card, v-btn, v-icon, v-alert

  USO:
  <QRScanner
    @scan-success="handleScanSuccess"
    @scan-error="handleScanError"
  />

  AUTOR: Senior Full Stack Engineer
  FECHA: 2025-12-01 (Refactorizado v4.0 - Isla HTML)
  ============================================================================
-->

<template>
  <!-- ========================================================================
       CONTENEDOR PRINCIPAL - VUETIFY CARD
       ======================================================================== -->
  <v-card class="qr-scanner-card" elevation="8" rounded="lg">
    <!-- HEADER -->
    <v-card-title class="scanner-header">
      <v-icon size="28" color="primary" class="mr-2">mdi-qrcode-scan</v-icon>
      <span class="text-h6 font-weight-bold">Escáner QR</span>
    </v-card-title>

    <!-- ========================================================================
         ISLA HTML - ÁREA DE CÁMARA (HTML PURO - SIN VUETIFY)
         ======================================================================== -->
    <v-card-text class="pa-0">
      <!-- Contenedor de la isla HTML -->
      <div class="camera-island-container">
        <!-- ISLA HTML: Elemento crudo para html5-qrcode -->
        <div
          id="reader"
          style="width: 100%; height: 350px; border: 1px solid #e0e0e0; background: #000;"
        ></div>

        <!-- ====================================================================
             OVERLAY: BOTÓN "INICIAR ESCÁNER" (Click para Iniciar)
             ==================================================================== -->
        <div v-if="!cameraReady && !error" class="start-overlay">
          <div class="start-content">
            <!-- Ícono animado -->
            <v-icon size="80" color="white" class="camera-icon-animated">
              mdi-camera
            </v-icon>

            <!-- Título -->
            <h3 class="text-h5 font-weight-bold white--text mt-4 mb-2">
              Listo para escanear
            </h3>

            <!-- Spinner mientras inicializa -->
            <div v-if="isInitializing" class="text-center">
              <v-progress-circular
                indeterminate
                color="white"
                size="64"
                width="6"
                class="mb-4"
              ></v-progress-circular>
              <p class="white--text text-body-1">Iniciando cámara...</p>
            </div>

            <!-- Botón de inicio (User Interaction) -->
            <div v-else class="text-center">
              <p class="white--text text-body-1 mb-4">
                Presiona el botón para activar la cámara
              </p>

              <v-btn
                size="x-large"
                color="primary"
                elevation="8"
                rounded="lg"
                @click="startScannerManually"
                class="start-button"
              >
                <v-icon left size="28">mdi-camera</v-icon>
                INICIAR ESCÁNER
              </v-btn>

              <p class="white--text text-caption mt-4 opacity-70">
                Se solicitarán permisos de cámara
              </p>
            </div>
          </div>
        </div>

        <!-- ====================================================================
             OVERLAY: ERROR (Solo si hay error)
             ==================================================================== -->
        <div v-if="error" class="error-overlay">
          <div class="error-content">
            <v-alert
              type="error"
              variant="tonal"
              prominent
              border="start"
              class="mb-4"
            >
              <template v-slot:prepend>
                <v-icon size="48">mdi-alert-circle</v-icon>
              </template>

              <div class="text-h6 font-weight-bold mb-2">
                Error al iniciar la cámara
              </div>

              <div class="text-body-2 mb-2">
                {{ error }}
              </div>

              <div v-if="errorDetails" class="text-caption error-details">
                {{ errorDetails }}
              </div>
            </v-alert>

            <!-- Botones de acción -->
            <div class="d-flex flex-column gap-2">
              <v-btn
                color="error"
                variant="elevated"
                size="large"
                @click="retryScanner"
                block
              >
                <v-icon left>mdi-refresh</v-icon>
                Reintentar
              </v-btn>

              <v-btn
                color="grey-darken-2"
                variant="outlined"
                size="small"
                @click="showDebugInfo"
                block
              >
                <v-icon left size="20">mdi-bug</v-icon>
                Ver información de debug
              </v-btn>
            </div>
          </div>
        </div>
      </div>
    </v-card-text>

    <!-- ========================================================================
         FOOTER: ESTADO DE LA CÁMARA
         ======================================================================== -->
    <v-card-actions v-if="cameraReady" class="scanner-footer">
      <v-chip color="success" variant="flat" size="small">
        <v-icon left size="16">mdi-circle</v-icon>
        Cámara activa
      </v-chip>
      <v-spacer></v-spacer>
      <v-chip color="primary" variant="outlined" size="small">
        Apunta al código QR
      </v-chip>
    </v-card-actions>

    <!-- ========================================================================
         DEBUG PANEL (Solo si debugMode = true)
         ======================================================================== -->
    <v-dialog v-model="debugMode" max-width="500">
      <v-card>
        <v-card-title class="bg-grey-darken-3 white--text">
          <v-icon left color="white">mdi-bug</v-icon>
          Información de Debug
        </v-card-title>

        <v-card-text class="pt-4">
          <v-list density="compact">
            <v-list-item>
              <v-list-item-title>Estado:</v-list-item-title>
              <v-list-item-subtitle>{{ scannerState }}</v-list-item-subtitle>
            </v-list-item>

            <v-list-item>
              <v-list-item-title>Cámara Lista:</v-list-item-title>
              <v-list-item-subtitle>{{ cameraReady ? '✅ Sí' : '❌ No' }}</v-list-item-subtitle>
            </v-list-item>

            <v-list-item>
              <v-list-item-title>Escaneando:</v-list-item-title>
              <v-list-item-subtitle>{{ isScanning ? '✅ Sí' : '❌ No' }}</v-list-item-subtitle>
            </v-list-item>

            <v-list-item>
              <v-list-item-title>HTTPS:</v-list-item-title>
              <v-list-item-subtitle>{{ isHttps ? '✅ Sí' : '❌ No' }}</v-list-item-subtitle>
            </v-list-item>

            <v-list-item>
              <v-list-item-title>MediaDevices API:</v-list-item-title>
              <v-list-item-subtitle>{{ hasMediaDevices ? '✅ Disponible' : '❌ No disponible' }}</v-list-item-subtitle>
            </v-list-item>

            <v-list-item>
              <v-list-item-title>Navegador:</v-list-item-title>
              <v-list-item-subtitle class="text-caption">{{ userAgent }}</v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="debugMode = false">Cerrar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { Html5Qrcode } from 'html5-qrcode'

// ============================================================================
// PROPS Y EMITS
// ============================================================================

const emit = defineEmits(['scan-success', 'scan-error'])

// ============================================================================
// STATE
// ============================================================================

let html5QrCode = null // NO usar ref() para evitar problemas de reactividad
const isInitializing = ref(false) // Cambiado a false - se activa manualmente
const isScanning = ref(false)
const cameraReady = ref(false) // NUEVO: Indica si la cámara está lista y el video visible
const error = ref(null)
const errorDetails = ref(null)
const debugMode = ref(false)
const scannerState = ref('IDLE')
const autoStartAttempted = ref(false) // NUEVO: Evita múltiples intentos automáticos

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
 * ESTRATEGIA "ISLA HTML": Delay de 200ms + configuración a prueba de balas
 */
async function startScanner() {
  console.log('🚀 [QRScanner v4.0] Iniciando escáner con estrategia Isla HTML...')
  console.log('📱 User Agent:', navigator.userAgent)
  console.log('🔒 HTTPS:', window.location.protocol === 'https:')
  console.log('📷 MediaDevices API:', !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia))

  try {
    isInitializing.value = true
    cameraReady.value = false
    error.value = null
    errorDetails.value = null
    scannerState.value = 'INITIALIZING'

    // ========================================================================
    // VERIFICACIÓN 1: MediaDevices API disponible
    // ========================================================================
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      throw new Error('MediaDevices API no disponible. Verifica que estés usando HTTPS.')
    }
    console.log('✅ [QRScanner] MediaDevices API disponible')

    // ========================================================================
    // VERIFICACIÓN 2: Esperar a que el DOM esté listo (nextTick)
    // ========================================================================
    await nextTick()
    console.log('✅ [QRScanner] nextTick() completado - DOM listo')

    // ========================================================================
    // VERIFICACIÓN 3: Elemento #reader existe en el DOM
    // ========================================================================
    const readerElement = document.getElementById('reader')
    if (!readerElement) {
      throw new Error('Elemento #reader no encontrado en el DOM después de nextTick()')
    }
    console.log('✅ [QRScanner] Elemento #reader encontrado')
    console.log('📐 [QRScanner] Dimensiones:', readerElement.offsetWidth, 'x', readerElement.offsetHeight)

    // ========================================================================
    // DELAY DE 200MS - CRÍTICO PARA RENDERIZADO
    // ========================================================================
    console.log('⏳ [QRScanner] Esperando 200ms para asegurar renderizado completo...')
    await new Promise(resolve => setTimeout(resolve, 200))
    console.log('✅ [QRScanner] Delay completado - DOM estable')

    // ========================================================================
    // CREAR INSTANCIA DE HTML5-QRCODE
    // ========================================================================
    html5QrCode = new Html5Qrcode('reader')
    console.log('✅ [QRScanner] Instancia Html5Qrcode creada')

    // ========================================================================
    // CONFIGURACIÓN A PRUEBA DE BALAS
    // ========================================================================
    const qrCodeConfig = {
      fps: 10,                    // ✅ 10 FPS óptimo para móviles
      qrbox: 250,                 // ✅ Área de escaneo 250x250px
      aspectRatio: 1.0,           // ✅ Relación de aspecto cuadrada (evita deformación)
      disableFlip: false          // ✅ Permitir flip horizontal
    }

    const cameraConstraints = {
      facingMode: { exact: 'environment' } // ✅ FORZAR cámara trasera
    }

    console.log('🔧 [QRScanner] Configuración:')
    console.log('   - FPS:', qrCodeConfig.fps)
    console.log('   - QR Box:', qrCodeConfig.qrbox)
    console.log('   - Aspect Ratio:', qrCodeConfig.aspectRatio)
    console.log('   - Facing Mode:', cameraConstraints.facingMode.exact)

    scannerState.value = 'REQUESTING_CAMERA'

    // ========================================================================
    // CALLBACKS
    // ========================================================================
    const onScanSuccess = (decodedText, decodedResult) => {
      console.log('✅ [QRScanner] QR Code detectado:', decodedText)
      stopScanner()
      emit('scan-success', { decodedText, decodedResult })
    }

    const onScanError = (errorMessage) => {
      // Silenciar errores normales de escaneo (no son críticos)
    }

    // ========================================================================
    // INICIAR ESCÁNER
    // ========================================================================
    console.log('📷 [QRScanner] Solicitando acceso a la cámara...')
    await html5QrCode.start(
      cameraConstraints,
      qrCodeConfig,
      onScanSuccess,
      onScanError
    )

    // ========================================================================
    // ÉXITO - CÁMARA ACTIVA
    // ========================================================================
    isScanning.value = true
    isInitializing.value = false
    cameraReady.value = true
    scannerState.value = 'SCANNING'

    console.log('✅ [QRScanner] Escáner iniciado correctamente')
    console.log('📹 [QRScanner] Video stream activo')
    console.log('🎬 [QRScanner] Overlay oculto - Cámara visible')

  } catch (err) {
    console.error('❌ [QRScanner] Error al iniciar el escáner:', err)
    console.error('❌ [QRScanner] Error name:', err.name)
    console.error('❌ [QRScanner] Error message:', err.message)

    isInitializing.value = false
    cameraReady.value = false
    scannerState.value = 'ERROR'

    // ========================================================================
    // MANEJO DETALLADO DE ERRORES
    // ========================================================================
    if (err.name === 'NotAllowedError' || err.message.includes('Permission denied')) {
      error.value = 'Permiso de cámara denegado'
      errorDetails.value = 'Ve a Configuración → Permisos → Cámara y permite el acceso.'
    } else if (err.name === 'NotFoundError' || err.message.includes('Requested device not found')) {
      error.value = 'No se encontró la cámara trasera'
      errorDetails.value = 'Verifica que tu dispositivo tenga cámara trasera.'
    } else if (err.name === 'NotReadableError' || err.message.includes('Could not start video source')) {
      error.value = 'La cámara está siendo usada por otra aplicación'
      errorDetails.value = 'Cierra otras apps que usen la cámara.'
    } else if (err.message.includes('HTTPS') || err.message.includes('secure context')) {
      error.value = 'Se requiere HTTPS para acceder a la cámara'
      errorDetails.value = `Protocolo actual: ${window.location.protocol}`
    } else if (err.message.includes('MediaDevices')) {
      error.value = 'API de MediaDevices no disponible'
      errorDetails.value = 'Tu navegador no soporta acceso a la cámara.'
    } else {
      error.value = 'Error desconocido al iniciar la cámara'
      errorDetails.value = `${err.name}: ${err.message}`
    }

    emit('scan-error', { error: error.value, details: errorDetails.value })

    // ========================================================================
    // ALERT PARA DEBUG (IMPORTANTE EN PRODUCCIÓN)
    // ========================================================================
    alert(`❌ ERROR DE CÁMARA\n\n${error.value}\n\n${errorDetails.value}\n\nError técnico: ${err.message}`)
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
      cameraReady.value = false
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
 * Inicia el escáner manualmente (User Interaction)
 * CRÍTICO: Los navegadores móviles requieren que la cámara sea activada por un click del usuario
 */
async function startScannerManually() {
  console.log('👆 [QRScanner] Inicio manual por User Interaction')
  await startScanner()
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

  // NO INICIAR AUTOMÁTICAMENTE - Esperar User Interaction
  // Esto es crítico para móviles que bloquean acceso a cámara sin click del usuario
  console.log('⏸️ [QRScanner] Esperando User Interaction para iniciar cámara')

  // OPCIONAL: Intentar inicio automático solo en desktop (no móviles)
  const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)

  if (!isMobile && !autoStartAttempted.value) {
    console.log('💻 [QRScanner] Desktop detectado - Intentando inicio automático')
    autoStartAttempted.value = true

    // Delay para asegurar que el DOM esté completamente renderizado
    setTimeout(async () => {
      await nextTick()
      startScanner()
    }, 200)
  } else {
    console.log('📱 [QRScanner] Móvil detectado - Requiere User Interaction')
  }
})

onUnmounted(async () => {
  console.log('🧹 [QRScanner] Componente desmontado - Liberando recursos...')
  await stopScanner()
})


</script>

<style scoped>
/* ============================================================================
   VUETIFY CARD - CONTENEDOR PRINCIPAL
   ============================================================================ */

.qr-scanner-card {
  max-width: 500px;
  margin: 0 auto;
  overflow: hidden;
}

.scanner-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white !important;
  padding: 16px 20px;
}

.scanner-footer {
  background: #f5f5f5;
  padding: 12px 16px;
  border-top: 1px solid #e0e0e0;
}

/* ============================================================================
   ISLA HTML - CONTENEDOR DE CÁMARA
   ============================================================================ */

.camera-island-container {
  position: relative;
  width: 100%;
  height: 350px;
  overflow: hidden;
  background: #000;
}

/* ============================================================================
   ELEMENTO #reader - ISLA HTML PURA (SIN VUETIFY)
   ============================================================================ */

#reader {
  /* Los estilos inline son críticos - NO sobrescribir */
  position: relative;
}

/* Estilos para el video generado por html5-qrcode */
#reader video {
  width: 100% !important;
  height: 100% !important;
  object-fit: cover !important;
  display: block !important;
  position: absolute !important;
  top: 0 !important;
  left: 0 !important;
  z-index: 1 !important;
}

/* Estilos para el canvas (overlay del QR box) */
#reader canvas {
  position: absolute !important;
  top: 0 !important;
  left: 0 !important;
  width: 100% !important;
  height: 100% !important;
  z-index: 2 !important;
}

/* Contenedor interno generado por html5-qrcode */
#reader > div {
  width: 100% !important;
  height: 100% !important;
  position: relative !important;
}

/* ============================================================================
   OVERLAY: BOTÓN "INICIAR ESCÁNER" (Click para Iniciar)
   ============================================================================ */

.start-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.95) 0%, rgba(118, 75, 162, 0.95) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
  transition: opacity 0.3s ease;
}

.start-content {
  text-align: center;
  padding: 2rem;
  max-width: 90%;
}

.camera-icon-animated {
  animation: pulse-icon 2s ease-in-out infinite;
}

@keyframes pulse-icon {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.7;
    transform: scale(1.1);
  }
}

.start-button {
  text-transform: none;
  letter-spacing: 0.5px;
  font-weight: 700;
  padding: 12px 32px !important;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3) !important;
}

.start-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.4) !important;
}

.opacity-70 {
  opacity: 0.7;
}

/* ============================================================================
   OVERLAY: ERROR
   ============================================================================ */

.error-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 20;
  padding: 1rem;
}

.error-content {
  width: 100%;
  max-width: 400px;
}

.error-details {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 12px;
  margin-top: 8px;
  font-family: monospace;
  font-size: 0.75rem;
  word-break: break-word;
}

.gap-2 {
  gap: 8px;
}

/* ============================================================================
   RESPONSIVE - MÓVILES
   ============================================================================ */

@media (max-width: 600px) {
  .qr-scanner-card {
    max-width: 100%;
    border-radius: 0 !important;
  }

  .camera-island-container {
    height: 300px;
  }

  .scanner-header {
    padding: 12px 16px;
  }

  .start-content {
    padding: 1.5rem;
  }

  .start-button {
    padding: 10px 24px !important;
    font-size: 0.875rem !important;
  }

  .error-content {
    padding: 1rem;
  }
}

/* ============================================================================
   LANDSCAPE MODE (MÓVILES EN HORIZONTAL)
   ============================================================================ */

@media (max-width: 900px) and (orientation: landscape) {
  .camera-island-container {
    height: 250px;
  }

  .start-content {
    padding: 1rem;
  }

  .camera-icon-animated {
    font-size: 48px !important;
  }
}
</style>



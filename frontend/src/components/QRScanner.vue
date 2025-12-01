<!--
  ============================================================================
  QR SCANNER COMPONENT v5.0 - PATRÓN "OVERLAY MANUAL"
  ============================================================================

  VERSIÓN: 5.0 - Reescritura total para móviles

  PROBLEMA RESUELTO:
  - Chrome/Safari móvil bloquean getUserMedia sin User Gesture
  - Vuetify colapsa contenedores sin altura fija

  SOLUCIÓN:
  - Altura fija de 400px en CSS (NO inline)
  - Overlay con botón ACTIVAR CÁMARA (User Gesture)
  - NO hay start() en onMounted
  - nextTick() + setTimeout(300ms) antes de start()
  - Limpieza con stop().clear() en onBeforeUnmount

  EVENTOS:
  - @scan-success: { decodedText, decodedResult }
  - @scan-error: { error, details }

  DEPENDENCIAS:
  - html5-qrcode: ^2.3.8
  - Vuetify 3

  ============================================================================
-->

<template>
  <!-- ========================================================================
       CONTENEDOR PRINCIPAL - ALTURA FIJA 400px
       ======================================================================== -->
  <div class="qr-scanner-wrapper">
    <!-- ======================================================================
         CAPA 1 (FONDO): LECTOR HTML PURO - SIN VUETIFY
         NOTA: Usamos un ID único para evitar conflictos si hay múltiples instancias
         ====================================================================== -->
    <div :id="readerId" class="qr-reader-element"></div>

    <!-- ======================================================================
         CAPA 2 (OVERLAY): Se muestra hasta que isCameraReady = true
         ====================================================================== -->
    <div v-if="!isCameraReady" class="overlay-manual">
      <!-- Estado: Esperando activación -->
      <div v-if="!isInitializing && !error" class="overlay-content">
        <v-icon size="72" color="white" class="mb-4 pulse-animation">
          mdi-camera
        </v-icon>

        <h3 class="text-h5 font-weight-bold text-white mb-2">
          Escáner QR
        </h3>

        <p class="text-body-2 text-white mb-6" style="opacity: 0.8;">
          Presiona el botón para activar la cámara
        </p>

        <v-btn
          size="x-large"
          color="primary"
          variant="elevated"
          rounded="pill"
          class="activate-btn"
          @click="iniciarCamara"
        >
          <v-icon start size="28">mdi-camera</v-icon>
          ACTIVAR CÁMARA
        </v-btn>

        <p class="text-caption text-white mt-4" style="opacity: 0.6;">
          Se solicitarán permisos de cámara
        </p>
      </div>

      <!-- Estado: Inicializando cámara -->
      <div v-if="isInitializing && !error" class="overlay-content">
        <v-progress-circular
          indeterminate
          color="white"
          size="80"
          width="6"
          class="mb-4"
        ></v-progress-circular>

        <p class="text-h6 text-white">Iniciando cámara...</p>
        <p class="text-caption text-white" style="opacity: 0.7;">
          Acepta los permisos si se solicitan
        </p>
      </div>

      <!-- Estado: Error -->
      <div v-if="error" class="overlay-content overlay-error">
        <v-alert
          type="error"
          variant="elevated"
          prominent
          class="mb-4"
          max-width="350"
        >
          <template v-slot:prepend>
            <v-icon size="40">mdi-alert-circle</v-icon>
          </template>

          <div class="text-subtitle-1 font-weight-bold mb-1">
            {{ error }}
          </div>

          <div v-if="errorDetails" class="text-caption">
            {{ errorDetails }}
          </div>
        </v-alert>

        <div class="d-flex flex-column" style="gap: 12px; width: 100%; max-width: 300px;">
          <v-btn
            color="error"
            variant="elevated"
            size="large"
            block
            @click="reintentar"
          >
            <v-icon start>mdi-refresh</v-icon>
            Reintentar
          </v-btn>

          <v-btn
            color="grey-lighten-2"
            variant="text"
            size="small"
            block
            @click="mostrarDebug = true"
          >
            <v-icon start size="18">mdi-bug</v-icon>
            Ver información técnica
          </v-btn>
        </div>
      </div>
    </div>

    <!-- ======================================================================
         INDICADOR DE CÁMARA ACTIVA (Solo cuando funciona)
         ====================================================================== -->
    <div v-if="isCameraReady" class="camera-active-indicator">
      <v-chip color="success" size="small" variant="elevated">
        <v-icon start size="12">mdi-circle</v-icon>
        Cámara activa - Apunta al código QR
      </v-chip>
    </div>

    <!-- ======================================================================
         DIALOG DE DEBUG
         ====================================================================== -->
    <v-dialog v-model="mostrarDebug" max-width="400">
      <v-card>
        <v-card-title class="bg-grey-darken-3">
          <v-icon start color="white">mdi-bug</v-icon>
          <span class="text-white">Información de Debug</span>
        </v-card-title>

        <v-card-text class="pt-4">
          <div class="debug-item">
            <strong>Estado:</strong> {{ scannerState }}
          </div>
          <div class="debug-item">
            <strong>Cámara Lista:</strong> {{ isCameraReady ? '✅' : '❌' }}
          </div>
          <div class="debug-item">
            <strong>HTTPS:</strong> {{ isHttps ? '✅' : '❌' }}
          </div>
          <div class="debug-item">
            <strong>MediaDevices:</strong> {{ hasMediaDevices ? '✅' : '❌' }}
          </div>
          <div class="debug-item">
            <strong>Reader ID:</strong> {{ readerId }}
          </div>
          <div class="debug-item">
            <strong>URL:</strong>
            <div class="text-caption" style="word-break: break-all;">
              {{ currentUrl }}
            </div>
          </div>
          <div class="debug-item">
            <strong>Error:</strong> {{ error || 'Ninguno' }}
          </div>
          <div class="debug-item">
            <strong>Error Detalle:</strong> {{ errorDetails || 'Ninguno' }}
          </div>
          <div class="debug-item">
            <strong>User Agent:</strong>
            <div class="text-caption" style="word-break: break-all;">
              {{ userAgent }}
            </div>
          </div>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="mostrarDebug = false">Cerrar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { Html5Qrcode } from 'html5-qrcode'

// ============================================================================
// EMITS
// ============================================================================

const emit = defineEmits(['scan-success', 'scan-error'])

// ============================================================================
// STATE - Solo lo esencial
// ============================================================================

let html5QrCode = null // NO usar ref() - evita problemas de reactividad
const isCameraReady = ref(false) // CRÍTICO: Controla visibilidad del overlay
const isInitializing = ref(false)
const error = ref(null)
const errorDetails = ref(null)
const mostrarDebug = ref(false)
const scannerState = ref('IDLE')

// ID único para el elemento reader (evita conflictos con múltiples instancias)
const readerId = `qr-reader-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`

// ============================================================================
// COMPUTED - Info de debug
// ============================================================================

const userAgent = computed(() => navigator.userAgent)
const isHttps = computed(() => window.location.protocol === 'https:')
const hasMediaDevices = computed(() => !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia))
const currentUrl = computed(() => window.location.href)

// ============================================================================
// FUNCIÓN PRINCIPAL: iniciarCamara() - ACTIVADA POR USER GESTURE
// ============================================================================

/**
 * Inicia la cámara tras un click del usuario (User Gesture)
 * PATRÓN: nextTick() + setTimeout(300ms) + start()
 */
async function iniciarCamara() {
  console.log('📸 [QRScanner v5.0] iniciarCamara() - User Gesture detectado')

  try {
    // ========================================================================
    // PASO 1: Preparar estado
    // ========================================================================
    isInitializing.value = true
    error.value = null
    errorDetails.value = null
    scannerState.value = 'INITIALIZING'

    // ========================================================================
    // PASO 2: Verificar MediaDevices API
    // ========================================================================
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      throw new Error('Tu navegador no soporta acceso a la cámara. Usa Chrome o Safari.')
    }
    console.log('✅ MediaDevices API disponible')

    // ========================================================================
    // PASO 3: Esperar a que el DOM esté listo (nextTick)
    // ========================================================================
    await nextTick()
    console.log('✅ nextTick() completado')

    // ========================================================================
    // PASO 4: Verificar elemento reader
    // ========================================================================
    const readerElement = document.getElementById(readerId)
    if (!readerElement) {
      throw new Error(`Elemento #${readerId} no encontrado en el DOM`)
    }
    console.log(`✅ Elemento #${readerId} encontrado:`, readerElement.offsetWidth, 'x', readerElement.offsetHeight)

    // Verificar que tenga dimensiones (crítico para móviles)
    if (readerElement.offsetWidth === 0 || readerElement.offsetHeight === 0) {
      console.warn('⚠️ El elemento reader no tiene dimensiones. Forzando...')
      readerElement.style.width = '100%'
      readerElement.style.height = '400px'
      readerElement.style.minHeight = '300px'
    }

    // ========================================================================
    // PASO 5: DELAY DE 300MS - CRÍTICO PARA MÓVILES
    // Asegura que el DOM esté completamente pintado
    // ========================================================================
    console.log('⏳ Esperando 300ms para asegurar renderizado...')
    await new Promise(resolve => setTimeout(resolve, 300))
    console.log('✅ Delay completado')

    // ========================================================================
    // PASO 6: Limpiar instancia previa si existe
    // ========================================================================
    if (html5QrCode) {
      try {
        await html5QrCode.stop()
        html5QrCode.clear()
      } catch (e) {
        console.warn('⚠️ Error limpiando instancia previa:', e.message)
      }
    }

    // ========================================================================
    // PASO 7: Crear instancia de Html5Qrcode
    // ========================================================================
    html5QrCode = new Html5Qrcode(readerId)
    console.log('✅ Instancia Html5Qrcode creada con ID:', readerId)

    // ========================================================================
    // PASO 8: Configuración optimizada para móviles
    // ========================================================================
    const config = {
      fps: 10,
      qrbox: 250,
      aspectRatio: 1.0,
      disableFlip: false
    }

    // ========================================================================
    // PASO 9: INICIAR CÁMARA - Intentar cámara trasera, fallback a cualquier cámara
    // ========================================================================
    console.log('📷 Solicitando acceso a cámara...')
    scannerState.value = 'REQUESTING_CAMERA'

    try {
      // Primero intentar con cámara trasera (móviles)
      await html5QrCode.start(
        { facingMode: 'environment' },
        config,
        onQRCodeSuccess,
        onQRCodeError
      )
      console.log('✅ Cámara trasera iniciada')
    } catch (envError) {
      console.warn('⚠️ Cámara trasera no disponible, intentando cámara frontal...')

      // Fallback: usar cualquier cámara disponible (PC/laptop)
      try {
        await html5QrCode.start(
          { facingMode: 'user' },
          config,
          onQRCodeSuccess,
          onQRCodeError
        )
        console.log('✅ Cámara frontal iniciada')
      } catch (userError) {
        console.warn('⚠️ Cámara frontal no disponible, buscando cualquier cámara...')

        // Último intento: obtener lista de cámaras y usar la primera
        const cameras = await Html5Qrcode.getCameras()
        if (cameras && cameras.length > 0) {
          const cameraId = cameras[0].id
          console.log('📷 Usando cámara:', cameras[0].label || cameraId)

          await html5QrCode.start(
            cameraId,
            config,
            onQRCodeSuccess,
            onQRCodeError
          )
          console.log('✅ Cámara iniciada por ID')
        } else {
          throw new Error('No se encontró ninguna cámara disponible en este dispositivo.')
        }
      }
    }

    // ========================================================================
    // ÉXITO: Cámara activa - Ocultar overlay
    // ========================================================================
    isCameraReady.value = true
    isInitializing.value = false
    scannerState.value = 'SCANNING'
    console.log('✅ Cámara iniciada correctamente - Overlay oculto')

  } catch (err) {
    console.error('❌ Error al iniciar cámara:', err)
    handleError(err)
  }
}

// ============================================================================
// CALLBACKS DE ESCANEO
// ============================================================================

function onQRCodeSuccess(decodedText, decodedResult) {
  console.log('✅ QR detectado:', decodedText)

  // Detener escáner antes de emitir
  detenerCamara()

  emit('scan-success', { decodedText, decodedResult })
}

function onQRCodeError(errorMessage) {
  // Silenciar - son errores normales mientras busca QR
}

// ============================================================================
// MANEJO DE ERRORES
// ============================================================================

function handleError(err) {
  isInitializing.value = false
  isCameraReady.value = false
  scannerState.value = 'ERROR'

  // Mapeo de errores a mensajes amigables
  if (err.name === 'NotAllowedError' || err.message?.includes('Permission denied')) {
    error.value = 'Permiso de cámara denegado'
    errorDetails.value = 'Ve a Configuración del navegador → Permisos → Cámara y permite el acceso a este sitio.'
  } else if (err.name === 'NotFoundError' || err.message?.includes('Requested device not found')) {
    error.value = 'No se encontró la cámara'
    errorDetails.value = 'Verifica que tu dispositivo tenga cámara trasera disponible.'
  } else if (err.name === 'NotReadableError' || err.message?.includes('Could not start video source')) {
    error.value = 'La cámara está ocupada'
    errorDetails.value = 'Cierra otras aplicaciones que estén usando la cámara.'
  } else if (err.message?.includes('HTTPS') || err.message?.includes('secure context')) {
    error.value = 'Se requiere conexión segura (HTTPS)'
    errorDetails.value = `Protocolo actual: ${window.location.protocol}. La cámara solo funciona en HTTPS.`
  } else {
    error.value = 'Error al acceder a la cámara'
    errorDetails.value = `${err.name || 'Error'}: ${err.message}`
  }

  emit('scan-error', { error: error.value, details: errorDetails.value })
}

// ============================================================================
// DETENER CÁMARA Y LIMPIAR
// ============================================================================

async function detenerCamara() {
  console.log('🛑 Deteniendo cámara...')

  if (html5QrCode) {
    try {
      // IMPORTANTE: stop() y luego clear()
      await html5QrCode.stop()
      html5QrCode.clear()
      console.log('✅ Cámara detenida y limpiada')
    } catch (err) {
      console.warn('⚠️ Error al detener cámara:', err.message)
    } finally {
      html5QrCode = null
      isCameraReady.value = false
      scannerState.value = 'STOPPED'
    }
  }
}

// ============================================================================
// REINTENTAR
// ============================================================================

function reintentar() {
  console.log('🔄 Reintentando...')
  error.value = null
  errorDetails.value = null
  iniciarCamara()
}

// ============================================================================
// LIFECYCLE HOOKS
// ============================================================================

onMounted(() => {
  console.log('🎬 [QRScanner v5.0] Componente montado')
  console.log('🌐 URL:', window.location.href)
  console.log('🔒 HTTPS:', window.location.protocol === 'https:')
  console.log('📱 User Agent:', navigator.userAgent)

  // ⚠️ NO INICIAR CÁMARA AQUÍ
  // Los navegadores móviles bloquean getUserMedia sin User Gesture
  console.log('⏸️ Esperando click del usuario para iniciar cámara...')
})

onBeforeUnmount(async () => {
  console.log('🧹 Componente desmontándose - Liberando cámara...')
  await detenerCamara()
})
</script>

<style scoped>
/* ============================================================================
   CONTENEDOR PRINCIPAL - ALTURA FIJA DE 400px (CRÍTICO)
   ============================================================================ */

.qr-scanner-wrapper {
  position: relative;
  width: 100%;
  max-width: 500px;
  height: 400px; /* ALTURA FIJA - Evita que Vuetify colapse a 0px */
  margin: 0 auto;
  background: #000;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

/* ============================================================================
   CAPA 1 (FONDO): LECTOR HTML PURO - SIN VUETIFY
   ============================================================================ */

.qr-reader-element {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: #000;
  z-index: 1;
}

/* Estilos para elementos generados por html5-qrcode */
.qr-reader-element video {
  width: 100% !important;
  height: 100% !important;
  object-fit: cover !important;
  display: block !important;
}

.qr-reader-element canvas {
  position: absolute !important;
  top: 0 !important;
  left: 0 !important;
  width: 100% !important;
  height: 100% !important;
}

.qr-reader-element > div {
  width: 100% !important;
  height: 100% !important;
}

/* ============================================================================
   CAPA 2 (OVERLAY): BOTÓN ACTIVAR CÁMARA
   ============================================================================ */

.overlay-manual {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10; /* Encima del lector */
}

.overlay-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 24px;
  width: 100%;
}

.overlay-error {
  background: rgba(0, 0, 0, 0.85);
  padding: 20px;
}

/* ============================================================================
   BOTÓN ACTIVAR CÁMARA
   ============================================================================ */

.activate-btn {
  text-transform: none !important;
  font-weight: 700 !important;
  font-size: 1.1rem !important;
  letter-spacing: 0.5px;
  padding: 16px 32px !important;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4) !important;
}

.activate-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.5) !important;
}

/* ============================================================================
   ANIMACIÓN PULSE
   ============================================================================ */

.pulse-animation {
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.7;
    transform: scale(1.1);
  }
}

/* ============================================================================
   INDICADOR DE CÁMARA ACTIVA
   ============================================================================ */

.camera-active-indicator {
  position: absolute;
  bottom: 16px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 5;
}

/* ============================================================================
   DEBUG
   ============================================================================ */

.debug-item {
  padding: 8px 0;
  border-bottom: 1px solid #eee;
}

.debug-item:last-child {
  border-bottom: none;
}

/* ============================================================================
   RESPONSIVE - MÓVILES
   ============================================================================ */

@media (max-width: 600px) {
  .qr-scanner-wrapper {
    max-width: 100%;
    height: 350px;
    border-radius: 0;
  }

  .overlay-content {
    padding: 16px;
  }

  .activate-btn {
    font-size: 1rem !important;
    padding: 14px 24px !important;
  }
}

/* ============================================================================
   LANDSCAPE MODE
   ============================================================================ */

@media (max-width: 900px) and (orientation: landscape) {
  .qr-scanner-wrapper {
    height: 280px;
  }

  .overlay-content {
    padding: 12px;
  }

  .activate-btn {
    font-size: 0.9rem !important;
    padding: 12px 20px !important;
  }
}
</style>

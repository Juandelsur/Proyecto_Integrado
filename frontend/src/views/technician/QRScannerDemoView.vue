<!--
  ============================================================================
  QR SCANNER DEMO VIEW - VISTA DE DEMOSTRACIÓN DEL ESCÁNER QR
  ============================================================================

  DESCRIPCIÓN:
  Vista de ejemplo que muestra cómo usar el componente QRScanner.
  Al detectar un código QR, redirige automáticamente a la vista de detalle
  del activo.

  FLUJO:
  1. Usuario abre la vista
  2. Se activa la cámara automáticamente
  3. Usuario apunta al código QR
  4. Al detectar el código, se detiene el escáner
  5. Se busca el activo en el backend
  6. Se redirige a la vista de detalle del activo

  AUTOR: Senior Frontend Developer
  FECHA: 2025-12-01
  ============================================================================
-->

<template>
  <div class="qr-scanner-demo-view">
    <!-- Header -->
    <div class="header">
      <button class="back-button" @click="goBack">
        <span class="back-icon">←</span>
      </button>
      <h1 class="title">Escanear Código QR</h1>
      <div style="width: 48px;"></div> <!-- Spacer -->
    </div>

    <!-- Escáner QR -->
    <div class="scanner-container">
      <QRScanner
        @scan-success="handleScanSuccess"
        @scan-error="handleScanError"
      />
    </div>

    <!-- Instrucciones -->
    <div class="instructions">
      <div class="info-icon">ℹ️</div>
      <p class="mt-2">Apunta la cámara al código QR</p>
      <p class="text-caption">INV-XXXX (Activo) o LOC-XXXX (Ubicación)</p>
    </div>

    <!-- Último código escaneado -->
    <div v-if="lastScannedCode" class="last-scanned">
      <div class="last-scanned-card">
        <div class="card-content">
          <span class="success-icon">✓</span>
          <div>
            <div class="text-caption">Último código escaneado:</div>
            <div class="font-weight-bold">{{ lastScannedCode }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading Overlay -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-content">
        <div class="spinner"></div>
        <p class="mt-4">Buscando activo...</p>
      </div>
    </div>

    <!-- Snackbar para errores -->
    <div v-if="showError" class="snackbar error">
      {{ errorMessage }}
      <button class="snackbar-close" @click="showError = false">✕</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import QRScanner from '@/components/QRScanner.vue'
import apiClient from '@/services/api'

// ============================================================================
// COMPOSABLES
// ============================================================================

const router = useRouter()

// ============================================================================
// STATE
// ============================================================================

const isLoading = ref(false)
const showError = ref(false)
const errorMessage = ref('')
const lastScannedCode = ref(null)

// ============================================================================
// MÉTODOS
// ============================================================================

/**
 * Maneja el evento de escaneo exitoso
 * Soporta dos tipos de códigos:
 * - INV-XXXX: Códigos de activos
 * - LOC-XXXX: Códigos de ubicaciones
 */
async function handleScanSuccess({ decodedText }) {
  console.log('✅ Código QR escaneado:', decodedText)

  lastScannedCode.value = decodedText

  // Evaluar prefijo según formato del backend
  if (decodedText.startsWith('INV-')) {
    await buscarActivo(decodedText)
  } else if (decodedText.startsWith('LOC-')) {
    await buscarUbicacion(decodedText)
  } else {
    showErrorMessage('Código inválido. Debe comenzar con INV- (Activo) o LOC- (Ubicación)')
  }
}

/**
 * Maneja errores del escáner
 */
function handleScanError({ error }) {
  console.error('❌ Error del escáner:', error)
  showErrorMessage(error)
}

/**
 * Busca el activo en el backend por código de inventario
 */
async function buscarActivo(codigo) {
  isLoading.value = true

  try {
    const response = await apiClient.get('/api/activos/', {
      params: { search: codigo }
    })

    const activos = response.data.results || response.data

    if (activos.length === 0) {
      showErrorMessage(`No se encontró el activo con código: ${codigo}`)
      return
    }

    const activo = activos[0]

    // Redirigir a la vista de detalle del activo
    router.push({
      name: 'asset-detail',
      params: { id: activo.id }
    })
  } catch (error) {
    console.error('Error al buscar activo:', error)
    showErrorMessage('Error al buscar el activo. Por favor, intenta de nuevo.')
  } finally {
    isLoading.value = false
  }
}

/**
 * Busca la ubicación en el backend por código QR
 */
async function buscarUbicacion(codigo) {
  isLoading.value = true

  try {
    const response = await apiClient.get('/api/ubicaciones/', {
      params: { search: codigo }
    })

    const ubicaciones = response.data.results || response.data

    if (ubicaciones.length === 0) {
      showErrorMessage(`No se encontró la ubicación con código: ${codigo}`)
      return
    }

    const ubicacion = ubicaciones[0]

    // Redirigir a la vista ScannerView en estado VIEW_LOCATION
    // Pasamos el código de ubicación como query param
    router.push({
      name: 'scan-qr',
      query: { ubicacion: ubicacion.codigo_qr || codigo }
    })
  } catch (error) {
    console.error('Error al buscar ubicación:', error)
    showErrorMessage('Error al buscar la ubicación. Por favor, intenta de nuevo.')
  } finally {
    isLoading.value = false
  }
}

/**
 * Muestra un mensaje de error
 */
function showErrorMessage(message) {
  errorMessage.value = message
  showError.value = true
}

/**
 * Volver a la vista anterior
 */
function goBack() {
  router.back()
}


</script>

<style scoped>
/* ============================================================================
   CONTENEDOR PRINCIPAL
   ============================================================================ */

.qr-scanner-demo-view {
  min-height: 100vh;
  background: #f5f7fa;
  padding-bottom: 80px; /* Espacio para bottom navigation */
}

/* ============================================================================
   HEADER
   ============================================================================ */

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.title {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
}

/* ============================================================================
   ESCÁNER
   ============================================================================ */

.scanner-container {
  padding: 1rem;
}

/* ============================================================================
   INSTRUCCIONES
   ============================================================================ */

.instructions {
  text-align: center;
  padding: 1rem 2rem;
}

.instructions p {
  margin: 0;
}

/* ============================================================================
   ÚLTIMO CÓDIGO ESCANEADO
   ============================================================================ */

.last-scanned {
  padding: 0 1rem;
  margin-top: 1rem;
}

.last-scanned-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background: white;
  padding: 1rem;
}

.card-content {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.success-icon {
  width: 24px;
  height: 24px;
  background: #4caf50;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  flex-shrink: 0;
}

.text-caption {
  font-size: 0.75rem;
  color: #666;
  margin-bottom: 0.25rem;
}

.font-weight-bold {
  font-weight: 700;
}

/* ============================================================================
   BACK BUTTON
   ============================================================================ */

.back-button {
  width: 48px;
  height: 48px;
  background: none;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.3s ease;
  border-radius: 50%;
}

.back-button:hover {
  background: rgba(0, 0, 0, 0.05);
}

.back-icon {
  font-size: 1.5rem;
  color: #424242;
}

/* ============================================================================
   INFO ICON
   ============================================================================ */

.info-icon {
  font-size: 32px;
  margin-bottom: 0.5rem;
}

.mt-2 {
  margin-top: 0.5rem;
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
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.loading-content {
  text-align: center;
}

.loading-content p {
  color: white;
  margin: 0;
}

.mt-4 {
  margin-top: 1rem;
}

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
   SNACKBAR
   ============================================================================ */

.snackbar {
  position: fixed;
  top: 1rem;
  left: 50%;
  transform: translateX(-50%);
  background: #d32f2f;
  color: white;
  padding: 1rem 1.5rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  gap: 1rem;
  z-index: 10000;
  animation: slideDown 0.3s ease;
  max-width: 90%;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateX(-50%) translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
}

.snackbar-close {
  background: none;
  border: none;
  color: white;
  font-size: 1.25rem;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background 0.3s ease;
}

.snackbar-close:hover {
  background: rgba(255, 255, 255, 0.2);
}
</style>



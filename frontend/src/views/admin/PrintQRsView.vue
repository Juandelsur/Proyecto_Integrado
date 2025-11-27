<template>
  <div class="print-qrs-view">
    <!-- Botón Flotante (No se imprime) -->
    <button @click="handlePrint" class="btn-print-floating no-print">
      <i class="bi bi-printer"></i>
      <span>Mandar a Impresora</span>
    </button>

    <!-- Header (No se imprime) -->
    <header class="print-header no-print">
      <button @click="goBack" class="btn-back">
        <i class="bi bi-arrow-left"></i>
        <span>Volver</span>
      </button>
      <h1 class="header-title">Etiquetas QR para Impresión</h1>
      <p class="header-subtitle">{{ activos.length }} activos seleccionados (máx. 12)</p>
    </header>

    <!-- Loading State -->
    <div v-if="isLoading" class="loading-container no-print">
      <div class="spinner"></div>
      <p class="loading-text">Generando códigos QR...</p>
    </div>

    <!-- Grilla de Etiquetas QR (Se imprime) -->
    <div v-else-if="activos.length > 0" class="qr-grid">
      <div
        v-for="activo in activos"
        :key="activo.id"
        class="qr-label"
      >
        <div class="qr-label-content">
          <!-- Nombre del Activo -->
          <h3 class="qr-title">{{ activo.marca }} {{ activo.modelo }}</h3>

          <!-- Imagen QR -->
          <div class="qr-image-container">
            <canvas
              :ref="el => setCanvasRef(activo.id, el)"
              class="qr-canvas"
            ></canvas>
          </div>

          <!-- Código de Texto -->
          <p class="qr-code-text">{{ activo.codigo_inventario }}</p>

          <!-- Información Adicional -->
          <div class="qr-info">
            <p class="qr-info-item">Serie: {{ activo.numero_serie }}</p>
            <p class="qr-info-item">{{ activo.ubicacion_actual?.nombre_ubicacion || 'N/A' }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="empty-state no-print">
      <i class="bi bi-inbox empty-icon"></i>
      <p class="empty-text">No hay activos para imprimir</p>
      <button @click="goBack" class="btn-back-empty">
        <i class="bi bi-arrow-left"></i>
        <span>Volver al Inventario</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import apiClient from '@/services/api'
import QRCode from 'qrcode'

const router = useRouter()
const route = useRoute()

// Estado
const activos = ref([])
const isLoading = ref(true)
const canvasRefs = ref({})

/**
 * Guarda la referencia del canvas para cada activo
 */
function setCanvasRef(activoId, el) {
  if (el) {
    canvasRefs.value[activoId] = el
  }
}

/**
 * Carga los activos desde la API (máximo 12)
 */
async function loadActivos() {
  try {
    isLoading.value = true

    const params = {
      page_size: 12, // Límite de seguridad para no saturar servidor
      ...route.query // Aplicar filtros de la URL
    }

    const response = await apiClient.get('/api/activos/', { params })
    activos.value = Array.isArray(response.data) ? response.data : response.data.results || []

    // Generar QR codes después de cargar los activos
    await generateQRCodes()
  } catch (error) {
    console.error('Error al cargar activos:', error)
    alert('Error al cargar los activos para impresión.')
  } finally {
    isLoading.value = false
  }
}

/**
 * Genera los códigos QR para todos los activos
 */
async function generateQRCodes() {
  // Esperar a que los canvas estén montados en el DOM
  await new Promise(resolve => setTimeout(resolve, 100))

  for (const activo of activos.value) {
    const canvas = canvasRefs.value[activo.id]

    if (canvas) {
      try {
        // Generar QR code con el código de inventario
        await QRCode.toCanvas(canvas, activo.codigo_inventario, {
          width: 200,
          margin: 1,
          color: {
            dark: '#000000',
            light: '#FFFFFF'
          }
        })
      } catch (error) {
        console.error(`Error al generar QR para activo ${activo.id}:`, error)
      }
    }
  }
}

/**
 * Ejecuta la impresión
 */
function handlePrint() {
  window.print()
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
  loadActivos()
})
</script>

<style scoped>
/* ============================================================================
   LAYOUT PRINCIPAL
   ============================================================================ */

.print-qrs-view {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 2rem 1rem;
}

/* ============================================================================
   BOTÓN FLOTANTE
   ============================================================================ */

.btn-print-floating {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%);
  border: none;
  color: white;
  padding: 1rem 2rem;
  border-radius: 50px;
  font-size: 1.1rem;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  box-shadow: 0 8px 24px rgba(13, 71, 161, 0.4);
  transition: all 0.3s ease;
  z-index: 1000;
}

.btn-print-floating:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(13, 71, 161, 0.5);
}

.btn-print-floating i {
  font-size: 1.5rem;
}

/* ============================================================================
   HEADER
   ============================================================================ */

.print-header {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.btn-back {
  background: transparent;
  border: 2px solid #1565c0;
  color: #1565c0;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
  transition: all 0.3s ease;
}

.btn-back:hover {
  background: #1565c0;
  color: white;
}

.header-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #333;
  margin: 0 0 0.5rem 0;
}

.header-subtitle {
  color: #666;
  font-size: 1rem;
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
   GRILLA DE ETIQUETAS QR
   ============================================================================ */

.qr-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
  padding: 1rem 0;
}

.qr-label {
  background: white;
  border: 2px dashed #ccc;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  page-break-inside: avoid;
  break-inside: avoid;
}

.qr-label-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.qr-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #333;
  margin: 0 0 1rem 0;
  word-wrap: break-word;
}

.qr-image-container {
  margin: 0.5rem 0;
}

.qr-canvas {
  display: block;
  max-width: 100%;
  height: auto;
}

.qr-code-text {
  font-size: 1rem;
  font-weight: 700;
  color: #1565c0;
  margin: 0.75rem 0;
  font-family: 'Courier New', monospace;
  letter-spacing: 1px;
}

.qr-info {
  margin-top: 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.qr-info-item {
  font-size: 0.85rem;
  color: #666;
  margin: 0;
}

/* ============================================================================
   EMPTY STATE
   ============================================================================ */

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 1rem;
  gap: 1rem;
}

.empty-icon {
  font-size: 4rem;
  color: #ccc;
}

.empty-text {
  color: #666;
  font-size: 1.1rem;
  font-weight: 600;
}

.btn-back-empty {
  background: #1565c0;
  border: none;
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
}

.btn-back-empty:hover {
  background: #0d47a1;
}

/* ============================================================================
   ESTILOS DE IMPRESIÓN
   ============================================================================ */

@media print {
  /* Ocultar elementos no imprimibles */
  .no-print {
    display: none !important;
  }

  /* Ajustar layout para impresión */
  .print-qrs-view {
    background: white;
    padding: 0;
  }

  /* Grilla de 3 columnas para impresión */
  .qr-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.5cm;
    padding: 1cm;
  }

  /* Etiquetas con tamaño fijo (aprox 8cm x 4cm) */
  .qr-label {
    width: 8cm;
    height: 4cm;
    border: 2px dashed #000;
    border-radius: 0;
    padding: 0.3cm;
    box-shadow: none;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .qr-label-content {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    gap: 0.3cm;
  }

  .qr-title {
    font-size: 0.7rem;
    margin: 0;
    flex: 1;
    text-align: left;
  }

  .qr-image-container {
    margin: 0;
    flex-shrink: 0;
  }

  .qr-canvas {
    width: 2.5cm !important;
    height: 2.5cm !important;
  }

  .qr-code-text {
    font-size: 0.6rem;
    margin: 0;
    writing-mode: vertical-rl;
    text-orientation: mixed;
  }

  .qr-info {
    display: none;
  }
}

/* ============================================================================
   RESPONSIVE
   ============================================================================ */

@media (min-width: 768px) {
  .qr-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (min-width: 1024px) {
  .print-qrs-view {
    padding: 2rem 3rem;
  }
}
</style>

<template>
  <div class="print-qrs-view">
    <!-- Controles (No se imprimen) -->
    <div class="controls no-print">
      <div class="header">
        <h1>🖨️ Impresión de Etiquetas QR</h1>
        <p class="subtitle">Hoja lista para imprimir - Tamaño A4</p>
      </div>

      <div class="actions">
        <button @click="goBack" class="btn-back">
          ← Volver a Lista
        </button>
        <button @click="printPage" class="btn-print">
          🖨️ Imprimir Hoja
        </button>
      </div>

      <div class="info-box">
        <p><strong>📋 Contenido de esta hoja:</strong></p>
        <ul>
          <li>✅ {{ activos.length }} etiquetas de Activos (máximo 12)</li>
          <li>✅ {{ ubicaciones.length }} etiquetas de Ubicaciones (máximo 6)</li>
        </ul>
        <p class="tip">💡 <strong>Tip:</strong> Usa papel adhesivo A4 para mejores resultados</p>
      </div>
    </div>

    <!-- Contenido Imprimible -->
    <div class="printable-content">
      <!-- SECCIÓN: ACTIVOS -->
      <div v-if="activos.length > 0" class="section">
        <h2 class="section-title">📦 ACTIVOS</h2>
        <div class="qr-grid">
          <div
            v-for="activo in activos"
            :key="activo.id_activo"
            class="qr-card qr-card-activo"
          >
            <div class="qr-image">
              <img
                v-if="activo.qr_url"
                :src="activo.qr_url"
                :alt="`QR Activo ${activo.id_activo}`"
              />
              <div v-else class="qr-placeholder">
                <p>QR no disponible</p>
              </div>
            </div>
            <div class="qr-info">
              <p class="qr-title">{{ activo.marca }} {{ activo.modelo }}</p>
              <p class="qr-subtitle">Serie: {{ activo.numero_serie }}</p>
              <p class="qr-id">ID: {{ activo.id_activo }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- SECCIÓN: UBICACIONES -->
      <div v-if="ubicaciones.length > 0" class="section">
        <h2 class="section-title">📍 UBICACIONES</h2>
        <div class="qr-grid">
          <div
            v-for="ubicacion in ubicaciones"
            :key="ubicacion.id_ubicacion"
            class="qr-card qr-card-ubicacion"
          >
            <div class="qr-image">
              <img
                v-if="ubicacion.qr_url"
                :src="ubicacion.qr_url"
                :alt="`QR Ubicación ${ubicacion.id_ubicacion}`"
              />
              <div v-else class="qr-placeholder">
                <p>QR no disponible</p>
              </div>
            </div>
            <div class="qr-info">
              <p class="qr-title">{{ ubicacion.nombre_ubicacion }}</p>
              <p class="qr-subtitle">{{ ubicacion.departamento?.nombre_departamento || 'Sin departamento' }}</p>
              <p class="qr-id">ID: {{ ubicacion.id_ubicacion }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="loading">
        <p>⏳ Cargando etiquetas QR...</p>
      </div>

      <!-- Sin datos -->
      <div v-if="!loading && activos.length === 0 && ubicaciones.length === 0" class="no-data">
        <p>📭 No hay etiquetas para imprimir.</p>
        <button @click="goBack" class="btn-back">← Volver</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import activosService from '@/services/activosService'
import ubicacionesService from '@/services/ubicacionesService'

// ============================================================================
// COMPOSABLES
// ============================================================================

const router = useRouter()
const route = useRoute()

// ============================================================================
// STATE
// ============================================================================

const activos = ref([])
const ubicaciones = ref([])
const loading = ref(false)

// ============================================================================
// METHODS
// ============================================================================

/**
 * Carga los activos filtrados desde la URL
 * Límite: 12 activos para no sobrecargar el servidor
 */
async function loadActivos() {
  try {
    const params = {
      page_size: 12, // Límite de seguridad
      ...route.query // Aplicar filtros de la URL
    }

    const response = await activosService.getAll(params)
    activos.value = response.results || response
  } catch (error) {
    console.error('Error al cargar activos:', error)
    alert('Error al cargar los activos para impresión.')
  }
}

/**
 * Carga las primeras 6 ubicaciones
 * Para tener variedad en la hoja de impresión
 */
async function loadUbicaciones() {
  try {
    const params = {
      page_size: 6
    }

    const response = await ubicacionesService.getAll(params)
    ubicaciones.value = response.results || response
  } catch (error) {
    console.error('Error al cargar ubicaciones:', error)
  }
}

/**
 * Carga todos los datos necesarios
 */
async function loadData() {
  loading.value = true
  try {
    await Promise.all([
      loadActivos(),
      loadUbicaciones()
    ])
  } finally {
    loading.value = false
  }
}

/**
 * Vuelve a la lista de activos
 */
function goBack() {
  router.push({ name: 'asset-list' })
}

/**
 * Abre el diálogo de impresión del navegador
 */
function printPage() {
  window.print()
}

// ============================================================================
// LIFECYCLE
// ============================================================================

onMounted(() => {
  loadData()
})
</script>

<style scoped>
/* ============================================================================
   ESTILOS GENERALES
   ============================================================================ */

.print-qrs-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

/* ============================================================================
   CONTROLES (No se imprimen)
   ============================================================================ */

.controls {
  margin-bottom: 2rem;
}

.header h1 {
  font-size: 2rem;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #7f8c8d;
  font-size: 1rem;
}

.actions {
  display: flex;
  gap: 1rem;
  margin: 1.5rem 0;
}

.btn-back {
  padding: 0.75rem 1.5rem;
  background: #95a5a6;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-back:hover {
  background: #7f8c8d;
}

.btn-print {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn-print:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.info-box {
  background: #e8f4f8;
  border-left: 4px solid #3498db;
  padding: 1rem 1.5rem;
  border-radius: 8px;
  margin-top: 1rem;
}

.info-box ul {
  margin: 0.5rem 0;
  padding-left: 1.5rem;
}

.info-box li {
  margin: 0.25rem 0;
}

.tip {
  margin-top: 0.75rem;
  color: #2c3e50;
}

/* ============================================================================
   CONTENIDO IMPRIMIBLE
   ============================================================================ */

.printable-content {
  background: white;
}

.section {
  margin-bottom: 3rem;
  page-break-inside: avoid;
}

.section-title {
  font-size: 1.5rem;
  color: #2c3e50;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 3px solid #3498db;
}

/* ============================================================================
   GRILLA DE QRS (3 columnas)
   ============================================================================ */

.qr-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.qr-card {
  border: 2px dashed #000;
  border-radius: 12px;
  padding: 1rem;
  text-align: center;
  background: white;
  page-break-inside: avoid;
  transition: transform 0.2s, box-shadow 0.2s;
}

.qr-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* Borde NEGRO para Activos */
.qr-card-activo {
  border-color: #000;
  border-width: 2px;
}

/* Borde AZUL para Ubicaciones */
.qr-card-ubicacion {
  border-color: #3498db;
  border-width: 2px;
}

.qr-image {
  width: 100%;
  height: 180px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.75rem;
}

.qr-image img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.qr-placeholder {
  width: 100%;
  height: 100%;
  background: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
}

.qr-placeholder p {
  color: #95a5a6;
  font-size: 0.9rem;
}

.qr-info {
  border-top: 1px solid #e0e0e0;
  padding-top: 0.75rem;
}

.qr-title {
  font-weight: 700;
  font-size: 1rem;
  color: #2c3e50;
  margin-bottom: 0.25rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.qr-subtitle {
  font-size: 0.85rem;
  color: #7f8c8d;
  margin-bottom: 0.25rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.qr-id {
  font-size: 0.8rem;
  color: #95a5a6;
  font-weight: 600;
}

/* ============================================================================
   ESTADOS DE CARGA
   ============================================================================ */

.loading,
.no-data {
  padding: 3rem;
  text-align: center;
  color: #7f8c8d;
  font-size: 1.1rem;
}

/* ============================================================================
   ESTILOS DE IMPRESIÓN - ETIQUETAS PROFESIONALES TIPO PLACA DE INVENTARIO
   ============================================================================ */

@media print {
  /* ========================================================================
     CONFIGURACIÓN DE PÁGINA
     ======================================================================== */

  /* Ocultar controles al imprimir */
  .no-print {
    display: none !important;
  }

  /* Configuración de página A4 */
  @page {
    size: A4 portrait;
    margin: 1cm 0.5cm;
  }

  /* Ajustar contenedor principal */
  .print-qrs-view {
    max-width: 100%;
    padding: 0;
    margin: 0;
  }

  /* ========================================================================
     TÍTULOS DE SECCIÓN
     ======================================================================== */

  .section {
    page-break-inside: avoid;
    margin-bottom: 0.5cm;
  }

  .section-title {
    font-size: 14pt;
    font-weight: bold;
    color: #000;
    margin-bottom: 0.3cm;
    padding-bottom: 0.2cm;
    border-bottom: 2px solid #000;
    page-break-after: avoid;
  }

  /* ========================================================================
     GRILLA DE ETIQUETAS - 2 COLUMNAS PARA ETIQUETAS HORIZONTALES
     ======================================================================== */

  .qr-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.4cm;
    margin-bottom: 0.5cm;
  }

  /* ========================================================================
     TARJETA DE ETIQUETA - DISEÑO HORIZONTAL TIPO PLACA DE INVENTARIO
     ======================================================================== */

  .qr-card {
    /* Tamaño físico de la etiqueta */
    width: 8cm;
    height: 5cm;

    /* Espaciado interno */
    padding: 0.5cm;

    /* Borde punteado fino para recortar */
    border: 1px dashed #333 !important;
    border-radius: 0 !important;

    /* Evitar que se corte entre páginas */
    page-break-inside: avoid;
    break-inside: avoid;

    /* Layout horizontal: QR a la izquierda, texto a la derecha */
    display: flex !important;
    flex-direction: row !important;
    align-items: center !important;
    justify-content: flex-start !important;
    gap: 0.4cm;

    /* Fondo blanco */
    background: white !important;

    /* Sin sombras en impresión */
    box-shadow: none !important;
  }

  /* Bordes diferenciados por tipo */
  .qr-card-activo {
    border: 1px dashed #000 !important;
  }

  .qr-card-ubicacion {
    border: 1px dashed #3498db !important;
  }

  /* ========================================================================
     IMAGEN QR - TAMAÑO EXACTO PARA ESCANEO ÓPTIMO
     ======================================================================== */

  .qr-image {
    /* Tamaño fijo del QR */
    width: 2.8cm !important;
    height: 2.8cm !important;
    min-width: 2.8cm !important;
    min-height: 2.8cm !important;

    /* Centrar la imagen */
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;

    /* Margen blanco alrededor del QR */
    padding: 0.1cm;
    background: white;

    /* Sin bordes ni márgenes adicionales */
    margin: 0 !important;
    border: none !important;
  }

  .qr-image img {
    /* Tamaño exacto de la imagen QR */
    width: 2.6cm !important;
    height: 2.6cm !important;
    max-width: 2.6cm !important;
    max-height: 2.6cm !important;

    /* Asegurar que se imprima correctamente */
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
    color-adjust: exact !important;

    /* Sin filtros ni transformaciones */
    object-fit: contain !important;
  }

  .qr-placeholder {
    width: 2.8cm !important;
    height: 2.8cm !important;
    background: #f0f0f0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 8pt !important;
    color: #999 !important;
  }

  /* ========================================================================
     INFORMACIÓN DE TEXTO - LADO DERECHO DE LA ETIQUETA
     ======================================================================== */

  .qr-info {
    /* Ocupa el espacio restante */
    flex: 1;

    /* Layout vertical */
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    align-items: flex-start !important;

    /* Sin bordes ni padding extra */
    border: none !important;
    padding: 0 !important;
    margin: 0 !important;

    /* Espaciado entre líneas */
    gap: 0.15cm;
  }

  /* Nombre del Activo - Visible pero compacto */
  .qr-title {
    font-size: 10pt !important;
    font-weight: bold !important;
    color: #000 !important;
    line-height: 1.2 !important;
    margin: 0 !important;
    padding: 0 !important;

    /* Permitir hasta 2 líneas */
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    display: -webkit-box !important;
    -webkit-line-clamp: 2 !important;
    -webkit-box-orient: vertical !important;
    white-space: normal !important;
    word-break: break-word !important;
  }

  /* Subtítulo (Serie o Departamento) */
  .qr-subtitle {
    font-size: 8pt !important;
    color: #333 !important;
    line-height: 1.2 !important;
    margin: 0 !important;
    padding: 0 !important;

    /* Una sola línea */
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    white-space: nowrap !important;
  }

  /* Código de Inventario - MUY LEGIBLE */
  .qr-id {
    font-size: 12pt !important;
    font-weight: bold !important;
    font-family: 'Courier New', Consolas, monospace !important;
    color: #000 !important;
    line-height: 1.2 !important;
    margin: 0 !important;
    padding: 0.1cm 0.2cm !important;

    /* Fondo gris claro para destacar */
    background: #f0f0f0 !important;
    border: 1px solid #ccc !important;
    border-radius: 2px !important;

    /* Texto centrado */
    text-align: center !important;
    letter-spacing: 0.5px !important;
  }

  /* ========================================================================
     OPTIMIZACIONES ADICIONALES
     ======================================================================== */

  /* Asegurar que los colores se impriman correctamente */
  * {
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
    color-adjust: exact !important;
  }

  /* Evitar saltos de página no deseados */
  h1, h2, h3, h4, h5, h6 {
    page-break-after: avoid !important;
  }

  /* Optimizar espaciado entre secciones */
  .section + .section {
    margin-top: 0.5cm;
  }
}

/* ============================================================================
   RESPONSIVE (Pantallas pequeñas)
   ============================================================================ */

@media (max-width: 768px) {
  .qr-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }

  .actions {
    flex-direction: column;
  }

  .btn-back,
  .btn-print {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .qr-grid {
    grid-template-columns: 1fr;
  }
}
</style>


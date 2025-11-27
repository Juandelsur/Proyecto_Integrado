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
   ESTILOS DE IMPRESIÓN
   ============================================================================ */

@media print {
  /* Ocultar controles al imprimir */
  .no-print {
    display: none !important;
  }

  /* Configuración de página */
  @page {
    size: A4;
    margin: 1cm;
  }

  /* Ajustar contenedor */
  .print-qrs-view {
    max-width: 100%;
    padding: 0;
  }

  /* Asegurar que las tarjetas no se corten */
  .qr-card {
    page-break-inside: avoid;
    break-inside: avoid;
  }

  /* Ajustar grilla para impresión */
  .qr-grid {
    gap: 1rem;
  }

  /* Mantener bordes visibles */
  .qr-card-activo {
    border: 2px dashed #000 !important;
  }

  .qr-card-ubicacion {
    border: 2px dashed #3498db !important;
  }

  /* Asegurar que las imágenes se impriman */
  .qr-image img {
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  /* Evitar saltos de página en secciones */
  .section {
    page-break-inside: avoid;
  }

  /* Títulos de sección */
  .section-title {
    page-break-after: avoid;
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


<template>
  <div class="asset-list-view">
    <!-- Encabezado -->
    <div class="header">
      <h1>📦 Gestión de Activos</h1>
      <p class="subtitle">Sistema de Control de Activos - Hospital</p>
    </div>

    <!-- Barra de herramientas -->
    <div class="toolbar">
      <!-- Búsqueda -->
      <div class="search-box">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="🔍 Buscar por marca, modelo, serie..."
          class="search-input"
          @input="handleSearch"
        />
      </div>

      <!-- Filtros -->
      <div class="filters">
        <select v-model="filterEstado" @change="applyFilters" class="filter-select">
          <option value="">Todos los estados</option>
          <option value="1">Operativo</option>
          <option value="2">En Mantenimiento</option>
          <option value="3">Fuera de Servicio</option>
        </select>

        <select v-model="filterTipo" @change="applyFilters" class="filter-select">
          <option value="">Todos los tipos</option>
          <option value="1">Equipo Médico</option>
          <option value="2">Mobiliario</option>
          <option value="3">Tecnología</option>
        </select>
      </div>

      <!-- Botón de Impresión (Solo Admin y Técnico) -->
      <button
        v-if="canPrintLabels"
        @click="goToPrintView"
        class="btn-print"
        title="Imprimir etiquetas QR de los activos filtrados"
      >
        🖨️ Imprimir Etiquetas
      </button>

      <!-- Botón de Crear (Solo Admin y Técnico) -->
      <button
        v-if="canEditAssets"
        @click="goToCreate"
        class="btn-create"
      >
        ➕ Nuevo Activo
      </button>
    </div>

    <!-- Tabla de Activos -->
    <div class="table-container">
      <table v-if="!loading && activos.length > 0" class="assets-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Marca</th>
            <th>Modelo</th>
            <th>Serie</th>
            <th>Estado</th>
            <th>Ubicación</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="activo in activos" :key="activo.id_activo">
            <td>{{ activo.id_activo }}</td>
            <td>{{ activo.marca }}</td>
            <td>{{ activo.modelo }}</td>
            <td>{{ activo.numero_serie }}</td>
            <td>
              <span :class="['badge', `badge-${getEstadoClass(activo.estado)}`]">
                {{ activo.estado?.nombre_estado || 'N/A' }}
              </span>
            </td>
            <td>{{ activo.ubicacion_actual?.nombre_ubicacion || 'Sin ubicación' }}</td>
            <td class="actions">
              <button @click="viewDetail(activo.id_activo)" class="btn-action btn-view">
                👁️ Ver
              </button>
              <button
                v-if="canEditAssets"
                @click="editAsset(activo.id_activo)"
                class="btn-action btn-edit"
              >
                ✏️ Editar
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Loading -->
      <div v-if="loading" class="loading">
        <p>⏳ Cargando activos...</p>
      </div>

      <!-- Sin resultados -->
      <div v-if="!loading && activos.length === 0" class="no-results">
        <p>📭 No se encontraron activos con los filtros aplicados.</p>
      </div>
    </div>

    <!-- Paginación -->
    <div v-if="totalPages > 1" class="pagination">
      <button
        @click="previousPage"
        :disabled="currentPage === 1"
        class="btn-page"
      >
        ← Anterior
      </button>
      <span class="page-info">Página {{ currentPage }} de {{ totalPages }}</span>
      <button
        @click="nextPage"
        :disabled="currentPage === totalPages"
        class="btn-page"
      >
        Siguiente →
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import activosService from '@/services/activosService'

// ============================================================================
// COMPOSABLES
// ============================================================================

const router = useRouter()
const authStore = useAuthStore()

// ============================================================================
// STATE
// ============================================================================

const activos = ref([])
const loading = ref(false)
const searchQuery = ref('')
const filterEstado = ref('')
const filterTipo = ref('')
const currentPage = ref(1)
const totalPages = ref(1)
const pageSize = ref(20)

// ============================================================================
// COMPUTED (Permisos)
// ============================================================================

const canPrintLabels = computed(() => authStore.canPrintLabels)
const canEditAssets = computed(() => authStore.canEditAssets)

// ============================================================================
// METHODS
// ============================================================================

/**
 * Carga los activos desde la API
 */
async function loadActivos() {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value
    }

    // Aplicar filtros
    if (searchQuery.value) {
      params.search = searchQuery.value
    }
    if (filterEstado.value) {
      params.estado = filterEstado.value
    }
    if (filterTipo.value) {
      params.tipo = filterTipo.value
    }

    const response = await activosService.getAll(params)
    activos.value = response.results || response

    // Calcular paginación
    if (response.count) {
      totalPages.value = Math.ceil(response.count / pageSize.value)
    }
  } catch (error) {
    console.error('Error al cargar activos:', error)
    alert('Error al cargar los activos. Por favor, intenta de nuevo.')
  } finally {
    loading.value = false
  }
}

/**
 * Maneja la búsqueda con debounce
 */
let searchTimeout = null
function handleSearch() {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    currentPage.value = 1
    loadActivos()
  }, 500)
}

/**
 * Aplica los filtros seleccionados
 */
function applyFilters() {
  currentPage.value = 1
  loadActivos()
}

/**
 * Navega a la vista de impresión con los filtros actuales
 */
function goToPrintView() {
  const query = {}

  if (searchQuery.value) query.search = searchQuery.value
  if (filterEstado.value) query.estado = filterEstado.value
  if (filterTipo.value) query.tipo = filterTipo.value

  router.push({
    name: 'print-qrs',
    query
  })
}

/**
 * Navega a la vista de creación de activo
 */
function goToCreate() {
  router.push({ name: 'asset-create' })
}

/**
 * Navega al detalle del activo
 */
function viewDetail(id) {
  router.push({ name: 'asset-detail', params: { id } })
}

/**
 * Navega a la edición del activo
 */
function editAsset(id) {
  router.push({ name: 'asset-edit', params: { id } })
}

/**
 * Obtiene la clase CSS según el estado
 */
function getEstadoClass(estado) {
  const estadoNombre = estado?.nombre_estado?.toLowerCase() || ''
  if (estadoNombre.includes('operativo')) return 'success'
  if (estadoNombre.includes('mantenimiento')) return 'warning'
  if (estadoNombre.includes('fuera')) return 'danger'
  return 'default'
}

/**
 * Paginación: Página anterior
 */
function previousPage() {
  if (currentPage.value > 1) {
    currentPage.value--
    loadActivos()
  }
}

/**
 * Paginación: Página siguiente
 */
function nextPage() {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
    loadActivos()
  }
}

// ============================================================================
// LIFECYCLE
// ============================================================================

onMounted(() => {
  loadActivos()
})
</script>

<style scoped>
.asset-list-view {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

.header {
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

.toolbar {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  align-items: center;
}

.search-box {
  flex: 1;
  min-width: 300px;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.search-input:focus {
  outline: none;
  border-color: #3498db;
}

.filters {
  display: flex;
  gap: 0.5rem;
}

.filter-select {
  padding: 0.75rem 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 0.95rem;
  background: white;
  cursor: pointer;
  transition: border-color 0.3s;
}

.filter-select:focus {
  outline: none;
  border-color: #3498db;
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

.btn-create {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn-create:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(17, 153, 142, 0.4);
}

.table-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.assets-table {
  width: 100%;
  border-collapse: collapse;
}

.assets-table thead {
  background: #f8f9fa;
}

.assets-table th {
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #2c3e50;
  border-bottom: 2px solid #e0e0e0;
}

.assets-table td {
  padding: 1rem;
  border-bottom: 1px solid #f0f0f0;
}

.assets-table tbody tr:hover {
  background: #f8f9fa;
}

.badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 600;
}

.badge-success {
  background: #d4edda;
  color: #155724;
}

.badge-warning {
  background: #fff3cd;
  color: #856404;
}

.badge-danger {
  background: #f8d7da;
  color: #721c24;
}

.badge-default {
  background: #e9ecef;
  color: #495057;
}

.actions {
  display: flex;
  gap: 0.5rem;
}

.btn-action {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: transform 0.2s;
}

.btn-action:hover {
  transform: scale(1.05);
}

.btn-view {
  background: #3498db;
  color: white;
}

.btn-edit {
  background: #f39c12;
  color: white;
}

.loading,
.no-results {
  padding: 3rem;
  text-align: center;
  color: #7f8c8d;
  font-size: 1.1rem;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
}

.btn-page {
  padding: 0.5rem 1rem;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-page:hover:not(:disabled) {
  background: #2980b9;
}

.btn-page:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
}

.page-info {
  font-weight: 600;
  color: #2c3e50;
}
</style>


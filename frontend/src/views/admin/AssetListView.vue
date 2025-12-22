<template>
  <div class="asset-list-view">
    <!-- Header -->
    <header class="list-header">
      <h1 class="header-title">Inventario</h1>
      <button @click="toggleFilters" class="btn-filters-mobile">
        <i class="bi bi-funnel"></i>
        <span>Filtros</span>
      </button>
    </header>

    <!-- Barra de Herramientas -->
    <div class="toolbar">
      <!-- Búsqueda -->
      <div class="search-container">
        <i class="bi bi-search search-icon"></i>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Buscar por código, marca, modelo..."
          class="search-input"
          @input="handleSearch"
        />
      </div>

      <!-- Botón Imprimir Etiquetas (Solo Admin/Técnico) -->
      <button
        v-if="authStore.canPrintLabels"
        @click="goToPrintView"
        class="btn-print"
      >
        <i class="bi bi-printer"></i>
        <span>Imprimir Etiquetas</span>
      </button>
    </div>

    <!-- Panel de Filtros (Móvil) -->
    <div v-if="showFilters" class="filters-panel">
      <div class="filter-group">
        <label for="filter-tipo" class="filter-label">Tipo de Equipo</label>
        <select id="filter-tipo" v-model="filters.tipo" class="filter-select">
          <option value="">Todos</option>
          <option v-for="tipo in tiposEquipo" :key="tipo.id" :value="tipo.id">
            {{ tipo.nombre_tipo }}
          </option>
        </select>
      </div>

      <div class="filter-group">
        <label for="filter-estado" class="filter-label">Estado</label>
        <select id="filter-estado" v-model="filters.estado" class="filter-select">
          <option value="">Todos</option>
          <option v-for="estado in estados" :key="estado.id" :value="estado.id">
            {{ estado.nombre_estado }}
          </option>
        </select>
      </div>

      <div class="filter-actions">
        <button @click="applyFilters" class="btn-apply">Aplicar</button>
        <button @click="clearFilters" class="btn-clear">Limpiar</button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="loading-container">
      <div class="spinner"></div>
      <p class="loading-text">Cargando activos...</p>
    </div>

    <!-- Lista/Tabla de Activos -->
    <div v-else-if="activos.length > 0" class="assets-container">
      <!-- Vista Móvil: Lista de Tarjetas -->
      <div class="assets-list-mobile">
        <div
          v-for="activo in activos"
          :key="activo.id"
          @click="goToDetail(activo.id)"
          class="asset-card-mobile"
        >
          <div class="card-header">
            <h3 class="card-title">{{ activo.marca }} {{ activo.modelo }}</h3>
            <span class="badge" :class="getEstadoClass(activo.estado?.nombre_estado)">
              {{ activo.estado?.nombre_estado || 'N/A' }}
            </span>
          </div>
          <div class="card-body">
            <p class="card-info">
              <i class="bi bi-upc-scan"></i>
              <span>{{ activo.codigo_inventario }}</span>
            </p>
            <p class="card-info">
              <i class="bi bi-geo-alt"></i>
              <span>{{ activo.ubicacion_actual?.nombre_ubicacion || 'N/A' }}</span>
            </p>
          </div>
        </div>
      </div>

      <!-- Vista Desktop: Tabla -->
      <div class="assets-table-desktop">
        <table class="assets-table">
          <thead>
            <tr>
              <th>Código</th>
              <th>Tipo</th>
              <th>Marca/Modelo</th>
              <th>Serie</th>
              <th>Estado</th>
              <th>Ubicación</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="activo in activos"
              :key="activo.id"
              @click="goToDetail(activo.id)"
              class="table-row"
            >
              <td class="td-codigo">{{ activo.codigo_inventario }}</td>
              <td>{{ activo.tipo?.nombre_tipo || 'N/A' }}</td>
              <td>{{ activo.marca }} {{ activo.modelo }}</td>
              <td>{{ activo.numero_serie }}</td>
              <td>
                <span class="badge" :class="getEstadoClass(activo.estado?.nombre_estado)">
                  {{ activo.estado?.nombre_estado || 'N/A' }}
                </span>
              </td>
              <td>{{ activo.ubicacion_actual?.nombre_ubicacion || 'N/A' }}</td>
              <td class="td-actions">
                <button
                  @click.stop="goToDetail(activo.id)"
                  class="btn-action"
                  title="Ver Detalle"
                >
                  <i class="bi bi-eye"></i>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="empty-state">
      <i class="bi bi-inbox empty-icon"></i>
      <p class="empty-text">No se encontraron activos</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import apiClient from '@/services/api'

const router = useRouter()
const authStore = useAuthStore()

// Estado
const activos = ref([])
const tiposEquipo = ref([])
const estados = ref([])
const searchQuery = ref('')
const showFilters = ref(false)
const isLoading = ref(true)
const filters = ref({
  tipo: '',
  estado: ''
})

/**
 * Carga los activos desde la API
 */
async function loadActivos() {
  try {
    isLoading.value = true
    const response = await apiClient.get('/api/activos/')
    activos.value = Array.isArray(response.data) ? response.data : response.data.results || []
  } catch (error) {
    console.error('Error al cargar activos:', error)
    alert('Error al cargar los activos')
  } finally {
    isLoading.value = false
  }
}

/**
 * Carga los tipos de equipo para los filtros
 */
async function loadTiposEquipo() {
  try {
    const response = await apiClient.get('/api/tipos-equipo/')
    tiposEquipo.value = Array.isArray(response.data) ? response.data : response.data.results || []
  } catch (error) {
    console.error('Error al cargar tipos de equipo:', error)
  }
}

/**
 * Carga los estados para los filtros
 */
async function loadEstados() {
  try {
    const response = await apiClient.get('/api/estados-activo/')
    estados.value = Array.isArray(response.data) ? response.data : response.data.results || []
  } catch (error) {
    console.error('Error al cargar estados:', error)
  }
}

/**
 * Maneja la búsqueda en tiempo real
 */
function handleSearch() {
  // Filtrar activos localmente por ahora
  // TODO: Implementar búsqueda en el backend
}

/**
 * Alterna la visibilidad del panel de filtros
 */
function toggleFilters() {
  showFilters.value = !showFilters.value
}

/**
 * Aplica los filtros seleccionados
 */
function applyFilters() {
  // TODO: Implementar filtrado en el backend
  showFilters.value = false
}

/**
 * Limpia todos los filtros
 */
function clearFilters() {
  filters.value = {
    tipo: '',
    estado: ''
  }
  searchQuery.value = ''
  loadActivos()
}

/**
 * Navega a la vista de impresión con los filtros actuales
 */
function goToPrintView() {
  router.push({
    name: 'print-qrs',
    query: {
      search: searchQuery.value,
      tipo: filters.value.tipo,
      estado: filters.value.estado
    }
  })
}

/**
 * Navega al detalle del activo
 */
function goToDetail(id) {
  router.push({ name: 'asset-detail', params: { id } })
}

/**
 * Retorna la clase CSS según el estado del activo
 */
function getEstadoClass(estado) {
  if (!estado) return 'badge-default'

  const estadoLower = estado.toLowerCase()

  if (estadoLower.includes('activo') || estadoLower.includes('operativo')) {
    return 'badge-success'
  } else if (estadoLower.includes('mantenimiento') || estadoLower.includes('mantención')) {
    return 'badge-warning'
  } else if (estadoLower.includes('baja') || estadoLower.includes('inactivo')) {
    return 'badge-danger'
  }

  return 'badge-default'
}

/**
 * Inicialización
 */
onMounted(async () => {
  await Promise.all([
    loadActivos(),
    loadTiposEquipo(),
    loadEstados()
  ])
})
</script>


<style scoped>
/* ============================================================================
   LAYOUT PRINCIPAL
   ============================================================================ */

.asset-list-view {
  min-height: 100vh;
  background: #f5f7fa;
  padding-bottom: 2rem;
}

/* ============================================================================
   HEADER
   ============================================================================ */

.list-header {
  background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%);
  color: white;
  padding: 1.5rem 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.header-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
}

.btn-filters-mobile {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
}

.btn-filters-mobile:hover {
  background: rgba(255, 255, 255, 0.3);
}

/* ============================================================================
   TOOLBAR
   ============================================================================ */

.toolbar {
  background: white;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.search-container {
  position: relative;
  flex: 1;
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #666;
  font-size: 1.1rem;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 3rem;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: #1565c0;
  box-shadow: 0 0 0 3px rgba(21, 101, 192, 0.1);
}

.btn-print {
  background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%);
  border: none;
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(13, 71, 161, 0.3);
}

.btn-print:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(13, 71, 161, 0.4);
}

.btn-print i {
  font-size: 1.25rem;
}

/* ============================================================================
   PANEL DE FILTROS
   ============================================================================ */

.filters-panel {
  background: white;
  padding: 1rem;
  margin: 0 1rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-top: 1rem;
}

.filter-group {
  margin-bottom: 1rem;
}

.filter-label {
  display: block;
  font-weight: 600;
  color: #333;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.filter-select {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  background: white;
  cursor: pointer;
}

.filter-actions {
  display: flex;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

.btn-apply,
.btn-clear {
  flex: 1;
  padding: 0.75rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-apply {
  background: #1565c0;
  border: none;
  color: white;
}

.btn-apply:hover {
  background: #0d47a1;
}

.btn-clear {
  background: white;
  border: 2px solid #e0e0e0;
  color: #666;
}

.btn-clear:hover {
  background: #f5f7fa;
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
   LISTA MÓVIL (TARJETAS)
   ============================================================================ */

.assets-container {
  padding: 1rem;
}

.assets-list-mobile {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.asset-card-mobile {
  background: white;
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.3s ease;
}

.asset-card-mobile:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.75rem;
  gap: 0.5rem;
}

.card-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #333;
  margin: 0;
  flex: 1;
}

.card-body {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.card-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #666;
  font-size: 0.9rem;
  margin: 0;
}

.card-info i {
  color: #1565c0;
  font-size: 1rem;
}

/* ============================================================================
   TABLA DESKTOP
   ============================================================================ */

.assets-table-desktop {
  display: none;
}

.assets-table {
  width: 100%;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.assets-table thead {
  background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%);
  color: white;
}

.assets-table th {
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.assets-table tbody tr {
  border-bottom: 1px solid #e0e0e0;
  cursor: pointer;
  transition: all 0.2s ease;
}

.assets-table tbody tr:hover {
  background: #f5f7fa;
}

.assets-table td {
  padding: 1rem;
  color: #333;
  font-size: 0.95rem;
}

.td-codigo {
  font-weight: 600;
  color: #1565c0;
}

.td-actions {
  text-align: center;
}

.btn-action {
  background: #1565c0;
  border: none;
  color: white;
  padding: 0.5rem 0.75rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-action:hover {
  background: #0d47a1;
  transform: scale(1.1);
}

/* ============================================================================
   BADGES DE ESTADO
   ============================================================================ */

.badge {
  display: inline-block;
  padding: 0.35rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
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
  background: #e0e0e0;
  color: #666;
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

/* ============================================================================
   RESPONSIVE
   ============================================================================ */

@media (min-width: 768px) {
  .list-header {
    padding: 2rem;
  }

  .header-title {
    font-size: 2rem;
  }

  .btn-filters-mobile {
    display: none;
  }

  .toolbar {
    flex-direction: row;
    padding: 1.5rem;
  }

  .filters-panel {
    display: flex;
    gap: 1rem;
    align-items: flex-end;
    margin: 1rem;
  }

  .filter-group {
    flex: 1;
    margin-bottom: 0;
  }

  .filter-actions {
    margin-top: 0;
    gap: 0.5rem;
  }

  .btn-apply,
  .btn-clear {
    flex: initial;
    padding: 0.75rem 1.5rem;
  }

  .assets-list-mobile {
    display: none;
  }

  .assets-table-desktop {
    display: block;
  }
}

@media (min-width: 1024px) {
  .assets-container {
    padding: 2rem;
  }
}
</style>


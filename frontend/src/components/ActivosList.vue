<script setup>
import { onMounted } from 'vue'
import { useActivosStore } from '@/stores/activos'

// Usar el store de activos
const activosStore = useActivosStore()

// Cargar activos al montar el componente
onMounted(async () => {
  await activosStore.fetchActivos()
})

// Función para cargar página siguiente
const loadNextPage = async () => {
  if (activosStore.hasNextPage) {
    await activosStore.fetchActivos({ page: activosStore.pagination.currentPage + 1 })
  }
}

// Función para cargar página anterior
const loadPreviousPage = async () => {
  if (activosStore.hasPreviousPage) {
    await activosStore.fetchActivos({ page: activosStore.pagination.currentPage - 1 })
  }
}
</script>

<template>
  <div class="activos-list">
    <h2>Lista de Activos</h2>
    
    <!-- Indicador de carga -->
    <div v-if="activosStore.loading" class="loading">
      Cargando activos...
    </div>
    
    <!-- Mensaje de error -->
    <div v-if="activosStore.error" class="error">
      {{ activosStore.error }}
    </div>
    
    <!-- Lista de activos -->
    <div v-if="!activosStore.loading && activosStore.activos.length > 0" class="activos-grid">
      <div 
        v-for="activo in activosStore.activos" 
        :key="activo.id" 
        class="activo-card"
      >
        <h3>{{ activo.codigo_inventario }}</h3>
        <p><strong>Marca:</strong> {{ activo.marca }}</p>
        <p><strong>Modelo:</strong> {{ activo.modelo }}</p>
        <p><strong>Estado:</strong> {{ activo.estado?.nombre_estado || 'N/A' }}</p>
        <p><strong>Ubicación:</strong> {{ activo.ubicacion_actual?.nombre_ubicacion || 'N/A' }}</p>
      </div>
    </div>
    
    <!-- Mensaje cuando no hay activos -->
    <div v-if="!activosStore.loading && activosStore.activos.length === 0" class="empty">
      No hay activos disponibles
    </div>
    
    <!-- Paginación -->
    <div v-if="activosStore.totalActivos > 0" class="pagination">
      <button 
        @click="loadPreviousPage" 
        :disabled="!activosStore.hasPreviousPage"
        class="btn"
      >
        ← Anterior
      </button>
      
      <span class="page-info">
        Página {{ activosStore.pagination.currentPage }} 
        ({{ activosStore.totalActivos }} activos en total)
      </span>
      
      <button 
        @click="loadNextPage" 
        :disabled="!activosStore.hasNextPage"
        class="btn"
      >
        Siguiente →
      </button>
    </div>
  </div>
</template>

<style scoped>
.activos-list {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

h2 {
  margin-bottom: 1.5rem;
  color: var(--color-heading);
}

.loading, .error, .empty {
  padding: 2rem;
  text-align: center;
  border-radius: 8px;
  margin: 1rem 0;
}

.loading {
  background-color: #e3f2fd;
  color: #1976d2;
}

.error {
  background-color: #ffebee;
  color: #c62828;
}

.empty {
  background-color: #f5f5f5;
  color: #757575;
}

.activos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.activo-card {
  background: var(--color-background-soft);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: 1.5rem;
  transition: transform 0.2s, box-shadow 0.2s;
}

.activo-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.activo-card h3 {
  margin: 0 0 1rem 0;
  color: var(--color-heading);
  font-size: 1.1rem;
}

.activo-card p {
  margin: 0.5rem 0;
  font-size: 0.9rem;
  color: var(--color-text);
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
}

.btn {
  padding: 0.5rem 1rem;
  background-color: hsla(160, 100%, 37%, 1);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.btn:hover:not(:disabled) {
  background-color: hsla(160, 100%, 30%, 1);
}

.btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.page-info {
  font-size: 0.9rem;
  color: var(--color-text);
}
</style>


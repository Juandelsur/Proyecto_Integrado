/**
 * Store de Pinia para gestionar Activos
 * 
 * Este store maneja el estado global de los activos en la aplicación.
 * Usa el servicio activosService para hacer peticiones al backend.
 */

import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { 
  getActivos, 
  getActivoById, 
  createActivo, 
  updateActivo,
  patchActivo,
  deleteActivo,
  movilizarActivo 
} from '@/services/activosService'

export const useActivosStore = defineStore('activos', () => {
  // Estado
  const activos = ref([])
  const activoActual = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const pagination = ref({
    count: 0,
    next: null,
    previous: null,
    currentPage: 1
  })

  // Getters (computed)
  const totalActivos = computed(() => pagination.value.count)
  const hasNextPage = computed(() => pagination.value.next !== null)
  const hasPreviousPage = computed(() => pagination.value.previous !== null)

  // Actions

  /**
   * Cargar lista de activos con paginación
   * @param {Object} params - Parámetros de consulta (page, search, ordering)
   */
  async function fetchActivos(params = {}) {
    loading.value = true
    error.value = null
    
    try {
      const data = await getActivos(params)
      activos.value = data.results
      pagination.value = {
        count: data.count,
        next: data.next,
        previous: data.previous,
        currentPage: params.page || 1
      }
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cargar activos'
      console.error('Error en fetchActivos:', err)
    } finally {
      loading.value = false
    }
  }

  /**
   * Cargar un activo específico por ID
   * @param {Number} id - ID del activo
   */
  async function fetchActivoById(id) {
    loading.value = true
    error.value = null
    
    try {
      const data = await getActivoById(id)
      activoActual.value = data
      return data
    } catch (err) {
      error.value = err.response?.data?.message || `Error al cargar activo ${id}`
      console.error('Error en fetchActivoById:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Crear un nuevo activo
   * @param {Object} activoData - Datos del activo
   */
  async function addActivo(activoData) {
    loading.value = true
    error.value = null
    
    try {
      const nuevoActivo = await createActivo(activoData)
      activos.value.unshift(nuevoActivo) // Agregar al inicio de la lista
      return nuevoActivo
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al crear activo'
      console.error('Error en addActivo:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Actualizar un activo existente
   * @param {Number} id - ID del activo
   * @param {Object} activoData - Datos actualizados
   */
  async function editActivo(id, activoData) {
    loading.value = true
    error.value = null
    
    try {
      const activoActualizado = await updateActivo(id, activoData)
      
      // Actualizar en la lista
      const index = activos.value.findIndex(a => a.id === id)
      if (index !== -1) {
        activos.value[index] = activoActualizado
      }
      
      // Actualizar activo actual si es el mismo
      if (activoActual.value?.id === id) {
        activoActual.value = activoActualizado
      }
      
      return activoActualizado
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al actualizar activo'
      console.error('Error en editActivo:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Eliminar un activo
   * @param {Number} id - ID del activo
   */
  async function removeActivo(id) {
    loading.value = true
    error.value = null
    
    try {
      await deleteActivo(id)
      
      // Eliminar de la lista
      activos.value = activos.value.filter(a => a.id !== id)
      
      // Limpiar activo actual si es el mismo
      if (activoActual.value?.id === id) {
        activoActual.value = null
      }
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al eliminar activo'
      console.error('Error en removeActivo:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Movilizar un activo a una nueva ubicación
   * @param {Number} id - ID del activo
   * @param {Object} movimientoData - { id_ubicacion_destino, notas }
   */
  async function moverActivo(id, movimientoData) {
    loading.value = true
    error.value = null
    
    try {
      const resultado = await movilizarActivo(id, movimientoData)
      
      // Recargar el activo para obtener la ubicación actualizada
      await fetchActivoById(id)
      
      return resultado
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al movilizar activo'
      console.error('Error en moverActivo:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Limpiar el estado
   */
  function clearState() {
    activos.value = []
    activoActual.value = null
    error.value = null
    pagination.value = {
      count: 0,
      next: null,
      previous: null,
      currentPage: 1
    }
  }

  return {
    // Estado
    activos,
    activoActual,
    loading,
    error,
    pagination,
    
    // Getters
    totalActivos,
    hasNextPage,
    hasPreviousPage,
    
    // Actions
    fetchActivos,
    fetchActivoById,
    addActivo,
    editActivo,
    removeActivo,
    moverActivo,
    clearState
  }
})


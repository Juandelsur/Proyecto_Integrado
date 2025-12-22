/**
 * Servicio para la gestión de Activos
 * 
 * Este servicio maneja todas las operaciones CRUD relacionadas con activos.
 * Utiliza el cliente de Axios configurado en api.js para hacer las peticiones HTTP.
 * 
 * Endpoints utilizados:
 * - GET    /api/activos/       - Listar activos (con filtros opcionales)
 * - GET    /api/activos/:id/   - Obtener un activo específico
 * - POST   /api/activos/       - Crear nuevo activo
 * - PUT    /api/activos/:id/   - Actualizar activo completo
 * - PATCH  /api/activos/:id/   - Actualizar activo parcial
 * - DELETE /api/activos/:id/   - Eliminar activo
 */

import apiClient from './api'

/**
 * Limpia los parámetros de query eliminando valores null, undefined o vacíos
 * @param {Object} params - Objeto con parámetros de query
 * @returns {Object} - Objeto limpio sin valores vacíos
 */
function cleanParams(params) {
  if (!params) return {}
  
  return Object.keys(params).reduce((acc, key) => {
    const value = params[key]
    
    // Solo incluir valores que no sean null, undefined o string vacío
    if (value !== null && value !== undefined && value !== '') {
      acc[key] = value
    }
    
    return acc
  }, {})
}

/**
 * Obtiene la lista de activos con filtros opcionales
 * @param {Object} params - Parámetros de filtrado
 * @param {string} params.search - Búsqueda general
 * @param {number} params.area - ID del área
 * @param {number} params.categoria - ID de la categoría
 * @param {string} params.estado - Estado del activo
 * @param {string} params.ordering - Campo de ordenamiento
 * @param {number} params.page - Número de página
 * @param {number} params.page_size - Tamaño de página
 * @returns {Promise} - Promesa con la respuesta del servidor
 */
export async function getActivos(params = {}) {
  try {
    // Limpiar parámetros antes de enviar
    const cleanedParams = cleanParams(params)
    
    const response = await apiClient.get('/api/activos/', {
      params: cleanedParams
    })
    
    return response.data
  } catch (error) {
    console.error('Error al obtener activos:', error)
    throw error
  }
}

/**
 * Obtiene un activo específico por su ID
 * @param {number} id - ID del activo
 * @returns {Promise} - Promesa con los datos del activo
 */
export async function getActivoById(id) {
  try {
    const response = await apiClient.get(`/api/activos/${id}/`)
    return response.data
  } catch (error) {
    console.error(`Error al obtener activo ${id}:`, error)
    throw error
  }
}

/**
 * Crea un nuevo activo
 * @param {Object} activoData - Datos del activo a crear
 * @returns {Promise} - Promesa con el activo creado
 */
export async function createActivo(activoData) {
  try {
    const response = await apiClient.post('/api/activos/', activoData)
    return response.data
  } catch (error) {
    console.error('Error al crear activo:', error)
    throw error
  }
}

/**
 * Actualiza un activo existente (PUT - actualización completa)
 * @param {number} id - ID del activo
 * @param {Object} activoData - Datos completos del activo
 * @returns {Promise} - Promesa con el activo actualizado
 */
export async function updateActivo(id, activoData) {
  try {
    const response = await apiClient.put(`/api/activos/${id}/`, activoData)
    return response.data
  } catch (error) {
    console.error(`Error al actualizar activo ${id}:`, error)
    throw error
  }
}

/**
 * Actualiza parcialmente un activo (PATCH - actualización parcial)
 * @param {number} id - ID del activo
 * @param {Object} activoData - Datos parciales del activo
 * @returns {Promise} - Promesa con el activo actualizado
 */
export async function patchActivo(id, activoData) {
  try {
    const response = await apiClient.patch(`/api/activos/${id}/`, activoData)
    return response.data
  } catch (error) {
    console.error(`Error al actualizar parcialmente activo ${id}:`, error)
    throw error
  }
}

/**
 * Elimina un activo
 * @param {number} id - ID del activo a eliminar
 * @returns {Promise} - Promesa con la confirmación de eliminación
 */
export async function deleteActivo(id) {
  try {
    const response = await apiClient.delete(`/api/activos/${id}/`)
    return response.data
  } catch (error) {
    console.error(`Error al eliminar activo ${id}:`, error)
    throw error
  }
}

// Exportación por defecto con todas las funciones
export default {
  getActivos,
  getActivoById,
  createActivo,
  updateActivo,
  patchActivo,
  deleteActivo
}

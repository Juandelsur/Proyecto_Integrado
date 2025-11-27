/**
 * Servicio de Ubicaciones
 * 
 * Maneja todas las peticiones relacionadas con ubicaciones del hospital.
 */

import apiClient from './api'

const ubicacionesService = {
  /**
   * Obtiene todas las ubicaciones
   * 
   * @param {Object} params - Parámetros de consulta (filtros, paginación)
   * @returns {Promise<Object>} - Lista de ubicaciones
   */
  async getAll(params = {}) {
    const response = await apiClient.get('/api/ubicaciones/', { params })
    return response.data
  },

  /**
   * Obtiene una ubicación por ID
   * 
   * @param {number} id - ID de la ubicación
   * @returns {Promise<Object>} - Ubicación
   */
  async getById(id) {
    const response = await apiClient.get(`/api/ubicaciones/${id}/`)
    return response.data
  },

  /**
   * Crea una nueva ubicación
   * 
   * @param {Object} ubicacionData - Datos de la ubicación
   * @returns {Promise<Object>} - Ubicación creada
   */
  async create(ubicacionData) {
    const response = await apiClient.post('/api/ubicaciones/', ubicacionData)
    return response.data
  },

  /**
   * Actualiza una ubicación
   * 
   * @param {number} id - ID de la ubicación
   * @param {Object} ubicacionData - Datos actualizados
   * @returns {Promise<Object>} - Ubicación actualizada
   */
  async update(id, ubicacionData) {
    const response = await apiClient.put(`/api/ubicaciones/${id}/`, ubicacionData)
    return response.data
  },

  /**
   * Actualiza parcialmente una ubicación
   * 
   * @param {number} id - ID de la ubicación
   * @param {Object} ubicacionData - Datos a actualizar
   * @returns {Promise<Object>} - Ubicación actualizada
   */
  async partialUpdate(id, ubicacionData) {
    const response = await apiClient.patch(`/api/ubicaciones/${id}/`, ubicacionData)
    return response.data
  },

  /**
   * Elimina una ubicación
   * 
   * @param {number} id - ID de la ubicación
   * @returns {Promise<void>}
   */
  async delete(id) {
    await apiClient.delete(`/api/ubicaciones/${id}/`)
  }
}

export default ubicacionesService


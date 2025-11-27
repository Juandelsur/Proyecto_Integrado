/**
 * Servicio para gestionar Activos
 * 
 * Este archivo contiene todas las funciones para interactuar con el endpoint de activos del backend.
 * Usa la instancia de Axios configurada en api.js
 */

import apiClient from './api'

/**
 * Obtener todos los activos (con paginación)
 * @param {Object} params - Parámetros de consulta (page, search, ordering)
 * @returns {Promise} - Promesa con la respuesta del servidor
 */
export const getActivos = async (params = {}) => {
  try {
    const response = await apiClient.get('/api/activos/', { params })
    return response.data
  } catch (error) {
    console.error('Error al obtener activos:', error)
    throw error
  }
}

/**
 * Obtener un activo por ID
 * @param {Number} id - ID del activo
 * @returns {Promise} - Promesa con los datos del activo
 */
export const getActivoById = async (id) => {
  try {
    const response = await apiClient.get(`/api/activos/${id}/`)
    return response.data
  } catch (error) {
    console.error(`Error al obtener activo ${id}:`, error)
    throw error
  }
}

/**
 * Crear un nuevo activo
 * @param {Object} activoData - Datos del activo a crear
 * @returns {Promise} - Promesa con el activo creado
 */
export const createActivo = async (activoData) => {
  try {
    const response = await apiClient.post('/api/activos/', activoData)
    return response.data
  } catch (error) {
    console.error('Error al crear activo:', error)
    throw error
  }
}

/**
 * Actualizar un activo existente
 * @param {Number} id - ID del activo
 * @param {Object} activoData - Datos actualizados del activo
 * @returns {Promise} - Promesa con el activo actualizado
 */
export const updateActivo = async (id, activoData) => {
  try {
    const response = await apiClient.put(`/api/activos/${id}/`, activoData)
    return response.data
  } catch (error) {
    console.error(`Error al actualizar activo ${id}:`, error)
    throw error
  }
}

/**
 * Actualizar parcialmente un activo
 * @param {Number} id - ID del activo
 * @param {Object} activoData - Datos parciales a actualizar
 * @returns {Promise} - Promesa con el activo actualizado
 */
export const patchActivo = async (id, activoData) => {
  try {
    const response = await apiClient.patch(`/api/activos/${id}/`, activoData)
    return response.data
  } catch (error) {
    console.error(`Error al actualizar parcialmente activo ${id}:`, error)
    throw error
  }
}

/**
 * Eliminar un activo
 * @param {Number} id - ID del activo
 * @returns {Promise} - Promesa con la respuesta del servidor
 */
export const deleteActivo = async (id) => {
  try {
    const response = await apiClient.delete(`/api/activos/${id}/`)
    return response.data
  } catch (error) {
    console.error(`Error al eliminar activo ${id}:`, error)
    throw error
  }
}

/**
 * Movilizar un activo a una nueva ubicación (HU2)
 * @param {Number} id - ID del activo
 * @param {Object} movimientoData - Datos del movimiento { id_ubicacion_destino, notas }
 * @returns {Promise} - Promesa con la respuesta del servidor
 */
export const movilizarActivo = async (id, movimientoData) => {
  try {
    const response = await apiClient.post(`/api/activos/${id}/movilizar/`, movimientoData)
    return response.data
  } catch (error) {
    console.error(`Error al movilizar activo ${id}:`, error)
    throw error
  }
}


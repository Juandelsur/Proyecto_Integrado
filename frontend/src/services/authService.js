/**
 * Servicio de Autenticación
 * 
 * Maneja todas las peticiones relacionadas con autenticación:
 * - Login (obtener token JWT)
 * - Refresh token
 * - Obtener información del usuario actual
 */

import apiClient from './api'

const authService = {
  /**
   * Login: Obtiene tokens JWT
   *
   * @param {string} username - Nombre de usuario
   * @param {string} password - Contraseña
   * @returns {Promise<{access: string, refresh: string}>}
   */
  async login(username, password) {
    const response = await apiClient.post('/api/auth/token/', {
      username,
      password
    })
    return response.data
  },

  /**
   * Refresh: Renueva el access token usando el refresh token
   *
   * @param {string} refreshToken - Refresh token
   * @returns {Promise<{access: string}>}
   */
  async refreshToken(refreshToken) {
    const response = await apiClient.post('/api/auth/token/refresh/', {
      refresh: refreshToken
    })
    return response.data
  },

  /**
   * Obtiene la información del usuario autenticado
   * 
   * NOTA: Este endpoint debe existir en el backend.
   * Si no existe, deberás crearlo o decodificar el JWT en el frontend.
   * 
   * Endpoint esperado: GET /api/usuarios/me/
   * 
   * @returns {Promise<Object>} - Información del usuario
   */
  async getCurrentUser() {
    const response = await apiClient.get('/api/usuarios/me/')
    return response.data
  },

  /**
   * Verifica si el token es válido
   *
   * @param {string} token - Token JWT
   * @returns {Promise<boolean>}
   */
  async verifyToken(token) {
    try {
      await apiClient.post('/api/auth/token/verify/', { token })
      return true
    } catch (error) {
      return false
    }
  }
}

export default authService


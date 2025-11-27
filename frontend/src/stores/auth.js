/**
 * Store de Autenticación (Pinia)
 * 
 * Gestiona el estado de autenticación del usuario, incluyendo:
 * - Token JWT
 * - Información del usuario (username, rol)
 * - Permisos basados en roles (RBAC)
 * 
 * Roles del sistema:
 * - Administrador: Acceso total
 * - Técnico: Operaciones CRUD en activos, movilización, impresión
 * - Jefe de Departamento: Solo lectura (supervisión)
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import apiClient from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  // ============================================================================
  // STATE
  // ============================================================================
  
  const token = ref(localStorage.getItem('access_token') || null)
  const refreshToken = ref(localStorage.getItem('refresh_token') || null)
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))
  
  // ============================================================================
  // GETTERS (Computed Properties)
  // ============================================================================
  
  /**
   * Verifica si el usuario está autenticado
   */
  const isAuthenticated = computed(() => {
    return !!token.value && !!user.value
  })
  
  /**
   * Obtiene el rol del usuario actual
   */
  const userRole = computed(() => {
    return user.value?.rol?.nombre_rol || null
  })
  
  /**
   * Verifica si el usuario es Administrador
   */
  const isAdmin = computed(() => {
    return userRole.value === 'Administrador'
  })
  
  /**
   * Verifica si el usuario es Técnico
   */
  const isTecnico = computed(() => {
    return userRole.value === 'Técnico'
  })
  
  /**
   * Verifica si el usuario es Jefe de Departamento
   */
  const isJefe = computed(() => {
    return userRole.value === 'Jefe de Departamento'
  })
  
  /**
   * PERMISO: Puede imprimir etiquetas QR
   * Solo Administradores y Técnicos pueden imprimir
   * Los Jefes NO tienen este permiso (solo supervisión)
   */
  const canPrintLabels = computed(() => {
    return isAdmin.value || isTecnico.value
  })
  
  /**
   * PERMISO: Puede crear/editar activos
   * Solo Administradores y Técnicos
   */
  const canEditAssets = computed(() => {
    return isAdmin.value || isTecnico.value
  })
  
  /**
   * PERMISO: Puede eliminar activos
   * Solo Administradores
   */
  const canDeleteAssets = computed(() => {
    return isAdmin.value
  })
  
  /**
   * PERMISO: Puede movilizar activos
   * Solo Administradores y Técnicos
   */
  const canMoveAssets = computed(() => {
    return isAdmin.value || isTecnico.value
  })
  
  /**
   * PERMISO: Puede gestionar usuarios
   * Solo Administradores
   */
  const canManageUsers = computed(() => {
    return isAdmin.value
  })
  
  // ============================================================================
  // ACTIONS
  // ============================================================================
  
  /**
   * Login: Autentica al usuario y guarda el token
   */
  async function login(username, password) {
    try {
      const response = await apiClient.post('/api/token/', {
        username,
        password
      })
      
      const { access, refresh } = response.data
      
      // Guardar tokens
      token.value = access
      refreshToken.value = refresh
      localStorage.setItem('access_token', access)
      localStorage.setItem('refresh_token', refresh)
      
      // Obtener información del usuario
      await fetchUserInfo()
      
      return { success: true }
    } catch (error) {
      console.error('Error en login:', error)
      return { 
        success: false, 
        message: error.response?.data?.detail || 'Error al iniciar sesión' 
      }
    }
  }
  
  /**
   * Obtiene la información del usuario autenticado
   */
  async function fetchUserInfo() {
    try {
      // Asumiendo que existe un endpoint /api/usuarios/me/ o similar
      // Si no existe, deberás decodificar el JWT o crear el endpoint
      const response = await apiClient.get('/api/usuarios/me/')
      user.value = response.data
      localStorage.setItem('user', JSON.stringify(response.data))
    } catch (error) {
      console.error('Error al obtener información del usuario:', error)
    }
  }
  
  /**
   * Logout: Cierra sesión y limpia el estado
   */
  function logout() {
    token.value = null
    refreshToken.value = null
    user.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
  }
  
  // ============================================================================
  // RETURN (Exponer estado y métodos)
  // ============================================================================
  
  return {
    // State
    token,
    user,
    
    // Getters
    isAuthenticated,
    userRole,
    isAdmin,
    isTecnico,
    isJefe,
    
    // Permisos
    canPrintLabels,
    canEditAssets,
    canDeleteAssets,
    canMoveAssets,
    canManageUsers,
    
    // Actions
    login,
    logout,
    fetchUserInfo
  }
})


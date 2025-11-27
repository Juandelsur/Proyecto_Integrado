/**
 * Store de Autenticación (Pinia)
 *
 * Gestiona el estado de autenticación del usuario, incluyendo:
 * - Token JWT (access y refresh)
 * - Información del usuario (username, email, rol)
 * - Permisos basados en roles (RBAC - Role-Based Access Control)
 *
 * ============================================================================
 * ROLES DEL SISTEMA Y PERMISOS
 * ============================================================================
 *
 * 1. ADMINISTRADOR
 *    ✅ Imprimir etiquetas
 *    ✅ Gestionar activos (crear/editar)
 *    ✅ Eliminar activos
 *    ✅ Movilizar activos
 *    ✅ Gestionar usuarios
 *    ✅ Ver auditoría
 *
 * 2. TÉCNICO
 *    ✅ Imprimir etiquetas
 *    ✅ Gestionar activos (crear/editar)
 *    ❌ Eliminar activos
 *    ✅ Movilizar activos
 *    ❌ Gestionar usuarios
 *    ❌ Ver auditoría
 *
 * 3. JEFE DE DEPARTAMENTO
 *    ✅ Imprimir etiquetas
 *    ❌ Gestionar activos (solo lectura)
 *    ❌ Eliminar activos
 *    ❌ Movilizar activos
 *    ❌ Gestionar usuarios
 *    ✅ Ver auditoría (supervisión)
 *
 * ============================================================================
 * CAMBIO IMPORTANTE: Impresión de Etiquetas
 * ============================================================================
 *
 * ANTES: Solo Admin y Técnico podían imprimir
 * AHORA: TODOS los roles pueden imprimir etiquetas (incluyendo Jefe)
 *
 * Razón: Los Jefes de Departamento necesitan poder imprimir etiquetas
 * para sus equipos, aunque no puedan editarlos.
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

  // ============================================================================
  // PERMISOS FUNCIONALES (RBAC - Role-Based Access Control)
  // ============================================================================

  /**
   * PERMISO: Puede imprimir etiquetas QR
   *
   * ✅ TODOS LOS ROLES pueden imprimir etiquetas
   * - Administrador: ✅
   * - Técnico: ✅
   * - Jefe de Departamento: ✅
   *
   * Requisito: Usuario debe estar autenticado
   */
  const canPrintLabels = computed(() => {
    return isAuthenticated.value
  })

  /**
   * PERMISO: Puede gestionar activos (Crear/Editar)
   *
   * ✅ Administrador: Puede crear y editar activos
   * ✅ Técnico: Puede crear y editar activos
   * ❌ Jefe de Departamento: Solo lectura (supervisión)
   */
  const canManageAssets = computed(() => {
    return isAdmin.value || isTecnico.value
  })

  /**
   * PERMISO: Puede eliminar activos
   *
   * ✅ Administrador: Puede eliminar activos
   * ❌ Técnico: NO puede eliminar
   * ❌ Jefe de Departamento: NO puede eliminar
   */
  const canDeleteAssets = computed(() => {
    return isAdmin.value
  })

  /**
   * PERMISO: Puede movilizar activos
   *
   * ✅ Administrador: Puede movilizar activos
   * ✅ Técnico: Puede movilizar activos
   * ❌ Jefe de Departamento: NO puede movilizar
   */
  const canMoveAssets = computed(() => {
    return isAdmin.value || isTecnico.value
  })

  /**
   * PERMISO: Puede gestionar usuarios
   *
   * ✅ Administrador: Puede crear/editar/eliminar usuarios
   * ❌ Técnico: NO puede gestionar usuarios
   * ❌ Jefe de Departamento: NO puede gestionar usuarios
   */
  const canManageUsers = computed(() => {
    return isAdmin.value
  })

  /**
   * PERMISO: Puede ver auditoría
   *
   * ✅ Administrador: Puede ver auditoría completa
   * ❌ Técnico: NO puede ver auditoría
   * ✅ Jefe de Departamento: Puede ver auditoría (supervisión)
   */
  const canViewAudit = computed(() => {
    return isAdmin.value || isJefe.value
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

    // Getters - Información del Usuario
    isAuthenticated,
    userRole,
    isAdmin,
    isTecnico,
    isJefe,

    // Permisos Funcionales (RBAC)
    canPrintLabels,      // ✅ TODOS los roles
    canManageAssets,     // ✅ Admin, Técnico
    canDeleteAssets,     // ✅ Solo Admin
    canMoveAssets,       // ✅ Admin, Técnico
    canManageUsers,      // ✅ Solo Admin
    canViewAudit,        // ✅ Admin, Jefe

    // Actions
    login,
    logout,
    fetchUserInfo
  }
})


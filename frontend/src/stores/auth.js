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
   * Login: Autentica al usuario contra el backend Django y guarda el token JWT
   *
   * VERSIÓN PRODUCCIÓN - AUTENTICACIÓN JWT REAL
   *
   * Flujo:
   * 1. POST /api/auth/token/ con username y password
   * 2. Recibe { access, refresh } tokens JWT
   * 3. Guarda tokens en localStorage y state
   * 4. GET /api/usuarios/me/ para obtener información del usuario
   * 5. Guarda usuario completo (con rol) en localStorage y state
   *
   * @param {string} username - Nombre de usuario
   * @param {string} password - Contraseña
   * @returns {Promise<{success: boolean, message?: string}>}
   */
  async function login(username, password) {
    try {
      console.log('🔐 [Auth] Iniciando login con backend Django...')

      // ========================================================================
      // PASO 1: OBTENER TOKENS JWT DEL BACKEND
      // ========================================================================

      const tokenResponse = await apiClient.post('/api/auth/token/', {
        username,
        password
      })

      console.log('✅ [Auth] Tokens JWT recibidos del backend')

      const { access, refresh } = tokenResponse.data

      // Validar que los tokens existan
      if (!access || !refresh) {
        throw new Error('El backend no retornó los tokens JWT correctamente')
      }

      // ========================================================================
      // PASO 2: GUARDAR TOKENS EN LOCALSTORAGE Y STATE
      // ========================================================================

      token.value = access
      refreshToken.value = refresh
      localStorage.setItem('access_token', access)
      localStorage.setItem('refresh_token', refresh)

      console.log('💾 [Auth] Tokens guardados en localStorage')

      // ========================================================================
      // PASO 3: OBTENER INFORMACIÓN DEL USUARIO AUTENTICADO
      // ========================================================================

      await fetchUserInfo()

      console.log('✅ [Auth] Login completado exitosamente')
      console.log('👤 [Auth] Usuario:', user.value?.username)
      console.log('🎭 [Auth] Rol:', user.value?.rol?.nombre_rol)

      return { success: true }

    } catch (error) {
      console.error('❌ [Auth] Error en login:', error)

      // Limpiar cualquier dato parcial
      token.value = null
      refreshToken.value = null
      user.value = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')

      // Determinar mensaje de error específico
      let errorMessage = 'Error al iniciar sesión'

      if (error.response) {
        // El servidor respondió con un código de error
        const status = error.response.status
        const data = error.response.data

        if (status === 401) {
          errorMessage = 'Usuario o contraseña incorrectos'
        } else if (status === 400) {
          errorMessage = data.detail || 'Datos de login inválidos'
        } else if (status === 500) {
          errorMessage = 'Error del servidor. Intenta nuevamente más tarde'
        } else {
          errorMessage = data.detail || `Error ${status}: ${error.response.statusText}`
        }
      } else if (error.request) {
        // La petición fue hecha pero no hubo respuesta
        errorMessage = 'No se pudo conectar con el servidor. Verifica tu conexión a internet'
      } else {
        // Error al configurar la petición
        errorMessage = error.message || 'Error inesperado al iniciar sesión'
      }

      return {
        success: false,
        message: errorMessage
      }
    }
  }
  
  /**
   * Obtiene la información del usuario autenticado desde el backend
   *
   * CRÍTICO: Este método debe llamarse INMEDIATAMENTE después de obtener los tokens JWT
   * para obtener el rol del usuario y sus permisos.
   *
   * Endpoint: GET /api/usuarios/me/
   *
   * Respuesta esperada:
   * {
   *   "id": 1,
   *   "username": "admin",
   *   "email": "admin@hospital.com",
   *   "nombre_completo": "Administrador del Sistema",
   *   "rol": {
   *     "id_rol": 1,
   *     "nombre_rol": "Administrador",
   *     "descripcion": "Acceso total al sistema"
   *   },
   *   "is_active": true,
   *   "is_staff": true,
   *   "date_joined": "2025-01-15T10:30:00Z",
   *   "last_login": "2025-01-20T14:45:00Z"
   * }
   *
   * @throws {Error} Si el endpoint falla o el usuario no tiene rol asignado
   */
  async function fetchUserInfo() {
    try {
      console.log('📡 [Auth] Obteniendo información del usuario desde /api/usuarios/me/')

      const response = await apiClient.get('/api/usuarios/me/')

      console.log('✅ [Auth] Información del usuario recibida:', response.data)

      // Validar que el usuario tenga un rol asignado (CRÍTICO para RBAC)
      if (!response.data.rol || !response.data.rol.nombre_rol) {
        throw new Error('El usuario no tiene un rol asignado. Contacta al administrador.')
      }

      // Guardar usuario en state y localStorage
      user.value = response.data
      localStorage.setItem('user', JSON.stringify(response.data))

      console.log('💾 [Auth] Usuario guardado en localStorage')

    } catch (error) {
      console.error('❌ [Auth] Error al obtener información del usuario:', error)

      // Limpiar tokens si falla la obtención del usuario
      token.value = null
      refreshToken.value = null
      user.value = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')

      // Re-lanzar el error para que login() lo maneje
      throw new Error(
        error.response?.data?.detail ||
        'No se pudo obtener la información del usuario. Intenta nuevamente.'
      )
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


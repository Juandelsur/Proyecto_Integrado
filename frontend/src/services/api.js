/**
 * Configuración de Axios para peticiones HTTP al backend
 * 
 * Este archivo centraliza la configuración del cliente HTTP usando Axios.
 * Utiliza variables de entorno para configurar la baseURL según el ambiente.
 * 
 * Variables de entorno:
 * - VITE_API_URL: URL del backend (definida en .env.production o .env.development)
 * 
 * Fallback: Si no se define VITE_API_URL, usa http://localhost:8000 (desarrollo local)
 */

import axios from 'axios'

// Configuración de la URL base del API
// FORZADO A PRODUCCIÓN: Conectar directamente a Render
const baseURL = 'https://backend-sca.onrender.com'

// Crear instancia de Axios con configuración personalizada
const apiClient = axios.create({
  baseURL: baseURL,
  timeout: 15000, // Timeout de 15 segundos
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

// Interceptor de Request: Agregar token JWT si existe
apiClient.interceptors.request.use(
  (config) => {
    // Obtener token del localStorage (si usas JWT)
    const token = localStorage.getItem('access_token')
    
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Interceptor de Response: Manejo de errores globales
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    // Manejo de errores comunes
    if (error.response) {
      // El servidor respondió con un código de error
      switch (error.response.status) {
        case 401:
          // Token expirado o no autorizado
          console.error('No autorizado. Redirigiendo al login...')
          localStorage.removeItem('access_token')
          // Aquí puedes redirigir al login si usas Vue Router
          // router.push('/login')
          break
        case 403:
          console.error('Acceso prohibido')
          break
        case 404:
          console.error('Recurso no encontrado')
          break
        case 500:
          console.error('Error interno del servidor')
          break
        default:
          console.error(`Error ${error.response.status}: ${error.response.statusText}`)
      }
    } else if (error.request) {
      // La petición fue hecha pero no hubo respuesta
      console.error('No se recibió respuesta del servidor. Verifica tu conexión.')
    } else {
      // Algo pasó al configurar la petición
      console.error('Error al configurar la petición:', error.message)
    }
    
    return Promise.reject(error)
  }
)

// Exportar la instancia configurada
export default apiClient

// Exportar también la baseURL por si se necesita en otros lugares
export { baseURL }


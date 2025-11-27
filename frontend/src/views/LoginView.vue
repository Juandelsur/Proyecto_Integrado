<template>
  <div class="login-view">
    <div class="login-container">
      <!-- Tarjeta de Login -->
      <div class="login-card">
        <!-- Logo e Icono -->
        <div class="logo-section">
          <div class="logo-icon">
            <i class="bi bi-chat-square-text-fill"></i>
          </div>
          <h1 class="app-title">SCA</h1>
          <p class="app-subtitle">Sistema de Control de Equipos Informáticos</p>
        </div>

        <!-- Formulario de Login -->
        <form @submit.prevent="handleLogin" class="login-form">
          <!-- Campo Usuario -->
          <div class="form-group">
            <label for="email" class="form-label">Usuario</label>
            <div class="input-group">
              <span class="input-icon">
                <i class="bi bi-person-fill"></i>
              </span>
              <input
                id="email"
                v-model="email"
                type="text"
                class="form-control"
                placeholder="tu@email.com"
                required
                autocomplete="username"
                :disabled="loading"
              />
            </div>
          </div>

          <!-- Campo Contraseña -->
          <div class="form-group">
            <label for="password" class="form-label">Contraseña</label>
            <div class="input-group">
              <span class="input-icon">
                <i class="bi bi-lock-fill"></i>
              </span>
              <input
                id="password"
                v-model="password"
                type="password"
                class="form-control"
                placeholder="••••••••"
                required
                autocomplete="current-password"
                :disabled="loading"
              />
            </div>
          </div>

          <!-- Link "Olvidé mi contraseña" -->
          <div class="forgot-password">
            <a href="#" @click.prevent="handleForgotPassword">Olvidé mi contraseña</a>
          </div>

          <!-- Mensaje de Error -->
          <div v-if="errorMessage" class="alert alert-danger" role="alert">
            <i class="bi bi-exclamation-triangle-fill me-2"></i>
            {{ errorMessage }}
          </div>

          <!-- Botón Ingresar -->
          <button type="submit" class="btn btn-primary btn-login w-100" :disabled="loading">
            <span v-if="loading">
              <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
              Ingresando...
            </span>
            <span v-else>Ingresar</span>
          </button>
        </form>

        <!-- Footer -->
        <div class="login-footer">
          <p>© 2025 Hospital IT Asset Control System</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import apiClient from '@/services/api'

const router = useRouter()
const route = useRoute()

// Estado del formulario
const email = ref('')
const password = ref('')
const loading = ref(false)
const errorMessage = ref('')

/**
 * Maneja el envío del formulario de login
 */
async function handleLogin() {
  loading.value = true
  errorMessage.value = ''

  try {
    // 1. Llamar al endpoint de autenticación
    const loginResponse = await apiClient.post('/api/auth/token/', {
      username: email.value,
      password: password.value
    })

    // 2. Guardar tokens en localStorage
    const { access, refresh } = loginResponse.data
    localStorage.setItem('access_token', access)
    localStorage.setItem('refresh_token', refresh)

    // 3. Obtener información del usuario (incluyendo rol)
    const userResponse = await apiClient.get('/api/usuarios/me/')
    const userData = userResponse.data

    // 4. Guardar información del usuario
    localStorage.setItem('user', JSON.stringify(userData))

    // 5. Determinar redirección según el rol
    const rolNombre = userData.rol?.nombre_rol

    let redirectPath = '/dashboard' // Default

    if (rolNombre === 'Técnico') {
      redirectPath = '/tecnico/home'
    } else if (rolNombre === 'Administrador' || rolNombre === 'Jefe de Departamento') {
      redirectPath = '/dashboard'
    }

    // 6. Redirigir (usar query redirect si existe)
    const finalRedirect = route.query.redirect || redirectPath
    router.push(finalRedirect)

  } catch (error) {
    // Manejo de errores
    if (error.response) {
      // Error del servidor
      if (error.response.status === 401) {
        errorMessage.value = 'Usuario o contraseña incorrectos'
      } else if (error.response.status === 400) {
        errorMessage.value = 'Por favor, completa todos los campos'
      } else {
        errorMessage.value = 'Error del servidor. Intenta de nuevo más tarde'
      }
    } else if (error.request) {
      // No hubo respuesta del servidor
      errorMessage.value = 'No se pudo conectar con el servidor. Verifica tu conexión'
    } else {
      // Error al configurar la petición
      errorMessage.value = 'Error inesperado. Por favor, intenta de nuevo'
    }

    console.error('Error en login:', error)
  } finally {
    loading.value = false
  }
}

/**
 * Maneja el click en "Olvidé mi contraseña"
 */
function handleForgotPassword() {
  alert('Funcionalidad de recuperación de contraseña no implementada aún.\nContacta al administrador del sistema.')
}
</script>

<style scoped>
/* ============================================================================
   CONTENEDOR PRINCIPAL - FONDO AZUL CORPORATIVO
   ============================================================================ */

.login-view {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0d47a1 0%, #1565c0 50%, #1976d2 100%);
  padding: 1rem;
}

.login-container {
  width: 100%;
  max-width: 420px;
}

/* ============================================================================
   TARJETA DE LOGIN - FONDO BLANCO, BORDES REDONDEADOS
   ============================================================================ */

.login-card {
  background: white;
  border-radius: 20px;
  padding: 2.5rem 2rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
}

/* ============================================================================
   LOGO E ICONO
   ============================================================================ */

.logo-section {
  text-align: center;
  margin-bottom: 2rem;
}

.logo-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 80px;
  background: #0d47a1;
  border-radius: 16px;
  margin-bottom: 1rem;
}

.logo-icon i {
  font-size: 2.5rem;
  color: white;
}

.app-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 0.5rem;
  letter-spacing: 2px;
}

.app-subtitle {
  font-size: 0.95rem;
  color: #666;
  margin: 0;
  line-height: 1.4;
}

/* ============================================================================
   FORMULARIO
   ============================================================================ */

.login-form {
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.25rem;
}

.form-label {
  display: block;
  font-size: 0.95rem;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 0.5rem;
}

/* ============================================================================
   INPUT GROUP CON ICONO
   ============================================================================ */

.input-group {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
  z-index: 10;
  pointer-events: none;
}

.input-icon i {
  font-size: 1.1rem;
}

.form-control {
  width: 100%;
  padding: 0.875rem 1rem 0.875rem 3rem;
  font-size: 1rem;
  background: #f0f2f5;
  border: 2px solid transparent;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.form-control:focus {
  outline: none;
  background: white;
  border-color: #0d47a1;
  box-shadow: 0 0 0 3px rgba(13, 71, 161, 0.1);
}

.form-control:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.form-control::placeholder {
  color: #aaa;
}

/* ============================================================================
   LINK "OLVIDÉ MI CONTRASEÑA"
   ============================================================================ */

.forgot-password {
  text-align: right;
  margin-bottom: 1.5rem;
}

.forgot-password a {
  font-size: 0.9rem;
  color: #0d47a1;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s;
}

.forgot-password a:hover {
  color: #1565c0;
  text-decoration: underline;
}

/* ============================================================================
   ALERTA DE ERROR
   ============================================================================ */

.alert {
  padding: 0.875rem 1rem;
  margin-bottom: 1.25rem;
  border-radius: 10px;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
}

.alert-danger {
  background: #fee;
  color: #c33;
  border: 1px solid #fcc;
}

/* ============================================================================
   BOTÓN INGRESAR - ANCHO COMPLETO, AZUL OSCURO
   ============================================================================ */

.btn-login {
  padding: 1rem;
  font-size: 1.05rem;
  font-weight: 600;
  background: #0d47a1;
  color: white;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(13, 71, 161, 0.3);
}

.btn-login:hover:not(:disabled) {
  background: #1565c0;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(13, 71, 161, 0.4);
}

.btn-login:active:not(:disabled) {
  transform: translateY(0);
  box-shadow: 0 2px 8px rgba(13, 71, 161, 0.3);
}

.btn-login:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
  border-width: 0.15em;
}

/* ============================================================================
   FOOTER
   ============================================================================ */

.login-footer {
  text-align: center;
  padding-top: 1.5rem;
  border-top: 1px solid #e0e0e0;
}

.login-footer p {
  margin: 0;
  font-size: 0.85rem;
  color: #999;
}

/* ============================================================================
   RESPONSIVE - MOBILE FIRST
   ============================================================================ */

/* Tablets y pantallas medianas */
@media (min-width: 768px) {
  .login-card {
    padding: 3rem 2.5rem;
  }

  .app-title {
    font-size: 3rem;
  }

  .logo-icon {
    width: 90px;
    height: 90px;
  }

  .logo-icon i {
    font-size: 3rem;
  }
}

/* Pantallas grandes */
@media (min-width: 1024px) {
  .login-container {
    max-width: 480px;
  }
}

/* Animación del spinner */
@keyframes spinner-border {
  to {
    transform: rotate(360deg);
  }
}

.spinner-border {
  display: inline-block;
  width: 1rem;
  height: 1rem;
  vertical-align: text-bottom;
  border: 0.15em solid currentColor;
  border-right-color: transparent;
  border-radius: 50%;
  animation: spinner-border 0.75s linear infinite;
}
</style>


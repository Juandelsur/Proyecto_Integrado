<template>
  <v-container fluid class="fill-height login-container">
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card elevation="8" class="login-card">
          <!-- Header -->
          <v-card-title class="text-center pa-6 bg-primary">
            <div class="d-flex flex-column align-center w-100">
              <v-icon size="64" color="white" class="mb-3">mdi-hospital-building</v-icon>
              <h2 class="text-h4 text-white font-weight-bold">SCA Hospital</h2>
              <p class="text-subtitle-1 text-white mt-2">Sistema de Control de Activos</p>
            </div>
          </v-card-title>

          <!-- Formulario de Login -->
          <v-card-text class="pa-8">
            <v-form @submit.prevent="handleLogin" ref="loginForm">
              <!-- Campo Usuario -->
              <v-text-field
                v-model="username"
                label="Usuario"
                prepend-inner-icon="mdi-account"
                variant="outlined"
                density="comfortable"
                :rules="[rules.required]"
                :disabled="loading"
                class="mb-4"
              ></v-text-field>

              <!-- Campo Contraseña -->
              <v-text-field
                v-model="password"
                label="Contraseña"
                prepend-inner-icon="mdi-lock"
                :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                :type="showPassword ? 'text' : 'password'"
                @click:append-inner="showPassword = !showPassword"
                variant="outlined"
                density="comfortable"
                :rules="[rules.required]"
                :disabled="loading"
              ></v-text-field>

              <!-- Mensaje de Error -->
              <v-alert
                v-if="errorMessage"
                type="error"
                variant="tonal"
                class="mb-4"
                closable
                @click:close="errorMessage = ''"
              >
                {{ errorMessage }}
              </v-alert>

              <!-- Botón Iniciar Sesión -->
              <v-btn
                type="submit"
                color="primary"
                size="large"
                block
                :loading="loading"
                class="text-none font-weight-bold"
              >
                <v-icon left class="mr-2">mdi-login</v-icon>
                Iniciar Sesión
              </v-btn>
            </v-form>
          </v-card-text>

          <!-- Footer con información del sistema -->
          <v-divider></v-divider>
          <v-card-text class="pa-4 bg-grey-lighten-4">
            <p class="text-caption text-center text-grey-darken-1">
              Sistema de Control de Activos - Hospital
            </p>
            <p class="text-caption text-center text-grey-darken-1 mt-1">
              Versión 1.0.0 - Producción
            </p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// ============================================================================
// COMPOSABLES
// ============================================================================

const router = useRouter()
const authStore = useAuthStore()

// ============================================================================
// STATE
// ============================================================================

const username = ref('')
const password = ref('')
const showPassword = ref(false)
const loading = ref(false)
const errorMessage = ref('')
const loginForm = ref(null)

// ============================================================================
// VALIDATION RULES
// ============================================================================

const rules = {
  required: (value) => !!value || 'Este campo es requerido'
}

// ============================================================================
// METHODS
// ============================================================================

/**
 * Maneja el envío del formulario de login
 *
 * Flujo:
 * 1. Valida el formulario
 * 2. Llama a authStore.login() que conecta con el backend Django
 * 3. Si es exitoso, redirige según el rol del usuario
 * 4. Si falla, muestra el mensaje de error específico
 */
async function handleLogin() {
  // Validar formulario
  const { valid } = await loginForm.value.validate()
  if (!valid) return

  loading.value = true
  errorMessage.value = ''

  try {
    console.log('🔐 [LoginView] Intentando login con usuario:', username.value)

    const result = await authStore.login(username.value, password.value)

    if (result.success) {
      // Login exitoso - Obtener rol del usuario
      const role = authStore.userRole

      console.log('✅ [LoginView] Login exitoso - Rol:', role)

      // Redirigir según el rol (RBAC)
      if (role === 'Administrador') {
        console.log('🔀 [LoginView] Redirigiendo a /admin')
        router.push('/admin')
      } else if (role === 'Técnico') {
        console.log('🔀 [LoginView] Redirigiendo a /tecnico')
        router.push('/tecnico')
      } else if (role === 'Jefe de Departamento') {
        console.log('🔀 [LoginView] Redirigiendo a /jefe')
        router.push('/jefe')
      } else {
        // Rol desconocido - redirigir al login
        console.warn('⚠️ [LoginView] Rol desconocido:', role)
        errorMessage.value = `Rol "${role}" no reconocido. Contacta al administrador.`
        authStore.logout()
      }
    } else {
      // Login fallido - Mostrar mensaje de error
      console.error('❌ [LoginView] Login fallido:', result.message)
      errorMessage.value = result.message || 'Error al iniciar sesión'
    }
  } catch (error) {
    // Error inesperado
    console.error('❌ [LoginView] Error inesperado en login:', error)
    errorMessage.value = 'Error inesperado al iniciar sesión. Intenta nuevamente.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
}

.login-card {
  border-radius: 16px !important;
  overflow: hidden;
}

.bg-primary {
  background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%) !important;
}
</style>

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

          <!-- Footer con usuarios de prueba -->
          <v-divider></v-divider>
          <v-card-text class="pa-4 bg-grey-lighten-4">
            <p class="text-subtitle-2 text-center mb-2 font-weight-bold">
              🔑 Usuarios de Prueba (Desarrollo)
            </p>
            <v-list density="compact" class="bg-transparent">
              <v-list-item density="compact">
                <template v-slot:prepend>
                  <v-icon size="small" color="error">mdi-shield-crown</v-icon>
                </template>
                <v-list-item-title class="text-caption">
                  <strong>admin</strong> / admin123 → Administrador
                </v-list-item-title>
              </v-list-item>
              <v-list-item density="compact">
                <template v-slot:prepend>
                  <v-icon size="small" color="info">mdi-account-wrench</v-icon>
                </template>
                <v-list-item-title class="text-caption">
                  <strong>tec</strong> / tec123 → Técnico
                </v-list-item-title>
              </v-list-item>
              <v-list-item density="compact">
                <template v-slot:prepend>
                  <v-icon size="small" color="success">mdi-account-tie</v-icon>
                </template>
                <v-list-item-title class="text-caption">
                  <strong>jefe</strong> / jefe123 → Jefe de Departamento
                </v-list-item-title>
              </v-list-item>
            </v-list>
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

async function handleLogin() {
  // Validar formulario
  const { valid } = await loginForm.value.validate()
  if (!valid) return

  loading.value = true
  errorMessage.value = ''

  try {
    const result = await authStore.login(username.value, password.value)

    if (result.success) {
      // Redirigir según el rol
      const role = authStore.userRole

      if (role === 'Administrador') {
        router.push('/admin')
      } else if (role === 'Técnico') {
        router.push('/tecnico')
      } else if (role === 'Jefe de Departamento') {
        router.push('/jefe')
      } else {
        router.push('/')
      }
    } else {
      errorMessage.value = result.message || 'Error al iniciar sesión'
    }
  } catch (error) {
    console.error('Error en login:', error)
    errorMessage.value = 'Error inesperado al iniciar sesión'
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

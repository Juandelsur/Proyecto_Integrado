<template>
  <div class="login-view">
    <div class="login-container">
      <div class="login-card">
        <div class="logo-section">
          <h1>🏥 SCA Hospital</h1>
          <p class="subtitle">Sistema de Control de Activos</p>
        </div>

        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-group">
            <label for="username">Usuario</label>
            <input
              id="username"
              v-model="username"
              type="text"
              placeholder="Ingresa tu usuario"
              required
              autocomplete="username"
            />
          </div>

          <div class="form-group">
            <label for="password">Contraseña</label>
            <input
              id="password"
              v-model="password"
              type="password"
              placeholder="Ingresa tu contraseña"
              required
              autocomplete="current-password"
            />
          </div>

          <button type="submit" class="btn-login" :disabled="loading">
            {{ loading ? '⏳ Iniciando sesión...' : '🔐 Iniciar Sesión' }}
          </button>

          <div v-if="errorMessage" class="error-message">
            ❌ {{ errorMessage }}
          </div>
        </form>

        <div class="demo-credentials">
          <p><strong>👤 Usuarios de prueba:</strong></p>
          <ul>
            <li><strong>Admin:</strong> admin / admin123</li>
            <li><strong>Técnico:</strong> tecnico1 / tecnico1123</li>
            <li><strong>Jefe:</strong> jefe1 / jefe1123</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const loading = ref(false)
const errorMessage = ref('')

async function handleLogin() {
  loading.value = true
  errorMessage.value = ''

  try {
    const result = await authStore.login(username.value, password.value)

    if (result.success) {
      // Redirigir a la página solicitada o al home
      const redirect = route.query.redirect || '/activos'
      router.push(redirect)
    } else {
      errorMessage.value = result.message || 'Error al iniciar sesión'
    }
  } catch (error) {
    errorMessage.value = 'Error de conexión. Por favor, intenta de nuevo.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-view {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
}

.login-container {
  width: 100%;
  max-width: 450px;
}

.login-card {
  background: white;
  border-radius: 16px;
  padding: 3rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.logo-section {
  text-align: center;
  margin-bottom: 2rem;
}

.logo-section h1 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #7f8c8d;
  font-size: 1rem;
}

.login-form {
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #2c3e50;
  font-weight: 600;
}

.form-group input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
}

.btn-login {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn-login:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-login:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-message {
  margin-top: 1rem;
  padding: 1rem;
  background: #f8d7da;
  color: #721c24;
  border-radius: 8px;
  text-align: center;
}

.demo-credentials {
  background: #e8f4f8;
  border-left: 4px solid #3498db;
  padding: 1rem 1.5rem;
  border-radius: 8px;
}

.demo-credentials p {
  margin-bottom: 0.5rem;
  color: #2c3e50;
}

.demo-credentials ul {
  margin: 0;
  padding-left: 1.5rem;
}

.demo-credentials li {
  margin: 0.25rem 0;
  color: #2c3e50;
}
</style>


<template>
  <div class="success-view">
    <!-- Contenido Principal -->
    <main class="success-content">
      <div class="success-card">
        <!-- Icono de Éxito con Círculo Verde -->
        <div class="success-icon-wrapper">
          <div class="success-icon-circle">
            <i class="bi bi-check-lg success-icon"></i>
          </div>
        </div>

        <!-- Mensaje -->
        <h2 class="success-title">Registro Exitoso</h2>
        <p class="success-message">
          El equipo informático ha sido registrado correctamente en el sistema
        </p>

        <!-- Información del Activo (si está disponible) -->
        <div v-if="asset" class="asset-summary">
          <div class="summary-row">
            <span class="summary-label">Código:</span>
            <span class="summary-value">{{ asset.codigo_inventario }}</span>
          </div>
          <div class="summary-row">
            <span class="summary-label">Hora:</span>
            <span class="summary-value">{{ currentDateTime }}</span>
          </div>
          <div class="summary-row">
            <span class="summary-label">Técnico:</span>
            <span class="summary-value">{{ technicianName }}</span>
          </div>
        </div>

        <!-- Botón de Acción -->
        <div class="action-buttons">
          <button @click="goHome" class="btn-primary">
            <i class="bi bi-house-door"></i>
            <span>Volver al Inicio</span>
          </button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

// Estado
const asset = ref(null)
const observaciones = ref('')

/**
 * Obtiene la fecha y hora actual formateada
 */
const currentDateTime = computed(() => {
  const now = new Date()
  const day = now.getDate().toString().padStart(2, '0')
  const months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
  const month = months[now.getMonth()]
  const year = now.getFullYear()
  const hours = now.getHours().toString().padStart(2, '0')
  const minutes = now.getMinutes().toString().padStart(2, '0')

  return `${hours}:${minutes} - ${day} ${month} ${year}`
})

/**
 * Obtiene el nombre del técnico actual
 */
const technicianName = computed(() => {
  return authStore.user?.username || 'Técnico'
})

/**
 * Obtiene los datos del state de la navegación
 */
onMounted(() => {
  if (history.state) {
    asset.value = history.state.asset
    observaciones.value = history.state.observaciones
  }
})

/**
 * Vuelve al home del técnico
 */
function goHome() {
  router.push({ name: 'technician-home' })
}
</script>

<style scoped>
/* ============================================================================
   CONTENEDOR PRINCIPAL
   ============================================================================ */

.success-view {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f7fa;
}

/* ============================================================================
   CONTENIDO PRINCIPAL
   ============================================================================ */

.success-content {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 1.5rem;
}

.success-card {
  width: 100%;
  max-width: 500px;
  background: white;
  border-radius: 20px;
  padding: 3rem 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  text-align: center;
}

/* ============================================================================
   SUCCESS ICON
   ============================================================================ */

.success-icon-wrapper {
  margin-bottom: 2rem;
  display: flex;
  justify-content: center;
  animation: scaleIn 0.5s ease;
}

@keyframes scaleIn {
  from {
    transform: scale(0);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

.success-icon-circle {
  width: 120px;
  height: 120px;
  background: #d4edda;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.success-icon {
  font-size: 3.5rem;
  color: #28a745;
  font-weight: bold;
}

/* ============================================================================
   SUCCESS MESSAGE
   ============================================================================ */

.success-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 1rem 0;
}

.success-message {
  font-size: 1rem;
  color: #666;
  margin: 0 0 2.5rem 0;
  line-height: 1.6;
  max-width: 400px;
  margin-left: auto;
  margin-right: auto;
}

/* ============================================================================
   ASSET SUMMARY
   ============================================================================ */

.asset-summary {
  background: #f5f7fa;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2.5rem;
  text-align: left;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.875rem 0;
  border-bottom: 1px solid #e0e0e0;
}

.summary-row:last-child {
  border-bottom: none;
}

.summary-label {
  font-size: 0.95rem;
  font-weight: 400;
  color: #666;
  flex-shrink: 0;
  margin-right: 1rem;
}

.summary-value {
  font-size: 0.95rem;
  font-weight: 700;
  color: #1a1a1a;
  text-align: right;
  word-break: break-word;
}

/* ============================================================================
   ACTION BUTTONS
   ============================================================================ */

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.btn-primary {
  background: #0d47a1;
  border: none;
  color: white;
  padding: 1rem 2rem;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  box-shadow: 0 4px 12px rgba(13, 71, 161, 0.3);
  width: 100%;
}

.btn-primary:hover {
  background: #1565c0;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(13, 71, 161, 0.4);
}

.btn-primary i {
  font-size: 1.25rem;
}

/* ============================================================================
   RESPONSIVE
   ============================================================================ */

@media (min-width: 768px) {
  .success-card {
    padding: 4rem 3rem;
  }

  .success-title {
    font-size: 2rem;
  }

  .success-icon-circle {
    width: 140px;
    height: 140px;
  }

  .success-icon {
    font-size: 4rem;
  }
}
</style>


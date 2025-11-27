<template>
  <div class="success-view">
    <!-- Header -->
    <header class="success-header">
      <h1 class="header-title">Registro Exitoso</h1>
    </header>

    <!-- Contenido Principal -->
    <main class="success-content">
      <div class="success-card">
        <!-- Icono de Éxito -->
        <div class="success-icon-container">
          <i class="bi bi-check-circle-fill success-icon"></i>
        </div>

        <!-- Mensaje -->
        <h2 class="success-title">¡Registro Confirmado!</h2>
        <p class="success-message">
          El movimiento del equipo ha sido registrado exitosamente.
        </p>

        <!-- Información del Activo (si está disponible) -->
        <div v-if="asset" class="asset-summary">
          <div class="summary-row">
            <span class="summary-label">Código:</span>
            <span class="summary-value">{{ asset.codigo_inventario }}</span>
          </div>
          <div class="summary-row">
            <span class="summary-label">Equipo:</span>
            <span class="summary-value">{{ asset.marca }} {{ asset.modelo }}</span>
          </div>
          <div v-if="observaciones" class="summary-row">
            <span class="summary-label">Observaciones:</span>
            <span class="summary-value">{{ observaciones }}</span>
          </div>
        </div>

        <!-- Botones de Acción -->
        <div class="action-buttons">
          <button @click="scanAnother" class="btn-primary">
            <i class="bi bi-qr-code-scan"></i>
            <span>Escanear Otro Equipo</span>
          </button>

          <button @click="goHome" class="btn-secondary">
            <i class="bi bi-house"></i>
            <span>Volver al Inicio</span>
          </button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Estado
const asset = ref(null)
const observaciones = ref('')

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
 * Vuelve al escáner para registrar otro equipo
 */
function scanAnother() {
  router.push({ name: 'scan-qr' })
}

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
  background: linear-gradient(135deg, #0d47a1 0%, #1565c0 50%, #1976d2 100%);
}

/* ============================================================================
   HEADER
   ============================================================================ */

.success-header {
  padding: 1.5rem;
  text-align: center;
}

.header-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: white;
  margin: 0;
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
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  text-align: center;
}

/* ============================================================================
   SUCCESS ICON
   ============================================================================ */

.success-icon-container {
  margin-bottom: 2rem;
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

.success-icon {
  font-size: 5rem;
  color: #4caf50;
}

/* ============================================================================
   SUCCESS MESSAGE
   ============================================================================ */

.success-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #0d47a1;
  margin: 0 0 1rem 0;
}

.success-message {
  font-size: 1rem;
  color: #666;
  margin: 0 0 2rem 0;
  line-height: 1.6;
}

/* ============================================================================
   ASSET SUMMARY
   ============================================================================ */

.asset-summary {
  background: #f5f7fa;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  text-align: left;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 0.75rem 0;
  border-bottom: 1px solid #e0e0e0;
}

.summary-row:last-child {
  border-bottom: none;
}

.summary-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #666;
  flex-shrink: 0;
  margin-right: 1rem;
}

.summary-value {
  font-size: 0.95rem;
  font-weight: 600;
  color: #333;
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
  background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%);
  border: none;
  color: white;
  padding: 1rem 1.5rem;
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
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(13, 71, 161, 0.4);
}

.btn-primary i {
  font-size: 1.25rem;
}

.btn-secondary {
  background: white;
  border: 2px solid #0d47a1;
  color: #0d47a1;
  padding: 1rem 1.5rem;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
}

.btn-secondary:hover {
  background: #f5f7fa;
}

.btn-secondary i {
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

  .action-buttons {
    flex-direction: row;
  }

  .btn-primary,
  .btn-secondary {
    flex: 1;
  }
}
</style>


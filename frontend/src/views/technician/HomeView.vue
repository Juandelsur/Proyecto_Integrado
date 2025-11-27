<template>
  <div class="technician-home">
    <!-- Header Azul con Nombre del Usuario -->
    <header class="header-welcome">
      <div class="header-content">
        <div class="welcome-text">
          <p class="greeting">Bienvenido,</p>
          <h1 class="user-name">{{ userName }}</h1>
        </div>
        <button @click="handleLogout" class="btn-logout" title="Cerrar Sesión">
          <i class="bi bi-box-arrow-right"></i>
        </button>
      </div>
    </header>

    <!-- Contenido Principal -->
    <main class="main-content">
      <!-- Botón Principal: Registrar Movimiento -->
      <div class="primary-action">
        <button @click="goToScan" class="btn-scan">
          <div class="scan-icon">
            <i class="bi bi-qr-code-scan"></i>
          </div>
          <h2 class="scan-title">Registrar Movimiento de Equipo</h2>
          <p class="scan-subtitle">Escanear Código QR</p>
        </button>
      </div>

      <!-- Botón Secundario: Imprimir Etiquetas -->
      <div class="print-action">
        <button @click="goToPrintLabels" class="btn-print">
          <i class="bi bi-printer"></i>
          <span>🖨️ Imprimir Etiquetas</span>
        </button>
      </div>

      <!-- Botones Secundarios -->
      <div class="secondary-actions">
        <button @click="goToHistory" class="btn-secondary">
          <i class="bi bi-clock-history"></i>
          <span>Histórico</span>
        </button>

        <button @click="goToSettings" class="btn-secondary">
          <i class="bi bi-gear"></i>
          <span>Configuración</span>
        </button>
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

/**
 * Obtiene el nombre del usuario desde el store
 */
const userName = computed(() => {
  // Intentar obtener el nombre completo, si no existe usar el username
  return authStore.user?.nombre_completo || authStore.user?.username || 'Usuario'
})

/**
 * Navega a la vista de escaneo QR
 */
function goToScan() {
  router.push('/escanear')
}

/**
 * Navega a la vista de impresión de etiquetas
 */
function goToPrintLabels() {
  router.push('/imprimir-etiquetas')
}

/**
 * Navega al histórico de movimientos
 */
function goToHistory() {
  router.push('/historico')
}

/**
 * Navega a la configuración
 */
function goToSettings() {
  router.push('/configuracion')
}

/**
 * Cierra sesión y redirige al login
 */
function handleLogout() {
  if (confirm('¿Estás seguro de que deseas cerrar sesión?')) {
    authStore.logout()
    router.push('/login')
  }
}
</script>

<style scoped>
/* ============================================================================
   CONTENEDOR PRINCIPAL
   ============================================================================ */

.technician-home {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f7fa;
}

/* ============================================================================
   HEADER AZUL CON NOMBRE DEL USUARIO
   ============================================================================ */

.header-welcome {
  background: linear-gradient(135deg, #0d47a1 0%, #1565c0 50%, #1976d2 100%);
  color: white;
  padding: 2rem 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-text {
  flex: 1;
}

.greeting {
  font-size: 0.95rem;
  font-weight: 400;
  margin: 0 0 0.25rem 0;
  opacity: 0.9;
}

.user-name {
  font-size: 2rem;
  font-weight: 700;
  margin: 0;
  line-height: 1.2;
}

.btn-logout {
  background: rgba(255, 255, 255, 0.2);
  border: 2px solid rgba(255, 255, 255, 0.3);
  color: white;
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.btn-logout:hover {
  background: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.5);
  transform: scale(1.05);
}

.btn-logout i {
  font-size: 1.5rem;
}

/* ============================================================================
   CONTENIDO PRINCIPAL
   ============================================================================ */

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem 1.5rem;
  max-width: 600px;
  margin: 0 auto;
  width: 100%;
}

/* ============================================================================
   BOTÓN PRINCIPAL: REGISTRAR MOVIMIENTO (TARJETA GRANDE CON QR)
   ============================================================================ */

.primary-action {
  width: 100%;
  margin-bottom: 2rem;
}

.btn-scan {
  width: 100%;
  background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%);
  border: none;
  border-radius: 24px;
  padding: 3rem 2rem;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 8px 24px rgba(13, 71, 161, 0.3);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  min-height: 320px;
}

.btn-scan:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(13, 71, 161, 0.4);
}

.btn-scan:active {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(13, 71, 161, 0.35);
}

.scan-icon {
  margin-bottom: 1.5rem;
}

.scan-icon i {
  font-size: 6rem;
  opacity: 0.95;
}

.scan-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0 0 0.75rem 0;
  line-height: 1.3;
}

.scan-subtitle {
  font-size: 1.1rem;
  font-weight: 400;
  margin: 0;
  opacity: 0.9;
}

/* ============================================================================
   BOTÓN DE IMPRESIÓN (OUTLINE BLANCO)
   ============================================================================ */

.print-action {
  width: 100%;
  margin-bottom: 1.5rem;
}

.btn-print {
  width: 100%;
  background: white;
  border: 2px solid #e0e0e0;
  color: #424242;
  padding: 1rem 1.5rem;
  border-radius: 16px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.btn-print:hover {
  background: #f5f5f5;
  border-color: #bdbdbd;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.btn-print:active {
  transform: translateY(0);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
}

.btn-print i {
  font-size: 1.3rem;
}

/* ============================================================================
   BOTONES SECUNDARIOS (HISTÓRICO Y CONFIGURACIÓN)
   ============================================================================ */

.secondary-actions {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.btn-secondary {
  width: 100%;
  background: white;
  border: 2px solid #0d47a1;
  color: #0d47a1;
  padding: 1.25rem 1.5rem;
  border-radius: 16px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.btn-secondary:hover {
  background: #0d47a1;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(13, 71, 161, 0.2);
}

.btn-secondary:active {
  transform: translateY(0);
  box-shadow: 0 2px 6px rgba(13, 71, 161, 0.15);
}

.btn-secondary i {
  font-size: 1.5rem;
}

/* ============================================================================
   RESPONSIVE - TABLET Y DESKTOP
   ============================================================================ */

/* Tablets (≥ 768px) */
@media (min-width: 768px) {
  .header-welcome {
    padding: 2.5rem 2rem;
  }

  .user-name {
    font-size: 2.5rem;
  }

  .main-content {
    padding: 3rem 2rem;
  }

  .btn-scan {
    padding: 4rem 3rem;
    min-height: 380px;
  }

  .scan-icon i {
    font-size: 7rem;
  }

  .scan-title {
    font-size: 1.75rem;
  }

  .scan-subtitle {
    font-size: 1.2rem;
  }

  .secondary-actions {
    flex-direction: row;
    gap: 1.5rem;
  }

  .btn-secondary {
    flex: 1;
  }
}

/* Desktop (≥ 1024px) */
@media (min-width: 1024px) {
  .btn-scan {
    min-height: 400px;
  }

  .scan-icon i {
    font-size: 8rem;
  }

  .scan-title {
    font-size: 2rem;
  }
}
</style>


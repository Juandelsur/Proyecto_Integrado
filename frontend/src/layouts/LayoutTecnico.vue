<template>
  <!-- ========================================================================
       LAYOUT TÉCNICO - MOBILE FIRST
       ======================================================================== -->
  <v-app>
    <!-- ====================================================================
         APP BAR SUPERIOR
         ==================================================================== -->
    <v-app-bar color="primary" density="comfortable" elevation="2">
      <!-- Título -->
      <v-app-bar-title>
        <span class="text-h6 font-weight-bold">SCA Hospital</span>
      </v-app-bar-title>

      <v-spacer></v-spacer>

      <!-- Botón de logout -->
      <v-btn icon @click="handleLogout">
        <v-icon>mdi-logout</v-icon>
      </v-btn>
    </v-app-bar>

    <!-- ====================================================================
         CONTENIDO PRINCIPAL
         ==================================================================== -->
    <v-main>
      <router-view />
    </v-main>

    <!-- ====================================================================
         BOTTOM NAVIGATION (NAVEGACIÓN INFERIOR)
         ==================================================================== -->
    <v-bottom-navigation v-model="activeTab" grow color="primary" class="bottom-nav">
      <v-btn value="home" @click="navigateTo('/tecnico/home')">
        <v-icon>mdi-home</v-icon>
        <span>Inicio</span>
      </v-btn>

      <v-btn value="mihistorial" @click="navigateTo('/tecnico/mihistorial')">
        <v-icon>mdi-history</v-icon>
        <span>Mi Historial</span>
      </v-btn>

      <v-btn value="print" @click="navigateTo('/tecnico/imprimir')">
        <v-icon>mdi-printer</v-icon>
        <span>Imprimir</span>
      </v-btn>
    </v-bottom-navigation>
  </v-app>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// ============================================================================
// COMPOSABLES
// ============================================================================
const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

// ============================================================================
// STATE
// ============================================================================
const activeTab = ref('home')

// ============================================================================
// WATCHERS - Sincronizar tab activo con la ruta
// ============================================================================
watch(
  () => route.path,
  (newPath) => {
    if (newPath.includes('/tecnico/home')) activeTab.value = 'home'
    else if (newPath.includes('/tecnico/history') || newPath.includes('/historico')) activeTab.value = 'history'
    else if (newPath.includes('/tecnico/imprimir')) activeTab.value = 'print'
  },
  { immediate: true }
)

// ============================================================================
// METHODS
// ============================================================================

/**
 * Navega a una ruta específica
 */
function navigateTo(path) {
  router.push(path)
}

/**
 * Maneja el logout del usuario
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
   FAB FLOTANTE - POSICIONAMIENTO CRÍTICO
   ============================================================================ */

/**
 * SOLUCIÓN CRÍTICA: FAB flotante sobre la barra de navegación inferior
 *
 * - position: fixed -> Mantiene el botón fijo en la pantalla
 * - bottom: 56px -> Posicionado justo encima de la bottom navigation (altura estándar 56px)
 * - left: 50% + transform -> Centrado horizontal perfecto
 * - z-index: 1001 -> Superior a v-bottom-navigation (z-index: 1000)
 */
.fab-scan {
  position: fixed !important;
  bottom: 56px !important; /* Altura de v-bottom-navigation */
  left: 50% !important;
  transform: translateX(-50%) !important;
  z-index: 1001 !important;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

/**
 * Efecto hover para el FAB
 */
.fab-scan:hover {
  transform: translateX(-50%) scale(1.1) !important;
  box-shadow: 0 8px 24px rgba(76, 175, 80, 0.5) !important;
}

/**
 * Ajuste de la barra de navegación inferior
 */
.bottom-nav {
  position: fixed !important;
  bottom: 0 !important;
  z-index: 1000 !important;
}

/* ============================================================================
   RESPONSIVE ADJUSTMENTS
   ============================================================================ */

/**
 * Tablets y pantallas más grandes
 */
@media (min-width: 768px) {
  .fab-scan {
    bottom: 64px !important; /* Ajustar si la bottom nav es más alta en tablet */
  }
}

/**
 * Pantallas muy pequeñas
 */
@media (max-width: 360px) {
  .fab-scan {
    bottom: 50px !important;
  }
}
</style>



<template>
  <!-- ========================================================================
       LAYOUT TÉCNICO - MOBILE FIRST
       ======================================================================== -->
  <v-app>
    <!-- ====================================================================
         APP BAR SUPERIOR
         ==================================================================== -->
    <v-app-bar color="primary" density="comfortable" elevation="2">
      <!-- Botón de menú lateral -->
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>

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
         NAVIGATION DRAWER (MENÚ LATERAL)
         ==================================================================== -->
    <v-navigation-drawer v-model="drawer" temporary>
      <!-- Header del drawer con info del usuario -->
      <v-list>
        <v-list-item
          :prepend-avatar="`https://ui-avatars.com/api/?name=${userName}&background=1565C0&color=fff`"
          :title="userName"
          :subtitle="userRole"
        ></v-list-item>
      </v-list>

      <v-divider></v-divider>

      <!-- Opciones de navegación -->
      <v-list density="compact" nav>
        <v-list-item
          prepend-icon="mdi-plus-circle"
          title="Crear Nuevo Activo"
          value="crear"
          @click="navigateTo('/tecnico/crear')"
        ></v-list-item>

        <v-list-item
          prepend-icon="mdi-pencil"
          title="Editar Activos"
          value="editar"
          @click="navigateTo('/tecnico/editar-buscar')"
        ></v-list-item>
      </v-list>
    </v-navigation-drawer>

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

      <v-btn value="history" @click="navigateTo('/tecnico/history')">
        <v-icon>mdi-history</v-icon>
        <span>Historial</span>
      </v-btn>

      <v-btn value="print" @click="navigateTo('/tecnico/imprimir')">
        <v-icon>mdi-printer</v-icon>
        <span>Imprimir</span>
      </v-btn>
    </v-bottom-navigation>

    <!-- ====================================================================
         FAB FLOTANTE CENTRAL (ESCANEAR QR)
         ==================================================================== -->
    <v-btn
      class="fab-scan"
      color="success"
      size="x-large"
      icon
      elevation="8"
      @click="navigateTo('/tecnico/scan')"
    >
      <v-icon size="40">mdi-qrcode-scan</v-icon>
    </v-btn>
  </v-app>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
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
const drawer = ref(false)
const activeTab = ref('home')

// ============================================================================
// COMPUTED
// ============================================================================
const userName = computed(() => {
  return authStore.user?.nombre_completo || authStore.user?.username || 'Usuario'
})

const userRole = computed(() => {
  return authStore.user?.rol?.nombre_rol || 'Técnico'
})

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
  drawer.value = false // Cerrar drawer al navegar
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



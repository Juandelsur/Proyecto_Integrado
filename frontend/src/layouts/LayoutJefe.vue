<template>
  <!-- ========================================================================
       LAYOUT JEFE DE DEPARTAMENTO - MOBILE FIRST
       ======================================================================== -->
  <v-app>
    <!-- ====================================================================
         APP BAR SUPERIOR
         ==================================================================== -->
    <v-app-bar color="primary" density="comfortable" elevation="2">
      <!-- Título -->
      <v-app-bar-title>
        <span class="text-h6 font-weight-bold">SCA Hospital - Jefe</span>
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
      <v-btn value="home" @click="navigateTo('/jefe/home')">
        <v-icon>mdi-home</v-icon>
        <span>Inicio</span>
      </v-btn>

      <v-btn value="scan" @click="navigateTo('/jefe/scan')">
        <v-icon>mdi-qrcode-scan</v-icon>
        <span>Escanear</span>
      </v-btn>

      <v-btn value="reportes" @click="navigateTo('/jefe/reportes')">
        <v-icon>mdi-file-chart</v-icon>
        <span>Reportes</span>
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
    if (newPath.includes('/jefe/home')) activeTab.value = 'home'
    else if (newPath.includes('/jefe/scan')) activeTab.value = 'scan'
    else if (newPath.includes('/jefe/reportes')) activeTab.value = 'reportes'
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
   BARRA DE NAVEGACIÓN INFERIOR
   ============================================================================ */

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
  .bottom-nav {
    max-width: 600px;
    left: 50%;
    transform: translateX(-50%);
    border-radius: 12px 12px 0 0;
  }
}

/**
 * Pantallas grandes - Ocultar navegación inferior y mostrar sidebar
 */
@media (min-width: 1024px) {
  .bottom-nav {
    display: none;
  }
  
  /* TODO: Implementar sidebar para pantallas grandes si es necesario */
}
</style>


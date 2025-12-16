<template>
  <v-app>
    <!-- Header -->
    <v-app-bar color="primary" density="compact">
      <v-app-bar-title>Técnico Operativo</v-app-bar-title>
      <v-spacer></v-spacer>
      <v-btn icon @click="handleLogout">
        <v-icon>mdi-logout</v-icon>
      </v-btn>
    </v-app-bar>

    <!-- Body -->
    <v-main>
      <v-container class="fill-height d-flex align-center justify-center">
        <v-row>
          <v-col cols="12" class="d-flex flex-column align-center">
            <!-- Botón 1: Escanear QR (DESTACADO) -->
            <!-- 🔥 PRÓXIMA INTEGRACIÓN: Componente QRScanner salvado de Fase 1 -->
            <v-btn
              color="secondary"
              size="x-large"
              block
              class="mb-4"
              @click="navigateTo('scanner')"
            >
              <v-icon left class="mr-2">mdi-qrcode-scan</v-icon>
              Escanear QR
            </v-btn>

            <!-- Botón 2: Movimientos -->
            <v-btn
              color="primary"
              size="x-large"
              block
              class="mb-4"
              @click="navigateTo('movimientos')"
            >
              <v-icon left class="mr-2">mdi-truck</v-icon>
              Movimientos
            </v-btn>

            <!-- Botón 3: Historial -->
            <v-btn
              color="primary"
              size="x-large"
              block
              class="mb-4"
              @click="navigateTo('historial')"
            >
              <v-icon left class="mr-2">mdi-history</v-icon>
              Historial
            </v-btn>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// ============================================================================
// COMPOSABLES
// ============================================================================

const router = useRouter()
const authStore = useAuthStore()

// ============================================================================
// METHODS
// ============================================================================

function handleLogout() {
  authStore.logout()
  router.push('/login')
}

function navigateTo(route) {
  // TODO: Implementar navegación cuando las rutas estén disponibles
  console.log(`Navegando a: ${route}`)
  // router.push(`/${route}`)
}
</script>

<style scoped>
/* Estilos adicionales si son necesarios */
</style>

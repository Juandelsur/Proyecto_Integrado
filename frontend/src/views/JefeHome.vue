<template>
  <v-app>
    <!-- Header -->
    <v-app-bar color="primary" density="compact">
      <v-app-bar-title>Jefe de Departamento</v-app-bar-title>
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
            <!-- Botón 1: Ver Inventario -->
            <v-btn
              color="primary"
              size="x-large"
              block
              class="mb-4"
              @click="navigateTo('inventario')"
            >
              <v-icon left class="mr-2">mdi-package-variant</v-icon>
              Ver Inventario
            </v-btn>

            <!-- Botón 2: Reportes -->
            <v-btn
              color="primary"
              size="x-large"
              block
              class="mb-4"
              @click="navigateTo('reportes')"
            >
              <v-icon left class="mr-2">mdi-chart-bar</v-icon>
              Reportes
            </v-btn>

            <!-- Botón 3: Aprobaciones -->
            <v-btn
              color="primary"
              size="x-large"
              block
              class="mb-4"
              @click="navigateTo('aprobaciones')"
            >
              <v-icon left class="mr-2">mdi-check-circle</v-icon>
              Aprobaciones
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

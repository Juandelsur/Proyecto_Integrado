<template>
  <v-app>
    <!-- Header -->
    <v-app-bar color="primary" density="compact">
      <v-app-bar-title>Administrador</v-app-bar-title>
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
            <!-- Botón 1: Gestionar Usuarios -->
            <v-btn
              color="primary"
              size="x-large"
              block
              class="mb-4"
              @click="navigateTo('usuarios')"
            >
              <v-icon left class="mr-2">mdi-account-multiple</v-icon>
              Gestionar Usuarios
            </v-btn>

            <!-- Botón 2: Maestro de Activos -->
            <v-btn
              color="primary"
              size="x-large"
              block
              class="mb-4"
              @click="navigateTo('activos')"
            >
              <v-icon left class="mr-2">mdi-clipboard-list</v-icon>
              Maestro de Activos
            </v-btn>

            <!-- Botón 3: Auditoría -->
            <v-btn
              color="primary"
              size="x-large"
              block
              class="mb-4"
              @click="navigateTo('auditoria')"
            >
              <v-icon left class="mr-2">mdi-file-document</v-icon>
              Auditoría
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

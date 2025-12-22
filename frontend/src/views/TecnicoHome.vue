<template>
  <v-container fluid class="pa-6">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-h4 font-weight-bold mb-2">Panel de Técnico</h1>
      <p class="text-subtitle-1 text-medium-emphasis">Gestión rápida de activos y movimientos</p>
    </div>

    <!-- Acción Principal: Escanear QR -->
    <v-row class="mb-6">
      <v-col cols="12">
        <v-card 
          hover 
          @click="router.push({ name: 'technician-scan' })"
          class="main-action-card"
          color="secondary"
          theme="dark"
          elevation="8"
        >
          <v-card-text class="text-center pa-8">
            <v-icon size="96" class="mb-4">mdi-qrcode-scan</v-icon>
            <h2 class="text-h4 font-weight-bold mb-2">Escanear QR</h2>
            <p class="text-h6">Iniciar lectura de código QR</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Acciones Rápidas -->
    <h2 class="text-h5 font-weight-bold mb-4">
      <v-icon class="mr-2">mdi-lightning-bolt</v-icon>
      Acciones Rápidas
    </h2>
    <v-row>
      <!-- Crear Activo -->
      <v-col cols="12" sm="6" md="4">
        <v-card 
          hover 
          @click="router.push({ name: 'technician-create' })"
          class="action-card"
          color="primary"
          theme="dark"
        >
          <v-card-text class="text-center pa-6">
            <v-icon size="64" class="mb-4">mdi-plus-circle</v-icon>
            <h3 class="text-h6 font-weight-bold mb-2">Crear Activo</h3>
            <p class="text-body-2">Registrar nuevo equipo</p>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Editar Activo -->
      <v-col cols="12" sm="6" md="4">
        <v-card 
          hover 
          @click="router.push({ name: 'technician-edit-search' })"
          class="action-card"
          color="info"
          theme="dark"
        >
          <v-card-text class="text-center pa-6">
            <v-icon size="64" class="mb-4">mdi-pencil</v-icon>
            <h3 class="text-h6 font-weight-bold mb-2">Editar Activo</h3>
            <p class="text-body-2">Modificar información</p>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Imprimir Etiquetas -->
      <v-col cols="12" sm="6" md="4">
        <v-card 
          hover 
          @click="router.push({ name: 'technician-print' })"
          class="action-card"
          color="success"
          theme="dark"
        >
          <v-card-text class="text-center pa-6">
            <v-icon size="64" class="mb-4">mdi-printer</v-icon>
            <h3 class="text-h6 font-weight-bold mb-2">Imprimir Etiquetas</h3>
            <p class="text-body-2">Generar etiquetas QR</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Historial y Consultas -->
    <h2 class="text-h5 font-weight-bold mt-8 mb-4">
      <v-icon class="mr-2">mdi-history</v-icon>
      Historial y Consultas
    </h2>
    <v-row>
      <!-- Historial de Movimientos -->
      <v-col cols="12" sm="6" md="4">
        <v-card hover @click="router.push({ name: 'TecnicoHistorial' })">
          <v-card-text class="text-center pa-4">
            <v-icon size="48" color="primary" class="mb-2">mdi-history</v-icon>
            <h4 class="text-subtitle-1 font-weight-bold">Mis Movimientos</h4>
            <p class="text-caption text-medium-emphasis">Ver historial</p>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Inventario -->
      <v-col cols="12" sm="6" md="4">
        <v-card hover @click="router.push({ name: 'asset-list' })">
          <v-card-text class="text-center pa-4">
            <v-icon size="48" color="primary" class="mb-2">mdi-package-variant</v-icon>
            <h4 class="text-subtitle-1 font-weight-bold">Inventario</h4>
            <p class="text-caption text-medium-emphasis">Consultar activos</p>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Otros -->
      <v-col cols="12" sm="6" md="4">
        <v-card hover @click="router.push({ name: 'TecnicoOtros' })">
          <v-card-text class="text-center pa-4">
            <v-icon size="48" color="primary" class="mb-2">mdi-dots-horizontal</v-icon>
            <h4 class="text-subtitle-1 font-weight-bold">Otras Opciones</h4>
            <p class="text-caption text-medium-emphasis">Más funciones</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Info Card -->
    <v-row class="mt-6">
      <v-col cols="12">
        <v-alert 
          type="info" 
          variant="tonal"
          border="start"
          prominent
        >
          <v-alert-title class="text-h6 mb-2">
            <v-icon class="mr-2">mdi-information</v-icon>
            Tip del día
          </v-alert-title>
          <div>
            Utiliza el escáner QR para un registro rápido de movimientos de equipos.
            Cada activo tiene un código único que puedes escanear desde tu dispositivo móvil.
          </div>
        </v-alert>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { useRouter } from 'vue-router'

// ============================================================================
// COMPOSABLES
// ============================================================================

const router = useRouter()
</script>

<style scoped>
.main-action-card {
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.main-action-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3) !important;
}

.action-card {
  cursor: pointer;
  transition: transform 0.2s ease-in-out;
  height: 100%;
}

.action-card:hover {
  transform: translateY(-4px);
}

.v-card {
  cursor: pointer;
  transition: all 0.2s ease-in-out;
}

.v-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15) !important;
}
</style>

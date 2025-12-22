<template>
  <v-container fluid class="pa-6">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-h4 font-weight-bold mb-2">Panel de Administrador</h1>
      <p class="text-subtitle-1 text-medium-emphasis">Bienvenido al sistema de control de activos hospitalarios</p>
    </div>

    <!-- Accesos Rápidos - Principales -->
        <v-row>
      <!-- Card: Inventario -->
      <v-col cols="12" sm="6" md="4">
        <v-card 
          hover 
          @click="router.push({ name: 'asset-list' })"
          class="dashboard-card"
              color="primary"
          theme="dark"
        >
          <v-card-text class="text-center pa-6">
            <v-icon size="64" class="mb-4">mdi-package-variant</v-icon>
            <h3 class="text-h6 font-weight-bold mb-2">Inventario</h3>
            <p class="text-body-2">Ver todos los activos</p>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Card: Gestión de Activos -->
      <v-col cols="12" sm="6" md="4">
        <v-card 
          hover 
          @click="router.push({ name: 'admin-activos' })"
          class="dashboard-card"
          color="secondary"
          theme="dark"
        >
          <v-card-text class="text-center pa-6">
            <v-icon size="64" class="mb-4">mdi-laptop</v-icon>
            <h3 class="text-h6 font-weight-bold mb-2">Gestión de Activos</h3>
            <p class="text-body-2">Administrar equipos</p>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Card: Gestión de Usuarios -->
      <v-col cols="12" sm="6" md="4">
        <v-card 
          hover 
          @click="router.push({ name: 'admin-usuarios' })"
          class="dashboard-card"
          color="success"
          theme="dark"
        >
          <v-card-text class="text-center pa-6">
            <v-icon size="64" class="mb-4">mdi-account-multiple</v-icon>
            <h3 class="text-h6 font-weight-bold mb-2">Usuarios</h3>
            <p class="text-body-2">Gestionar usuarios</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Sección: Catálogos del Sistema -->
    <h2 class="text-h5 font-weight-bold mt-8 mb-4">
      <v-icon class="mr-2">mdi-cog</v-icon>
      Catálogos del Sistema
    </h2>
    <v-row>
      <!-- Departamentos -->
      <v-col cols="12" sm="6" md="3">
        <v-card hover @click="router.push({ name: 'admin-departamentos' })">
          <v-card-text class="text-center pa-4">
            <v-icon size="48" color="primary" class="mb-2">mdi-office-building</v-icon>
            <h4 class="text-subtitle-1 font-weight-bold">Departamentos</h4>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Ubicaciones -->
      <v-col cols="12" sm="6" md="3">
        <v-card hover @click="router.push({ name: 'admin-ubicaciones' })">
          <v-card-text class="text-center pa-4">
            <v-icon size="48" color="primary" class="mb-2">mdi-map-marker</v-icon>
            <h4 class="text-subtitle-1 font-weight-bold">Ubicaciones</h4>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Tipos de Equipo -->
      <v-col cols="12" sm="6" md="3">
        <v-card hover @click="router.push({ name: 'admin-tipos-equipo' })">
          <v-card-text class="text-center pa-4">
            <v-icon size="48" color="primary" class="mb-2">mdi-shape</v-icon>
            <h4 class="text-subtitle-1 font-weight-bold">Tipos de Equipo</h4>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Estados de Activos -->
      <v-col cols="12" sm="6" md="3">
        <v-card hover @click="router.push({ name: 'admin-estado-activos' })">
          <v-card-text class="text-center pa-4">
            <v-icon size="48" color="primary" class="mb-2">mdi-tag</v-icon>
            <h4 class="text-subtitle-1 font-weight-bold">Estados</h4>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Roles -->
      <v-col cols="12" sm="6" md="3">
        <v-card hover @click="router.push({ name: 'admin-roles' })">
          <v-card-text class="text-center pa-4">
            <v-icon size="48" color="primary" class="mb-2">mdi-shield-account</v-icon>
            <h4 class="text-subtitle-1 font-weight-bold">Roles</h4>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Sección: Reportes y Auditoría -->
    <h2 class="text-h5 font-weight-bold mt-8 mb-4">
      <v-icon class="mr-2">mdi-chart-bar</v-icon>
      Reportes y Auditoría
    </h2>
    <v-row>
      <!-- Historial -->
      <v-col cols="12" sm="6" md="4">
        <v-card hover @click="router.push({ name: 'admin-historial' })">
          <v-card-text class="text-center pa-4">
            <v-icon size="48" color="info" class="mb-2">mdi-history</v-icon>
            <h4 class="text-subtitle-1 font-weight-bold">Historial</h4>
            <p class="text-caption text-medium-emphasis">Movimientos registrados</p>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Reportes -->
      <v-col cols="12" sm="6" md="4">
        <v-card hover @click="router.push({ name: 'admin-reportes' })">
          <v-card-text class="text-center pa-4">
            <v-icon size="48" color="success" class="mb-2">mdi-chart-bar</v-icon>
            <h4 class="text-subtitle-1 font-weight-bold">Reportes</h4>
            <p class="text-caption text-medium-emphasis">Estadísticas y análisis</p>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Auditoría -->
      <v-col cols="12" sm="6" md="4">
        <v-card hover @click="router.push({ name: 'admin-auditoria' })">
          <v-card-text class="text-center pa-4">
            <v-icon size="48" color="warning" class="mb-2">mdi-file-document-outline</v-icon>
            <h4 class="text-subtitle-1 font-weight-bold">Auditoría</h4>
            <p class="text-caption text-medium-emphasis">Registro de acciones</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Sección: Herramientas -->
    <h2 class="text-h5 font-weight-bold mt-8 mb-4">
      <v-icon class="mr-2">mdi-tools</v-icon>
      Herramientas
    </h2>
    <v-row>
      <!-- Imprimir QR -->
      <v-col cols="12" sm="6" md="4">
        <v-card hover @click="router.push({ name: 'admin-imprimir-qr' })">
          <v-card-text class="text-center pa-4">
            <v-icon size="48" color="primary" class="mb-2">mdi-qrcode</v-icon>
            <h4 class="text-subtitle-1 font-weight-bold">Imprimir QR</h4>
            <p class="text-caption text-medium-emphasis">Generar etiquetas QR</p>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Gestión General -->
      <v-col cols="12" sm="6" md="4">
        <v-card hover @click="router.push({ name: 'AdminGestion' })">
          <v-card-text class="text-center pa-4">
            <v-icon size="48" color="primary" class="mb-2">mdi-cog</v-icon>
            <h4 class="text-subtitle-1 font-weight-bold">Gestión</h4>
            <p class="text-caption text-medium-emphasis">Configuración general</p>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Otros -->
      <v-col cols="12" sm="6" md="4">
        <v-card hover @click="router.push({ name: 'AdminOtros' })">
          <v-card-text class="text-center pa-4">
            <v-icon size="48" color="primary" class="mb-2">mdi-dots-horizontal</v-icon>
            <h4 class="text-subtitle-1 font-weight-bold">Otros</h4>
            <p class="text-caption text-medium-emphasis">Opciones adicionales</p>
          </v-card-text>
        </v-card>
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
.dashboard-card {
  cursor: pointer;
  transition: transform 0.2s ease-in-out;
  height: 100%;
}

.dashboard-card:hover {
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

<template>
  <div class="gestion-entidades-content">
    <!-- ====================================================================
         HEADER
         ==================================================================== -->
    <v-card variant="tonal" color="primary" class="mb-4">
      <v-card-text>
        <h2 class="text-h5 font-weight-bold mb-1">Gestión de Entidades</h2>
        <p class="text-subtitle-1 mb-0">Administra las entidades del sistema</p>
      </v-card-text>
    </v-card>

    <!-- ====================================================================
         GRID DE ENTIDADES
         ==================================================================== -->
    <v-row>
      <v-col
        v-for="(entidad, index) in entidades"
        :key="index"
        cols="12"
        sm="6"
        md="4"
        lg="3"
      >
        <v-card
          class="entidad-card"
          elevation="2"
          @click="navigateTo(entidad.route)"
        >
          <v-card-text class="text-center pa-6">
            <v-avatar
              :color="entidad.color"
              size="64"
              class="mb-4"
            >
              <v-icon size="32" color="white">
                {{ entidad.icon }}
              </v-icon>
            </v-avatar>
            
            <h3 class="text-h6 font-weight-bold mb-2">
              {{ entidad.nombre }}
            </h3>
            
            <p class="text-body-2 text-grey-darken-1 mb-3">
              {{ entidad.descripcion }}
            </p>

            <v-chip
              :color="entidad.color"
              variant="tonal"
              size="small"
            >
              <v-icon start size="16">mdi-database</v-icon>
              {{ entidad.total }} registros
            </v-chip>
          </v-card-text>

          <v-divider></v-divider>

          <v-card-actions class="pa-3">
            <v-btn
              block
              :color="entidad.color"
              variant="text"
            >
              Administrar
              <v-icon end>mdi-arrow-right</v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- ====================================================================
         ACCIONES RÁPIDAS
         ==================================================================== -->
    <v-card class="mt-6">
      <v-card-title class="text-h6 font-weight-bold">
        Acciones Rápidas
      </v-card-title>
      <v-card-text>
        <v-row>
          <v-col cols="12" sm="6" md="4">
            <v-btn
              block
              color="success"
              variant="tonal"
              size="large"
              prepend-icon="mdi-plus-circle"
              @click="accionRapida('crear-activo')"
            >
              Crear Activo
            </v-btn>
          </v-col>
          
          <v-col cols="12" sm="6" md="4">
            <v-btn
              block
              color="primary"
              variant="tonal"
              size="large"
              prepend-icon="mdi-account-plus"
              @click="accionRapida('crear-usuario')"
            >
              Crear Usuario
            </v-btn>
          </v-col>
          
          <v-col cols="12" sm="6" md="4">
            <v-btn
              block
              color="info"
              variant="tonal"
              size="large"
              prepend-icon="mdi-map-marker-plus"
              @click="accionRapida('crear-ubicacion')"
            >
              Crear Ubicación
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup>
/**
 * ============================================================================
 * GESTIÓN DE ENTIDADES - VISTA PRINCIPAL
 * ============================================================================
 *
 * Vista centralizada para acceder a la gestión de todas las entidades del sistema
 */

import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/services/api'

// ============================================================================
// COMPOSABLES
// ============================================================================

const router = useRouter()

// ============================================================================
// STATE
// ============================================================================

const entidades = ref([
  {
    nombre: 'Activos',
    descripcion: 'Gestión de equipos e inventario',
    icon: 'mdi-laptop',
    color: 'blue',
    route: '/admin/activos',
    total: 0,
    apiEndpoint: '/api/activos/'
  },
  {
    nombre: 'Estado Activos',
    descripcion: 'Estados de los activos',
    icon: 'mdi-state-machine',
    color: 'purple',
    route: '/admin/estado-activos',
    total: 0,
    apiEndpoint: '/api/estados-activo/'
  },
  {
    nombre: 'Departamentos',
    descripcion: 'Departamentos de la organización',
    icon: 'mdi-office-building',
    color: 'teal',
    route: '/admin/departamentos',
    total: 0,
    apiEndpoint: '/api/departamentos/'
  },
  {
    nombre: 'Roles',
    descripcion: 'Roles y permisos de usuarios',
    icon: 'mdi-shield-account',
    color: 'orange',
    route: '/admin/roles',
    total: 0,
    apiEndpoint: '/api/roles/'
  },
  {
    nombre: 'Tipos de Equipo',
    descripcion: 'Categorías de equipos',
    icon: 'mdi-devices',
    color: 'indigo',
    route: '/admin/tipos-equipo',
    total: 0,
    apiEndpoint: '/api/tipos-equipo/'
  },
  {
    nombre: 'Ubicaciones',
    descripcion: 'Ubicaciones físicas',
    icon: 'mdi-map-marker',
    color: 'red',
    route: '/admin/ubicaciones',
    total: 0,
    apiEndpoint: '/api/ubicaciones/'
  },
  {
    nombre: 'Usuarios',
    descripcion: 'Usuarios del sistema',
    icon: 'mdi-account-group',
    color: 'green',
    route: '/admin/usuarios',
    total: 0,
    apiEndpoint: '/api/usuarios/'
  }
])

// ============================================================================
// MÉTODOS - NAVEGACIÓN
// ============================================================================

/**
 * Navega a la ruta de gestión de una entidad
 */
function navigateTo(route) {
  router.push(route)
}

/**
 * Ejecuta una acción rápida
 */
function accionRapida(accion) {
  switch (accion) {
    case 'crear-activo':
      router.push('/admin/activos/crear')
      break
    case 'crear-usuario':
      router.push('/admin/usuarios/crear')
      break
    case 'crear-ubicacion':
      router.push('/admin/ubicaciones/crear')
      break
    default:
      console.log('Acción no implementada:', accion)
  }
}

// ============================================================================
// MÉTODOS - API
// ============================================================================

/**
 * Obtiene el total de registros para cada entidad
 */
async function cargarTotales() {
  for (const entidad of entidades.value) {
    try {
      const response = await apiClient.get(entidad.apiEndpoint, {
        params: { page_size: 1 } // Solo necesitamos el count, no los datos
      })
      
      // Intentar obtener el total de diferentes formas según la respuesta de la API
      if (response.data.count !== undefined) {
        entidad.total = response.data.count
      } else if (response.data.results) {
        // Si viene paginado pero sin count, hacer una llamada sin limit
        const fullResponse = await apiClient.get(entidad.apiEndpoint, {
          params: { page_size: 1000 }
        })
        entidad.total = fullResponse.data.results?.length || 0
      } else if (Array.isArray(response.data)) {
        entidad.total = response.data.length
      }
    } catch (error) {
      console.error(`Error al cargar total de ${entidad.nombre}:`, error)
      entidad.total = 0
    }
  }
}

// ============================================================================
// LIFECYCLE HOOKS
// ============================================================================

/**
 * Al montar el componente, cargar los totales
 */
onMounted(async () => {
  await cargarTotales()
})

</script>

<style scoped>
/* ============================================================================
   CONTENEDOR PRINCIPAL
   ============================================================================ */

.gestion-entidades-content {
  min-height: calc(100vh - 112px);
  background: #f5f7fa;
  padding: 1rem;
  padding-bottom: 80px;
}

/* ============================================================================
   TARJETAS DE ENTIDADES
   ============================================================================ */

.entidad-card {
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  height: 100%;
  border-radius: 12px !important;
}

.entidad-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15) !important;
}

.entidad-card:active {
  transform: translateY(-4px);
}

/* ============================================================================
   RESPONSIVE ADJUSTMENTS
   ============================================================================ */

@media (max-width: 600px) {
  .gestion-entidades-content {
    padding: 0.75rem;
  }
}

@media (min-width: 960px) {
  .gestion-entidades-content {
    max-width: 1400px;
    margin: 0 auto;
  }
}
</style>
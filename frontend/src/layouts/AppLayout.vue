<template>
  <v-app>
    <!-- ========================================================================= -->
    <!-- APP BAR - BARRA SUPERIOR (Siempre Visible) -->
    <!-- ========================================================================= -->
    <v-app-bar color="primary" prominent>
      <v-app-bar-title class="text-h5 font-weight-bold">
        ScaHos
      </v-app-bar-title>

      <v-spacer />

      <!-- Botón Logout -->
      <v-btn 
        icon="mdi-logout" 
        @click="handleLogout"
        title="Cerrar sesión"
      />
    </v-app-bar>

    <!-- ========================================================================= -->
    <!-- NAVIGATION DRAWER - MENÚ LATERAL (Solo Escritorio md/lg/xl) -->
    <!-- ========================================================================= -->
    <v-navigation-drawer
      v-if="$vuetify.display.mdAndUp"
      permanent
      color="grey-lighten-4"
    >
      <v-list density="comfortable" nav>
        <v-list-item
          v-for="item in navItems"
          :key="item.to"
          :prepend-icon="item.icon"
          :title="item.title"
          :to="item.to"
          :active="$route.path === item.to"
          color="primary"
        />
      </v-list>
    </v-navigation-drawer>

    <!-- ========================================================================= -->
    <!-- MAIN CONTENT - CONTENIDO PRINCIPAL -->
    <!-- ========================================================================= -->
    <v-main>
      <router-view />
    </v-main>

    <!-- ========================================================================= -->
    <!-- BOTTOM NAVIGATION - NAVEGACIÓN INFERIOR (Solo Móvil xs/sm) -->
    <!-- ========================================================================= -->
    <v-bottom-navigation
      v-if="$vuetify.display.smAndDown"
      grow
      color="primary"
      :model-value="currentRoute"
    >
      <v-btn
        v-for="item in navItems"
        :key="item.to"
        :value="item.to"
        :to="item.to"
      >
        <v-icon>{{ item.icon }}</v-icon>
        <span>{{ item.title }}</span>
      </v-btn>
    </v-bottom-navigation>
  </v-app>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// ============================================================================
// COMPOSABLES
// ============================================================================

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

// ============================================================================
// COMPUTED - NAVEGACIÓN DINÁMICA POR ROL
// ============================================================================

/**
 * Obtiene el path actual para activar el botón correcto en el bottom nav
 */
const currentRoute = computed(() => route.path)

/**
 * Genera los items de navegación según el rol del usuario
 * 
 * CONFIGURACIÓN POR ROL:
 * 
 * TÉCNICO:
 * - Inicio (/tecnico)
 * - Historial (/tecnico/historial)
 * - Otros (/tecnico/otros)
 * 
 * ADMINISTRADOR:
 * - Inicio (/admin)
 * - Gestión (/admin/gestion)
 * - Otros (/admin/otros)
 * 
 * JEFE DE DEPARTAMENTO:
 * - Inicio (/jefe)
 * - Otros (/jefe/otros)
 */
const navItems = computed(() => {
  const role = authStore.userRole

  // =========================================================================
  // TÉCNICO - Navegación
  // =========================================================================
  if (role === 'Técnico') {
    return [
      { 
        title: 'Inicio', 
        icon: 'mdi-home', 
        to: '/tecnico' 
      },
      { 
        title: 'Historial', 
        icon: 'mdi-history', 
        to: '/tecnico/historial' 
      },
      { 
        title: 'Otros', 
        icon: 'mdi-dots-horizontal', 
        to: '/tecnico/otros' 
      }
    ]
  }

  // =========================================================================
  // ADMINISTRADOR - Navegación
  // =========================================================================
  if (role === 'Administrador') {
    return [
      { 
        title: 'Inicio', 
        icon: 'mdi-view-dashboard', 
        to: '/admin' 
      },
      { 
        title: 'Gestión', 
        icon: 'mdi-cog', 
        to: '/admin/gestion' 
      },
      { 
        title: 'Otros', 
        icon: 'mdi-dots-horizontal', 
        to: '/admin/otros' 
      }
    ]
  }

  // =========================================================================
  // JEFE DE DEPARTAMENTO - Navegación
  // =========================================================================
  if (role === 'Jefe de Departamento') {
    return [
      { 
        title: 'Inicio', 
        icon: 'mdi-chart-box', 
        to: '/jefe' 
      },
      { 
        title: 'Otros', 
        icon: 'mdi-dots-horizontal', 
        to: '/jefe/otros' 
      }
    ]
  }

  // Por defecto, retornar array vacío si no hay rol
  return []
})

// ============================================================================
// METHODS - ACCIONES
// ============================================================================

/**
 * Maneja el logout del usuario
 */
function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
/* ============================================================================
   ESTILOS PERSONALIZADOS DEL LAYOUT
   ============================================================================ */

/* Asegurar que el título sea legible en mobile */
.v-app-bar-title {
  letter-spacing: 0.5px;
}

/* Mejorar la apariencia del drawer en desktop */
.v-navigation-drawer {
  border-right: 1px solid rgba(0, 0, 0, 0.05);
}

/* Espaciado más cómodo para los items de navegación */
.v-list-item {
  margin: 4px 8px;
  border-radius: 8px;
}

/* Estilo para el item activo en el drawer */
.v-list-item--active {
  font-weight: 500;
}

/* Bottom navigation - mejor legibilidad */
.v-bottom-navigation .v-btn {
  flex-direction: column;
  gap: 4px;
}

.v-bottom-navigation .v-btn span {
  font-size: 0.75rem;
  text-transform: capitalize;
}
</style>

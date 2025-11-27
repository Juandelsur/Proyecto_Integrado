import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
    // ========================================================================
    // RUTAS DE ACTIVOS
    // ========================================================================
    {
      path: '/activos',
      name: 'asset-list',
      component: () => import('../views/AssetListView.vue'),
      meta: {
        title: 'Lista de Activos',
        requiresAuth: true
      }
    },
    {
      path: '/activos/:id',
      name: 'asset-detail',
      component: () => import('../views/AssetDetailView.vue'),
      meta: {
        title: 'Detalle de Activo',
        requiresAuth: true
      }
    },
    {
      path: '/activos/:id/editar',
      name: 'asset-edit',
      component: () => import('../views/AssetEditView.vue'),
      meta: {
        title: 'Editar Activo',
        requiresAuth: true,
        requiresPermission: 'canEditAssets'
      }
    },
    {
      path: '/activos/nuevo',
      name: 'asset-create',
      component: () => import('../views/AssetCreateView.vue'),
      meta: {
        title: 'Crear Activo',
        requiresAuth: true,
        requiresPermission: 'canEditAssets'
      }
    },
    {
      path: '/activos/:id/movilizar',
      name: 'asset-move',
      component: () => import('../views/AssetMoveView.vue'),
      meta: {
        title: 'Movilizar Activo',
        requiresAuth: true,
        requiresPermission: 'canMoveAssets'
      }
    },
    // ========================================================================
    // RUTA DE IMPRESIÓN DE QRS
    // ========================================================================
    {
      path: '/imprimir-etiquetas',
      name: 'print-qrs',
      component: () => import('../views/PrintQRsView.vue'),
      meta: {
        title: 'Imprimir Etiquetas QR',
        requiresAuth: true,
        requiresPermission: 'canPrintLabels'
      }
    },
    // ========================================================================
    // RUTAS DEL TÉCNICO
    // ========================================================================
    {
      path: '/tecnico/home',
      name: 'technician-home',
      component: () => import('../views/technician/HomeView.vue'),
      meta: {
        title: 'Home - Técnico',
        requiresAuth: true,
        requiresRole: 'Técnico'
      }
    },
    {
      path: '/escanear',
      name: 'scan-qr',
      component: () => import('../views/technician/ScannerView.vue'),
      meta: {
        title: 'Escanear QR',
        requiresAuth: true
      }
    },
    {
      path: '/confirmar-equipo/:id',
      name: 'confirm-asset',
      component: () => import('../views/technician/ConfirmAssetView.vue'),
      meta: {
        title: 'Confirmar Equipo',
        requiresAuth: true
      }
    },
    {
      path: '/registro-exitoso',
      name: 'movement-success',
      component: () => import('../views/technician/MovementSuccessView.vue'),
      meta: {
        title: 'Registro Exitoso',
        requiresAuth: true
      }
    },
    {
      path: '/historico',
      name: 'history',
      component: () => import('../views/technician/HistoryView.vue'),
      meta: {
        title: 'Histórico',
        requiresAuth: true
      }
    },
    {
      path: '/configuracion',
      name: 'settings',
      component: () => import('../views/technician/SettingsView.vue'),
      meta: {
        title: 'Configuración',
        requiresAuth: true
      }
    },
    // ========================================================================
    // RUTA DE LOGIN
    // ========================================================================
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      meta: {
        title: 'Iniciar Sesión'
      }
    }
  ],
})

// ============================================================================
// NAVIGATION GUARDS (Protección de Rutas)
// ============================================================================

router.beforeEach((to, from, next) => {
  // Importar el store de autenticación
  const { useAuthStore } = require('@/stores/auth')
  const authStore = useAuthStore()

  // Actualizar el título de la página
  document.title = to.meta.title ? `${to.meta.title} - SCA Hospital` : 'SCA Hospital'

  // Verificar si la ruta requiere autenticación
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    // Redirigir al login si no está autenticado
    next({ name: 'login', query: { redirect: to.fullPath } })
    return
  }

  // Verificar permisos específicos
  if (to.meta.requiresPermission) {
    const permission = to.meta.requiresPermission
    if (!authStore[permission]) {
      // Redirigir a home si no tiene el permiso
      alert('❌ No tienes permisos para acceder a esta página.')
      next({ name: 'home' })
      return
    }
  }

  // Verificar rol específico
  if (to.meta.requiresRole) {
    const requiredRole = to.meta.requiresRole
    if (authStore.userRole !== requiredRole) {
      // Redirigir según el rol del usuario
      alert('❌ Esta página es solo para técnicos.')

      if (authStore.isAdmin || authStore.isJefe) {
        next({ name: 'home' })
      } else {
        next({ name: 'home' })
      }
      return
    }
  }

  // Continuar con la navegación
  next()
})

export default router

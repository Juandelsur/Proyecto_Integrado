import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // ========================================================================
    // RUTA RAÍZ - REDIRIGE AL LOGIN
    // ========================================================================
    {
      path: '/',
      redirect: '/login'
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
    },
    // ========================================================================
    // RUTA DE HOME (DASHBOARD PRINCIPAL)
    // ========================================================================
    {
      path: '/home',
      name: 'home',
      component: () => import('../views/HomeView.vue'),
      meta: {
        title: 'Dashboard',
        requiresAuth: true
      }
    },
    // ========================================================================
    // RUTAS DE ACTIVOS (ADMIN)
    // ========================================================================
    {
      path: '/inventario',
      name: 'asset-list',
      component: () => import('../views/admin/AssetListView.vue'),
      meta: {
        title: 'Inventario',
        requiresAuth: true
      }
    },
    {
      path: '/activos/:id',
      name: 'asset-detail',
      component: () => import('../views/admin/AssetDetailView.vue'),
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
      component: () => import('../views/admin/PrintQRsView.vue'),
      meta: {
        title: 'Imprimir Etiquetas QR',
        requiresAuth: true,
        requiresPermission: 'canPrintLabels'
      }
    },
    // ========================================================================
    // RUTAS DEL TÉCNICO (CON LAYOUT)
    // ========================================================================
    {
      path: '/tecnico',
      component: () => import('../layouts/LayoutTecnico.vue'),
      meta: {
        requiresAuth: true,
        requiresRole: 'Técnico'
      },
      children: [
        {
          path: 'home',
          name: 'technician-home',
          component: () => import('../views/technician/HomeView.vue'),
          meta: {
            title: 'Home - Técnico'
          }
        },
        {
          path: 'scan',
          name: 'technician-scan',
          component: () => import('../views/technician/ScannerView.vue'),
          meta: {
            title: 'Escanear QR'
          }
        },
        {
          path: 'history',
          name: 'technician-history',
          component: () => import('../views/technician/TecnicoHistorialView.vue'),
          meta: {
            title: 'Historial de Movimientos'
          }
        },
        {
          path: 'imprimir',
          name: 'technician-print',
          component: () => import('../views/technician/PrintLabelsView.vue'),
          meta: {
            title: 'Imprimir Etiquetas'
          }
        },
        {
          path: 'crear',
          name: 'technician-create',
          component: () => import('../views/technician/CreateAssetView.vue'),
          meta: {
            title: 'Crear Activo'
          }
        },
        {
          path: 'editar-buscar',
          name: 'technician-edit-search',
          component: () => import('../views/technician/EditAssetSearchView.vue'),
          meta: {
            title: 'Editar Activos'
          }
        }
      ]
    },
    // ========================================================================
    // RUTAS DEL TÉCNICO (SIN LAYOUT - COMPATIBILIDAD)
    // ========================================================================
    {
      path: '/escanear',
      name: 'scan-qr',
      component: () => import('../views/technician/ScannerView.vue'),
      meta: {
        title: 'Escanear QR',
        requiresAuth: true
      }
    },
    // ========================================================================
    // RUTA DE PRUEBA - QR SCANNER DEMO (SIN AUTENTICACIÓN PARA TESTING)
    // ========================================================================
    {
      path: '/qr-scanner-demo',
      name: 'qr-scanner-demo',
      component: () => import('../views/technician/QRScannerDemoView.vue'),
      meta: {
        title: 'QR Scanner Demo',
        requiresAuth: false // Sin auth para pruebas
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
    }
  ],
})

// ============================================================================
// NAVIGATION GUARDS (Protección de Rutas)
// ============================================================================

router.beforeEach((to, from, next) => {
  // Obtener el store de autenticación
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
      next('/home')
      return
    }
  }

  // Verificar rol específico
  if (to.meta.requiresRole) {
    const requiredRole = to.meta.requiresRole
    if (authStore.userRole !== requiredRole) {
      // Redirigir según el rol del usuario
      alert('❌ Esta página es solo para técnicos.')
      next('/home')
      return
    }
  }

  // Continuar con la navegación
  next()
})

export default router

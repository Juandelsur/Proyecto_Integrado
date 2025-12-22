import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// ============================================================================
// IMPORTAR LAYOUTS
// ============================================================================

import AppLayout from '@/layouts/AppLayout.vue'

// ============================================================================
// IMPORTAR VISTAS EXISTENTES (TU ARQUITECTURA LIMPIA)
// ============================================================================

// Vistas Públicas
import LoginView from '@/views/LoginView.vue'

// Vistas de Home (Inicio) por Rol
import AdminHome from '@/views/AdminHome.vue'
import TecnicoHome from '@/views/TecnicoHome.vue'
import JefeHome from '@/views/JefeHome.vue'

// Vistas Secundarias - Técnico
import TecnicoHistorial from '@/views/tecnico/HistorialView.vue'
import TecnicoOtros from '@/views/tecnico/OtrosView.vue'

// Vistas Secundarias - Admin
import AdminGestion from '@/views/admin/GestionView.vue'
import AdminOtros from '@/views/admin/OtrosView.vue'

// Vistas Secundarias - Jefe
import JefeOtros from '@/views/jefe/OtrosView.vue'

// ============================================================================
// CONFIGURACIÓN DE RUTAS CON RBAC + RUTAS NUEVAS INTEGRADAS
// ============================================================================

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // ========================================================================
    // RUTA PÚBLICA - LOGIN
    // ========================================================================
    {
      path: '/login',
      name: 'Login',
      component: LoginView,
      meta: {
        title: 'Iniciar Sesión',
        requiresAuth: false,
        public: true
      }
    },

    // ========================================================================
    // RUTA RAÍZ - REDIRIGE AL LOGIN
    // ========================================================================
    {
      path: '/',
      redirect: '/login'
    },

    // ========================================================================
    // RUTAS PROTEGIDAS - ADMINISTRADOR (CON APPLAYOUT)
    // ========================================================================
    {
      path: '/admin',
      component: AppLayout,
      meta: {
        requiresAuth: true,
        requiredRole: 'Administrador'
      },
      children: [
        // ──────────────────────────────────────────────────────────────────
        // RUTAS EXISTENTES (TU ARQUITECTURA LIMPIA)
        // ──────────────────────────────────────────────────────────────────
        {
          path: '',
          name: 'AdminHome',
          component: AdminHome,
          meta: {
            title: 'Inicio - Administrador',
          }
        },
        {
          path: 'gestion',
          name: 'AdminGestion',
          component: AdminGestion,
          meta: {
            title: 'Gestión del Sistema',
          }
        },
        {
          path: 'otros',
          name: 'AdminOtros',
          component: AdminOtros,
          meta: {
            title: 'Otras Opciones',
          }
        },

        // ──────────────────────────────────────────────────────────────────
        // RUTAS NUEVAS - INTEGRADAS DEL ROUTER DE TU AMIGO
        // ──────────────────────────────────────────────────────────────────

        // Gestión de Activos
        {
          path: 'activos',
          name: 'admin-activos',
          component: () => import('@/views/admin/gestion/GestionActivos.vue'),
          meta: {
            title: 'Gestión de Activos',
          }
        },
        {
          path: 'estado-activos',
          name: 'admin-estado-activos',
          component: () => import('@/views/admin/gestion/GestionEstadoActivo.vue'),
          meta: {
            title: 'Gestión de Estados de Activos',
          }
        },

        // Gestión de Catálogos
        {
          path: 'departamentos',
          name: 'admin-departamentos',
          component: () => import('@/views/admin/gestion/GestionDepartamentos.vue'),
          meta: {
            title: 'Gestión de Departamentos',
          }
        },
        {
          path: 'roles',
          name: 'admin-roles',
          component: () => import('@/views/admin/gestion/GestionRoles.vue'),
          meta: {
            title: 'Gestión de Roles',
          }
        },
        {
          path: 'tipos-equipo',
          name: 'admin-tipos-equipo',
          component: () => import('@/views/admin/gestion/GestionTipoEquipo.vue'),
          meta: {
            title: 'Gestión de Tipos de Equipo',
          }
        },
        {
          path: 'ubicaciones',
          name: 'admin-ubicaciones',
          component: () => import('@/views/admin/gestion/GestionUbicaciones.vue'),
          meta: {
            title: 'Gestión de Ubicaciones',
          }
        },
        {
          path: 'usuarios',
          name: 'admin-usuarios',
          component: () => import('@/views/admin/gestion/GestionUsuarios.vue'),
          meta: {
            title: 'Gestión de Usuarios',
          }
        },

        // Reportes y Auditoría
        {
          path: 'historial',
          name: 'admin-historial',
          component: () => import('@/views/admin/HistorialView.vue'),
          meta: {
            title: 'Historial de Movimientos',
          }
        },
        {
          path: 'reportes',
          name: 'admin-reportes',
          component: () => import('@/views/admin/ReportesView.vue'),
          meta: {
            title: 'Reportes',
          }
        },
        {
          path: 'auditoria',
          name: 'admin-auditoria',
          component: () => import('@/views/admin/AuditoriaView.vue'),
          meta: {
            title: 'Auditoría del Sistema',
          }
        },

        // Impresión de QR
        {
          path: 'imprimir-qr',
          name: 'admin-imprimir-qr',
          component: () => import('@/views/ImprimirQrView.vue'),
          meta: {
            title: 'Imprimir Códigos QR',
          }
        },
      ]
    },

    // ========================================================================
    // RUTAS PROTEGIDAS - TÉCNICO (CON APPLAYOUT)
    // ========================================================================
    {
      path: '/tecnico',
      component: AppLayout,
      meta: {
        requiresAuth: true,
        requiredRole: 'Técnico'
      },
      children: [
        // ──────────────────────────────────────────────────────────────────
        // RUTAS EXISTENTES (TU ARQUITECTURA LIMPIA)
        // ──────────────────────────────────────────────────────────────────
        {
          path: '',
          name: 'TecnicoHome',
          component: TecnicoHome,
          meta: {
            title: 'Inicio - Técnico',
          }
        },
        {
          path: 'historial',
          name: 'TecnicoHistorial',
          component: TecnicoHistorial,
          meta: {
            title: 'Historial de Movimientos',
          }
        },
        {
          path: 'otros',
          name: 'TecnicoOtros',
          component: TecnicoOtros,
          meta: {
            title: 'Otras Opciones',
          }
        },

        // ──────────────────────────────────────────────────────────────────
        // RUTAS NUEVAS - INTEGRADAS DEL ROUTER DE TU AMIGO
        // ──────────────────────────────────────────────────────────────────

        // Escanear QR
        {
          path: 'scan',
          name: 'technician-scan',
          component: () => import('@/views/technician/ScannerView.vue'),
          meta: {
            title: 'Escanear QR',
          }
        },

        // Impresión de Etiquetas
        {
          path: 'imprimir',
          name: 'technician-print',
          component: () => import('@/views/technician/PrintLabelsView.vue'),
          meta: {
            title: 'Imprimir Etiquetas',
          }
        },

        // Gestión de Activos (Técnico)
        {
          path: 'crear',
          name: 'technician-create',
          component: () => import('@/views/technician/CreateAssetView.vue'),
          meta: {
            title: 'Crear Activo',
          }
        },
        {
          path: 'editar-buscar',
          name: 'technician-edit-search',
          component: () => import('@/views/technician/EditAssetSearchView.vue'),
          meta: {
            title: 'Editar Activos',
          }
        },

        // Sub-rutas de Activos
        {
          path: 'activos/crear',
          name: 'technician-crear-activo',
          component: () => import('@/views/technician/activos/CrearActivoView.vue'),
          meta: {
            title: 'Crear Activo - Técnico',
          }
        },
        {
          path: 'activos/editar',
          name: 'technician-edit-activo',
          component: () => import('@/views/technician/activos/EditarActivoView.vue'),
          meta: {
            title: 'Editar Activo - Técnico',
          }
        },
      ]
    },

    // ========================================================================
    // RUTAS PROTEGIDAS - JEFE DE DEPARTAMENTO (CON APPLAYOUT)
    // ========================================================================
    {
      path: '/jefe',
      component: AppLayout,
      meta: {
        requiresAuth: true,
        requiredRole: 'Jefe de Departamento'
      },
      children: [
        {
          path: '',
          name: 'JefeHome',
          component: JefeHome,
          meta: {
            title: 'Inicio - Jefe de Departamento',
          }
        },
        {
          path: 'otros',
          name: 'JefeOtros',
          component: JefeOtros,
          meta: {
            title: 'Otras Opciones',
          }
        }
      ]
    },

    // ========================================================================
    // RUTAS COMPARTIDAS - INVENTARIO Y ACTIVOS (ADMIN/TÉCNICO)
    // ========================================================================
    {
      path: '/inventario',
      name: 'asset-list',
      component: () => import('@/views/admin/AssetListView.vue'),
      meta: {
        title: 'Inventario de Activos',
        requiresAuth: true
      }
    },
    {
      path: '/activos/:id',
      name: 'asset-detail',
      component: () => import('@/views/admin/AssetDetailView.vue'),
      meta: {
        title: 'Detalle de Activo',
        requiresAuth: true
      }
    },
    {
      path: '/activos/:id/editar',
      name: 'asset-edit',
      component: () => import('@/views/AssetEditView.vue'),
      meta: {
        title: 'Editar Activo',
        requiresAuth: true,
      }
    },
    {
      path: '/activos/nuevo',
      name: 'asset-create',
      component: () => import('@/views/AssetCreateView.vue'),
      meta: {
        title: 'Crear Activo',
        requiresAuth: true,
      }
    },
    {
      path: '/activos/:id/movilizar',
      name: 'asset-move',
      component: () => import('@/views/AssetMoveView.vue'),
      meta: {
        title: 'Movilizar Activo',
        requiresAuth: true,
      }
    },

    // ========================================================================
    // RUTAS DE IMPRESIÓN
    // ========================================================================
    {
      path: '/imprimir-etiquetas',
      name: 'print-qrs',
      component: () => import('@/views/admin/PrintQRsView.vue'),
      meta: {
        title: 'Imprimir Etiquetas QR',
        requiresAuth: true,
      }
    },

    // ========================================================================
    // RUTAS DE FLUJO - CONFIRMACIÓN Y ÉXITO
    // ========================================================================
    {
      path: '/confirmar-equipo/:id',
      name: 'confirm-asset',
      component: () => import('@/views/technician/MovimientoTecnicoView.vue'),
      meta: {
        title: 'Confirmar Equipo',
        requiresAuth: true
      }
    },
    {
      path: '/registro-exitoso',
      name: 'movement-success',
      component: () => import('@/views/technician/MovementSuccessView.vue'),
      meta: {
        title: 'Registro Exitoso',
        requiresAuth: true
      }
    },

    // ========================================================================
    // RUTAS DE CONFIGURACIÓN
    // ========================================================================
    {
      path: '/configuracion',
      name: 'settings',
      component: () => import('@/views/technician/SettingsView.vue'),
      meta: {
        title: 'Configuración',
        requiresAuth: true
      }
    },

    // ========================================================================
    // RUTAS DE DESARROLLO/TESTING (OPCIONAL - COMENTAR EN PRODUCCIÓN)
    // ========================================================================
    {
      path: '/qr-scanner-demo',
      name: 'qr-scanner-demo',
      component: () => import('@/views/technician/QRScannerDemoView.vue'),
      meta: {
        title: 'QR Scanner Demo',
        requiresAuth: false // Sin auth para pruebas
      }
    },

    // ========================================================================
    // RUTA 404 - NO ENCONTRADA
    // ========================================================================
    {
      path: '/:pathMatch(.*)*',
      redirect: '/login'
    }
  ]
})

// ============================================================================
// NAVIGATION GUARDS - PROTECCIÓN DE RUTAS CON RBAC (TU LÓGICA LIMPIA)
// ============================================================================

router.beforeEach((to, from, next) => {
  // Actualizar el título de la página
  document.title = to.meta.title ? `${to.meta.title} - SCA Hospital` : 'SCA Hospital'

  // Obtener el store de autenticación
  const authStore = useAuthStore()

  console.log('🔍 Router Guard - Navegando a:', to.path)
  console.log('🔍 isAuthenticated:', authStore.isAuthenticated)
  console.log('🔍 userRole:', authStore.userRole)

  // =========================================================================
  // 1. VERIFICAR SI LA RUTA REQUIERE AUTENTICACIÓN
  // =========================================================================

  const requiresAuth = to.meta.requiresAuth

  if (requiresAuth) {
    // Si requiere autenticación, verificar si el usuario está autenticado
    if (!authStore.isAuthenticated) {
      // No está autenticado -> Redirigir al login
      console.warn('⛔ Acceso denegado: Usuario no autenticado')
      return next({
        path: '/login',
        query: { redirect: to.fullPath } // Guardar ruta destino para redirigir después del login
      })
    }

    // ========================================================================
    // 2. VERIFICAR ROLES (RBAC - Role-Based Access Control)
    // ========================================================================

    const requiredRole = to.meta.requiredRole

    if (requiredRole) {
      const userRole = authStore.userRole

      // Verificar si el usuario tiene el rol requerido
      if (userRole !== requiredRole) {
        // No tiene el rol correcto -> Denegar acceso
        console.warn(`⛔ Acceso denegado: Se requiere rol "${requiredRole}", pero el usuario tiene rol "${userRole}"`)

        // Redirigir al panel correcto según su rol
        if (userRole === 'Administrador') {
          return next('/admin')
        } else if (userRole === 'Técnico') {
          return next('/tecnico')
        } else if (userRole === 'Jefe de Departamento') {
          return next('/jefe')
        } else {
          return next('/login')
        }
      }
    }
  }

  // =========================================================================
  // 3. SI ESTÁ AUTENTICADO Y TRATA DE IR AL LOGIN, REDIRIGIR A SU PANEL
  // =========================================================================

  if (to.path === '/login' && authStore.isAuthenticated) {
    const userRole = authStore.userRole

    console.log('✅ Usuario ya autenticado, redirigiendo a su panel...')

    if (userRole === 'Administrador') {
      return next('/admin')
    } else if (userRole === 'Técnico') {
      return next('/tecnico')
    } else if (userRole === 'Jefe de Departamento') {
      return next('/jefe')
    }
  }

  // =========================================================================
  // 4. TODO OK - PERMITIR NAVEGACIÓN
  // =========================================================================

  console.log('✅ Navegación permitida a:', to.path)
  next()
})

// ============================================================================
// EXPORTAR ROUTER
// ============================================================================

export default router


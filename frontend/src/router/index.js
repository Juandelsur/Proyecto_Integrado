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
      component: () => import('../views/HomeViewAdmin.vue'),
      meta: {
        title: 'Dashboard',
        requiresAuth: true,
        requiresRole: ['Administrador']
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
        requiresRole: ['Técnico', 'Administrador']
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
          path: 'mihistorial',
          name: 'tecnico-MiHistorial',
          component: () => import('../views/technician/MiHistorialView.vue'),
          meta: {
            title: 'Mis Movimientos'
          }
        },
        {
          path: 'imprimir',
          name: 'tecnico-imprimir-qr',
          component: () => import('../views/ImprimirQrView.vue'),
          meta: {
            title: 'Imprimir QR - Técnico'
          }
        },
        {
          path: 'activos',
          children: [
            {
              path: 'crear',
              name: 'technician-crear-activo',
              component: () => import('../views/technician/activos/CrearActivoView.vue'),
              meta: {
                title: 'Crear Activo - Técnico'
              }
            },
            {
              path: 'editar/:id',
              name: 'technician-edit-activo',
              component: () => import('../views/technician/activos/EditarActivoAutoView.vue'),
              props: true,
              meta: {
                title: 'Editar Activo - Técnico'
              }
            },
            {
              path: 'actualizar-activo',
              name: 'tecnico-actualizar-activo',
              component: () => import('../views/technician/activos/EditarActivoView.vue'),
              meta: {
                title: 'Actualizar Activo - Técnico'
              }
            },
          ]
        },
        {
          path: 'movimiento-tecnico/:id',
          name: 'movimiento-tecnico-create',
          component: () => import('../views/technician/MovimientoTecnicoView.vue'),
          props: true,
          meta: {
            title: 'Mover Activo - Técnico'
          }
        },
      ]
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
      component: () => import('../views/technician/MovimientoTecnicoView.vue'),
      props: true,
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
      path: '/configuracion',
      name: 'settings',
      component: () => import('../views/technician/SettingsView.vue'),
      meta: {
        title: 'Configuración',
        requiresAuth: true
      }
    },
    // ========================================================================
    // RUTAS DEL JEFE DE DEPARTAMENTO
    // ========================================================================
    {
      path: '/jefe',
      component: () => import('../layouts/LayoutJefe.vue'),
      meta: {
        requiresAuth: true,
        requiresRole: 'Jefe de Departamento'
      },
      children: [
        {
          path: 'home',
          name: 'jefe-home',
          component: () => import('../views/jefe/JefeHome.vue'),
          meta: {
            title: 'Dashboard - Jefe de Departamento'
          }
        },
        {
          path: 'reportes',
          name: 'jefe-reportes',
          component: () => import('../views/jefe/ReportesView.vue'),
          meta: {
            title: 'Reportes - Jefe de Departamento'
          }
        },
        {
          path: 'imprimir-qr',
          name: 'jefe-imprimir-qr',
          component: () => import('../views/ImprimirQrView.vue'),
          meta: {
            title: 'Imprimir QR - Jefe de Departamento'
          }
        }
      ]
    },
    // ========================================================================
    // RUTAS DEL ADMINISTRADOR
    // ========================================================================
    {
      path: '/admin',
      component: () => import('../layouts/LayoutAdministrador.vue'),
      meta: {
        requiresAuth: true,
        requiresRole: 'Administrador'
      },
      children: [
        {
          path: 'home',
          name: 'admin-home',
          component: () => import('../views/admin/HomeView.vue'),
          meta: {
            title: 'Home - Administrador'
          }
        },
        {
          path: 'otros',
          name: 'admin-otros',
          component: () => import('../views/admin/OtherView.vue'),
          meta: {
            title: 'Otros - Administrador'
          }
        },
        {
          path: 'gestion',
          name: 'admin-gestion',
          component: () => import('../views/admin/GestionView.vue'),
          meta: {
            title: 'Gestión - Administrador'
          }
        },
        {
          path: 'activos',
          name: 'admin-activos',
          component: () => import('../views/admin/gestion/GestionActivos.vue'),
          meta: {
            title: 'Gestión Activos'
          }
        },
        {
          path: 'estado-activos',
          name: 'admin-estado-activos',
          component: () => import('../views/admin/gestion/GestionEstadoActivo.vue'),
          meta: {
            title: 'Gestión Estado-Activos'
          }
        },
        {
          path: 'departamentos',
          name: 'admin-departamentos',
          component: () => import('../views/admin/gestion/GestionDepartamentos.vue'),
          meta: {
            title: 'Gestión Departamentos'
          }
        },
        {
          path: 'roles',
          name: 'admin-roles',
          component: () => import('../views/admin/gestion/GestionRoles.vue'),
          meta: {
            title: 'Gestión Roles'
          }
        },
        {
          path: 'tipos-equipo',
          name: 'admin-tipos-equipo',
          component: () => import('../views/admin/gestion/GestionTipoEquipo.vue'),
          meta: {
            title: 'Gestión Tipos de Equipo'
          }
        },
        {
          path: 'ubicaciones',
          name: 'admin-ubicaciones',
          component: () => import('../views/admin/gestion/GestionUbicaciones.vue'),
          meta: {
            title: 'Gestión Ubicaciones'
          }
        },
        {
          path: 'usuarios',
          name: 'admin-usuarios',
          component: () => import('../views/admin/gestion/GestionUsuarios.vue'),
          meta: {
            title: 'Gestión Usuarios'
          }
        },
        {
          path: 'historial',
          name: 'admin-historial',
          component: () => import('../views/admin/HistorialView.vue'),
          meta: {
            title: 'Historial - Administrador'
          }
        },
        {
          path: 'reportes',
          name: 'admin-reportes',
          component: () => import('../views/admin/ReportesView.vue'),
          meta: {
            title: 'Reportes - Administrador'
          }
        },
        {
          path: 'auditoria',
          name: 'admin-auditoria',
          component: () => import('../views/admin/AuditoriaView.vue'),
          meta: {
            title: 'Auditoría - Administrador'
          }
        },
        {
          path: 'imprimir-qr',
          name: 'admin-imprimir-qr',
          component: () => import('../views/ImprimirQrView.vue'),
          meta: {
            title: 'Imprimir QR - Administrador'
          }
        },
      ]
    }
  ],
})

// ============================================================================
// NAVIGATION GUARDS (Protección de Rutas)
// ============================================================================

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  // Actualizar título
  document.title = to.meta.title ? `${to.meta.title} - SCA Hospital` : 'SCA Hospital'

  // 1. Verificar autenticación
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
    return
  }

  // 2. Verificar rol (ahora soporta string o array)
  if (to.meta.requiresRole) {
    const requiredRoles = Array.isArray(to.meta.requiresRole)
      ? to.meta.requiresRole
      : [to.meta.requiresRole]

    if (!requiredRoles.includes(authStore.userRole)) {
      console.warn(`Acceso denegado. Rol requerido: ${requiredRoles.join(' o ')}`)

      // Redirigir según el rol del usuario
      if (authStore.userRole === 'Administrador') {
        next({ name: 'admin-home' })
      } else if (authStore.userRole === 'Técnico') {
        next({ name: 'technician-home' })
      } else if (authStore.userRole === 'Jefe de Departamento') {
        next({ name: 'jefe-home' })
      } else {
        next({ name: 'login' })
      }
      return
    }
  }

  // 3. Verificar permisos específicos
  if (to.meta.requiresPermission) {
    const permission = to.meta.requiresPermission
    if (!authStore[permission]) {
      console.warn(`Permiso denegado: ${permission}`)
      // Redirigir al home correspondiente
      const homeRoute = authStore.userRole === 'Administrador' ? 'admin-home' : 'technician-home'
      next({ name: homeRoute })
      return
    }
  }

  next()
})

export default router

import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// ============================================================================
// IMPORTAR LAYOUT
// ============================================================================

import AppLayout from '@/layouts/AppLayout.vue'

// ============================================================================
// IMPORTAR VISTAS
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
// CONFIGURACIÓN DE RUTAS CON RBAC
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
    // RUTAS PROTEGIDAS CON LAYOUT (RBAC)
    // ========================================================================
    
    // ------------------------------------------------------------------
    // ADMINISTRADOR - Rutas con AppLayout
    // ------------------------------------------------------------------
    {
      path: '/admin',
      component: AppLayout,
      meta: {
        requiresAuth: true,
        requiredRole: 'Administrador'
      },
      children: [
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
        }
      ]
    },

    // ------------------------------------------------------------------
    // TÉCNICO - Rutas con AppLayout
    // ------------------------------------------------------------------
    {
      path: '/tecnico',
      component: AppLayout,
      meta: {
        requiresAuth: true,
        requiredRole: 'Técnico'
      },
      children: [
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
        }
      ]
    },

    // ------------------------------------------------------------------
    // JEFE DE DEPARTAMENTO - Rutas con AppLayout
    // ------------------------------------------------------------------
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
    // RUTA POR DEFECTO - REDIRIGE AL LOGIN
    // ========================================================================
    {
      path: '/',
      redirect: '/login'
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
// NAVIGATION GUARDS - PROTECCIÓN DE RUTAS CON RBAC
// ============================================================================

router.beforeEach((to, from, next) => {
  // Actualizar el título de la página
  document.title = to.meta.title ? `${to.meta.title} - SCA Hospital` : 'SCA Hospital'

  // ✅ CABLE REPARADO: Obtener el store de autenticación
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

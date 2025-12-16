# Arquitectura Frontend V2 - ScaHos (SCA Hospital)

## 📐 Índice

1. [Introducción](#introducción)
2. [App Shell - Layout Principal](#app-shell---layout-principal)
3. [Sistema de Navegación Responsiva](#sistema-de-navegación-responsiva)
4. [Configuración de Rutas](#configuración-de-rutas)
5. [Navegación por Roles (RBAC)](#navegación-por-roles-rbac)
6. [Estructura de Archivos](#estructura-de-archivos)
7. [Flujo de Usuario](#flujo-de-usuario)

---

## 🎯 Introducción

La **Arquitectura V2** introduce un **App Shell** (Layout Principal) que proporciona una experiencia de usuario coherente y profesional en toda la aplicación. Este layout implementa:

- ✅ **Navegación responsiva** adaptada a móvil y escritorio
- ✅ **Sistema basado en roles (RBAC)** con navegación dinámica
- ✅ **Barra superior persistente** con branding y logout
- ✅ **Drawer lateral** para escritorio (md/lg/xl)
- ✅ **Bottom Navigation** para móvil (xs/sm)

---

## 🏗️ App Shell - Layout Principal

### Ubicación
```
src/layouts/AppLayout.vue
```

### Componentes del Layout

#### 1. **App Bar (Barra Superior)**
- **Componente:** `<v-app-bar>`
- **Color:** `primary` (Azul Hospital)
- **Contenido:**
  - **Izquierda:** Logo/Nombre de la app "ScaHos"
  - **Derecha:** Botón de logout (`mdi-logout`)
- **Siempre visible** en todas las pantallas

#### 2. **Navigation Drawer (Menú Lateral)**
- **Componente:** `<v-navigation-drawer>`
- **Visibilidad:** Solo en **pantallas md y superiores** (Desktop/Tablet)
- **Condición:** `v-if="$vuetify.display.mdAndUp"`
- **Modo:** `permanent` (siempre visible cuando aplica)
- **Contenido:** Lista de navegación con iconos y títulos
- **Estilo:** Fondo gris claro con separador

#### 3. **Main Content (Contenido Principal)**
- **Componente:** `<v-main>`
- **Contenido:** `<router-view />` - Renderiza las vistas específicas
- **Área de trabajo principal** donde se cargan las diferentes vistas

#### 4. **Bottom Navigation (Navegación Inferior)**
- **Componente:** `<v-bottom-navigation>`
- **Visibilidad:** Solo en **pantallas sm y menores** (Móvil)
- **Condición:** `v-if="$vuetify.display.smAndDown"`
- **Modo:** `grow` activado (botones ocupan espacio equitativo)
- **Contenido:** Mismo array de navegación que el drawer

---

## 📱 Sistema de Navegación Responsiva

### Breakpoints de Vuetify

| Breakpoint | Tamaño | Navegación Activa |
|-----------|---------|-------------------|
| **xs** | < 600px | Bottom Navigation |
| **sm** | 600-960px | Bottom Navigation |
| **md** | 960-1280px | Navigation Drawer |
| **lg** | 1280-1920px | Navigation Drawer |
| **xl** | > 1920px | Navigation Drawer |

### Lógica de Visualización

```vue
<!-- ESCRITORIO: md/lg/xl -->
<v-navigation-drawer v-if="$vuetify.display.mdAndUp">
  <!-- Menú Lateral -->
</v-navigation-drawer>

<!-- MÓVIL: xs/sm -->
<v-bottom-navigation v-if="$vuetify.display.smAndDown">
  <!-- Navegación Inferior -->
</v-bottom-navigation>
```

### ¿Por qué esta estrategia?

- **Desktop (md+):** El drawer lateral aprovecha el espacio horizontal sin obstruir el contenido
- **Móvil (sm-):** La bottom navigation está al alcance del pulgar y no ocupa espacio vertical valioso

---

## 🗂️ Configuración de Rutas

### Estructura de Rutas con Layout

El router utiliza **rutas anidadas** (nested routes) para aplicar el `AppLayout` como componente padre:

```javascript
{
  path: '/tecnico',
  component: AppLayout,  // 👈 Layout como padre
  meta: {
    requiresAuth: true,
    requiredRole: 'Técnico'
  },
  children: [
    {
      path: '',               // /tecnico
      name: 'TecnicoHome',
      component: TecnicoHome
    },
    {
      path: 'historial',      // /tecnico/historial
      name: 'TecnicoHistorial',
      component: TecnicoHistorial
    },
    {
      path: 'otros',          // /tecnico/otros
      name: 'TecnicoOtros',
      component: TecnicoOtros
    }
  ]
}
```

### Ventajas de las Rutas Anidadas

1. **DRY (Don't Repeat Yourself):** El layout se define una sola vez
2. **Protección centralizada:** Los meta guards se aplican a toda la rama
3. **Transiciones suaves:** Solo cambia el `<router-view />` interno
4. **Mantenibilidad:** Fácil agregar nuevas subrutas

---

## 👥 Navegación por Roles (RBAC)

### Navegación Dinámica

La navegación se genera **dinámicamente** según el rol del usuario:

```javascript
const navItems = computed(() => {
  const role = authStore.userRole
  
  if (role === 'Técnico') {
    return [
      { title: 'Inicio', icon: 'mdi-home', to: '/tecnico' },
      { title: 'Historial', icon: 'mdi-history', to: '/tecnico/historial' },
      { title: 'Otros', icon: 'mdi-dots-horizontal', to: '/tecnico/otros' }
    ]
  }
  
  // ... más roles
})
```

### Configuración por Rol

#### 🔧 TÉCNICO
| Opción | Icono | Ruta |
|--------|-------|------|
| Inicio | `mdi-home` | `/tecnico` |
| Historial | `mdi-history` | `/tecnico/historial` |
| Otros | `mdi-dots-horizontal` | `/tecnico/otros` |

**Funcionalidades:**
- Visualizar activos
- Imprimir etiquetas QR
- Movilizar activos
- Ver historial de movimientos

---

#### 👔 ADMINISTRADOR
| Opción | Icono | Ruta |
|--------|-------|------|
| Inicio | `mdi-view-dashboard` | `/admin` |
| Gestión | `mdi-cog` | `/admin/gestion` |
| Otros | `mdi-dots-horizontal` | `/admin/otros` |

**Funcionalidades:**
- Todas las del técnico +
- Gestionar usuarios
- Eliminar activos
- Configuración del sistema
- Ver auditoría completa

---

#### 📊 JEFE DE DEPARTAMENTO
| Opción | Icono | Ruta |
|--------|-------|------|
| Inicio | `mdi-chart-box` | `/jefe` |
| Otros | `mdi-dots-horizontal` | `/jefe/otros` |

**Funcionalidades:**
- Visualizar activos (solo lectura)
- Ver auditoría y reportes
- Supervisar operaciones

---

## 📂 Estructura de Archivos

```
frontend/src/
├── layouts/
│   └── AppLayout.vue          # 🆕 Layout principal con navegación
│
├── views/
│   ├── LoginView.vue          # Vista pública (sin layout)
│   │
│   ├── TecnicoHome.vue        # Vista principal de Técnico
│   ├── tecnico/
│   │   ├── HistorialView.vue  # 🆕 Subvista: Historial
│   │   └── OtrosView.vue      # 🆕 Subvista: Otros
│   │
│   ├── AdminHome.vue          # Vista principal de Admin
│   ├── admin/
│   │   ├── GestionView.vue    # 🆕 Subvista: Gestión
│   │   └── OtrosView.vue      # 🆕 Subvista: Otros
│   │
│   ├── JefeHome.vue           # Vista principal de Jefe
│   └── jefe/
│       └── OtrosView.vue      # 🆕 Subvista: Otros
│
├── router/
│   └── index.js               # ✏️ Actualizado con rutas anidadas
│
├── stores/
│   └── auth.js                # Store de autenticación (RBAC)
│
└── App.vue                    # Componente raíz (solo <router-view />)
```

---

## 🔄 Flujo de Usuario

### 1. Inicio de Sesión

```
Usuario → LoginView
  ↓
  Ingresa credenciales
  ↓
  authStore.login()
  ↓
  ✅ Éxito → Redirige según rol
  ❌ Error → Muestra mensaje
```

### 2. Navegación Autenticada

```
Ruta protegida (ej: /tecnico)
  ↓
  Router Guard verifica:
  - ✅ ¿Está autenticado? (token válido)
  - ✅ ¿Tiene el rol correcto?
  ↓
  Renderiza AppLayout
  ↓
  AppLayout calcula navItems según rol
  ↓
  Renderiza:
  - App Bar (superior)
  - Navigation Drawer (desktop) O Bottom Nav (mobile)
  - <router-view /> con la vista específica
```

### 3. Cambio de Vista (Dentro de la App)

```
Usuario hace clic en "Historial"
  ↓
  Router navega a /tecnico/historial
  ↓
  AppLayout permanece (no se re-renderiza)
  ↓
  Solo cambia el <router-view /> interno
  ↓
  Se carga HistorialView.vue
```

### 4. Logout

```
Usuario hace clic en botón Logout
  ↓
  handleLogout() en AppLayout
  ↓
  authStore.logout()
  - Limpia tokens
  - Limpia localStorage
  - Resetea estado
  ↓
  router.push('/login')
```

---

## 🎨 Diseño y UX

### Principios de Diseño

1. **Mobile First:** Diseñado primero para móvil, mejorado para desktop
2. **Thumb-Friendly:** Bottom nav al alcance del pulgar en móvil
3. **Consistencia:** Misma navegación en ambos formatos
4. **Accesibilidad:** Iconos + texto para claridad
5. **Performance:** Componentes condicionales (no ocultos)

### Colores del Sistema

| Elemento | Color | Código |
|----------|-------|--------|
| Primary | Azul Hospital | `#1565C0` |
| Secondary | Azul Oscuro | `#0D47A1` |
| Success | Verde | `#4CAF50` |
| Error | Rojo | `#F44336` |
| Warning | Naranja | `#FF9800` |

---

## 🔒 Seguridad (RBAC)

### Capas de Protección

1. **Router Guards:** Verifican autenticación y roles antes de cada navegación
2. **Navegación dinámica:** Solo muestra opciones permitidas por rol
3. **Store de Auth:** Computed properties para permisos (`canManageAssets`, etc.)
4. **Meta tags:** Cada ruta define su rol requerido

### Ejemplo de Protección

```javascript
// Router Guard (router/index.js)
router.beforeEach((to, from, next) => {
  const requiresAuth = to.meta.requiresAuth
  const requiredRole = to.meta.requiredRole
  
  if (requiresAuth && !authStore.isAuthenticated) {
    return next('/login')  // No autenticado
  }
  
  if (requiredRole && authStore.userRole !== requiredRole) {
    return next('/login')  // Rol incorrecto
  }
  
  next()  // Todo OK
})
```

---

## 🚀 Próximos Pasos

### Fase 3 - Funcionalidades Avanzadas

1. **Vistas Funcionales:**
   - Implementar TecnicoHistorial con tabla de movimientos
   - Implementar AdminGestion con CRUD de usuarios
   - Agregar dashboards con estadísticas

2. **Mejoras de UX:**
   - Skeleton loaders durante carga
   - Animaciones de transición entre vistas
   - Notificaciones toast para acciones exitosas

3. **Optimizaciones:**
   - Lazy loading de rutas
   - Caché de datos frecuentes
   - Modo offline con service workers

---

## 📚 Referencias

- [Vuetify 3 - Layout System](https://vuetifyjs.com/en/features/layouts/)
- [Vue Router - Nested Routes](https://router.vuejs.org/guide/essentials/nested-routes.html)
- [Pinia Stores](https://pinia.vuejs.org/)
- [Material Design Icons](https://materialdesignicons.com/)

---

## 📝 Changelog

### v2.0.0 - Layout Principal (16/12/2025)

✨ **Nuevas Características:**
- Componente AppLayout con navegación responsiva
- Navigation Drawer para desktop
- Bottom Navigation para móvil
- Navegación dinámica por roles
- Rutas anidadas para todas las secciones

🔄 **Cambios:**
- Refactorización del router con nested routes
- Reorganización de vistas en subdirectorios por rol

📁 **Archivos Nuevos:**
- `src/layouts/AppLayout.vue`
- `src/views/tecnico/HistorialView.vue`
- `src/views/tecnico/OtrosView.vue`
- `src/views/admin/GestionView.vue`
- `src/views/admin/OtrosView.vue`
- `src/views/jefe/OtrosView.vue`

---

**Autor:** Equipo de Desarrollo ScaHos  
**Fecha:** 16 de Diciembre, 2025  
**Versión:** 2.0.0

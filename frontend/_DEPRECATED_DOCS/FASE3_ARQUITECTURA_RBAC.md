# 🏗️ FASE 3: NUEVA ARQUITECTURA - RBAC & RUTAS PROTEGIDAS

> **Estado**: ✅ **COMPLETADO**  
> **Fecha**: 15 de Diciembre, 2025  
> **Arquitecto**: Sistema de Control de Activos Hospital

---

## 📋 ÍNDICE

1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Arquitectura Implementada](#arquitectura-implementada)
3. [Store de Autenticación (Pinia)](#store-de-autenticación-pinia)
4. [Sistema de Roles (RBAC)](#sistema-de-roles-rbac)
5. [Rutas y Protección](#rutas-y-protección)
6. [Vistas Implementadas](#vistas-implementadas)
7. [Usuarios de Prueba](#usuarios-de-prueba)
8. [Flujo de Autenticación](#flujo-de-autenticación)
9. [Próximos Pasos](#próximos-pasos)

---

## 🎯 RESUMEN EJECUTIVO

En esta fase se ha implementado la **nueva arquitectura frontend** con un sistema completo de **autenticación** y **control de acceso basado en roles (RBAC)**.

### ✅ Logros Principales

- ✅ Store de autenticación con Pinia
- ✅ Sistema RBAC con 3 roles definidos
- ✅ Router con rutas protegidas
- ✅ Navigation Guards (beforeEach)
- ✅ 4 vistas funcionales (Login + 3 paneles de rol)
- ✅ Login simulado para desarrollo
- ✅ Persistencia en localStorage

---

## 🏛️ ARQUITECTURA IMPLEMENTADA

```
frontend/src/
├── stores/
│   └── auth.js              # ⭐ Store de autenticación (Pinia)
├── router/
│   └── index.js             # ⭐ Configuración de rutas con RBAC
├── views/
│   ├── LoginView.vue        # ⭐ Vista de inicio de sesión
│   ├── AdminView.vue        # ⭐ Panel de Administrador
│   ├── TecnicoView.vue      # ⭐ Panel de Técnico
│   └── JefeView.vue         # ⭐ Panel de Jefe de Departamento
└── main.js                  # Configuración de Vue + Pinia + Router
```

### 🔧 Tecnologías Utilizadas

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| Vue 3 | 3.5.22 | Framework frontend |
| Pinia | 3.0.3 | State Management |
| Vue Router | 4.6.3 | Routing con guards |
| Vuetify 3 | 3.11.0 | UI Components |

---

## 🔐 STORE DE AUTENTICACIÓN (PINIA)

**Ubicación**: `src/stores/auth.js`

### State

```javascript
{
  token: String | null,           // JWT Token (simulado)
  refreshToken: String | null,    // Refresh Token (simulado)
  user: Object | null             // Información del usuario
}
```

### Getters (Computed)

| Getter | Tipo | Descripción |
|--------|------|-------------|
| `isAuthenticated` | Boolean | ¿Usuario autenticado? |
| `userRole` | String | Rol del usuario actual |
| `isAdmin` | Boolean | ¿Es Administrador? |
| `isTecnico` | Boolean | ¿Es Técnico? |
| `isJefe` | Boolean | ¿Es Jefe de Departamento? |

### Permisos Funcionales (RBAC)

| Permiso | Descripción | Admin | Técnico | Jefe |
|---------|-------------|-------|---------|------|
| `canPrintLabels` | Imprimir etiquetas QR | ✅ | ✅ | ✅ |
| `canManageAssets` | Gestionar activos | ✅ | ✅ | ❌ |
| `canDeleteAssets` | Eliminar activos | ✅ | ❌ | ❌ |
| `canMoveAssets` | Movilizar activos | ✅ | ✅ | ❌ |
| `canManageUsers` | Gestionar usuarios | ✅ | ❌ | ❌ |
| `canViewAudit` | Ver auditoría | ✅ | ❌ | ✅ |

### Actions

```javascript
// Login simulado (para desarrollo)
await authStore.login(username, password)

// Logout
authStore.logout()

// Obtener información del usuario (preparado para backend real)
await authStore.fetchUserInfo()
```

---

## 👥 SISTEMA DE ROLES (RBAC)

### 1. 👑 ADMINISTRADOR

**Permisos Completos**:
- ✅ Imprimir etiquetas QR
- ✅ Gestionar activos (crear/editar)
- ✅ Eliminar activos
- ✅ Movilizar activos
- ✅ Gestionar usuarios
- ✅ Ver auditoría completa

**Ruta**: `/admin`

---

### 2. 🔧 TÉCNICO

**Permisos Operativos**:
- ✅ Imprimir etiquetas QR
- ✅ Gestionar activos (crear/editar)
- ✅ Movilizar activos
- ❌ Eliminar activos
- ❌ Gestionar usuarios
- ❌ Ver auditoría

**Ruta**: `/tecnico`

---

### 3. 👔 JEFE DE DEPARTAMENTO

**Permisos de Supervisión**:
- ✅ Imprimir etiquetas QR
- ✅ Ver auditoría (supervisión)
- 👁️ Ver activos (solo lectura)
- ❌ Gestionar activos
- ❌ Eliminar activos
- ❌ Movilizar activos
- ❌ Gestionar usuarios

**Ruta**: `/jefe`

---

## 🛣️ RUTAS Y PROTECCIÓN

**Ubicación**: `src/router/index.js`

### Configuración de Rutas

```javascript
const routes = [
  // PÚBLICA
  {
    path: '/login',
    component: LoginView,
    meta: { requiresAuth: false, public: true }
  },

  // PROTEGIDA - ADMINISTRADOR
  {
    path: '/admin',
    component: AdminView,
    meta: { requiresAuth: true, requiredRole: 'Administrador' }
  },

  // PROTEGIDA - TÉCNICO
  {
    path: '/tecnico',
    component: TecnicoView,
    meta: { requiresAuth: true, requiredRole: 'Técnico' }
  },

  // PROTEGIDA - JEFE DE DEPARTAMENTO
  {
    path: '/jefe',
    component: JefeView,
    meta: { requiresAuth: true, requiredRole: 'Jefe de Departamento' }
  }
]
```

### Navigation Guard (beforeEach)

El router implementa un **guard de navegación** que:

1. ✅ **Actualiza el título** de la página
2. ✅ **Verifica autenticación** (token + usuario)
3. ✅ **Valida roles** (RBAC)
4. ✅ **Redirige automáticamente** según rol
5. ✅ **Protege rutas** de accesos no autorizados

```javascript
router.beforeEach((to, from, next) => {
  // 1. Actualizar título
  document.title = to.meta.title 
    ? `${to.meta.title} - SCA Hospital` 
    : 'SCA Hospital'

  const authStore = useAuthStore()

  // 2. Verificar autenticación
  if (to.meta.requiresAuth) {
    if (!authStore.isAuthenticated) {
      return next('/login')
    }

    // 3. Verificar roles (RBAC)
    const requiredRole = to.meta.requiredRole
    const userRole = authStore.userRole

    if (requiredRole && userRole !== requiredRole) {
      // Redirigir a su panel correcto
      return next(getRoleRoute(userRole))
    }
  }

  // 4. Si está autenticado y va al login, redirigir a su panel
  if (to.path === '/login' && authStore.isAuthenticated) {
    return next(getRoleRoute(authStore.userRole))
  }

  next()
})
```

### Flujo de Protección

```
Usuario intenta acceder a /admin
         ↓
¿Está autenticado?
    NO → Redirigir a /login
    SÍ ↓
¿Tiene rol "Administrador"?
    NO → Redirigir a su panel correcto
    SÍ ↓
✅ ACCESO PERMITIDO
```

---

## 🖼️ VISTAS IMPLEMENTADAS

### 1. LoginView.vue

**Características**:
- 📝 Formulario de login con validación
- 🎨 Diseño moderno con Vuetify
- 🔒 Campos: usuario y contraseña
- 🔄 Estados de carga (loading)
- ❌ Manejo de errores
- 💡 Lista de usuarios de prueba visible

**Funcionalidad**:
```javascript
async handleLogin() {
  const result = await authStore.login(username, password)
  
  if (result.success) {
    // Redirigir según rol
    if (role === 'Administrador') router.push('/admin')
    else if (role === 'Técnico') router.push('/tecnico')
    else if (role === 'Jefe de Departamento') router.push('/jefe')
  }
}
```

---

### 2. AdminView.vue

**Características**:
- 👑 Panel completo de administrador
- 📊 Estadísticas: Activos, Usuarios, Ubicaciones, Alertas
- ✅ Lista completa de permisos
- ⚡ 6 Acciones rápidas
- 🎨 Tema rojo/error (rol admin)

---

### 3. TecnicoView.vue

**Características**:
- 🔧 Panel operativo de técnico
- 📊 Estadísticas: Activos asignados, Completados, Pendientes
- ✅ Permisos detallados (con restricciones)
- ⚡ 6 Acciones rápidas
- 📜 Timeline de actividad reciente
- 🎨 Tema azul/info (rol técnico)

---

### 4. JefeView.vue

**Características**:
- 👔 Panel de supervisión
- 📊 Estadísticas del departamento
- ✅ Permisos limitados (supervisión)
- ⚡ 6 Acciones disponibles
- 📈 Resumen de auditoría mensual
- 👥 Actividad del equipo
- 🎨 Tema verde/success (rol jefe)

---

## 👤 USUARIOS DE PRUEBA

### Credenciales de Desarrollo

| Usuario | Contraseña | Rol | Panel |
|---------|-----------|-----|-------|
| `admin` | `admin123` | Administrador | `/admin` |
| `tec` | `tec123` | Técnico | `/tecnico` |
| `jefe` | `jefe123` | Jefe de Departamento | `/jefe` |

### Cómo Probar

```bash
# 1. Iniciar servidor de desarrollo
cd frontend
npm run dev

# 2. Abrir navegador en http://localhost:5173

# 3. Usar credenciales de prueba:
#    - admin / admin123
#    - tec / tec123
#    - jefe / jefe123

# 4. Verificar:
#    ✅ Login funciona
#    ✅ Redirección automática según rol
#    ✅ No se puede acceder a paneles de otros roles
#    ✅ Logout funciona correctamente
```

---

## 🔄 FLUJO DE AUTENTICACIÓN

### Diagrama de Flujo

```
┌─────────────┐
│   INICIO    │
└──────┬──────┘
       │
       v
┌─────────────────┐
│  Usuario abre   │
│  la aplicación  │
└──────┬──────────┘
       │
       v
   ¿Autenticado?
   (verificar token)
       │
   ┌───┴───┐
   │       │
  NO      SÍ
   │       │
   v       v
┌────────┐ ┌──────────────┐
│ LOGIN  │ │ Redirigir a  │
│  VIEW  │ │ panel según  │
└───┬────┘ │     rol      │
    │      └──────────────┘
    v
Ingresa credenciales
    │
    v
authStore.login()
    │
    v
¿Credenciales válidas?
    │
  ┌─┴─┐
  │   │
 NO  SÍ
  │   │
  v   v
ERROR ┌──────────────┐
      │ Guardar token│
      │ Guardar user │
      └──────┬───────┘
             │
             v
      Obtener rol del user
             │
        ┌────┼────┐
        │    │    │
        v    v    v
     /admin  /tecnico  /jefe
        │    │    │
        └────┼────┘
             │
             v
       Panel del Rol
             │
        (Navegación)
             │
    ┌────────┴────────┐
    │                 │
    v                 v
Otras rutas      Cerrar Sesión
    │                 │
    v                 v
beforeEach()     logout()
    │                 │
    v                 v
¿Tiene permisos?   Limpiar state
    │                 │
  ┌─┴─┐               v
  │   │            /login
 NO  SÍ
  │   │
  v   v
Denegar Permitir
  │   │
  v   v
Redirigir Acceder
```

---

## 🚀 PRÓXIMOS PASOS (Fase 4)

### 1. Integración con Backend Real

- [ ] Conectar `authStore.login()` con API real
- [ ] Implementar refresh token automático
- [ ] Manejo de tokens JWT reales
- [ ] Endpoint `/api/usuarios/me/` para obtener info del usuario

### 2. Vistas Funcionales

- [ ] Vista de Gestión de Activos
- [ ] Vista de Impresión de Etiquetas QR
- [ ] Vista de Movilización de Activos
- [ ] Vista de Auditoría
- [ ] Vista de Gestión de Usuarios (solo Admin)

### 3. Scanner QR

- [ ] Integrar componente QRScanner salvado de la Fase 1
- [ ] Crear vista de escaneo
- [ ] Conectar con backend para obtener datos del activo

### 4. Navegación

- [ ] Implementar menú lateral (drawer)
- [ ] Breadcrumbs
- [ ] Menú de usuario (perfil + logout)

### 5. Mejoras de Seguridad

- [ ] Implementar refresh token automático
- [ ] Expiración de sesión
- [ ] Cierre de sesión en todas las pestañas
- [ ] Protección contra CSRF

---

## 📊 MÉTRICAS DE LA FASE 3

| Métrica | Valor |
|---------|-------|
| Archivos creados | 5 |
| Archivos modificados | 1 |
| Líneas de código | ~1,200 |
| Rutas implementadas | 4 |
| Roles definidos | 3 |
| Permisos RBAC | 6 |
| Vistas funcionales | 4 |
| Tiempo estimado | 2-3 horas |

---

## ✅ CHECKLIST DE VALIDACIÓN

### Funcionalidad

- [x] Store de autenticación funciona
- [x] Login simulado funciona
- [x] Roles se asignan correctamente
- [x] Rutas están protegidas
- [x] beforeEach valida permisos
- [x] Redirección automática según rol
- [x] Logout limpia el estado
- [x] Persistencia en localStorage

### UI/UX

- [x] Login tiene diseño moderno
- [x] Cada panel tiene su propio estilo
- [x] Colores identifican roles
- [x] Permisos están claramente visibles
- [x] Estadísticas simuladas
- [x] Acciones rápidas disponibles

### Seguridad

- [x] Rutas protegidas por autenticación
- [x] Rutas protegidas por roles
- [x] No se puede acceder sin token
- [x] No se puede acceder con rol incorrecto
- [x] Redirección a login si no autenticado

---

## 📝 NOTAS TÉCNICAS

### Login Simulado

El login actual es **simulado** para permitir desarrollo sin backend. Para producción:

1. Descomentar el código de login real en `auth.js`
2. Configurar endpoint `/api/auth/token/` en el backend
3. Implementar endpoint `/api/usuarios/me/`
4. Verificar estructura de respuesta del backend

### Persistencia

Los datos se guardan en `localStorage`:
- `access_token`: Token JWT
- `refresh_token`: Refresh token
- `user`: Información del usuario (JSON)

### Estructura de Usuario

```javascript
{
  id: Number,
  username: String,
  email: String,
  rol: {
    id: Number,
    nombre_rol: String  // 'Administrador' | 'Técnico' | 'Jefe de Departamento'
  }
}
```

---

## 🎉 CONCLUSIÓN

La **Fase 3** ha sido completada exitosamente. El sistema ahora cuenta con:

✅ Arquitectura frontend moderna (Vue 3 + Pinia + Vuetify)  
✅ Sistema de autenticación completo  
✅ Control de acceso basado en roles (RBAC)  
✅ Rutas protegidas con navigation guards  
✅ 4 vistas funcionales con diseño moderno  
✅ Login simulado listo para desarrollo  

**El proyecto está listo para la Fase 4**: Implementación de vistas funcionales y conexión con el backend.

---

## 📞 SOPORTE

Para dudas o problemas:
1. Revisar esta documentación
2. Verificar la consola del navegador
3. Revisar los comentarios en el código
4. Consultar documentación de Vue Router y Pinia

---

**Documentación generada**: 15 de Diciembre, 2025  
**Versión**: 1.0.0  
**Estado**: ✅ Producción (Desarrollo)

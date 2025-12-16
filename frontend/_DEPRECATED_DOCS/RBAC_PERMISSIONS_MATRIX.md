# 🔐 Matriz de Permisos RBAC - Frontend

## 📋 Resumen

Documentación completa de la **matriz de permisos basada en roles (RBAC)** implementada en el Auth Store del frontend.

---

## 🎯 Roles del Sistema

El sistema tiene **3 roles principales**:

1. **Administrador** - Acceso total al sistema
2. **Técnico** - Operaciones sobre activos (crear, editar, movilizar, imprimir)
3. **Jefe de Departamento** - Supervisión y consulta (solo lectura + impresión)

---

## 📊 Matriz de Permisos Completa

| Permiso | Administrador | Técnico | Jefe de Departamento |
|---------|---------------|---------|----------------------|
| **Imprimir Etiquetas** | ✅ | ✅ | ✅ |
| **Gestionar Activos** (Crear/Editar) | ✅ | ✅ | ❌ |
| **Eliminar Activos** | ✅ | ❌ | ❌ |
| **Movilizar Activos** | ✅ | ✅ | ❌ |
| **Gestionar Usuarios** | ✅ | ❌ | ❌ |
| **Ver Auditoría** | ✅ | ❌ | ✅ |
| **Ver Activos** (Lectura) | ✅ | ✅ | ✅ |

---

## 🔑 Getters de Rol (Auth Store)

### **Getters Básicos**

```javascript
// Verifica si el usuario está autenticado
const isAuthenticated = computed(() => {
  return !!token.value && !!user.value
})

// Obtiene el nombre del rol
const userRole = computed(() => {
  return user.value?.rol?.nombre_rol || null
})

// Verifica si es Administrador
const isAdmin = computed(() => {
  return userRole.value === 'Administrador'
})

// Verifica si es Técnico
const isTecnico = computed(() => {
  return userRole.value === 'Técnico'
})

// Verifica si es Jefe de Departamento
const isJefe = computed(() => {
  return userRole.value === 'Jefe de Departamento'
})
```

---

## 🛡️ Permisos Funcionales

### **1. canPrintLabels** ✅ TODOS LOS ROLES

```javascript
const canPrintLabels = computed(() => {
  return isAuthenticated.value
})
```

**Descripción:**
- ✅ **Administrador**: Puede imprimir
- ✅ **Técnico**: Puede imprimir
- ✅ **Jefe de Departamento**: Puede imprimir

**Uso en componentes:**
```vue
<button v-if="authStore.canPrintLabels" @click="printLabels">
  Imprimir Etiquetas
</button>
```

**⚠️ CAMBIO IMPORTANTE:**
- **ANTES**: Solo Admin y Técnico podían imprimir
- **AHORA**: TODOS los roles pueden imprimir (incluyendo Jefe)
- **Razón**: Los Jefes necesitan imprimir etiquetas para sus equipos

---

### **2. canManageAssets** ✅ Admin, Técnico

```javascript
const canManageAssets = computed(() => {
  return isAdmin.value || isTecnico.value
})
```

**Descripción:**
- ✅ **Administrador**: Puede crear y editar activos
- ✅ **Técnico**: Puede crear y editar activos
- ❌ **Jefe de Departamento**: Solo lectura

**Uso en componentes:**
```vue
<button v-if="authStore.canManageAssets" @click="createAsset">
  Crear Activo
</button>

<button v-if="authStore.canManageAssets" @click="editAsset">
  Editar Activo
</button>
```

---

### **3. canDeleteAssets** ✅ Solo Admin

```javascript
const canDeleteAssets = computed(() => {
  return isAdmin.value
})
```

**Descripción:**
- ✅ **Administrador**: Puede eliminar activos
- ❌ **Técnico**: NO puede eliminar
- ❌ **Jefe de Departamento**: NO puede eliminar

**Uso en componentes:**
```vue
<button v-if="authStore.canDeleteAssets" @click="deleteAsset" class="btn-danger">
  Eliminar Activo
</button>
```

---

### **4. canMoveAssets** ✅ Admin, Técnico

```javascript
const canMoveAssets = computed(() => {
  return isAdmin.value || isTecnico.value
})
```

**Descripción:**
- ✅ **Administrador**: Puede movilizar activos
- ✅ **Técnico**: Puede movilizar activos
- ❌ **Jefe de Departamento**: NO puede movilizar

**Uso en componentes:**
```vue
<button v-if="authStore.canMoveAssets" @click="moveAsset">
  Movilizar Activo
</button>
```

---

### **5. canManageUsers** ✅ Solo Admin

```javascript
const canManageUsers = computed(() => {
  return isAdmin.value
})
```

**Descripción:**
- ✅ **Administrador**: Puede crear/editar/eliminar usuarios
- ❌ **Técnico**: NO puede gestionar usuarios
- ❌ **Jefe de Departamento**: NO puede gestionar usuarios

**Uso en componentes:**
```vue
<router-link v-if="authStore.canManageUsers" to="/usuarios">
  Gestionar Usuarios
</router-link>
```

---

### **6. canViewAudit** ✅ Admin, Jefe

```javascript
const canViewAudit = computed(() => {
  return isAdmin.value || isJefe.value
})
```

**Descripción:**
- ✅ **Administrador**: Puede ver auditoría completa
- ❌ **Técnico**: NO puede ver auditoría
- ✅ **Jefe de Departamento**: Puede ver auditoría (supervisión)

**Uso en componentes:**
```vue
<router-link v-if="authStore.canViewAudit" to="/auditoria">
  Ver Auditoría
</router-link>
```

---

## 💻 Uso en Componentes Vue

### **Importar el Store**

```javascript
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
```

### **Ejemplo Completo**

```vue
<template>
  <div class="asset-actions">
    <!-- Todos pueden imprimir -->
    <button v-if="authStore.canPrintLabels" @click="printLabels">
      🖨️ Imprimir Etiquetas
    </button>

    <!-- Solo Admin y Técnico pueden editar -->
    <button v-if="authStore.canManageAssets" @click="editAsset">
      ✏️ Editar Activo
    </button>

    <!-- Solo Admin puede eliminar -->
    <button v-if="authStore.canDeleteAssets" @click="deleteAsset">
      🗑️ Eliminar Activo
    </button>

    <!-- Solo Admin y Técnico pueden movilizar -->
    <button v-if="authStore.canMoveAssets" @click="moveAsset">
      🚚 Movilizar Activo
    </button>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

function printLabels() {
  console.log('Imprimiendo etiquetas...')
}

function editAsset() {
  console.log('Editando activo...')
}

function deleteAsset() {
  console.log('Eliminando activo...')
}

function moveAsset() {
  console.log('Movilizando activo...')
}
</script>
```

---

## 🔄 Persistencia del Estado

### **Login y Guardado del Rol**

```javascript
async function login(username, password) {
  try {
    // 1. Obtener tokens
    const response = await apiClient.post('/api/token/', {
      username,
      password
    })
    
    const { access, refresh } = response.data
    
    // 2. Guardar tokens en localStorage
    token.value = access
    refreshToken.value = refresh
    localStorage.setItem('access_token', access)
    localStorage.setItem('refresh_token', refresh)
    
    // 3. Obtener información del usuario (incluyendo rol)
    await fetchUserInfo()
    
    return { success: true }
  } catch (error) {
    return { success: false, message: 'Error al iniciar sesión' }
  }
}

async function fetchUserInfo() {
  try {
    const response = await apiClient.get('/api/usuarios/me/')
    user.value = response.data
    
    // Guardar en localStorage para persistencia
    localStorage.setItem('user', JSON.stringify(response.data))
  } catch (error) {
    console.error('Error al obtener usuario:', error)
  }
}
```

### **Estructura del Usuario en localStorage**

```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@hospital.com",
  "nombre_completo": "Administrador del Sistema",
  "rol": {
    "id_rol": 1,
    "nombre_rol": "Administrador",
    "descripcion": "Acceso total al sistema"
  },
  "is_active": true,
  "is_staff": true
}
```

---

## ✅ Checklist de Implementación

- [x] Getters de rol implementados (`isAdmin`, `isTecnico`, `isJefe`)
- [x] `canPrintLabels` retorna `true` para TODOS los roles autenticados
- [x] `canManageAssets` retorna `true` para Admin y Técnico
- [x] `canDeleteAssets` retorna `true` solo para Admin
- [x] `canMoveAssets` implementado para Admin y Técnico
- [x] `canManageUsers` implementado solo para Admin
- [x] `canViewAudit` implementado para Admin y Jefe
- [x] Persistencia del rol en localStorage
- [x] Documentación completa
- [x] Sin errores de sintaxis

---

## 🎉 Estado

✅ **IMPLEMENTADO Y LISTO PARA PRODUCCIÓN**

La lógica de permisos está centralizada en el Auth Store y lista para ser usada en todos los componentes.

---

**Implementado por:** Senior Frontend Engineer  
**Fecha:** 2025-11-27  
**Archivo:** `frontend/src/stores/auth.js`


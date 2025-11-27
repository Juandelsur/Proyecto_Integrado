# 🖨️ Implementación de Impresión de Etiquetas QR con Control de Roles

## 📋 Resumen Ejecutivo

Se ha implementado un sistema completo de **impresión de etiquetas QR** con **control de visibilidad basado en roles (RBAC)** en el frontend Vue 3.

El sistema permite a **Administradores** y **Técnicos** imprimir etiquetas QR de activos y ubicaciones, mientras que los **Jefes de Departamento** no tienen acceso a esta funcionalidad (solo supervisión).

---

## ✅ Tareas Completadas

### **TAREA 1: Store de Autenticación con Lógica de Permisos** ✅

**Archivo:** `frontend/src/stores/auth.js`

**Características:**
- Store de Pinia con gestión completa de autenticación
- Almacenamiento de token JWT y datos del usuario
- **Getter `canPrintLabels`**: Retorna `true` solo para Admin y Técnico
- Otros permisos: `canEditAssets`, `canDeleteAssets`, `canMoveAssets`, `canManageUsers`
- Métodos: `login()`, `logout()`, `fetchUserInfo()`

**Código clave:**
```javascript
const canPrintLabels = computed(() => {
  return isAdmin.value || isTecnico.value
})
```

---

### **TAREA 2: Vista de Lista de Activos con Botón de Impresión** ✅

**Archivo:** `frontend/src/views/AssetListView.vue`

**Características:**
- Tabla completa de activos con filtros y búsqueda
- **Botón "🖨️ Imprimir Etiquetas"** con `v-if="canPrintLabels"`
- El botón desaparece automáticamente para Jefes
- Al hacer clic, redirige a `/imprimir-etiquetas` con los filtros actuales como query params
- Botón "➕ Nuevo Activo" también con control de permisos (`canEditAssets`)
- Paginación y estados de carga

**Ubicación del botón:**
```vue
<button
  v-if="canPrintLabels"
  @click="goToPrintView"
  class="btn-print"
>
  🖨️ Imprimir Etiquetas
</button>
```

---

### **TAREA 3: Vista de Impresión de QRs** ✅

**Archivo:** `frontend/src/views/PrintQRsView.vue`

**Características:**
- **Diseño de grilla 3 columnas** optimizado para impresión A4
- **Separación clara:** Sección "📦 ACTIVOS" y sección "📍 UBICACIONES"
- **Bordes diferenciados:**
  - Negro (2px dashed) para Activos
  - Azul (2px dashed) para Ubicaciones
- **Límites de seguridad:**
  - Máximo 12 activos (protege el servidor)
  - Máximo 6 ubicaciones (variedad en la hoja)
- **Filtros de URL:** Lee los filtros de la lista y los aplica
- **Campo `qr_url`:** Muestra las imágenes QR desde el backend
- **Controles no imprimibles:** Botones y header con clase `.no-print`
- **Estilos de impresión:** `@media print` optimizado para A4

**Estructura:**
```vue
<div class="qr-grid">
  <div class="qr-card qr-card-activo">  <!-- Borde negro -->
    <img :src="activo.qr_url" />
    <p>{{ activo.marca }} {{ activo.modelo }}</p>
  </div>
</div>

<div class="qr-grid">
  <div class="qr-card qr-card-ubicacion">  <!-- Borde azul -->
    <img :src="ubicacion.qr_url" />
    <p>{{ ubicacion.nombre_ubicacion }}</p>
  </div>
</div>
```

---

### **TAREA 4: Vista de Detalle de Activo con QR** ✅

**Archivo:** `frontend/src/views/AssetDetailView.vue`

**Características:**
- **Imagen QR en grande** en columna derecha (sticky)
- **Botón "⬇️ Descargar / Imprimir QR"** con `v-if="canPrintLabels"`
- Información completa del activo (marca, modelo, serie, estado, ubicación)
- Botones de acción con control de permisos:
  - "✏️ Editar" → `v-if="canEditAssets"`
  - "🚚 Movilizar" → `v-if="canMoveAssets"`
  - "🗑️ Eliminar" → `v-if="canDeleteAssets"`
- Función `downloadQR()` para descargar la imagen
- Diseño responsive con grid 2 columnas

**Código del botón:**
```vue
<button
  v-if="canPrintLabels && activo.qr_url"
  @click="downloadQR"
  class="btn-download"
>
  ⬇️ Descargar / Imprimir QR
</button>
```

---

## 📁 Archivos Creados

### **Stores**
1. ✅ `frontend/src/stores/auth.js` - Store de autenticación con permisos

### **Services**
2. ✅ `frontend/src/services/authService.js` - Servicio de autenticación
3. ✅ `frontend/src/services/ubicacionesService.js` - Servicio de ubicaciones

### **Views**
4. ✅ `frontend/src/views/AssetListView.vue` - Lista de activos con filtros
5. ✅ `frontend/src/views/AssetDetailView.vue` - Detalle de activo con QR
6. ✅ `frontend/src/views/PrintQRsView.vue` - Vista de impresión de etiquetas
7. ✅ `frontend/src/views/LoginView.vue` - Vista de login

### **Router**
8. ✅ `frontend/src/router/index.js` - Rutas actualizadas con guards

### **Documentación**
9. ✅ `frontend/PRINT_QR_IMPLEMENTATION.md` - Este documento

---

## 🎯 Matriz de Visibilidad por Rol

| Elemento | Admin | Técnico | Jefe |
|----------|-------|---------|------|
| **Botón "🖨️ Imprimir Etiquetas"** (Lista) | ✅ | ✅ | ❌ |
| **Ruta `/imprimir-etiquetas`** | ✅ | ✅ | ❌ |
| **Botón "⬇️ Descargar QR"** (Detalle) | ✅ | ✅ | ❌ |
| **Botón "➕ Nuevo Activo"** | ✅ | ✅ | ❌ |
| **Botón "✏️ Editar"** | ✅ | ✅ | ❌ |
| **Botón "🚚 Movilizar"** | ✅ | ✅ | ❌ |
| **Botón "🗑️ Eliminar"** | ✅ | ❌ | ❌ |
| **Ver Activos** | ✅ | ✅ | ✅ |

---

## 🚀 Flujo de Usuario

### **Administrador / Técnico:**
1. Inicia sesión → Redirige a `/activos`
2. Ve la lista de activos con filtros
3. **Ve el botón "🖨️ Imprimir Etiquetas"**
4. Aplica filtros (estado, tipo, búsqueda)
5. Click en "Imprimir Etiquetas"
6. Redirige a `/imprimir-etiquetas?estado=1&tipo=2`
7. Ve la hoja con 12 activos + 6 ubicaciones
8. Click en "🖨️ Imprimir Hoja" → Abre diálogo de impresión
9. Imprime en papel adhesivo A4

### **Jefe de Departamento:**
1. Inicia sesión → Redirige a `/activos`
2. Ve la lista de activos con filtros
3. **NO ve el botón "🖨️ Imprimir Etiquetas"** (oculto)
4. Puede ver detalles de activos
5. **NO ve el botón "Descargar QR"** (oculto)
6. Solo puede consultar información (supervisión)

---

## 🎨 Diseño de Impresión

### **Grilla de 3 Columnas**
```
┌─────────────┬─────────────┬─────────────┐
│   Activo 1  │   Activo 2  │   Activo 3  │
│   [QR IMG]  │   [QR IMG]  │   [QR IMG]  │
│   Dell XPS  │   HP Laser  │   Canon MX  │
│   ID: 001   │   ID: 002   │   ID: 003   │
├─────────────┼─────────────┼─────────────┤
│   Activo 4  │   Activo 5  │   Activo 6  │
│     ...     │     ...     │     ...     │
└─────────────┴─────────────┴─────────────┘
```

### **Bordes Diferenciados**
- **Activos:** `border: 2px dashed #000` (Negro)
- **Ubicaciones:** `border: 2px dashed #3498db` (Azul)

---

## 🔧 Configuración del Router

### **Rutas Protegidas**
```javascript
{
  path: '/imprimir-etiquetas',
  name: 'print-qrs',
  component: () => import('../views/PrintQRsView.vue'),
  meta: {
    requiresAuth: true,
    requiresPermission: 'canPrintLabels'  // Solo Admin y Técnico
  }
}
```

### **Navigation Guard**
```javascript
router.beforeEach((to, from, next) => {
  if (to.meta.requiresPermission) {
    const permission = to.meta.requiresPermission
    if (!authStore[permission]) {
      alert('❌ No tienes permisos para acceder a esta página.')
      next({ name: 'home' })
      return
    }
  }
  next()
})
```

---

## 📊 Integración con Backend

### **Endpoints Utilizados**

1. **Autenticación:**
   - `POST /api/token/` - Login (obtener JWT)
   - `GET /api/usuarios/me/` - Obtener usuario actual

2. **Activos:**
   - `GET /api/activos/` - Listar activos (con filtros)
   - `GET /api/activos/{id}/` - Detalle de activo
   - Campo esperado: `qr_url` (URL de la imagen QR)

3. **Ubicaciones:**
   - `GET /api/ubicaciones/` - Listar ubicaciones
   - Campo esperado: `qr_url` (URL de la imagen QR)

### **Formato de Respuesta Esperado**
```json
{
  "id_activo": 1,
  "marca": "Dell",
  "modelo": "XPS 15",
  "numero_serie": "ABC123",
  "qr_url": "https://backend.com/media/qr/activo_1.png",
  "estado": {
    "nombre_estado": "Operativo"
  },
  "ubicacion_actual": {
    "nombre_ubicacion": "Quirófano 1"
  }
}
```

---

## ✅ Checklist de Implementación

- [x] Store de autenticación creado (`auth.js`)
- [x] Getter `canPrintLabels` implementado
- [x] Vista de lista de activos creada (`AssetListView.vue`)
- [x] Botón de impresión con `v-if="canPrintLabels"`
- [x] Vista de impresión creada (`PrintQRsView.vue`)
- [x] Grilla de 3 columnas implementada
- [x] Bordes diferenciados (Negro/Azul)
- [x] Límites de seguridad (12 activos, 6 ubicaciones)
- [x] Filtros de URL aplicados
- [x] Vista de detalle creada (`AssetDetailView.vue`)
- [x] Botón de descarga QR con control de permisos
- [x] Router actualizado con guards
- [x] Vista de login creada
- [x] Servicios de API creados
- [x] Estilos de impresión optimizados
- [x] Documentación completa

---

## 🎉 Resultado Final

✅ **Sistema completo de impresión de etiquetas QR**  
✅ **Control de visibilidad por roles (RBAC)**  
✅ **Interfaz adaptativa según perfil del usuario**  
✅ **Diseño optimizado para impresión A4**  
✅ **Límites de seguridad implementados**  
✅ **Documentación completa**  

**El sistema está listo para ser integrado con el backend.** 🚀

---

**Implementado por:** Senior Frontend Engineer  
**Fecha:** 2025-11-27  
**Estado:** ✅ COMPLETADO


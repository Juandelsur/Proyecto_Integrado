# Estado del Proyecto Frontend - SCA Hospital

**Fecha de Análisis:** $(date)  
**Tech Lead:** Análisis de transferencia al Arquitecto

---

## 1. Mapa de Vistas Actual

### Vistas Operativas y Funcionales

#### **LoginView.vue** (`/login`)
- ✅ **Estado:** Completamente funcional
- **Funcionalidad:** Autenticación de usuarios con validación de formulario
- **Características:**
  - Formulario de login con campos Usuario y Contraseña
  - Validación de campos requeridos
  - Manejo de errores con alertas
  - Redirección automática según rol después del login
  - Muestra usuarios de prueba en el footer (admin/admin123, tec/tec123, jefe/jefe123)

#### **AdminHome.vue** (`/admin`)
- ✅ **Estado:** Vista creada y operativa visualmente
- **Botones/Acciones presentes:**
  1. **"Gestionar Usuarios"** → `navigateTo('usuarios')` - ⚠️ **LINK MUERTO**
  2. **"Maestro de Activos"** → `navigateTo('activos')` - ⚠️ **LINK MUERTO**
  3. **"Auditoría"** → `navigateTo('auditoria')` - ⚠️ **LINK MUERTO**
- **Nota:** Todos los botones tienen `navigateTo()` implementado pero solo hace `console.log()`, no navegan a ninguna ruta.

#### **TecnicoHome.vue** (`/tecnico`)
- ✅ **Estado:** Vista creada y operativa visualmente
- **Botones/Acciones presentes:**
  1. **"Escanear QR"** (destacado, color secondary) → `navigateTo('scanner')` - ⚠️ **LINK MUERTO**
  2. **"Movimientos"** → `navigateTo('movimientos')` - ⚠️ **LINK MUERTO**
  3. **"Historial"** → `navigateTo('historial')` - ⚠️ **LINK MUERTO** (aunque existe ruta `/tecnico/historial`)
- **Nota:** El botón "Historial" no está conectado a la ruta existente `/tecnico/historial`. Todos los botones usan `navigateTo()` que solo hace `console.log()`.

#### **JefeHome.vue** (`/jefe`)
- ✅ **Estado:** Vista creada y operativa visualmente
- **Botones/Acciones presentes:**
  1. **"Ver Inventario"** → `navigateTo('inventario')` - ⚠️ **LINK MUERTO**
  2. **"Reportes"** → `navigateTo('reportes')` - ⚠️ **LINK MUERTO**
  3. **"Aprobaciones"** → `navigateTo('aprobaciones')` - ⚠️ **LINK MUERTO**
- **Nota:** Todos los botones tienen `navigateTo()` implementado pero solo hace `console.log()`, no navegan a ninguna ruta.

### Vistas Secundarias (Placeholders)

#### **admin/GestionView.vue** (`/admin/gestion`)
- ✅ **Estado:** Vista placeholder creada
- **Funcionalidad:** Solo muestra un mensaje "Vista en desarrollo"
- **Ruta:** ✅ Definida y funcional en el router

#### **admin/OtrosView.vue** (`/admin/otros`)
- ✅ **Estado:** Vista creada
- **Ruta:** ✅ Definida y funcional en el router

#### **tecnico/HistorialView.vue** (`/tecnico/historial`)
- ✅ **Estado:** Vista placeholder creada
- **Funcionalidad:** Solo muestra un mensaje "Vista en desarrollo"
- **Ruta:** ✅ Definida y funcional en el router
- **⚠️ Problema:** El botón "Historial" en `TecnicoHome.vue` no está conectado a esta ruta

#### **tecnico/OtrosView.vue** (`/tecnico/otros`)
- ✅ **Estado:** Vista creada
- **Ruta:** ✅ Definida y funcional en el router

#### **jefe/OtrosView.vue** (`/jefe/otros`)
- ✅ **Estado:** Vista creada
- **Ruta:** ✅ Definida y funcional en el router

---

## 2. Análisis de Conectividad (El Router)

### Rutas Definidas en `router/index.js`

#### ✅ Rutas Funcionales (Componente existe y ruta configurada):
- `/login` → `LoginView.vue` ✅
- `/admin` → `AdminHome.vue` ✅
- `/admin/gestion` → `admin/GestionView.vue` ✅
- `/admin/otros` → `admin/OtrosView.vue` ✅
- `/tecnico` → `TecnicoHome.vue` ✅
- `/tecnico/historial` → `tecnico/HistorialView.vue` ✅
- `/tecnico/otros` → `tecnico/OtrosView.vue` ✅
- `/jefe` → `JefeHome.vue` ✅
- `/jefe/otros` → `jefe/OtrosView.vue` ✅

### ⚠️ Links Muertos (Botones sin ruta funcional)

#### **AdminHome.vue:**
1. **Botón "Gestionar Usuarios"**
   - Llama a: `navigateTo('usuarios')`
   - Ruta esperada: `/admin/usuarios` (NO EXISTE)
   - Componente esperado: `src/views/admin/UsuariosView.vue` o `src/views/admin/UsersList.vue` (NO EXISTE)

2. **Botón "Maestro de Activos"**
   - Llama a: `navigateTo('activos')`
   - Ruta esperada: `/admin/activos` (NO EXISTE)
   - Componente esperado: `src/views/admin/ActivosView.vue` o `src/views/admin/MaestroActivosView.vue` (NO EXISTE)

3. **Botón "Auditoría"**
   - Llama a: `navigateTo('auditoria')`
   - Ruta esperada: `/admin/auditoria` (NO EXISTE)
   - Componente esperado: `src/views/admin/AuditoriaView.vue` (NO EXISTE)

#### **TecnicoHome.vue:**
1. **Botón "Escanear QR"**
   - Llama a: `navigateTo('scanner')`
   - Ruta esperada: `/tecnico/scanner` (NO EXISTE)
   - Componente esperado: `src/views/tecnico/ScannerView.vue` (NO EXISTE)
   - **Nota:** Existe código de QRScanner en `_QR_SAFEZONE/` que podría reutilizarse

2. **Botón "Movimientos"**
   - Llama a: `navigateTo('movimientos')`
   - Ruta esperada: `/tecnico/movimientos` (NO EXISTE)
   - Componente esperado: `src/views/tecnico/MovimientosView.vue` (NO EXISTE)

3. **Botón "Historial"**
   - Llama a: `navigateTo('historial')`
   - **Problema:** La ruta `/tecnico/historial` SÍ EXISTE y el componente `HistorialView.vue` también existe
   - **Solución:** Conectar el botón a `router.push('/tecnico/historial')` o usar el nombre de ruta `'TecnicoHistorial'`

#### **JefeHome.vue:**
1. **Botón "Ver Inventario"**
   - Llama a: `navigateTo('inventario')`
   - Ruta esperada: `/jefe/inventario` (NO EXISTE)
   - Componente esperado: `src/views/jefe/InventarioView.vue` (NO EXISTE)

2. **Botón "Reportes"**
   - Llama a: `navigateTo('reportes')`
   - Ruta esperada: `/jefe/reportes` (NO EXISTE)
   - Componente esperado: `src/views/jefe/ReportesView.vue` (NO EXISTE)

3. **Botón "Aprobaciones"**
   - Llama a: `navigateTo('aprobaciones')`
   - Ruta esperada: `/jefe/aprobaciones` (NO EXISTE)
   - Componente esperado: `src/views/jefe/AprobacionesView.vue` (NO EXISTE)

### Resumen de Links Muertos
- **Total de botones con links muertos:** 8
- **Botones con ruta existente pero no conectados:** 1 (Historial en TecnicoHome)
- **Botones que requieren nueva vista:** 7

---

## 3. Próximos Pasos Técnicos

### Archivos `.vue` Faltantes por Crear

#### **Para Administrador (`src/views/admin/`):**
1. ❌ `src/views/admin/UsuariosView.vue` o `UsersList.vue`
   - Ruta a crear: `/admin/usuarios`
   - Funcionalidad: Gestión CRUD de usuarios del sistema

2. ❌ `src/views/admin/ActivosView.vue` o `MaestroActivosView.vue`
   - Ruta a crear: `/admin/activos`
   - Funcionalidad: Maestro de activos (listado, creación, edición, eliminación)

3. ❌ `src/views/admin/AuditoriaView.vue`
   - Ruta a crear: `/admin/auditoria`
   - Funcionalidad: Visualización de logs de auditoría del sistema

#### **Para Técnico (`src/views/tecnico/`):**
1. ❌ `src/views/tecnico/ScannerView.vue`
   - Ruta a crear: `/tecnico/scanner`
   - Funcionalidad: Escaneo de códigos QR de activos
   - **Nota:** Existe código de referencia en `_QR_SAFEZONE/components/QRScanner.vue` que podría reutilizarse

2. ❌ `src/views/tecnico/MovimientosView.vue`
   - Ruta a crear: `/tecnico/movimientos`
   - Funcionalidad: Crear y gestionar movimientos de activos

3. ✅ `src/views/tecnico/HistorialView.vue` (YA EXISTE pero necesita conexión)
   - Ruta existente: `/tecnico/historial`
   - **Acción:** Conectar el botón "Historial" en `TecnicoHome.vue` a esta ruta

#### **Para Jefe (`src/views/jefe/`):**
1. ❌ `src/views/jefe/InventarioView.vue`
   - Ruta a crear: `/jefe/inventario`
   - Funcionalidad: Visualización del inventario completo de activos

2. ❌ `src/views/jefe/ReportesView.vue`
   - Ruta a crear: `/jefe/reportes`
   - Funcionalidad: Generación y visualización de reportes

3. ❌ `src/views/jefe/AprobacionesView.vue`
   - Ruta a crear: `/jefe/aprobaciones`
   - Funcionalidad: Aprobación/rechazo de movimientos pendientes

### Tareas de Conexión en Archivos Existentes

#### **AdminHome.vue:**
- Actualizar `navigateTo('usuarios')` → `router.push('/admin/usuarios')`
- Actualizar `navigateTo('activos')` → `router.push('/admin/activos')`
- Actualizar `navigateTo('auditoria')` → `router.push('/admin/auditoria')`

#### **TecnicoHome.vue:**
- Actualizar `navigateTo('scanner')` → `router.push('/tecnico/scanner')`
- Actualizar `navigateTo('movimientos')` → `router.push('/tecnico/movimientos')`
- Actualizar `navigateTo('historial')` → `router.push('/tecnico/historial')` o `router.push({ name: 'TecnicoHistorial' })`

#### **JefeHome.vue:**
- Actualizar `navigateTo('inventario')` → `router.push('/jefe/inventario')`
- Actualizar `navigateTo('reportes')` → `router.push('/jefe/reportes')`
- Actualizar `navigateTo('aprobaciones')` → `router.push('/jefe/aprobaciones')`

### Actualizaciones Necesarias en `router/index.js`

Agregar las siguientes rutas hijas en las secciones correspondientes:

```javascript
// En children de /admin:
{
  path: 'usuarios',
  name: 'AdminUsuarios',
  component: () => import('@/views/admin/UsuariosView.vue'),
  meta: { title: 'Gestión de Usuarios' }
},
{
  path: 'activos',
  name: 'AdminActivos',
  component: () => import('@/views/admin/ActivosView.vue'),
  meta: { title: 'Maestro de Activos' }
},
{
  path: 'auditoria',
  name: 'AdminAuditoria',
  component: () => import('@/views/admin/AuditoriaView.vue'),
  meta: { title: 'Auditoría' }
}

// En children de /tecnico:
{
  path: 'scanner',
  name: 'TecnicoScanner',
  component: () => import('@/views/tecnico/ScannerView.vue'),
  meta: { title: 'Escanear QR' }
},
{
  path: 'movimientos',
  name: 'TecnicoMovimientos',
  component: () => import('@/views/tecnico/MovimientosView.vue'),
  meta: { title: 'Movimientos' }
}

// En children de /jefe:
{
  path: 'inventario',
  name: 'JefeInventario',
  component: () => import('@/views/jefe/InventarioView.vue'),
  meta: { title: 'Inventario' }
},
{
  path: 'reportes',
  name: 'JefeReportes',
  component: () => import('@/views/jefe/ReportesView.vue'),
  meta: { title: 'Reportes' }
},
{
  path: 'aprobaciones',
  name: 'JefeAprobaciones',
  component: () => import('@/views/jefe/AprobacionesView.vue'),
  meta: { title: 'Aprobaciones' }
}
```

---

## 4. Árbol de Archivos Relevante

```
sca-hospital/frontend/src/
├── router/
│   └── index.js                    ✅ Router configurado con RBAC
├── views/
│   ├── LoginView.vue               ✅ Funcional
│   ├── AdminHome.vue               ✅ Vista creada (3 links muertos)
│   ├── TecnicoHome.vue             ✅ Vista creada (3 links muertos)
│   ├── JefeHome.vue                ✅ Vista creada (3 links muertos)
│   ├── admin/
│   │   ├── GestionView.vue         ✅ Placeholder (ruta funcional)
│   │   └── OtrosView.vue           ✅ Vista creada (ruta funcional)
│   ├── tecnico/
│   │   ├── HistorialView.vue       ✅ Placeholder (ruta funcional, no conectada)
│   │   └── OtrosView.vue           ✅ Vista creada (ruta funcional)
│   └── jefe/
│       └── OtrosView.vue           ✅ Vista creada (ruta funcional)
├── components/                     ⚠️ VACÍA (no hay componentes reutilizables aún)
├── layouts/
│   └── AppLayout.vue               ✅ Layout principal (usado en rutas protegidas)
├── stores/
│   ├── auth.js                     ✅ Store de autenticación
│   ├── activos.js                  ✅ Store de activos
│   └── counter.js                  ⚠️ Store de ejemplo (posiblemente no usado)
└── services/
    ├── api.js                      ✅ Servicio base de API
    ├── authService.js              ✅ Servicio de autenticación
    ├── activosService.js           ✅ Servicio de activos
    └── ubicacionesService.js       ✅ Servicio de ubicaciones
```

### Archivos Faltantes (Resumen)
- **Total de vistas faltantes:** 7
- **Vistas que necesitan conexión:** 1 (Historial ya existe)
- **Componentes reutilizables:** 0 (carpeta components vacía)

---

## Notas Adicionales

1. **Código de Referencia:** Existe código de QRScanner en `_QR_SAFEZONE/components/QRScanner.vue` que podría reutilizarse para `tecnico/ScannerView.vue`

2. **Patrón de Navegación:** Todas las vistas Home usan el mismo patrón `navigateTo(route)` que solo hace `console.log()`. Necesitan actualizarse para usar `router.push()`.

3. **Layout:** Todas las rutas protegidas usan `AppLayout.vue` como layout padre, lo cual está correctamente configurado.

4. **RBAC:** El router tiene protección por roles correctamente implementada con navigation guards.

5. **Estado de Stores:** Existen stores para `auth` y `activos`, lo que sugiere que la lógica de negocio está parcialmente preparada para las vistas faltantes.

---

**Fin del Documento de Estado**


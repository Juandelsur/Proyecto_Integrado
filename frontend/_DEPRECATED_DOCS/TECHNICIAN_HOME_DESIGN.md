# 🏠 Technician Home - Diseño Mobile First

## 📋 Resumen

Vista principal del **Técnico** con diseño **Mobile First** optimizado para escaneo rápido de códigos QR y registro de movimientos de equipos.

---

## 🎨 Características Visuales

### **1. Header Azul con Nombre del Usuario**

```html
<header class="header-welcome">
  <div class="header-content">
    <div class="welcome-text">
      <p class="greeting">Bienvenido,</p>
      <h1 class="user-name">Juan Muñoz</h1>
    </div>
    <button class="btn-logout">
      <i class="bi bi-box-arrow-right"></i>
    </button>
  </div>
</header>
```

**Características:**
- ✅ Fondo azul corporativo con gradiente
- ✅ Texto "Bienvenido," pequeño (0.95rem)
- ✅ Nombre del usuario grande y bold (2rem → 2.5rem)
- ✅ Botón de logout a la derecha con icono
- ✅ Sombra suave para profundidad

**Estilos:**
```css
background: linear-gradient(135deg, #0d47a1 0%, #1565c0 50%, #1976d2 100%);
color: white;
padding: 2rem 1.5rem;
```

---

### **2. Botón Principal: Registrar Movimiento (Tarjeta Grande con QR)**

```html
<button class="btn-scan">
  <div class="scan-icon">
    <i class="bi bi-qr-code-scan"></i>
  </div>
  <h2 class="scan-title">Registrar Movimiento de Equipo</h2>
  <p class="scan-subtitle">Escanear Código QR</p>
</button>
```

**Características:**
- ✅ Tarjeta GRANDE cuadrada centrada
- ✅ Gradiente azul (#1565c0 → #0d47a1)
- ✅ Icono QR gigante (6rem → 8rem)
- ✅ Título grande y bold
- ✅ Subtexto descriptivo
- ✅ Sombra azul pronunciada
- ✅ Hover: Elevación y sombra más grande
- ✅ Min-height: 320px (mobile) → 400px (desktop)

**Estilos:**
```css
background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%);
border-radius: 24px;
padding: 3rem 2rem;
min-height: 320px;
box-shadow: 0 8px 24px rgba(13, 71, 161, 0.3);
```

**Hover:**
```css
transform: translateY(-4px);
box-shadow: 0 12px 32px rgba(13, 71, 161, 0.4);
```

---

### **3. Botones Secundarios (Histórico y Configuración)**

```html
<div class="secondary-actions">
  <button class="btn-secondary">
    <i class="bi bi-clock-history"></i>
    <span>Histórico</span>
  </button>

  <button class="btn-secondary">
    <i class="bi bi-gear"></i>
    <span>Configuración</span>
  </button>
</div>
```

**Características:**
- ✅ Estilo outline (borde azul, fondo blanco)
- ✅ Iconos a la izquierda
- ✅ Texto descriptivo
- ✅ Hover: Fondo azul, texto blanco
- ✅ Sombra suave
- ✅ Mobile: Apilados verticalmente
- ✅ Tablet+: Lado a lado (flex-direction: row)

**Estilos:**
```css
background: white;
border: 2px solid #0d47a1;
color: #0d47a1;
padding: 1.25rem 1.5rem;
border-radius: 16px;
```

**Hover:**
```css
background: #0d47a1;
color: white;
transform: translateY(-2px);
```

---

## 🔧 Lógica de la Vista

### **Obtener Nombre del Usuario**

```javascript
const userName = computed(() => {
  // Intentar obtener el nombre completo, si no existe usar el username
  return authStore.user?.nombre_completo || authStore.user?.username || 'Usuario'
})
```

**Fuentes de datos (en orden de prioridad):**
1. `authStore.user.nombre_completo` (ej: "Juan Muñoz")
2. `authStore.user.username` (ej: "tecnico1")
3. Fallback: "Usuario"

---

### **Navegación**

```javascript
// Navega a la vista de escaneo QR
function goToScan() {
  router.push('/escanear')
}

// Navega al histórico de movimientos
function goToHistory() {
  router.push('/historico')
}

// Navega a la configuración
function goToSettings() {
  router.push('/configuracion')
}
```

---

### **Logout**

```javascript
function handleLogout() {
  if (confirm('¿Estás seguro de que deseas cerrar sesión?')) {
    authStore.logout()
    router.push('/login')
  }
}
```

**Flujo:**
1. Confirmar con el usuario
2. Llamar a `authStore.logout()` (limpia tokens y user)
3. Redirigir a `/login`

---

## 🛣️ Rutas Agregadas al Router

### **Ruta Principal del Técnico**

```javascript
{
  path: '/tecnico/home',
  name: 'technician-home',
  component: () => import('../views/technician/HomeView.vue'),
  meta: {
    title: 'Home - Técnico',
    requiresAuth: true,
    requiresRole: 'Técnico'
  }
}
```

---

### **Rutas Secundarias**

```javascript
// Escanear QR
{
  path: '/escanear',
  name: 'scan-qr',
  component: () => import('../views/technician/ScanQRView.vue'),
  meta: {
    title: 'Escanear QR',
    requiresAuth: true
  }
}

// Histórico
{
  path: '/historico',
  name: 'history',
  component: () => import('../views/technician/HistoryView.vue'),
  meta: {
    title: 'Histórico',
    requiresAuth: true
  }
}

// Configuración
{
  path: '/configuracion',
  name: 'settings',
  component: () => import('../views/technician/SettingsView.vue'),
  meta: {
    title: 'Configuración',
    requiresAuth: true
  }
}
```

---

## 🔐 Navigation Guard (Protección de Rutas)

### **Verificación de Rol**

```javascript
// Verificar rol específico
if (to.meta.requiresRole) {
  const requiredRole = to.meta.requiresRole
  if (authStore.userRole !== requiredRole) {
    alert('❌ Esta página es solo para técnicos.')
    next({ name: 'home' })
    return
  }
}
```

**Protección:**
- ✅ Solo usuarios con rol "Técnico" pueden acceder a `/tecnico/home`
- ✅ Si un Admin o Jefe intenta acceder, se redirige a `/home`
- ✅ Mensaje de error claro

---

## 📱 Responsive Design (Mobile First)

### **Mobile (< 768px)**

```css
.header-welcome {
  padding: 2rem 1.5rem;
}

.user-name {
  font-size: 2rem;
}

.btn-scan {
  padding: 3rem 2rem;
  min-height: 320px;
}

.scan-icon i {
  font-size: 6rem;
}

.secondary-actions {
  flex-direction: column;
  gap: 1rem;
}
```

---

### **Tablet (≥ 768px)**

```css
.header-welcome {
  padding: 2.5rem 2rem;
}

.user-name {
  font-size: 2.5rem;
}

.btn-scan {
  padding: 4rem 3rem;
  min-height: 380px;
}

.scan-icon i {
  font-size: 7rem;
}

.secondary-actions {
  flex-direction: row;
  gap: 1.5rem;
}
```

---

### **Desktop (≥ 1024px)**

```css
.btn-scan {
  min-height: 400px;
}

.scan-icon i {
  font-size: 8rem;
}

.scan-title {
  font-size: 2rem;
}
```

---

## 🎨 Paleta de Colores

| Elemento | Color | Hex |
|----------|-------|-----|
| **Header Background** | Azul Oscuro → Azul Claro | `#0d47a1` → `#1976d2` |
| **Botón Principal** | Azul Medio → Azul Oscuro | `#1565c0` → `#0d47a1` |
| **Botones Secundarios (Border)** | Azul Oscuro | `#0d47a1` |
| **Botones Secundarios (Hover)** | Azul Oscuro | `#0d47a1` |
| **Fondo Principal** | Gris Claro | `#f5f7fa` |
| **Texto Blanco** | Blanco | `#ffffff` |

---

## 🔤 Tipografía

| Elemento | Tamaño | Peso |
|----------|--------|------|
| **Greeting** | 0.95rem | 400 (Regular) |
| **User Name** | 2rem (mobile) / 2.5rem (tablet+) | 700 (Bold) |
| **Scan Title** | 1.5rem (mobile) / 2rem (desktop) | 700 (Bold) |
| **Scan Subtitle** | 1.1rem (mobile) / 1.2rem (tablet+) | 400 (Regular) |
| **Secondary Buttons** | 1.1rem | 600 (Semi-Bold) |

---

## 📦 Dependencias

### **Bootstrap Icons**

**Iconos usados:**
- `bi-box-arrow-right` (Logout)
- `bi-qr-code-scan` (Escanear QR)
- `bi-clock-history` (Histórico)
- `bi-gear` (Configuración)

---

## ✅ Checklist de Implementación

- [x] Header azul con nombre del usuario
- [x] Botón de logout funcional
- [x] Botón principal grande con icono QR
- [x] Gradiente azul en botón principal
- [x] Hover con elevación
- [x] Botones secundarios estilo outline
- [x] Navegación a `/escanear`, `/historico`, `/configuracion`
- [x] Obtener nombre del usuario desde Auth Store
- [x] Logout con confirmación
- [x] Rutas agregadas al router
- [x] Navigation guard para verificar rol
- [x] Responsive Mobile First
- [x] Sin errores de sintaxis

---

## 🎉 Estado

✅ **IMPLEMENTADO Y LISTO PARA PRODUCCIÓN**

La vista Home del Técnico está completamente funcional con diseño profesional Mobile First.

---

**Implementado por:** Senior Frontend Engineer  
**Fecha:** 2025-11-27  
**Archivo:** `frontend/src/views/technician/HomeView.vue`


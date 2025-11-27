# 🔐 LoginView - Diseño Mobile First con Bootstrap 5

## 📋 Resumen

Vista de login profesional con diseño **Mobile First** basada en la imagen de referencia proporcionada.

---

## 🎨 Características Visuales

### **1. Fondo Azul Corporativo**
```css
background: linear-gradient(135deg, #0d47a1 0%, #1565c0 50%, #1976d2 100%);
```
- Gradiente azul profesional que cubre toda la pantalla
- Colores corporativos: `#0d47a1` (azul oscuro) → `#1976d2` (azul claro)

---

### **2. Tarjeta Central**
```css
background: white;
border-radius: 20px;
padding: 2.5rem 2rem;
box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
```

**Características:**
- ✅ Fondo blanco
- ✅ Bordes redondeados (20px)
- ✅ Sombra suave
- ✅ Centrada vertical y horizontalmente
- ✅ Responsive (max-width: 420px en mobile, 480px en desktop)

---

### **3. Logo e Icono**
```html
<div class="logo-icon">
  <i class="bi bi-chat-square-text-fill"></i>
</div>
<h1 class="app-title">SCA</h1>
<p class="app-subtitle">Sistema de Control de Equipos Informáticos</p>
```

**Características:**
- ✅ Icono Bootstrap Icons (chat-square-text-fill)
- ✅ Fondo azul oscuro (#0d47a1)
- ✅ Tamaño: 80px × 80px (mobile), 90px × 90px (tablet+)
- ✅ Título "SCA" grande y bold (2.5rem → 3rem)
- ✅ Subtítulo descriptivo en gris (#666)

---

### **4. Inputs con Iconos**
```html
<div class="input-group">
  <span class="input-icon">
    <i class="bi bi-person-fill"></i>
  </span>
  <input class="form-control" placeholder="tu@email.com" />
</div>
```

**Características:**
- ✅ Fondo gris claro (#f0f2f5)
- ✅ Bordes suaves (border-radius: 12px)
- ✅ Iconos a la izquierda (person-fill, lock-fill)
- ✅ Padding: 0.875rem con espacio para icono (3rem left)
- ✅ Focus: Fondo blanco + borde azul + sombra suave
- ✅ Placeholder en gris claro (#aaa)

---

### **5. Botón "Ingresar"**
```css
background: #0d47a1;
color: white;
padding: 1rem;
border-radius: 12px;
box-shadow: 0 4px 12px rgba(13, 71, 161, 0.3);
```

**Características:**
- ✅ Ancho completo (w-100)
- ✅ Color azul oscuro (#0d47a1)
- ✅ Texto blanco, bold
- ✅ Sombra azul
- ✅ Hover: Color más claro + elevación
- ✅ Spinner animado durante carga

---

### **6. Footer**
```html
<p>© 2025 Hospital IT Asset Control System</p>
```

**Características:**
- ✅ Texto pequeño (0.85rem)
- ✅ Color gris (#999)
- ✅ Borde superior (#e0e0e0)
- ✅ Centrado

---

## 🔧 Lógica de Autenticación

### **Flujo Completo**

```javascript
1. Usuario ingresa email y password
   ↓
2. Submit del formulario
   ↓
3. POST /api/token/ (obtener tokens JWT)
   ↓
4. Guardar access_token y refresh_token en localStorage
   ↓
5. GET /api/usuarios/me/ (obtener rol del usuario)
   ↓
6. Guardar user en localStorage
   ↓
7. Determinar redirección según rol:
   - Técnico → /tecnico/home
   - Admin/Jefe → /dashboard
   ↓
8. Redirigir al usuario
```

---

### **Código de Autenticación**

```javascript
async function handleLogin() {
  try {
    // 1. Login
    const loginResponse = await apiClient.post('/api/token/', {
      username: email.value,
      password: password.value
    })

    // 2. Guardar tokens
    const { access, refresh } = loginResponse.data
    localStorage.setItem('access_token', access)
    localStorage.setItem('refresh_token', refresh)

    // 3. Obtener usuario
    const userResponse = await apiClient.get('/api/usuarios/me/')
    const userData = userResponse.data
    localStorage.setItem('user', JSON.stringify(userData))

    // 4. Redirigir según rol
    const rolNombre = userData.rol?.nombre_rol
    let redirectPath = '/dashboard'

    if (rolNombre === 'Técnico') {
      redirectPath = '/tecnico/home'
    }

    router.push(redirectPath)
  } catch (error) {
    // Manejo de errores
    errorMessage.value = 'Usuario o contraseña incorrectos'
  }
}
```

---

## 🎯 Redirección por Rol

| Rol | Ruta de Redirección |
|-----|---------------------|
| **Técnico** | `/tecnico/home` |
| **Administrador** | `/dashboard` |
| **Jefe de Departamento** | `/dashboard` |

---

## ❌ Manejo de Errores

### **Errores HTTP**

| Código | Mensaje |
|--------|---------|
| **401** | "Usuario o contraseña incorrectos" |
| **400** | "Por favor, completa todos los campos" |
| **500** | "Error del servidor. Intenta de nuevo más tarde" |
| **Network Error** | "No se pudo conectar con el servidor. Verifica tu conexión" |

### **Visualización**

```html
<div class="alert alert-danger">
  <i class="bi bi-exclamation-triangle-fill me-2"></i>
  {{ errorMessage }}
</div>
```

---

## 📱 Responsive Design (Mobile First)

### **Mobile (< 768px)**
```css
.login-card {
  padding: 2.5rem 2rem;
}

.app-title {
  font-size: 2.5rem;
}

.logo-icon {
  width: 80px;
  height: 80px;
}
```

---

### **Tablet (≥ 768px)**
```css
.login-card {
  padding: 3rem 2.5rem;
}

.app-title {
  font-size: 3rem;
}

.logo-icon {
  width: 90px;
  height: 90px;
}
```

---

### **Desktop (≥ 1024px)**
```css
.login-container {
  max-width: 480px;
}
```

---

## 🎨 Paleta de Colores

| Elemento | Color | Hex |
|----------|-------|-----|
| **Fondo Principal** | Azul Oscuro | `#0d47a1` |
| **Fondo Gradiente** | Azul Medio | `#1565c0` |
| **Fondo Gradiente** | Azul Claro | `#1976d2` |
| **Tarjeta** | Blanco | `#ffffff` |
| **Texto Principal** | Negro | `#1a1a1a` |
| **Texto Secundario** | Gris | `#666666` |
| **Input Background** | Gris Claro | `#f0f2f5` |
| **Placeholder** | Gris Medio | `#aaaaaa` |
| **Footer** | Gris Claro | `#999999` |

---

## 🔤 Tipografía

| Elemento | Tamaño | Peso |
|----------|--------|------|
| **Título "SCA"** | 2.5rem (mobile) / 3rem (tablet+) | 700 (Bold) |
| **Subtítulo** | 0.95rem | 400 (Regular) |
| **Labels** | 0.95rem | 600 (Semi-Bold) |
| **Inputs** | 1rem | 400 (Regular) |
| **Botón** | 1.05rem | 600 (Semi-Bold) |
| **Footer** | 0.85rem | 400 (Regular) |

---

## 📦 Dependencias

### **Bootstrap Icons**
```html
<!-- Agregar en index.html -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">
```

**Iconos usados:**
- `bi-chat-square-text-fill` (Logo)
- `bi-person-fill` (Usuario)
- `bi-lock-fill` (Contraseña)
- `bi-exclamation-triangle-fill` (Error)

---

## ✅ Checklist de Implementación

- [x] Fondo azul corporativo con gradiente
- [x] Tarjeta blanca centrada con sombra
- [x] Logo con icono Bootstrap Icons
- [x] Título "SCA" grande y bold
- [x] Subtítulo descriptivo
- [x] Inputs con fondo gris claro (#f0f2f5)
- [x] Iconos en inputs (person, lock)
- [x] Link "Olvidé mi contraseña"
- [x] Botón "Ingresar" azul oscuro, ancho completo
- [x] Footer con copyright
- [x] Lógica de autenticación con JWT
- [x] Llamada a /api/token/
- [x] Llamada a /api/usuarios/me/
- [x] Redirección según rol
- [x] Manejo de errores
- [x] Spinner de carga
- [x] Responsive Mobile First
- [x] Sin errores de sintaxis

---

## 🎉 Estado

✅ **IMPLEMENTADO Y LISTO PARA PRODUCCIÓN**

La vista de login está completamente funcional con diseño profesional Mobile First.

---

**Implementado por:** Senior Frontend Engineer  
**Fecha:** 2025-11-27  
**Archivo:** `frontend/src/views/LoginView.vue`


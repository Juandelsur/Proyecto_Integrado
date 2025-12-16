# 🧪 INSTRUCCIONES DE PRUEBA - FASE 3

> Guía paso a paso para probar todas las funcionalidades implementadas

---

## 🚀 INICIO

### Paso 1: Abrir Terminal
```bash
cd /Users/juanmunoz/Documents/trae_projects/Proyecto_Integrado/sca-hospital/frontend
```

### Paso 2: Iniciar Servidor de Desarrollo
```bash
npm run dev
```

### Paso 3: Verificar que el Servidor Esté Corriendo
✅ Deberías ver en la terminal:
```
  VITE v7.1.11  ready in XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

### Paso 4: Abrir Navegador
Abre tu navegador en:
```
http://localhost:5173
```

---

## 🧪 TESTS FUNCIONALES

### TEST 1: Login como Administrador ⭐

#### Pasos:
1. Deberías ver la pantalla de login automáticamente
2. Ingresa las credenciales:
   - **Usuario**: `admin`
   - **Contraseña**: `admin123`
3. Haz clic en "Iniciar Sesión"

#### Resultado Esperado ✅
- ✅ Carga por ~0.5 segundos (delay simulado)
- ✅ Redirección automática a `/admin`
- ✅ Se muestra el "Panel de Administrador"
- ✅ Header con fondo rojo y el nombre de usuario "admin"
- ✅ 4 estadísticas visibles (Activos, Usuarios, Ubicaciones, Alertas)
- ✅ Lista de permisos mostrando 6 permisos con ✅
- ✅ 6 botones de acciones rápidas

#### Screenshot Mental:
```
┌─────────────────────────────────────────┐
│ 👑 Panel de Administrador               │
│ Bienvenido, admin            [Logout]   │
├─────────────────────────────────────────┤
│ [156] [12]  [8]   [3]                   │
│ Activos Usuarios Ubic Alertas          │
├─────────────────────────────────────────┤
│ Permisos del Rol: Administrador         │
│ ✅ Imprimir etiquetas                   │
│ ✅ Gestionar activos                    │
│ ... (6 permisos en total)               │
├─────────────────────────────────────────┤
│ [Crear Activo] [Crear Usuario] ...     │
└─────────────────────────────────────────┘
```

---

### TEST 2: Logout y Protección de Rutas 🔒

#### Pasos:
1. En el panel de admin, haz clic en "Cerrar Sesión"
2. Deberías volver al login
3. En la barra de direcciones, escribe manualmente: `http://localhost:5173/admin`
4. Presiona Enter

#### Resultado Esperado ✅
- ✅ Te redirige automáticamente a `/login`
- ✅ No puedes acceder a `/admin` sin estar autenticado
- ✅ La consola del navegador muestra: "⛔ Acceso denegado: Usuario no autenticado"

---

### TEST 3: Login como Técnico 🔧

#### Pasos:
1. En el login, ingresa:
   - **Usuario**: `tec`
   - **Contraseña**: `tec123`
2. Haz clic en "Iniciar Sesión"

#### Resultado Esperado ✅
- ✅ Redirección automática a `/tecnico`
- ✅ Panel de Técnico con fondo azul
- ✅ 3 estadísticas (Asignados, Completados, Pendientes)
- ✅ Lista de permisos mostrando 3 ✅ y 3 ❌
- ✅ Timeline de actividad reciente
- ✅ 6 botones de acciones operativas

#### Screenshot Mental:
```
┌─────────────────────────────────────────┐
│ 🔧 Panel de Técnico                     │
│ Bienvenido, tec              [Logout]   │
├─────────────────────────────────────────┤
│ [23]      [18]        [5]               │
│ Asignados Completados Pendientes        │
├─────────────────────────────────────────┤
│ Permisos del Rol: Técnico               │
│ ✅ Imprimir etiquetas                   │
│ ✅ Gestionar activos                    │
│ ✅ Movilizar activos                    │
│ ❌ Eliminar activos                     │
│ ❌ Gestionar usuarios                   │
│ ❌ Ver auditoría                        │
├─────────────────────────────────────────┤
│ [Crear Activo] [Escanear QR] ...       │
└─────────────────────────────────────────┘
```

---

### TEST 4: Validación de Roles (RBAC) 🛡️

#### Pasos:
1. Estando logueado como `tec` (técnico)
2. En la barra de direcciones, intenta acceder a: `http://localhost:5173/admin`
3. Presiona Enter

#### Resultado Esperado ✅
- ✅ Te redirige automáticamente DE VUELTA a `/tecnico`
- ✅ NO puedes acceder al panel de admin siendo técnico
- ✅ La consola muestra: "⛔ Acceso denegado: Se requiere rol 'Administrador', pero el usuario tiene rol 'Técnico'"

---

### TEST 5: Login como Jefe de Departamento 👔

#### Pasos:
1. Haz logout
2. En el login, ingresa:
   - **Usuario**: `jefe`
   - **Contraseña**: `jefe123`
3. Haz clic en "Iniciar Sesión"

#### Resultado Esperado ✅
- ✅ Redirección automática a `/jefe`
- ✅ Panel de Jefe con fondo verde
- ✅ 4 estadísticas del departamento
- ✅ Lista de permisos mostrando 3 ✅ y 4 ❌
- ✅ Resumen de auditoría mensual
- ✅ Timeline de actividad del equipo
- ✅ 6 botones de acciones de gestión

#### Screenshot Mental:
```
┌─────────────────────────────────────────┐
│ 👔 Panel de Jefe de Departamento        │
│ Bienvenido, jefe             [Logout]   │
├─────────────────────────────────────────┤
│ [45]         [87%]      [7]      [124]  │
│ Activos Depto Eficiencia Técnicos Audit│
├─────────────────────────────────────────┤
│ Permisos del Rol: Jefe de Departamento  │
│ ✅ Imprimir etiquetas                   │
│ ✅ Ver auditoría                        │
│ 👁️ Ver activos (lectura)                │
│ ❌ Gestionar activos                    │
│ ❌ Eliminar activos                     │
│ ... (4 restricciones más)               │
├─────────────────────────────────────────┤
│ [Ver Activos] [Ver Auditoría] ...      │
└─────────────────────────────────────────┘
```

---

### TEST 6: Persistencia en localStorage 💾

#### Pasos:
1. Logueate con cualquier usuario (ej: `admin`)
2. Abre las Developer Tools (F12 o Cmd+Option+I)
3. Ve a la pestaña "Application" → "Local Storage" → `http://localhost:5173`
4. Observa las claves guardadas

#### Resultado Esperado ✅
Deberías ver 3 claves:
- ✅ `access_token`: Token simulado (ej: `mock_access_admin_1702685123456`)
- ✅ `refresh_token`: Refresh token simulado
- ✅ `user`: Objeto JSON con información del usuario

#### Ejemplo:
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@hospital.com",
  "rol": {
    "id": 1,
    "nombre_rol": "Administrador"
  }
}
```

---

### TEST 7: Persistencia Después de Recargar ♻️

#### Pasos:
1. Logueate con cualquier usuario
2. Recarga la página (F5 o Cmd+R)

#### Resultado Esperado ✅
- ✅ NO vuelves al login
- ✅ Sigues en tu panel de rol
- ✅ El estado se mantiene (usuario y token en localStorage)

---

### TEST 8: Validación de Credenciales Incorrectas ❌

#### Pasos:
1. Haz logout
2. En el login, ingresa credenciales incorrectas:
   - **Usuario**: `admin`
   - **Contraseña**: `wrongpassword`
3. Haz clic en "Iniciar Sesión"

#### Resultado Esperado ✅
- ✅ Aparece un alert rojo con el mensaje: "Usuario o contraseña incorrectos"
- ✅ NO redirige a ningún panel
- ✅ El botón vuelve a estado normal (no loading)

---

### TEST 9: Validación de Formulario Vacío ⚠️

#### Pasos:
1. En el login, deja los campos vacíos
2. Haz clic en "Iniciar Sesión"

#### Resultado Esperado ✅
- ✅ Los campos muestran mensaje de error: "Este campo es requerido"
- ✅ NO se envía el formulario
- ✅ NO hay llamada al store

---

### TEST 10: Redirección Automática Desde Login 🔄

#### Pasos:
1. Logueate con `admin` / `admin123`
2. Una vez en el panel de admin, en la URL escribe: `http://localhost:5173/login`
3. Presiona Enter

#### Resultado Esperado ✅
- ✅ Te redirige automáticamente DE VUELTA a `/admin`
- ✅ No puedes volver al login estando autenticado

---

## 🔍 TESTS DE CONSOLA (Developer Tools)

### Test Console 1: Verificar Store de Pinia

#### Pasos:
1. Logueate con cualquier usuario
2. Abre la consola del navegador (F12)
3. Escribe:
```javascript
// Acceder al store desde la consola
const authStore = window.$pinia?.state.value.auth
console.log('User:', authStore?.user)
console.log('Role:', authStore?.user?.rol?.nombre_rol)
console.log('Token:', authStore?.token)
```

#### Resultado Esperado ✅
- ✅ Muestra el objeto usuario
- ✅ Muestra el rol
- ✅ Muestra el token simulado

---

### Test Console 2: Navigation Guard Logs

#### Pasos:
1. Abre la consola del navegador
2. Intenta navegar a una ruta sin estar autenticado

#### Resultado Esperado ✅
Deberías ver logs como:
- `⛔ Acceso denegado: Usuario no autenticado`
- `⛔ Acceso denegado: Se requiere rol "Administrador", pero el usuario tiene rol "Técnico"`

---

## 📱 TESTS DE RESPONSIVE DESIGN

### Test Responsive 1: Mobile (320px - 480px)

#### Pasos:
1. Abre Developer Tools (F12)
2. Activa el modo "Device Toolbar" (Cmd+Shift+M o Ctrl+Shift+M)
3. Selecciona "iPhone SE" o "iPhone 12 Pro"
4. Navega por las diferentes vistas

#### Resultado Esperado ✅
- ✅ Login se ve correctamente en móvil
- ✅ Cards de estadísticas se apilan verticalmente
- ✅ Botones ocupan todo el ancho
- ✅ Texto es legible
- ✅ Sin overflow horizontal

---

### Test Responsive 2: Tablet (768px - 1024px)

#### Pasos:
1. En Device Toolbar, selecciona "iPad" o "iPad Pro"
2. Navega por las vistas

#### Resultado Esperado ✅
- ✅ Layout se adapta correctamente
- ✅ Cards mantienen buen espaciado
- ✅ Botones en 2 columnas

---

## 🎨 TESTS VISUALES

### Test Visual 1: Colores por Rol

#### Verificar:
- ✅ **Admin**: Header rojo (#F44336)
- ✅ **Técnico**: Header azul (#2196F3)
- ✅ **Jefe**: Header verde (#4CAF50)

### Test Visual 2: Iconos

#### Verificar que todos los iconos sean visibles:
- ✅ `mdi-hospital-building` en login
- ✅ `mdi-shield-crown` en admin
- ✅ `mdi-account-wrench` en técnico
- ✅ `mdi-account-tie` en jefe
- ✅ Iconos en cards de estadísticas
- ✅ Iconos en botones de acciones

---

## ⚡ TESTS DE RENDIMIENTO

### Test Perf 1: Tiempo de Login

#### Pasos:
1. Abre la pestaña "Network" en Developer Tools
2. Haz login con cualquier usuario
3. Observa el tiempo

#### Resultado Esperado ✅
- ✅ Login toma ~500ms (delay simulado)
- ✅ Redirección es instantánea
- ✅ No hay llamadas HTTP (login simulado)

### Test Perf 2: Navegación Entre Rutas

#### Pasos:
1. Estando logueado, navega entre diferentes rutas manualmente
2. Observa la velocidad

#### Resultado Esperado ✅
- ✅ Navegación es instantánea (< 100ms)
- ✅ No hay recargas de página
- ✅ Transiciones suaves

---

## 🐛 TESTS DE EDGE CASES

### Edge Case 1: localStorage Bloqueado

#### Pasos:
1. En la consola, ejecuta:
```javascript
localStorage.clear()
```
2. Intenta loguearte

#### Resultado Esperado ✅
- ✅ Login funciona (guarda en localStorage)
- ✅ Redirección funciona

---

### Edge Case 2: Token Corrupto

#### Pasos:
1. En Application → Local Storage, edita manualmente `user` con datos inválidos
2. Recarga la página

#### Resultado Esperado ✅
- ✅ Te redirige al login
- ✅ No hay errores de JavaScript

---

### Edge Case 3: Múltiples Tabs

#### Pasos:
1. Logueate en una tab
2. Abre una nueva tab en la misma URL
3. Haz logout en la primera tab
4. Intenta navegar en la segunda tab

#### Resultado Esperado ⚠️
- ⚠️ La segunda tab NO se sincroniza automáticamente (limitación conocida)
- ⚠️ Debes recargar la segunda tab para ver el logout

---

## ✅ CHECKLIST FINAL

### Funcionalidad Básica
- [ ] Login con admin funciona
- [ ] Login con tec funciona
- [ ] Login con jefe funciona
- [ ] Logout funciona
- [ ] Credenciales incorrectas muestran error
- [ ] Campos vacíos muestran validación

### Protección de Rutas
- [ ] No puedo acceder sin login
- [ ] No puedo acceder con rol incorrecto
- [ ] Redirección automática funciona
- [ ] No puedo volver a login estando autenticado

### Persistencia
- [ ] localStorage guarda token
- [ ] localStorage guarda user
- [ ] Recargar mantiene sesión
- [ ] Logout limpia localStorage

### UI/UX
- [ ] Cada panel tiene su color distintivo
- [ ] Permisos son claros y visibles
- [ ] Estadísticas son legibles
- [ ] Botones funcionan visualmente
- [ ] Responsive funciona en móvil
- [ ] Iconos son visibles

### Performance
- [ ] Login es rápido (~500ms)
- [ ] Navegación es fluida
- [ ] Sin errores en consola
- [ ] Sin warnings en consola

---

## 🎉 SI TODOS LOS TESTS PASAN

**¡FELICIDADES! ✅**

La Fase 3 está completamente funcional y lista para continuar con la Fase 4 (integración con backend real).

---

## 🐛 SI ALGO FALLA

### Troubleshooting

#### Problema: No redirige después del login
**Solución**: 
1. Abre la consola y busca errores
2. Verifica que el store tenga `user` y `token`
3. Limpia localStorage y reintenta

#### Problema: Página en blanco
**Solución**:
1. Verifica que el servidor esté corriendo
2. Revisa la consola por errores de import
3. Intenta `npm install` y `npm run dev` de nuevo

#### Problema: Estilos no cargan
**Solución**:
1. Verifica que Vuetify esté importado en `main.js`
2. Recarga con Cmd+Shift+R (hard reload)

---

## 📞 SOPORTE

Si encuentras algún problema:
1. Revisa la consola del navegador
2. Lee la documentación: `FASE3_ARQUITECTURA_RBAC.md`
3. Verifica `TROUBLESHOOTING.md` si existe

---

**Última actualización**: 15 de Diciembre, 2025  
**Versión**: 1.0.0  
**Tiempo estimado de testing**: ~20 minutos

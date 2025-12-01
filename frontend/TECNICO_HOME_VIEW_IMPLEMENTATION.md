# 📱 TecnicoHomeView.vue - Dashboard Operativo

## ✅ IMPLEMENTACIÓN COMPLETADA

Se ha desarrollado exitosamente la vista **Home del Técnico** como un **Dashboard Operativo ligero** utilizando **Vue 3 Composition API** y **Vuetify 3**.

---

## 🎯 CARACTERÍSTICAS IMPLEMENTADAS

### **1. Tarjeta de Bienvenida (Header)**
✅ **Componente:** `<v-card variant="tonal" color="primary">`
- **Título:** "Hola, {{ nombreUsuario }}" (clase `text-h5 font-weight-bold`)
- **Subtítulo:** Fecha actual formateada dinámicamente en español
  - Ejemplo: "Lunes, 25 de Noviembre de 2024"
- **Margen:** `mb-4` (margin-bottom)

**Fuente de datos:**
- `userName`: Computed property desde `authStore.user.nombre_completo` o `username`
- `fechaActual`: Computed property con `toLocaleDateString('es-ES')`

---

### **2. Accesos Rápidos de Gestión (Grid)**
✅ **Layout:** `<v-row>` con dos columnas (`<v-col cols="6">`)

#### **Botón 1: Crear Activo**
- **Icono:** `mdi-plus-box` (tamaño 64, color `primary`)
- **Texto:** "Crear Activo"
- **Acción:** Navega a `/tecnico/crear`
- **Efectos:** Hover con elevación y ripple

#### **Botón 2: Editar Activos**
- **Icono:** `mdi-pencil-box-multiple` (tamaño 64, color `info`)
- **Texto:** "Editar Activos"
- **Acción:** Navega a `/tecnico/editar-buscar`
- **Efectos:** Hover con elevación y ripple

**Características UX:**
- Tarjetas clickeables con `hover` y `ripple`
- Transición suave con `transform: translateY(-4px)` en hover
- Sombra elevada en hover para feedback visual

---

### **3. Feed de Actividad del Equipo (Listado)**
✅ **Componente:** `<v-card>` con `<v-list lines="two">`

#### **Título:**
"Últimos Movimientos del Equipo"

#### **Estados de la Vista:**

**Loading State:**
- `<v-progress-circular>` con mensaje "Cargando movimientos..."

**Error State:**
- Icono `mdi-alert-circle` (color error)
- Mensaje de error personalizado
- Botón "Reintentar" para recargar

**Empty State:**
- Icono `mdi-inbox` (color grey)
- Mensaje "No hay movimientos registrados"

**Lista de Movimientos:**
- **Configuración:** `lines="two"` (optimizado para móvil)
- **Iteración:** Sobre `ultimosMovimientos` (array de 15 ítems)

#### **Diseño del Ítem (`<v-list-item>`):**

**Avatar (Prepend):**
- Colores semánticos según tipo de acción:
  - `TRASLADO` → `primary` (Azul) + Icono `mdi-swap-horizontal`
  - `ASIGNACION` → `success` (Verde) + Icono `mdi-account-check`
  - `DEVOLUCION` → `info` (Azul claro) + Icono `mdi-keyboard-return`
  - `MANTENIMIENTO` → `warning` (Naranja) + Icono `mdi-wrench`
  - `RETORNO` → `success` (Verde) + Icono `mdi-check-circle`
  - `BAJA` → `error` (Rojo) + Icono `mdi-delete`

**Contenido:**
- **Título:** Nombre del Activo (ej: "Notebook HP ProBook")
- **Subtítulo:** "Acción por Usuario • Tiempo"
  - Ejemplo: "Trasladado a Bodega por Juan • Hace 10 min"

#### **Footer:**
- Botón `variant="text"` y `block`
- Texto: "Ver Historial Completo"
- Acción: Redirige a `/tecnico/history`

---

## 📡 INTEGRACIÓN CON LA API

### **Endpoint Utilizado:**
```
GET /api/historial-movimientos/?ordering=-fecha_movimiento&page_size=15
```

### **Parámetros:**
- `ordering=-fecha_movimiento`: Ordenar por fecha descendente (más recientes primero)
- `page_size=15`: Limitar a 15 resultados

### **Estructura de Respuesta Esperada:**
```json
{
  "results": [
    {
      "id": 1,
      "activo": {
        "id": 1,
        "codigo_inventario": "ACT-2024-001",
        "marca": "HP",
        "modelo": "EliteBook 840 G8"
      },
      "usuario_registra": {
        "id": 1,
        "nombre_completo": "Juan Pérez"
      },
      "ubicacion_origen": {
        "id": 1,
        "nombre_ubicacion": "Sala 101"
      },
      "ubicacion_destino": {
        "id": 2,
        "nombre_ubicacion": "Bodega"
      },
      "tipo_movimiento": "TRASLADO",
      "fecha_movimiento": "2024-11-25T10:30:00Z",
      "comentarios": "Traslado por mantenimiento"
    }
  ]
}
```

---

## 🧠 LÓGICA Y FUNCIONES PRINCIPALES

### **Computed Properties:**

#### `userName`
```javascript
const userName = computed(() => {
  return authStore.user?.nombre_completo || authStore.user?.username || 'Usuario'
})
```

#### `fechaActual`
```javascript
const fechaActual = computed(() => {
  const fecha = new Date()
  const opciones = {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }
  
  return fecha.toLocaleDateString('es-ES', opciones)
    .split(' ')
    .map((palabra, index) => index === 0 ? palabra.charAt(0).toUpperCase() + palabra.slice(1) : palabra)
    .join(' ')
})
```

### **Métodos de API:**

#### `fetchMovimientos()`
- Carga los últimos 15 movimientos desde la API
- Maneja estados de loading y error
- Se ejecuta automáticamente en `onMounted()`

### **Helpers de Visualización:**

#### `getColorByTipo(tipo)`
Retorna el color del avatar según el tipo de movimiento.

#### `getIconByTipo(tipo)`
Retorna el icono MDI según el tipo de movimiento.

#### `getActivoNombre(movimiento)`
Extrae el nombre del activo desde el objeto movimiento.

#### `getDescripcionMovimiento(movimiento)`
Genera la descripción completa del movimiento.
Formato: "Acción por Usuario • Tiempo"

#### `getTimeAgo(fechaISO)`
Calcula el tiempo transcurrido desde una fecha.
- "Ahora" (< 1 min)
- "Hace X min" (< 60 min)
- "Hace X h" (< 24 h)
- "Ayer" (1 día)
- "Hace X días" (< 7 días)
- Fecha formateada (> 7 días)

---

## 🎨 ESTILOS Y UX

### **Contenedor Principal:**
```css
.technician-home-content {
  min-height: calc(100vh - 112px);
  background: #f5f7fa;
  padding: 1rem;
  padding-bottom: 80px; /* Espacio para el FAB flotante */
}
```

### **Tarjetas de Acción:**
```css
.action-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15) !important;
}
```

### **Responsive Design:**
- **Mobile:** Padding de 0.75rem
- **Desktop (≥ 960px):** Max-width de 800px centrado

---

## ✅ CHECKLIST DE IMPLEMENTACIÓN

- [x] Tarjeta de bienvenida con `variant="tonal"` y `color="primary"`
- [x] Fecha actual formateada dinámicamente en español
- [x] Grid de accesos rápidos (2 columnas)
- [x] Botón "Crear Activo" con icono `mdi-plus-box`
- [x] Botón "Editar Activos" con icono `mdi-pencil-box-multiple`
- [x] Feed de actividad con `<v-list lines="two">`
- [x] Avatares con colores semánticos según tipo de movimiento
- [x] Integración con API `/api/historial-movimientos/`
- [x] Estados de loading, error y empty
- [x] Botón "Ver Historial Completo" en el footer
- [x] Función `getTimeAgo()` para tiempo relativo
- [x] Responsive design para móvil y desktop
- [x] Sin errores de compilación

---

## 🚀 CÓMO PROBAR

1. **Asegúrate de que el backend esté corriendo:**
   ```bash
   cd backend
   python manage.py runserver
   ```

2. **Inicia el frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Navega a:** `http://localhost:5173/tecnico/home`

4. **Verifica:**
   - ✅ Tarjeta de bienvenida con tu nombre
   - ✅ Fecha actual en español
   - ✅ Dos botones de acceso rápido
   - ✅ Lista de movimientos con avatares de colores
   - ✅ Tiempo relativo ("Hace X min")
   - ✅ Botón "Ver Historial Completo"

---

## 📝 NOTAS IMPORTANTES

### **Restricción Arquitectónica:**
Esta vista **NO incluye** barras de navegación (`v-app-bar`, `v-bottom-navigation`) ni el botón flotante (FAB), ya que son gestionados por **LayoutTecnico.vue**.

### **Datos Simulados vs Reales:**
La vista está configurada para consumir datos reales de la API. Si no hay movimientos en la base de datos, se mostrará el estado vacío.

---

**Desarrollado con:** Vue 3 Composition API + Vuetify 3 + Material Design Icons


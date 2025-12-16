# 🖨️ PrintLabelsView.vue - Impresión de Etiquetas QR

## ✅ IMPLEMENTACIÓN COMPLETADA

Se ha desarrollado exitosamente la vista **PrintLabelsView.vue** como una **interfaz crítica de gestión** para imprimir etiquetas de activos con códigos QR, siguiendo el estándar establecido en las vistas anteriores.

---

## 🎯 CARACTERÍSTICAS IMPLEMENTADAS

### **ESTRUCTURA DE INTERFAZ: 3 TABS DE SELECCIÓN**

#### **TAB 1: POR ACTIVOS (Selección Granular)**

✅ **Filtros Avanzados:**
- **Buscador Universal:** Campo de texto con búsqueda en tiempo real
- **Selector de Marca:** Dropdown con marcas disponibles (generado dinámicamente)
- **Selector de Tipo de Equipo:** Dropdown con tipos desde la API
- **Selector de Ubicación:** Dropdown con ubicaciones desde la API
- **Botón Limpiar Filtros:** Resetea todos los filtros

✅ **Tabla de Activos (`<v-data-table>`):**
- **Selección Múltiple:** `show-select` habilitado
- **Columnas:**
  - Nombre (Marca + Modelo)
  - Código de Inventario
  - Marca
  - Ubicación (con chip de color)
- **Estados:**
  - Loading con skeleton loader
  - Empty state con icono y mensaje
- **Paginación:** 10 ítems por página

✅ **Acción:**
- Botón "Agregar X Seleccionados a Cola"
- Deshabilitado si no hay selección

---

#### **TAB 2: POR UBICACIONES (Selección Masiva)**

✅ **Filtros:**
- **Selector de Departamento:** Filtra ubicaciones por departamento
- **Buscador de Ubicaciones:** Búsqueda en tiempo real

✅ **Tabla de Ubicaciones:**
- **Columnas:**
  - Nombre de Ubicación
  - Departamento (con chip)
  - Total de Activos (con chip)
- **Selección Múltiple:** Checkbox para cada ubicación

✅ **Lógica:**
- Al seleccionar una ubicación, se agregan **todos los activos** de esa ubicación a la cola
- Evita duplicados automáticamente

---

#### **TAB 3: MANUAL (Ingreso Rápido)**

✅ **Componente:**
- `<v-combobox>` con chips múltiples
- Permite escribir códigos y presionar Enter
- Chips removibles individualmente

✅ **Funcionalidad:**
- Validación automática contra códigos existentes
- Botón "Limpiar" para resetear
- Botón "Agregar X Códigos" para agregar a cola

---

### **ÁREA DE COLA DE IMPRESIÓN**

✅ **Visualización:**
- Card con título dinámico: "Cola de Impresión (X activos)"
- Chips con información del activo
- Cada chip es removible individualmente
- Botón "Limpiar Cola" para vaciar todo

✅ **Características:**
- Evita duplicados automáticamente
- Persistencia durante la sesión
- Feedback visual con chips de colores

---

### **BOTÓN FLOTANTE DE VISTA PREVIA**

✅ **Diseño:**
- Botón flotante (FAB) en la esquina inferior derecha
- Color: `success` (verde)
- Tamaño: `x-large`
- Elevación: 8
- Muestra contador de activos en cola

✅ **Acción:**
- Abre el diálogo de vista previa fullscreen
- Genera QR codes automáticamente

---

### **DIÁLOGO DE VISTA PREVIA E IMPRESIÓN**

✅ **Características:**
- **Fullscreen:** Ocupa toda la pantalla
- **Transición:** `dialog-bottom-transition`
- **Toolbar:**
  - Botón cerrar
  - Título con contador
  - Botón "Imprimir Ahora"

✅ **Área de Impresión (`#print-area`):**
- Contenedor con grid de 3 columnas
- Gap de 10px entre etiquetas
- Fondo blanco para impresión

---

## 🏷️ DISEÑO DE ETIQUETA (CSS GRID - Réplica Industrial)

### **Contenedor Principal:**
```css
.print-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}
```

### **Tarjeta de Etiqueta:**
```css
.etiqueta-card {
  border: 1px dashed #000;
  padding: 8px;
  page-break-inside: avoid;
  display: flex;
  align-items: center;
}
```

### **Contenido de Etiqueta:**

#### **Izquierda (70%): Nombre del Activo**
- Texto grande y negrita
- Alineado a la izquierda-centro
- Word-wrap para nombres largos

#### **Derecha (30%): QR + Código Vertical**
- **QR Code:** 60x60px
- **Código Vertical:**
  - `writing-mode: vertical-rl`
  - `text-orientation: mixed`
  - Rotado 90 grados verticalmente
  - Estilo industrial de inventario

---

## 📡 INTEGRACIÓN CON LA API

### **Endpoints Utilizados:**

```javascript
GET /api/activos/              // Listar todos los activos
GET /api/ubicaciones/          // Listar todas las ubicaciones
GET /api/departamentos/        // Listar todos los departamentos
GET /api/tipos-equipo/         // Listar todos los tipos de equipo
```

### **Estructura de Datos:**

**Activo:**
```json
{
  "id": 1,
  "codigo_inventario": "INV-25-A1B2C3",
  "numero_serie": "SN123456",
  "marca": "HP",
  "modelo": "EliteBook 840 G8",
  "tipo": {
    "id": 1,
    "nombre_tipo": "Computador"
  },
  "ubicacion_actual": {
    "id": 1,
    "nombre_ubicacion": "Sala 101",
    "departamento": {
      "id": 1,
      "nombre_departamento": "Urgencias"
    }
  }
}
```

---

## 🔧 FUNCIONALIDAD TÉCNICA

### **Generación de QR Codes:**

```javascript
import QRCode from 'qrcode'

async function generarQRCode(codigo) {
  const qrDataUrl = await QRCode.toDataURL(codigo, {
    width: 120,
    margin: 1,
    color: {
      dark: '#000000',
      light: '#FFFFFF'
    }
  })
  return qrDataUrl
}
```

### **Gestión de Cola:**

**Agregar Seleccionados:**
```javascript
function agregarSeleccionadosACola() {
  const nuevosActivos = activos.value.filter(a =>
    activosSeleccionados.value.includes(a.id) &&
    !colaImpresion.value.some(c => c.id === a.id)
  )
  colaImpresion.value.push(...nuevosActivos)
  activosSeleccionados.value = []
}
```

**Agregar por Ubicación:**
```javascript
async function agregarActivosPorUbicacion() {
  for (const ubicacionId of ubicacionesSeleccionadas.value) {
    const activosDeUbicacion = activos.value.filter(a =>
      a.ubicacion_actual?.id === ubicacionId &&
      !colaImpresion.value.some(c => c.id === a.id)
    )
    colaImpresion.value.push(...activosDeUbicacion)
  }
  ubicacionesSeleccionadas.value = []
}
```

---

## 🖨️ ESTILOS DE IMPRESIÓN (@media print)

### **Reglas Críticas:**

```css
@media print {
  /* Ocultar todo excepto el área de impresión */
  body * {
    visibility: hidden;
  }

  #print-area,
  #print-area * {
    visibility: visible;
  }

  #print-area {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
  }

  /* Ajustar márgenes de página */
  @page {
    margin: 10mm;
    size: A4;
  }

  /* Evitar cortes de etiquetas */
  .etiqueta-card {
    page-break-inside: avoid;
    break-inside: avoid;
  }

  /* Mantener grid de 3 columnas */
  .print-container {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
  }
}
```

---

## 📱 RESPONSIVE DESIGN

### **Tablets (≤ 960px):**
- Grid de 2 columnas

### **Móviles (≤ 600px):**
- Grid de 1 columna
- FAB ajustado a la posición

---

## ✅ CHECKLIST DE IMPLEMENTACIÓN

- [x] Tab 1: Por Activos con filtros avanzados
- [x] Tab 2: Por Ubicaciones con selección masiva
- [x] Tab 3: Manual con combobox de chips
- [x] Tabla de activos con selección múltiple
- [x] Tabla de ubicaciones con información completa
- [x] Cola de impresión con chips removibles
- [x] Botón flotante de vista previa
- [x] Diálogo fullscreen con toolbar
- [x] Generación de QR codes con librería `qrcode`
- [x] Diseño de etiqueta con grid 3 columnas
- [x] Código vertical rotado 90 grados
- [x] Estilos @media print optimizados
- [x] Responsive design para móvil y tablet
- [x] Integración con API real
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

3. **Navega a:** `http://localhost:5173/tecnico/imprimir`

4. **Prueba los 3 modos:**
   - **Por Activos:** Filtra y selecciona activos individuales
   - **Por Ubicaciones:** Selecciona ubicaciones completas
   - **Manual:** Ingresa códigos manualmente

5. **Agrega a la cola y haz clic en "Vista Previa / Imprimir"**

6. **Verifica:**
   - ✅ QR codes generados correctamente
   - ✅ Código vertical rotado 90 grados
   - ✅ Grid de 3 etiquetas por fila
   - ✅ Botón "Imprimir Ahora" ejecuta `window.print()`

---

## 📝 NOTAS IMPORTANTES

### **Librería QR Code:**
- Usa `qrcode` v1.5.4 (ya instalada)
- Genera QR codes como Data URLs (base64)
- Configuración optimizada para impresión

### **Diseño Industrial:**
- Borde punteado (`dashed`) para facilitar corte
- Código vertical al estilo de etiquetas de inventario profesionales
- QR de 60x60px para escaneo óptimo

### **Impresión:**
- Tamaño de página: A4
- Márgenes: 10mm
- 3 etiquetas por fila
- Evita cortes con `page-break-inside: avoid`

---

**Desarrollado con:** Vue 3 Composition API + Vuetify 3 + QRCode.js + Material Design Icons


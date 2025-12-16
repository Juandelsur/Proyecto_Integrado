# 🔧 CORRECCIÓN: Generación de QR Codes en el Frontend

## ⚠️ PROBLEMA IDENTIFICADO

Algunos archivos **INCORRECTAMENTE** esperan que el backend devuelva URLs de imágenes QR (`qr_url`), cuando en realidad:

**❌ EL BACKEND NO ALMACENA NI DEVUELVE IMÁGENES QR**

**✅ LOS QR CODES DEBEN GENERARSE DINÁMICAMENTE EN EL FRONTEND**

---

## 📊 ESTADO ACTUAL DE LOS ARCHIVOS

### ✅ ARCHIVOS CORRECTOS (Ya generan QR en frontend):

1. **`frontend/src/views/technician/PrintLabelsView.vue`**
   - ✅ Usa `QRCode.toDataURL(activo.codigo_inventario)`
   - ✅ Genera QR dinámicamente antes de imprimir
   - ✅ Almacena en `activo.qrDataUrl` (temporal, no persistente)

2. **`frontend/src/views/admin/AssetDetailView.vue`**
   - ✅ Usa `QRCode.toCanvas(qrCanvas.value, activo.codigo_inventario)`
   - ✅ Genera QR en canvas al cargar el activo
   - ✅ Permite descargar como PNG

3. **`frontend/src/views/admin/PrintQRsView.vue`**
   - ✅ Usa `QRCode.toDataURL(activo.codigo_inventario)`
   - ✅ Genera QR en paralelo para todos los activos
   - ✅ Almacena en `qrImages.value[activo.id]` (temporal)

4. **`frontend/src/views/technician/ScannerView.vue`**
   - ✅ No muestra imágenes QR (solo es un centro de decisión)
   - ✅ Solo muestra `codigo_qr` como texto

---

### ❌ ARCHIVOS INCORRECTOS (Esperan `qr_url` del backend):

1. **`frontend/src/views/PrintQRsView.vue`** (raíz)
   - ❌ Espera `activo.qr_url` del backend
   - ❌ Espera `ubicacion.qr_url` del backend
   - 🔧 **NECESITA CORRECCIÓN**

2. **`frontend/src/views/AssetDetailView.vue`** (raíz)
   - ❌ Espera `activo.qr_url` del backend
   - 🔧 **NECESITA CORRECCIÓN**

---

## 🔧 SOLUCIÓN: Patrón de Generación de QR Codes

### **Método 1: Generar como Data URL (Base64)**

**Uso:** Para mostrar en `<img>` tags o imprimir

```javascript
import QRCode from 'qrcode'

async function generarQRCode(codigo) {
  try {
    const qrDataUrl = await QRCode.toDataURL(codigo, {
      width: 200,
      margin: 1,
      color: {
        dark: '#000000',
        light: '#FFFFFF'
      },
      errorCorrectionLevel: 'M'
    })
    return qrDataUrl // Retorna: "data:image/png;base64,iVBORw0KGgoAAAANS..."
  } catch (error) {
    console.error('Error al generar QR:', error)
    return ''
  }
}

// Uso:
const qrImage = await generarQRCode(activo.codigo_inventario)
// Luego en template: <img :src="qrImage" />
```

---

### **Método 2: Generar en Canvas**

**Uso:** Para mostrar directamente en canvas o descargar como PNG

```javascript
import QRCode from 'qrcode'

async function generarQREnCanvas(canvasRef, codigo) {
  try {
    await QRCode.toCanvas(canvasRef, codigo, {
      width: 300,
      margin: 2,
      color: {
        dark: '#000000',
        light: '#FFFFFF'
      }
    })
  } catch (error) {
    console.error('Error al generar QR:', error)
  }
}

// Uso:
const qrCanvas = ref(null)
await generarQREnCanvas(qrCanvas.value, activo.codigo_inventario)
// Luego en template: <canvas ref="qrCanvas"></canvas>
```

---

## 📝 CÓDIGOS A USAR PARA GENERAR QR

### **Para Activos:**
```javascript
const codigoQR = activo.codigo_inventario
// Ejemplo: "INV-25-A1B2C3"
```

### **Para Ubicaciones:**
```javascript
const codigoQR = ubicacion.codigo_qr
// Ejemplo: "LOC-F8A1B2"
```

---

## 🎯 PLAN DE CORRECCIÓN

### **Archivo 1: `frontend/src/views/PrintQRsView.vue`**

**Cambios necesarios:**

1. Importar librería QRCode:
   ```javascript
   import QRCode from 'qrcode'
   ```

2. Crear estado reactivo para almacenar QR generados:
   ```javascript
   const qrImagesActivos = ref({})
   const qrImagesUbicaciones = ref({})
   ```

3. Generar QR codes después de cargar datos:
   ```javascript
   async function generateQRsActivos() {
     for (const activo of activos.value) {
       qrImagesActivos.value[activo.id] = await QRCode.toDataURL(activo.codigo_inventario)
     }
   }

   async function generateQRsUbicaciones() {
     for (const ubicacion of ubicaciones.value) {
       qrImagesUbicaciones.value[ubicacion.id] = await QRCode.toDataURL(ubicacion.codigo_qr)
     }
   }
   ```

4. Actualizar template:
   ```vue
   <!-- Antes (INCORRECTO): -->
   <img :src="activo.qr_url" />

   <!-- Después (CORRECTO): -->
   <img :src="qrImagesActivos[activo.id]" />
   ```

---

### **Archivo 2: `frontend/src/views/AssetDetailView.vue`**

**Cambios necesarios:**

1. Importar librería QRCode:
   ```javascript
   import QRCode from 'qrcode'
   ```

2. Crear ref para canvas:
   ```javascript
   const qrCanvas = ref(null)
   ```

3. Generar QR code después de cargar activo:
   ```javascript
   async function generateQRCode() {
     if (!activo.value || !qrCanvas.value) return
     
     await QRCode.toCanvas(qrCanvas.value, activo.value.codigo_inventario, {
       width: 300,
       margin: 2
     })
   }

   onMounted(async () => {
     await loadActivo()
     await generateQRCode()
   })
   ```

4. Actualizar template:
   ```vue
   <!-- Antes (INCORRECTO): -->
   <img :src="activo.qr_url" />

   <!-- Después (CORRECTO): -->
   <canvas ref="qrCanvas"></canvas>
   ```

---

## ✅ VERIFICACIÓN

Después de aplicar las correcciones, verifica que:

1. ✅ No hay referencias a `qr_url` en el código
2. ✅ Todos los QR codes se generan con `QRCode.toDataURL()` o `QRCode.toCanvas()`
3. ✅ Los códigos usados son:
   - `activo.codigo_inventario` para activos
   - `ubicacion.codigo_qr` para ubicaciones
4. ✅ Los QR codes se generan **después** de cargar los datos del backend
5. ✅ Los QR codes se almacenan en variables reactivas temporales (no en el backend)

---

## 📚 DOCUMENTACIÓN DE LA LIBRERÍA

**Librería:** `qrcode` v1.5.4

**Métodos principales:**

- `QRCode.toDataURL(text, options)` - Genera imagen base64
- `QRCode.toCanvas(canvas, text, options)` - Renderiza en canvas
- `QRCode.toString(text, options)` - Genera SVG string

**Opciones comunes:**
```javascript
{
  width: 200,           // Ancho en píxeles
  margin: 1,            // Margen en módulos
  color: {
    dark: '#000000',    // Color del QR
    light: '#FFFFFF'    // Color de fondo
  },
  errorCorrectionLevel: 'M'  // L, M, Q, H
}
```

**Documentación oficial:** https://github.com/soldair/node-qrcode

---

## 🎯 RESUMEN

**REGLA DE ORO:**

> **NUNCA esperes que el backend devuelva imágenes QR.**
> **SIEMPRE genera los QR codes dinámicamente en el frontend usando la librería `qrcode`.**

**Códigos a usar:**
- Activos: `activo.codigo_inventario`
- Ubicaciones: `ubicacion.codigo_qr`

**Librería:** `qrcode` v1.5.4 (ya instalada)

---

**Fecha de corrección:** 2025-12-01
**Responsable:** Senior Frontend Developer


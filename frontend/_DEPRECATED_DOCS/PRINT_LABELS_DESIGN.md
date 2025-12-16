# 🏷️ Diseño de Etiquetas de Inventario - Especificaciones Técnicas

## 📐 Dimensiones Físicas

### **Tamaño de Etiqueta Individual**
```
┌─────────────────────────────────────────────────┐
│  Ancho: 8 cm                                    │
│  Alto: 5 cm                                     │
│  Padding: 0.5 cm                                │
│  Borde: 1px dashed (punteado para recortar)    │
└─────────────────────────────────────────────────┘
```

### **Distribución en Hoja A4**
```
Página A4 (21 cm × 29.7 cm)
Márgenes: 1 cm arriba/abajo, 0.5 cm izquierda/derecha

┌─────────────────────────────────────────────────┐
│  Margen Superior: 1 cm                          │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────┐  ┌──────────┐                    │
│  │ Etiqueta │  │ Etiqueta │  ← Fila 1          │
│  │    1     │  │    2     │                    │
│  └──────────┘  └──────────┘                    │
│                                                 │
│  ┌──────────┐  ┌──────────┐                    │
│  │ Etiqueta │  │ Etiqueta │  ← Fila 2          │
│  │    3     │  │    4     │                    │
│  └──────────┘  └──────────┘                    │
│                                                 │
│  ┌──────────┐  ┌──────────┐                    │
│  │ Etiqueta │  │ Etiqueta │  ← Fila 3          │
│  │    5     │  │    6     │                    │
│  └──────────┘  └──────────┘                    │
│                                                 │
│  ... (hasta 10-12 etiquetas por hoja)          │
│                                                 │
├─────────────────────────────────────────────────┤
│  Margen Inferior: 1 cm                          │
└─────────────────────────────────────────────────┘

Grilla: 2 columnas
Gap: 0.4 cm entre etiquetas
```

---

## 🎨 Diseño de Etiqueta Individual (Horizontal)

### **Layout Tipo "Placa de Inventario"**

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  ┌─────────┐   Dell Latitude 5420                          │
│  │         │   Serie: ABC123XYZ                             │
│  │   QR    │   ┌─────────────┐                             │
│  │  CODE   │   │  INV-00042  │                             │
│  │         │   └─────────────┘                             │
│  └─────────┘                                                │
│   2.8 cm                                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
    8 cm × 5 cm
```

### **Estructura Flexbox**
```css
display: flex;
flex-direction: row;
align-items: center;
gap: 0.4cm;

├── QR Image (Izquierda)
│   └── 2.8 cm × 2.8 cm
│
└── Información (Derecha)
    ├── Título: "Dell Latitude 5420" (10pt, bold)
    ├── Subtítulo: "Serie: ABC123XYZ" (8pt)
    └── Código: "INV-00042" (12pt, monospace, destacado)
```

---

## 📏 Especificaciones Detalladas

### **1. Contenedor de Etiqueta**
```css
.qr-card {
  width: 8cm;                    /* Ancho fijo */
  height: 5cm;                   /* Alto fijo */
  padding: 0.5cm;                /* Espaciado interno */
  border: 1px dashed #333;       /* Borde punteado para recortar */
  display: flex;                 /* Layout horizontal */
  flex-direction: row;
  align-items: center;
  gap: 0.4cm;
  page-break-inside: avoid;      /* No cortar entre páginas */
}
```

**Variantes de Borde:**
- **Activos:** `border: 1px dashed #000` (Negro)
- **Ubicaciones:** `border: 1px dashed #3498db` (Azul)

---

### **2. Imagen QR**
```css
.qr-image {
  width: 2.8cm;                  /* Tamaño exacto */
  height: 2.8cm;
  padding: 0.1cm;                /* Margen blanco alrededor */
}

.qr-image img {
  width: 2.6cm;                  /* Imagen interna */
  height: 2.6cm;
  -webkit-print-color-adjust: exact;  /* Asegurar impresión correcta */
  print-color-adjust: exact;
}
```

**Justificación del tamaño:**
- 2.8 cm es el tamaño óptimo para escaneo con smartphones
- Suficientemente grande para ser legible
- No invasivo en equipos pequeños (laptops)
- Margen blanco de 0.1 cm mejora la detección

---

### **3. Información de Texto**

#### **Título (Nombre del Activo)**
```css
.qr-title {
  font-size: 10pt;               /* Visible pero compacto */
  font-weight: bold;
  color: #000;
  line-height: 1.2;
  -webkit-line-clamp: 2;         /* Máximo 2 líneas */
  overflow: hidden;
  text-overflow: ellipsis;
}
```

**Ejemplo:** "Dell Latitude 5420"

---

#### **Subtítulo (Serie o Departamento)**
```css
.qr-subtitle {
  font-size: 8pt;                /* Más pequeño */
  color: #333;
  white-space: nowrap;           /* Una sola línea */
  overflow: hidden;
  text-overflow: ellipsis;
}
```

**Ejemplo:** "Serie: ABC123XYZ"

---

#### **Código de Inventario (Destacado)**
```css
.qr-id {
  font-size: 12pt;               /* MUY LEGIBLE */
  font-weight: bold;
  font-family: 'Courier New', monospace;
  color: #000;
  background: #f0f0f0;           /* Fondo gris claro */
  border: 1px solid #ccc;
  padding: 0.1cm 0.2cm;
  text-align: center;
  letter-spacing: 0.5px;
}
```

**Ejemplo:** `INV-00042`

**Justificación:**
- Fuente monospace para mejor legibilidad
- Tamaño 12pt para lectura rápida
- Fondo destacado para identificación visual inmediata
- Formato tipo "placa de matrícula"

---

## 🖨️ Configuración de Impresión

### **Configuración de Página**
```css
@page {
  size: A4 portrait;             /* Vertical */
  margin: 1cm 0.5cm;             /* Márgenes optimizados */
}
```

### **Grilla de Etiquetas**
```css
.qr-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);  /* 2 columnas */
  gap: 0.4cm;                              /* Espacio entre etiquetas */
}
```

### **Capacidad por Hoja**
- **Etiquetas por fila:** 2
- **Filas por hoja:** 5-6 (dependiendo del contenido)
- **Total por hoja:** 10-12 etiquetas

---

## 📋 Ejemplo Visual Completo

### **Etiqueta de Activo (Borde Negro)**
```
┌───────────────────────────────────────────────────────────┐
│ ┌─────────┐                                               │
│ │  ████   │  HP EliteBook 840 G8                          │
│ │  ████   │  Serie: 5CD1234ABC                            │
│ │  ████   │  ┌──────────────┐                            │
│ │  ████   │  │  INV-00123   │                            │
│ └─────────┘  └──────────────┘                            │
└───────────────────────────────────────────────────────────┘
  Borde: 1px dashed #000 (Negro)
```

### **Etiqueta de Ubicación (Borde Azul)**
```
┌───────────────────────────────────────────────────────────┐
│ ┌─────────┐                                               │
│ │  ████   │  Quirófano 3                                  │
│ │  ████   │  Dpto: Cirugía                                │
│ │  ████   │  ┌──────────────┐                            │
│ │  ████   │  │  UBI-00015   │                            │
│ └─────────┘  └──────────────┘                            │
└───────────────────────────────────────────────────────────┘
  Borde: 1px dashed #3498db (Azul)
```

---

## ✅ Ventajas del Diseño Horizontal

1. **Profesional:** Parece una placa de inventario real
2. **Compacto:** 8×5 cm cabe en cualquier laptop/PC
3. **Legible:** Código grande y destacado
4. **Escaneable:** QR de 2.8 cm es óptimo para smartphones
5. **Eficiente:** 10-12 etiquetas por hoja A4
6. **Recortable:** Borde punteado marca la línea de corte
7. **Diferenciado:** Colores de borde distinguen tipos

---

## 🎯 Casos de Uso

### **Laptops / PCs de Escritorio**
- Pegar en la parte trasera de la pantalla
- Pegar en la base del equipo (cerca del teclado)
- Pegar en el lateral del case (PCs de escritorio)

### **Equipos Médicos**
- Pegar en superficie plana visible
- Evitar zonas de contacto con pacientes
- Preferir zonas de fácil escaneo

### **Ubicaciones**
- Pegar en puertas de salas
- Pegar en paredes cerca de la entrada
- Pegar en muebles fijos (escritorios, estantes)

---

## 📦 Material Recomendado

### **Papel Adhesivo**
- **Tipo:** Papel adhesivo A4 para impresora láser/inkjet
- **Gramaje:** 80-100 g/m²
- **Acabado:** Mate (mejor para escaneo QR)
- **Adhesivo:** Permanente o removible según necesidad

### **Impresora**
- **Láser:** Mejor calidad y durabilidad
- **Inkjet:** Usar papel específico para inkjet
- **Configuración:** Calidad alta, sin ahorro de tinta

---

## 🔧 Instrucciones de Impresión

1. **Cargar papel adhesivo A4** en la impresora
2. **Abrir vista de impresión** en el navegador
3. **Configurar impresión:**
   - Tamaño: A4
   - Orientación: Vertical (Portrait)
   - Márgenes: Predeterminados
   - Escala: 100% (sin ajustar)
4. **Imprimir**
5. **Esperar 1 minuto** para que seque la tinta
6. **Recortar** siguiendo las líneas punteadas
7. **Pegar** en el equipo/ubicación

---

## ✅ Checklist de Calidad

- [ ] QR escaneable desde 20-30 cm de distancia
- [ ] Código de inventario legible sin acercarse
- [ ] Borde punteado visible para recortar
- [ ] Texto no cortado ni truncado
- [ ] Colores impresos correctamente
- [ ] Etiqueta no se corta entre páginas
- [ ] Tamaño físico correcto (8×5 cm)

---

**Diseñado por:** Senior Frontend Engineer  
**Fecha:** 2025-11-27  
**Estado:** ✅ OPTIMIZADO PARA PRODUCCIÓN


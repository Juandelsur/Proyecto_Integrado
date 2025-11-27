# 📱 Guía de Pruebas - Scanner View (Android)

## 🎯 Objetivo
Verificar que el componente `ScannerView.vue` funcione correctamente en dispositivos Android, manejando permisos de cámara y errores de forma robusta.

---

## ✅ Mejoras Implementadas

### 1. **Manejo de Errores de Permisos**
- ✅ Try-catch robusto en el método `.start()`
- ✅ Detección específica de errores:
  - `NotAllowedError` / `PermissionDeniedError` → Permisos denegados
  - `NotFoundError` → No se encontró cámara
  - `NotReadableError` / `TrackStartError` → Cámara en uso
  - `OverconstrainedError` → Configuración no compatible
- ✅ Mensajes de error amigables y accionables
- ✅ Instrucciones en consola para habilitar permisos

### 2. **Configuración de Cámara Trasera**
- ✅ `facingMode: { exact: 'environment' }` → Fuerza cámara trasera
- ✅ Optimizado para Android (evita cámara frontal por defecto)
- ✅ Configuración de `aspectRatio: 1.0` para mejor detección

### 3. **Validación de HTTPS**
- ✅ Verifica `window.isSecureContext` al montar
- ✅ Muestra advertencia si no está en HTTPS
- ✅ La API de cámara solo funciona en HTTPS (excepto localhost)

### 4. **UX Mejorada**
- ✅ Botón "Reintentar" cuando fallan los permisos
- ✅ Indicador visual "Cámara activa" (verde con animación)
- ✅ Transiciones suaves entre modos (escáner ↔ manual)
- ✅ Limpieza automática de errores al cambiar de modo

---

## 🧪 Plan de Pruebas

### **Prueba 1: Acceso Inicial a la Cámara**

**Pasos:**
1. Abrir la app en un dispositivo Android
2. Navegar a `/escanear`
3. El navegador debe solicitar permiso de cámara

**Resultado Esperado:**
- ✅ Aparece el diálogo de permisos del navegador
- ✅ Si se acepta: La cámara se activa y muestra el indicador "Cámara activa" (verde)
- ✅ Si se rechaza: Aparece mensaje de error con botón "Reintentar"

---

### **Prueba 2: Permisos Denegados**

**Pasos:**
1. Navegar a `/escanear`
2. Denegar el permiso de cámara
3. Verificar el mensaje de error

**Resultado Esperado:**
- ✅ Aparece mensaje: "⚠️ No podemos acceder a la cámara. Por favor, revisa los permisos de tu navegador o usa el ingreso manual."
- ✅ Aparece botón "Reintentar"
- ✅ Aparece botón "Cerrar"
- ✅ En consola aparecen instrucciones para habilitar permisos

**Acciones Adicionales:**
- Hacer clic en "Reintentar" → Debe solicitar permisos nuevamente
- Hacer clic en "Ingresar Manualmente" → Debe cambiar a modo manual

---

### **Prueba 3: Cámara Trasera en Android**

**Pasos:**
1. Navegar a `/escanear` en Android
2. Aceptar permisos
3. Verificar qué cámara se activa

**Resultado Esperado:**
- ✅ Se activa la cámara **trasera** (no la frontal/selfie)
- ✅ La vista muestra el entorno (no la cara del usuario)

---

### **Prueba 4: Contexto No Seguro (HTTP)**

**Pasos:**
1. Intentar acceder a la app desde HTTP (no HTTPS)
2. Navegar a `/escanear`

**Resultado Esperado:**
- ✅ Aparece advertencia: "⚠️ La cámara solo funciona en conexiones seguras (HTTPS). Por favor, usa el ingreso manual."
- ✅ No se intenta acceder a la cámara

**Nota:** En Vercel siempre es HTTPS, pero es buena práctica validarlo.

---

### **Prueba 5: Escaneo Exitoso**

**Pasos:**
1. Navegar a `/escanear`
2. Aceptar permisos
3. Apuntar la cámara a un código QR válido (ej: `INV-001`)

**Resultado Esperado:**
- ✅ El código se detecta automáticamente
- ✅ Aparece overlay de "Buscando equipo..."
- ✅ Se detiene el escáner
- ✅ Redirige a `/confirmar-equipo/:id`

---

### **Prueba 6: Código No Encontrado**

**Pasos:**
1. Escanear un código QR que no existe en la BD (ej: `INV-999`)

**Resultado Esperado:**
- ✅ Aparece mensaje: "No se encontró ningún equipo con el código: INV-999"
- ✅ Después de 2 segundos, el escáner se reinicia automáticamente
- ✅ Se puede escanear otro código

---

### **Prueba 7: Modo Manual**

**Pasos:**
1. Navegar a `/escanear`
2. Hacer clic en "¿Problemas con la cámara? Ingresar Manualmente"
3. Escribir un código (ej: `INV-001`)
4. Hacer clic en "Buscar Equipo"

**Resultado Esperado:**
- ✅ El escáner se detiene
- ✅ Aparece el formulario de ingreso manual
- ✅ Al buscar, funciona igual que el escaneo
- ✅ Botón "Volver al Escáner" reinicia la cámara

---

## 📱 Dispositivos de Prueba Recomendados

### **Android:**
- ✅ Chrome 90+ (recomendado)
- ✅ Samsung Internet 14+
- ✅ Firefox 88+

### **iOS:**
- ✅ Safari 14+ (iOS 14+)
- ✅ Chrome iOS 90+

---

## 🐛 Problemas Conocidos y Soluciones

### **Problema 1: Cámara no se activa en Android**
**Solución:**
1. Verificar que la app esté en HTTPS
2. Ir a Configuración del navegador → Permisos del sitio → Cámara → Permitir
3. Recargar la página

### **Problema 2: Se activa la cámara frontal en lugar de la trasera**
**Solución:**
- Ya implementado: `facingMode: { exact: 'environment' }`
- Si persiste, verificar que el dispositivo tenga cámara trasera

### **Problema 3: Error "Camera already in use"**
**Solución:**
1. Cerrar otras apps que usen la cámara
2. Recargar la página
3. Si persiste, reiniciar el navegador

---

## 🔍 Logs de Depuración

El componente incluye logs detallados en consola:

```javascript
✅ Escáner QR iniciado correctamente
❌ Error al iniciar escáner: [error details]
📱 INSTRUCCIONES PARA HABILITAR LA CÁMARA: [instructions]
📝 Modo manual activado
📷 Intentando reiniciar escáner...
🔄 Reintentando acceso a la cámara...
```

---

## ✅ Checklist de Validación

- [ ] La cámara se activa correctamente en Android
- [ ] Se solicita permiso de cámara al usuario
- [ ] Se activa la cámara **trasera** (no frontal)
- [ ] Los mensajes de error son claros y accionables
- [ ] El botón "Reintentar" funciona correctamente
- [ ] El modo manual funciona como fallback
- [ ] El indicador "Cámara activa" aparece cuando está funcionando
- [ ] El escaneo de códigos QR funciona correctamente
- [ ] La navegación a la vista de confirmación funciona
- [ ] El escáner se reinicia después de errores

---

## 📞 Soporte

Si encuentras problemas, revisa:
1. Consola del navegador (logs detallados)
2. Permisos del sitio en el navegador
3. Conexión HTTPS activa
4. Compatibilidad del navegador

---

**Última actualización:** 2025-11-27  
**Versión:** 2.0 (Robustecida para Android)


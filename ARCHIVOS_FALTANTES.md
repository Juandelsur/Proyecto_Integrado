# 📋 LISTA DE ARCHIVOS FALTANTES PARA MIGRACIÓN

## ✅ ARCHIVOS QUE YA TIENES (NO COPIAR)
- ✓ `/frontend/src/views/LoginView.vue`
- ✓ `/frontend/src/views/AdminHome.vue`
- ✓ `/frontend/src/views/TecnicoHome.vue`
- ✓ `/frontend/src/views/JefeHome.vue`
- ✓ `/frontend/src/views/admin/GestionView.vue`
- ✓ `/frontend/src/views/admin/OtrosView.vue`
- ✓ `/frontend/src/views/tecnico/HistorialView.vue`
- ✓ `/frontend/src/views/tecnico/OtrosView.vue`
- ✓ `/frontend/src/views/jefe/OtrosView.vue`
- ✓ `/frontend/src/layouts/AppLayout.vue`

---

## 🆕 ARCHIVOS NUEVOS QUE NECESITAS COPIAR DE LA RAMA FEATURE-LOGIN

### 📂 VISTAS ADMIN - GESTIÓN (`/frontend/src/views/admin/gestion/`)
```
❌ GestionActivos.vue
❌ GestionEstadoActivo.vue
❌ GestionDepartamentos.vue
❌ GestionRoles.vue
❌ GestionTipoEquipo.vue
❌ GestionUbicaciones.vue
❌ GestionUsuarios.vue
```

### 📂 VISTAS ADMIN - REPORTES Y AUDITORÍA (`/frontend/src/views/admin/`)
```
❌ AssetListView.vue         # Vista de inventario (lista de activos)
❌ AssetDetailView.vue        # Detalle de un activo específico
❌ PrintQRsView.vue           # Impresión de etiquetas QR
❌ HistorialView.vue          # Historial de movimientos (Admin)
❌ ReportesView.vue           # Reportes del sistema
❌ AuditoriaView.vue          # Auditoría del sistema
```

### 📂 VISTAS TÉCNICO (`/frontend/src/views/technician/`)
```
❌ ScannerView.vue            # Escanear códigos QR
❌ PrintLabelsView.vue        # Imprimir etiquetas
❌ CreateAssetView.vue        # Crear activo (Técnico)
❌ EditAssetSearchView.vue    # Buscar activo para editar
❌ MovimientoTecnicoView.vue  # Confirmar equipo/movimiento
❌ MovementSuccessView.vue    # Vista de éxito tras registro
❌ SettingsView.vue           # Configuración
❌ QRScannerDemoView.vue      # Demo de escáner QR (opcional, para testing)
```

### 📂 VISTAS TÉCNICO - SUB-CARPETA ACTIVOS (`/frontend/src/views/technician/activos/`)
```
❌ CrearActivoView.vue        # Crear activo (versión alternativa)
❌ EditarActivoView.vue       # Editar activo (versión alternativa)
```

### 📂 VISTAS COMPARTIDAS - RAÍZ (`/frontend/src/views/`)
```
❌ AssetEditView.vue          # Editar activo (compartida)
❌ AssetCreateView.vue        # Crear activo (compartida)
❌ AssetMoveView.vue          # Movilizar activo
❌ ImprimirQrView.vue         # Imprimir QR (usado en /admin/imprimir-qr)
```

---

## 📊 RESUMEN NUMÉRICO

| Categoría | Cantidad |
|-----------|----------|
| **Vistas Admin - Gestión** | 7 archivos |
| **Vistas Admin - Reportes** | 6 archivos |
| **Vistas Técnico** | 8 archivos |
| **Vistas Técnico - Activos** | 2 archivos |
| **Vistas Compartidas** | 4 archivos |
| **TOTAL** | **27 archivos .vue** |

---

## 🎯 INSTRUCCIONES DE COPIADO

### OPCIÓN 1: Copiar archivos manualmente desde la rama `feature-login`

```bash
# 1. Crear un worktree temporal de la rama feature-login
git worktree add ../temp-feature-login origin/feature-login

# 2. Copiar los archivos necesarios
cp -r ../temp-feature-login/frontend/src/views/admin/gestion ./frontend/src/views/admin/
cp ../temp-feature-login/frontend/src/views/admin/AssetListView.vue ./frontend/src/views/admin/
cp ../temp-feature-login/frontend/src/views/admin/AssetDetailView.vue ./frontend/src/views/admin/
cp ../temp-feature-login/frontend/src/views/admin/PrintQRsView.vue ./frontend/src/views/admin/
cp ../temp-feature-login/frontend/src/views/admin/HistorialView.vue ./frontend/src/views/admin/
cp ../temp-feature-login/frontend/src/views/admin/ReportesView.vue ./frontend/src/views/admin/
cp ../temp-feature-login/frontend/src/views/admin/AuditoriaView.vue ./frontend/src/views/admin/

# Copiar vistas del técnico
cp -r ../temp-feature-login/frontend/src/views/technician ./frontend/src/views/

# Copiar vistas compartidas
cp ../temp-feature-login/frontend/src/views/AssetEditView.vue ./frontend/src/views/
cp ../temp-feature-login/frontend/src/views/AssetCreateView.vue ./frontend/src/views/
cp ../temp-feature-login/frontend/src/views/AssetMoveView.vue ./frontend/src/views/
cp ../temp-feature-login/frontend/src/views/ImprimirQrView.vue ./frontend/src/views/

# 3. Limpiar worktree temporal
git worktree remove ../temp-feature-login
```

### OPCIÓN 2: Extraer archivos específicos con `git show`

```bash
# Crear directorios necesarios
mkdir -p frontend/src/views/admin/gestion
mkdir -p frontend/src/views/technician/activos

# Extraer cada archivo individualmente
git show origin/feature-login:frontend/src/views/admin/gestion/GestionActivos.vue > frontend/src/views/admin/gestion/GestionActivos.vue
git show origin/feature-login:frontend/src/views/admin/gestion/GestionEstadoActivo.vue > frontend/src/views/admin/gestion/GestionEstadoActivo.vue
# ... (repetir para cada archivo)
```

### OPCIÓN 3: Merge selectivo (MÁS RIESGOSO)

```bash
# ⚠️ CUIDADO: Esto puede traer cambios no deseados
git checkout origin/feature-login -- frontend/src/views/admin/gestion
git checkout origin/feature-login -- frontend/src/views/technician
git checkout origin/feature-login -- frontend/src/views/AssetEditView.vue
# ... etc
```

---

## ⚠️ NOTAS IMPORTANTES

### 🔴 LAYOUTS - DECISIÓN ARQUITECTÓNICA

Tu amigo usa 2 layouts diferentes:
- `LayoutTecnico.vue`
- `LayoutAdministrador.vue`

**TÚ** usas un único `AppLayout.vue`.

**RECOMENDACIÓN:** 
1. **Mantén tu AppLayout** (ya está en el router migrado)
2. Si los componentes nuevos tienen referencias a `LayoutTecnico` o `LayoutAdministrador`, necesitarás:
   - **Adaptar las referencias** dentro de los componentes
   - O **copiar también esos layouts** y decidir cuál usar

### 🔴 STORES - VERIFICAR COMPATIBILIDAD

Los componentes nuevos probablemente usan stores de Pinia. Verifica que tienes:
- `@/stores/auth.js` ✅ (Ya lo tienes, lo usa el router)
- `@/stores/activos.js` ❓ (Probablemente necesario)
- `@/stores/departamentos.js` ❓
- `@/stores/usuarios.js` ❓
- etc.

### 🔴 SERVICIOS API - VERIFICAR AXIOS

Los componentes probablemente llaman a servicios API. Verifica que tienes:
- `@/services/api.js` o similar
- Configuración de Axios con baseURL apuntando a Render

---

## 📝 SIGUIENTE PASO RECOMENDADO

Después de copiar los archivos:

1. **Reemplazar tu router actual** con el migrado:
   ```bash
   mv frontend/src/router/index.js frontend/src/router/index_OLD_BACKUP.js
   mv frontend/src/router/index_MIGRADO.js frontend/src/router/index.js
   ```

2. **Instalar las dependencias nuevas**:
   ```bash
   npm install jspdf@^3.0.4 jspdf-autotable@^5.0.2 xlsx@^0.18.5
   ```

3. **Probar la aplicación**:
   ```bash
   npm run dev
   ```

4. **Revisar errores de imports** y ajustar paths si es necesario.

---

## 🎓 FILOSOFÍA DE MIGRACIÓN

Este router migrado mantiene:
- ✅ Tu lógica de `beforeEach` (RBAC limpio)
- ✅ Tu AppLayout único
- ✅ Tus guards de autenticación
- ✅ Tu estructura de meta (`requiredRole`, no `requiresRole`)

Y agrega:
- ✅ Todas las rutas nuevas de tu amigo
- ✅ Lazy loading con `() => import()` para las vistas nuevas
- ✅ Comentarios organizados por sección
- ✅ Rutas compartidas fuera del layout (inventario, activos)

**RESULTADO:** Router híbrido que respeta tu arquitectura pero integra todas las funcionalidades nuevas.


# 🔌 Configuración de API - Frontend

## 🎯 Problema: Diferentes URLs según el Ambiente

Tu frontend necesita conectarse a **diferentes URLs** según dónde esté ejecutándose:

| Ambiente | Frontend corre en | Backend está en | URL Backend |
|----------|------------------|-----------------|-------------|
| **Desarrollo Local (Docker)** | Docker (localhost:5173) | Docker (localhost:8000) | `http://localhost:8000` |
| **Desarrollo Local (sin Docker)** | npm run dev (localhost:5173) | Docker o local (localhost:8000) | `http://localhost:8000` |
| **Producción** | Vercel/Netlify | Render/Railway | `https://tu-backend.onrender.com` |

---

## ✅ Solución: Variables de Entorno por Ambiente

Tu `api.js` ya está configurado correctamente:

```javascript
// frontend/src/services/api.js
const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
```

Solo necesitas crear archivos `.env` con la URL correcta para cada ambiente.

---

## 📁 Archivos .env a Crear

### 1️⃣ `.env.local` (Desarrollo con Docker)

```bash
cd sca-hospital/frontend
cat > .env.local << 'EOF'
VITE_API_URL=http://localhost:8000
NODE_ENV=development
EOF
```

**Cuándo se usa**: Cuando corres `docker-compose up`

---

### 2️⃣ `.env.development` (Desarrollo sin Docker)

```bash
cd sca-hospital/frontend
cat > .env.development << 'EOF'
VITE_API_URL=http://localhost:8000
NODE_ENV=development
EOF
```

**Cuándo se usa**: Cuando corres `npm run dev` fuera de Docker

---

### 3️⃣ `.env.production` (Producción)

```bash
cd sca-hospital/frontend
cat > .env.production << 'EOF'
VITE_API_URL=https://tu-backend-real-desplegado.onrender.com
NODE_ENV=production
EOF
```

**⚠️ IMPORTANTE**: Cambia `https://tu-backend-real-desplegado.onrender.com` por tu URL real.

**Cuándo se usa**: Cuando construyes para producción (`npm run build`)

---

## 🚀 Cómo Funciona

### En Desarrollo Local (Docker)

```bash
# 1. Levantar servicios
cd sca-hospital
docker-compose up -d

# 2. El frontend usa .env.local
# Frontend: http://localhost:5173
# Backend:  http://localhost:8000
# Llamadas API: http://localhost:8000/api/activos/
```

### En Desarrollo Local (sin Docker)

```bash
# 1. Levantar solo backend en Docker
cd sca-hospital
docker-compose up -d backend db

# 2. Frontend en tu máquina
cd frontend
npm run dev

# Frontend usa .env.development
# Frontend: http://localhost:5173
# Backend:  http://localhost:8000 (Docker)
# Llamadas API: http://localhost:8000/api/activos/
```

### En Producción

```bash
# 1. Build del frontend
cd sca-hospital/frontend
npm run build

# Frontend usa .env.production
# Frontend: https://tu-app.vercel.app
# Backend:  https://tu-backend.onrender.com
# Llamadas API: https://tu-backend.onrender.com/api/activos/
```

---

## 🔍 Verificar qué URL está usando

### Durante desarrollo:

```javascript
// En cualquier componente Vue
console.log('API URL:', import.meta.env.VITE_API_URL)
```

### En la consola del navegador:

```javascript
// Abrir DevTools (F12) → Console
import.meta.env.VITE_API_URL
```

---

## 🌐 Configuración para Producción

### Si tienes backend desplegado en Render:

```bash
# .env.production
VITE_API_URL=https://sca-hospital-backend-abc123.onrender.com
NODE_ENV=production
```

### Si tienes backend desplegado en Railway:

```bash
# .env.production
VITE_API_URL=https://sca-hospital-backend-production.up.railway.app
NODE_ENV=production
```

### Si tienes backend en servidor propio:

```bash
# .env.production
VITE_API_URL=https://api.tu-dominio.com
NODE_ENV=production
```

---

## 🔒 Seguridad y CORS

### En desarrollo (localhost):

Tu `settings.py` de Django ya permite CORS en desarrollo:

```python
CORS_ALLOW_ALL_ORIGINS = True  # Solo en desarrollo
```

### En producción:

Debes configurar los orígenes permitidos en el backend:

**En Render/Railway** (variables de entorno del backend):

```env
# Backend - Variables de entorno en Render/Railway
CORS_ALLOWED_ORIGINS=https://tu-frontend.vercel.app,https://tu-frontend.netlify.app
CORS_ALLOW_ALL=False
ALLOWED_HOSTS=tu-backend.onrender.com
CSRF_TRUSTED_ORIGINS=https://tu-frontend.vercel.app
```

---

## 📦 Deploy del Frontend

### Opción 1: Vercel

1. **Conectar repositorio** a Vercel

2. **Configurar variables de entorno** en Vercel:
   ```
   VITE_API_URL=https://tu-backend.onrender.com
   ```

3. **Deploy**:
   ```bash
   git push origin main
   # Vercel hace deploy automáticamente
   ```

### Opción 2: Netlify

1. **Conectar repositorio** a Netlify

2. **Configurar build**:
   - Build command: `npm run build`
   - Publish directory: `dist`

3. **Configurar variables de entorno** en Netlify:
   ```
   VITE_API_URL=https://tu-backend.onrender.com
   ```

### Opción 3: Manual

```bash
# 1. Crear .env.production con tu URL real
cd sca-hospital/frontend
echo "VITE_API_URL=https://tu-backend.onrender.com" > .env.production

# 2. Build
npm run build

# 3. El directorio dist/ contiene tu app lista para deploy
# Súbelo a tu servidor
```

---

## ⚙️ Configuración Avanzada: Múltiples Backends

Si tienes varios backends (desarrollo, staging, producción):

### `.env.development`
```bash
VITE_API_URL=http://localhost:8000
```

### `.env.staging`
```bash
VITE_API_URL=https://staging-backend.onrender.com
```

### `.env.production`
```bash
VITE_API_URL=https://production-backend.onrender.com
```

**Build con ambiente específico**:
```bash
# Para staging
vite build --mode staging

# Para producción
vite build --mode production
```

---

## 🧪 Testing con diferentes APIs

### Cambiar temporalmente la URL:

```bash
# En desarrollo, sobrescribir temporalmente
VITE_API_URL=https://otro-backend.com npm run dev
```

### En código (para testing):

```javascript
// frontend/src/services/api.js
const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Para probar con otra URL sin cambiar .env
if (import.meta.env.MODE === 'test') {
  baseURL = 'http://mock-api:8000'
}
```

---

## 📋 Checklist de Configuración

### Desarrollo Local (Docker):
- [ ] Crear `.env.local` con `VITE_API_URL=http://localhost:8000`
- [ ] `docker-compose up -d`
- [ ] Verificar en consola: `import.meta.env.VITE_API_URL`
- [ ] Probar login en http://localhost:5173

### Producción:
- [ ] Crear `.env.production` con URL real del backend
- [ ] Configurar CORS en backend con URL del frontend
- [ ] Configurar `ALLOWED_HOSTS` en backend
- [ ] Configurar `CSRF_TRUSTED_ORIGINS` en backend
- [ ] `npm run build`
- [ ] Deploy a Vercel/Netlify
- [ ] Verificar en producción que las llamadas API funcionan

---

## 🐛 Troubleshooting

### Error: "Network Error" o "CORS policy"

**Causa**: El backend no permite requests desde tu frontend

**Solución**:
```python
# Backend - settings.py o variables de entorno
CORS_ALLOWED_ORIGINS=https://tu-frontend.vercel.app
CSRF_TRUSTED_ORIGINS=https://tu-frontend.vercel.app
```

### Error: "Failed to fetch" en producción

**Causa**: URL del backend incorrecta en `.env.production`

**Solución**:
```bash
# Verificar que la URL esté bien
cat .env.production

# Debe ser HTTPS en producción
VITE_API_URL=https://tu-backend.onrender.com  # ✅ Correcto
VITE_API_URL=http://tu-backend.onrender.com   # ❌ Incorrecto (http)
```

### El frontend usa la URL incorrecta

**Causa**: Vite carga variables en build time, no runtime

**Solución**:
```bash
# Después de cambiar .env, rebuild
npm run build

# O reiniciar dev server
npm run dev
```

---

## 📚 Resumen

| Archivo | Contenido | Cuándo se usa |
|---------|-----------|---------------|
| `.env.local` | `VITE_API_URL=http://localhost:8000` | Docker Compose |
| `.env.development` | `VITE_API_URL=http://localhost:8000` | npm run dev |
| `.env.production` | `VITE_API_URL=https://backend-real.com` | npm run build |

**NO subas archivos `.env.*` a Git** - Ya están en `.gitignore`

---

¿Necesitas ayuda con alguna configuración específica? 🚀


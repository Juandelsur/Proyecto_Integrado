# 🚀 GUÍA DE DESPLIEGUE EN VERCEL

## 📋 Pre-requisitos

✅ Código frontend migrado a arquitectura Cloud (sin referencias localhost)  
✅ Backend desplegado en Render: `https://backend-sca.onrender.com`  
✅ Variables de entorno configuradas localmente (`.env`, `.env.production`)

---

## 🔧 PASO 1: Preparar el Proyecto

### 1.1 Verificar que el código esté en Git

```bash
cd frontend/
git status
```

Si hay cambios sin commitear:

```bash
git add .
git commit -m "feat: Migrar frontend a arquitectura Cloud (Vercel)"
git push origin main
```

### 1.2 Verificar configuración de build

Archivo `package.json` debe tener:

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  }
}
```

---

## 🌐 PASO 2: Desplegar en Vercel

### Opción A: Desde el Dashboard de Vercel (Recomendado)

1. **Ir a:** [vercel.com](https://vercel.com)
2. **Login** con GitHub/GitLab/Bitbucket
3. **Click:** "Add New..." → "Project"
4. **Importar** el repositorio de Git
5. **Configurar:**
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend` (si tu repo incluye backend)
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
   - **Install Command:** `npm install`

6. **Click:** "Deploy"

### Opción B: Desde CLI (Avanzado)

```bash
# Instalar Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy desde el directorio frontend
cd frontend/
vercel

# Seguir las instrucciones interactivas
```

---

## ⚙️ PASO 3: Configurar Variables de Entorno

### 3.1 En Vercel Dashboard

1. Ir a: **Project Settings** → **Environment Variables**
2. Agregar variable:

| Key | Value | Environments |
|-----|-------|--------------|
| `VITE_API_URL` | `https://backend-sca.onrender.com` | ✅ Production, ✅ Preview, ✅ Development |

3. **Click:** "Save"

### 3.2 Redeploy

Después de agregar variables de entorno:

1. Ir a: **Deployments**
2. Click en los "..." del último deployment
3. **Redeploy**

---

## 🔒 PASO 4: Configurar CORS en Backend

### 4.1 Obtener la URL de Vercel

Después del deploy, Vercel te dará una URL como:
- `https://your-app.vercel.app` (Producción)
- `https://your-app-git-branch.vercel.app` (Preview)

### 4.2 Actualizar Django settings.py (Backend en Render)

En `backend/config/settings.py`:

```python
# CORS Configuration
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",                    # Dev local
    "https://your-app.vercel.app",              # Producción
    "https://your-app-git-main.vercel.app",     # Preview (opcional)
]

# O si prefieres wildcards (menos seguro):
# CORS_ALLOWED_ORIGIN_REGEXES = [
#     r"^https://.*\.vercel\.app$",
# ]

# Headers permitidos
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Métodos permitidos
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
```

### 4.3 Commitear y Deploy en Render

```bash
cd backend/
git add config/settings.py
git commit -m "feat: Configurar CORS para Vercel"
git push origin main
```

Render re-desplegará automáticamente.

---

## ✅ PASO 5: Verificar el Despliegue

### 5.1 Probar la Aplicación

1. Abrir la URL de Vercel: `https://your-app.vercel.app`
2. **Pruebas básicas:**
   - ✅ La página carga correctamente
   - ✅ Los assets (CSS, JS, imágenes) cargan
   - ✅ El login funciona
   - ✅ Las peticiones al backend se completan
   - ✅ No hay errores de CORS en la consola

### 5.2 Revisar Logs

**En Vercel:**
- Ir a: **Deployments** → Click en el deployment → **Logs**

**En Render (Backend):**
- Ir a: Dashboard → Servicio → **Logs**

### 5.3 Revisar Consola del Navegador

Abrir DevTools (F12) y verificar:
- ❌ No hay errores de CORS
- ❌ No hay errores 404 en assets
- ✅ Las peticiones API responden 200/201

---

## 🐛 SOLUCIÓN DE PROBLEMAS COMUNES

### Problema 1: Error CORS

**Síntoma:**
```
Access to XMLHttpRequest at 'https://backend-sca.onrender.com/api/...' 
from origin 'https://your-app.vercel.app' has been blocked by CORS policy
```

**Solución:**
1. Verificar que la URL de Vercel esté en `CORS_ALLOWED_ORIGINS` del backend
2. Commitear y redeploy el backend en Render
3. Esperar 1-2 minutos para que Render aplique cambios
4. Probar nuevamente

### Problema 2: 404 en Rutas de Vue Router

**Síntoma:** Al refrescar la página en una ruta como `/activos/123`, obtienes 404.

**Solución:** Crear archivo `vercel.json` en la raíz del proyecto:

```json
{
  "routes": [
    {
      "src": "/assets/(.*)",
      "dest": "/assets/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ]
}
```

### Problema 3: Variables de Entorno no se Cargan

**Síntoma:** `import.meta.env.VITE_API_URL` es `undefined`.

**Solución:**
1. Verificar que la variable empiece con `VITE_`
2. Verificar que esté configurada en Vercel Dashboard
3. Redeploy después de agregar variables
4. Verificar en build logs que la variable se carga

### Problema 4: Backend en Cold Start (Render Free Tier)

**Síntoma:** Primera petición tarda 30+ segundos.

**Solución:**
1. **Temporal:** Configurar timeout en Axios a 30 segundos
2. **Permanente:** Upgrade a plan de pago en Render
3. **Alternativa:** Implementar "keep-alive" pings cada 10 minutos

---

## 🔄 FLUJO DE DESARROLLO

### Desarrollo Local

```bash
# Iniciar dev server
npm run dev

# La app usará .env.development
# Por defecto apunta a Render (no localhost)
```

### Deploy de Preview (Ramas)

```bash
git checkout -b feature/nueva-funcionalidad
# Hacer cambios...
git add .
git commit -m "feat: Nueva funcionalidad"
git push origin feature/nueva-funcionalidad
```

Vercel automáticamente crea un **Preview Deployment** con URL única.

### Deploy a Producción

```bash
git checkout main
git merge feature/nueva-funcionalidad
git push origin main
```

Vercel automáticamente despliega a **Producción**.

---

## 📊 MONITOREO Y ANALYTICS

### Vercel Analytics (Opcional)

1. Ir a: **Project** → **Analytics**
2. Habilitar **Web Analytics**
3. Instalar paquete:

```bash
npm install @vercel/analytics
```

4. Agregar en `src/main.js`:

```javascript
import { inject } from '@vercel/analytics'
inject()
```

### Logs en Tiempo Real

```bash
vercel logs https://your-app.vercel.app --follow
```

---

## 🎉 ¡LISTO!

Tu aplicación Vue 3 ahora está desplegada en Vercel y conectada al backend en Render.

**URLs importantes:**
- 🌐 Frontend (Vercel): `https://your-app.vercel.app`
- 🔧 Backend (Render): `https://backend-sca.onrender.com`
- 🗄️ Base de Datos (Neon): Conectada al backend

---

## 📚 Recursos Adicionales

- [Documentación de Vercel](https://vercel.com/docs)
- [Vite + Vercel](https://vercel.com/docs/frameworks/vite)
- [Variables de Entorno en Vercel](https://vercel.com/docs/environment-variables)
- [CORS en Django](https://github.com/adamchainz/django-cors-headers)

---

**Última actualización:** 2025-12-22

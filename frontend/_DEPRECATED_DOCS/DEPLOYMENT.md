# 🚀 Guía de Despliegue en Vercel

Esta guía te ayudará a desplegar la aplicación Vue 3 en Vercel y conectarla con el backend en Render.

---

## 📋 Pre-requisitos

- Cuenta en [Vercel](https://vercel.com)
- Repositorio Git (GitHub, GitLab, o Bitbucket)
- Backend desplegado en Render: `https://backend-sca.onrender.com`

---

## 🔧 Configuración Local

### 1. Variables de Entorno

El proyecto usa diferentes archivos `.env` según el ambiente:

- **`.env.development`**: Desarrollo local (usa `http://localhost:8000`)
- **`.env.production`**: Producción (usa `https://backend-sca.onrender.com`)
- **`.env.local`**: Sobrescribe cualquier configuración (no se sube a Git)

### 2. Probar Localmente

```bash
# Desarrollo (usa .env.development)
npm run dev

# Build de producción (usa .env.production)
npm run build

# Preview del build
npm run preview
```

---

## 🌐 Despliegue en Vercel

### Opción 1: Despliegue desde la CLI de Vercel

1. **Instalar Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Login en Vercel:**
   ```bash
   vercel login
   ```

3. **Desplegar:**
   ```bash
   cd frontend
   vercel
   ```

4. **Configurar variables de entorno en Vercel:**
   ```bash
   vercel env add VITE_API_URL production
   # Ingresa: https://backend-sca.onrender.com
   ```

5. **Desplegar a producción:**
   ```bash
   vercel --prod
   ```

### Opción 2: Despliegue desde el Dashboard de Vercel (Recomendado)

1. **Ir a [vercel.com](https://vercel.com) y hacer login**

2. **Importar proyecto:**
   - Click en "Add New..." → "Project"
   - Selecciona tu repositorio Git
   - Vercel detectará automáticamente que es un proyecto Vite

3. **Configurar el proyecto:**
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend` (si tu repo es un monorepo)
   - **Build Command:** `npm run build` (ya configurado por defecto)
   - **Output Directory:** `dist` (ya configurado por defecto)

4. **Agregar Variables de Entorno:**
   - En "Environment Variables", agregar:
     ```
     VITE_API_URL = https://backend-sca.onrender.com
     ```
   - Aplicar a: Production, Preview, Development

5. **Deploy:**
   - Click en "Deploy"
   - Espera a que termine el build (1-2 minutos)

---

## ✅ Verificación Post-Despliegue

### 1. Verificar que la aplicación carga

Abre la URL de Vercel (ej: `https://tu-proyecto.vercel.app`)

### 2. Verificar la conexión con el backend

Abre la consola del navegador (F12) y verifica:

```javascript
// En la consola del navegador
console.log(import.meta.env.VITE_API_URL)
// Debería mostrar: https://backend-sca.onrender.com
```

### 3. Probar una petición al backend

```javascript
// En la consola del navegador
fetch('https://backend-sca.onrender.com/api/activos/')
  .then(res => res.json())
  .then(data => console.log(data))
```

---

## 🔄 Configuración de CORS en el Backend

**IMPORTANTE:** Asegúrate de que tu backend en Render tenga configurado CORS para permitir peticiones desde Vercel.

En tu `backend/config/settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',  # Desarrollo local (Vite)
    'http://localhost:4173',  # Preview local (Vite)
    'https://tu-proyecto.vercel.app',  # Producción Vercel
    'https://*.vercel.app',  # Todos los previews de Vercel
]

# O si prefieres permitir todos los orígenes (menos seguro):
CORS_ALLOW_ALL_ORIGINS = True
```

---

## 🐛 Troubleshooting

### Error 404 al recargar páginas internas

**Causa:** Vue Router usa modo history, necesita rewrites.

**Solución:** Ya está configurado en `vercel.json`:
```json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}
```

### Error de CORS

**Causa:** El backend no permite peticiones desde el dominio de Vercel.

**Solución:** Actualiza `CORS_ALLOWED_ORIGINS` en el backend (ver sección anterior).

### Variables de entorno no funcionan

**Causa:** Las variables deben empezar con `VITE_` para ser expuestas al cliente.

**Solución:** Asegúrate de usar `VITE_API_URL` (no `API_URL`).

---

## 📚 Recursos Adicionales

- [Documentación de Vercel](https://vercel.com/docs)
- [Vite Environment Variables](https://vitejs.dev/guide/env-and-mode.html)
- [Vue Router History Mode](https://router.vuejs.org/guide/essentials/history-mode.html)

---

## 🎯 Checklist de Despliegue

- [ ] Axios instalado (`npm install axios`)
- [ ] Archivo `src/services/api.js` creado
- [ ] Archivos `.env.production` y `.env.development` creados
- [ ] Archivo `vercel.json` creado
- [ ] Variables de entorno configuradas en Vercel Dashboard
- [ ] CORS configurado en el backend
- [ ] Aplicación desplegada y funcionando
- [ ] Peticiones al backend funcionando correctamente


# 🔒 CONFIGURACIÓN CRÍTICA: CORS en Backend (Render)

## ⚠️ IMPORTANTE

Para que el frontend en Vercel pueda comunicarse con el backend en Render, **DEBES** configurar CORS correctamente en Django.

---

## 📝 PASO A PASO

### 1. Instalar django-cors-headers (si no está instalado)

```bash
cd backend/
pip install django-cors-headers
pip freeze > requirements.txt
```

### 2. Actualizar settings.py

#### 2.1 Agregar a INSTALLED_APPS

```python
# backend/config/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',  # ← Agregar esto
    
    # Local apps
    'core',
]
```

#### 2.2 Agregar middleware

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Si usas WhiteNoise
    'corsheaders.middleware.CorsMiddleware',  # ← Debe ir ANTES de CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

#### 2.3 Configurar CORS_ALLOWED_ORIGINS

**Opción A: Dominios específicos (Recomendado para Producción)**

```python
# Configuración CORS para Vercel
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",                      # Dev local (Vite)
    "http://localhost:3000",                      # Dev local alternativo
    "https://your-app.vercel.app",                # ← REEMPLAZAR con tu dominio real
    "https://your-app-git-main.vercel.app",       # ← Preview deployments (opcional)
]
```

**Opción B: Wildcard (Solo para Testing/Development)**

```python
# ⚠️ NO USAR EN PRODUCCIÓN REAL
CORS_ALLOW_ALL_ORIGINS = True
```

**Opción C: Regex (Si tienes múltiples subdominios)**

```python
import re

CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://.*\.vercel\.app$",          # Todos los dominios *.vercel.app
    r"^http://localhost:\d+$",             # Localhost en cualquier puerto
]
```

#### 2.4 Configurar Headers y Métodos

```python
# Headers permitidos
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',      # ← CRÍTICO para JWT
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Métodos HTTP permitidos
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# Si necesitas enviar credenciales (cookies, auth)
# Para JWT con Bearer token NO es necesario
CORS_ALLOW_CREDENTIALS = False
```

---

## 🔍 CÓMO OBTENER TU DOMINIO DE VERCEL

### Después del primer deploy en Vercel:

1. Ve a tu proyecto en Vercel Dashboard
2. Copia la URL que aparece, por ejemplo:
   - `https://tu-proyecto-abc123.vercel.app` (Preview)
   - `https://tu-proyecto.vercel.app` (Production)

3. Actualiza `CORS_ALLOWED_ORIGINS` en `settings.py` con esa URL

---

## 🧪 VERIFICAR CONFIGURACIÓN

### 1. Verificar en el código

```bash
cd backend/
grep -A 10 "CORS_ALLOWED_ORIGINS" config/settings.py
```

### 2. Probar desde el navegador

Abre la consola del navegador (F12) en tu app de Vercel y ejecuta:

```javascript
fetch('https://backend-sca.onrender.com/api/activos/', {
  headers: {
    'Content-Type': 'application/json'
  }
})
.then(res => res.json())
.then(data => console.log('✅ CORS OK:', data))
.catch(err => console.error('❌ CORS Error:', err))
```

Si ves `✅ CORS OK:` → CORS configurado correctamente  
Si ves `❌ CORS Error:` → Revisar configuración

---

## 🐛 TROUBLESHOOTING

### Error: "CORS policy: No 'Access-Control-Allow-Origin' header"

**Causa:** El dominio de Vercel no está en `CORS_ALLOWED_ORIGINS`

**Solución:**
1. Verificar la URL exacta en Vercel
2. Agregarla a `CORS_ALLOWED_ORIGINS` en `settings.py`
3. Commitear y push → Render re-desplegará automáticamente
4. Esperar 1-2 minutos
5. Probar nuevamente

### Error: "CORS policy: The value of the 'Access-Control-Allow-Origin' header"

**Causa:** Hay un typo en la URL o falta el protocolo (https://)

**Solución:**
```python
# ❌ MAL
CORS_ALLOWED_ORIGINS = [
    "your-app.vercel.app",  # Falta https://
]

# ✅ BIEN
CORS_ALLOWED_ORIGINS = [
    "https://your-app.vercel.app",
]
```

### Error: "Method PUT is not allowed by Access-Control-Allow-Methods"

**Causa:** Método HTTP no está en `CORS_ALLOW_METHODS`

**Solución:** Agregar el método en `settings.py`

---

## 📝 CHECKLIST FINAL

- [ ] `django-cors-headers` instalado en `requirements.txt`
- [ ] `corsheaders` en `INSTALLED_APPS`
- [ ] `CorsMiddleware` en `MIDDLEWARE` (antes de `CommonMiddleware`)
- [ ] `CORS_ALLOWED_ORIGINS` con dominio real de Vercel
- [ ] `CORS_ALLOW_HEADERS` incluye `'authorization'`
- [ ] `CORS_ALLOW_METHODS` incluye todos los métodos necesarios
- [ ] Cambios commiteados y pusheados a Git
- [ ] Render re-desplegó automáticamente (verificar logs)
- [ ] Probado desde Vercel: API calls funcionan sin errores CORS

---

## 🚀 DEPLOY

Después de hacer los cambios:

```bash
cd backend/
git add .
git commit -m "feat: Configurar CORS para Vercel"
git push origin main
```

Render detectará el push y re-desplegará automáticamente (1-2 minutos).

---

## 📚 REFERENCIA

- [django-cors-headers docs](https://github.com/adamchainz/django-cors-headers)
- [MDN: CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [Vercel Domains](https://vercel.com/docs/concepts/projects/domains)

---

**Última actualización:** 2025-12-22

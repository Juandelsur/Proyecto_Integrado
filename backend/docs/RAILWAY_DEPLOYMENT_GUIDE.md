# 🚀 Guía de Despliegue en Railway + NeonTech

## ✅ Configuración Completada

El proyecto **backend_sca** está configurado para despliegue en producción con:
- **Railway**: Plataforma de hosting
- **NeonTech**: Base de datos PostgreSQL con SSL
- **Gunicorn**: Servidor WSGI de producción
- **Whitenoise**: Servicio de archivos estáticos

---

## 📁 Archivos Configurados

### ✅ 1. requirements.txt
Se agregaron las dependencias de producción:
```txt
# Production Server
gunicorn>=21.2.0

# Static Files (Production)
whitenoise>=6.6.0

# Database URL Parser
dj-database-url>=2.1.0
```

### ✅ 2. Procfile (Raíz del proyecto)
```
web: gunicorn config.wsgi:application --log-file -
```

**Nota**: Railway detecta automáticamente este archivo y ejecuta el comando especificado.

### ✅ 3. config/settings.py
Se modificaron las siguientes secciones:

#### A) Imports
```python
import dj_database_url
```

#### B) Seguridad y Hosts
```python
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-...')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')
CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', 'http://localhost').split(',')
```

#### C) Middleware (Orden crítico)
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # PRIMERO
    'whitenoise.middleware.WhiteNoiseMiddleware',     # SEGUNDO
    'corsheaders.middleware.CorsMiddleware',
    # ... resto de middlewares
]
```

#### D) Base de Datos (Dinámica)
```python
if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True
        )
    }
else:
    # Configuración local...
```

#### E) Archivos Estáticos (Whitenoise)
```python
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

---

## 🗄️ Paso 1: Configurar Base de Datos en NeonTech

### 1.1. Crear Cuenta en NeonTech
1. Ve a https://neon.tech/
2. Crea una cuenta gratuita
3. Haz clic en **"Create Project"**

### 1.2. Configurar Proyecto
1. **Project Name**: `sca-hospital`
2. **Region**: Selecciona la más cercana (ej: US East)
3. **PostgreSQL Version**: 16 (recomendado)
4. Haz clic en **"Create Project"**

### 1.3. Obtener Connection String
1. En el dashboard, haz clic en **"Connection Details"**
2. Copia la **Connection String** (formato: `postgresql://user:password@host/database?sslmode=require`)
3. **IMPORTANTE**: Guarda esta URL, la necesitarás en Railway

**Ejemplo de Connection String**:
```
postgresql://sca_user:AbCd1234XyZ@ep-cool-name-123456.us-east-2.aws.neon.tech/sca_hospital?sslmode=require
```

---

## 🚂 Paso 2: Desplegar en Railway

### 2.1. Crear Cuenta en Railway
1. Ve a https://railway.app/
2. Crea una cuenta (puedes usar GitHub)
3. Haz clic en **"New Project"**

### 2.2. Conectar Repositorio
1. Selecciona **"Deploy from GitHub repo"**
2. Autoriza Railway para acceder a tu repositorio
3. Selecciona el repositorio `Proyecto_Integrado`
4. Railway detectará automáticamente el `Procfile`

### 2.3. Configurar Variables de Entorno
1. En el dashboard de Railway, haz clic en tu proyecto
2. Ve a la pestaña **"Variables"**
3. Agrega las siguientes variables:

```env
# Django Core
SECRET_KEY=tu-clave-secreta-super-segura-genera-una-nueva
DEBUG=False
ALLOWED_HOSTS=*.railway.app,tu-dominio-personalizado.com

# CSRF (CRÍTICO)
CSRF_TRUSTED_ORIGINS=https://tu-proyecto.railway.app,https://tu-dominio-personalizado.com

# Database (NeonTech)
DATABASE_URL=postgresql://sca_user:AbCd1234XyZ@ep-cool-name-123456.us-east-2.aws.neon.tech/sca_hospital?sslmode=require

# JWT
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440

# CORS
CORS_ALLOW_ALL=False
CORS_ALLOWED_ORIGINS=https://tu-frontend.vercel.app,https://tu-dominio-personalizado.com
```

**IMPORTANTE**:
- Reemplaza `tu-proyecto.railway.app` con tu URL real de Railway
- Reemplaza la `DATABASE_URL` con la de NeonTech
- Genera una nueva `SECRET_KEY` segura (ver sección 2.4)

### 2.4. Generar SECRET_KEY Segura
```python
# En tu terminal local:
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copia el resultado y úsalo como `SECRET_KEY` en Railway.

---

## 🔧 Paso 3: Ejecutar Migraciones en Producción

### 3.1. Acceder a la Terminal de Railway
1. En el dashboard de Railway, haz clic en tu proyecto
2. Ve a la pestaña **"Deployments"**
3. Haz clic en el deployment activo
4. Haz clic en **"View Logs"**

### 3.2. Ejecutar Migraciones
Railway ejecutará automáticamente las migraciones si agregas un script de inicio.

**Opción A: Agregar comando de migración al Procfile**
```
release: python backend/manage.py migrate
web: gunicorn config.wsgi:application --log-file -
```

**Opción B: Ejecutar manualmente desde Railway CLI**
```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Conectar al proyecto
railway link

# Ejecutar migraciones
railway run python backend/manage.py migrate
```

---

## 🌱 Paso 4: Poblar Datos Iniciales

### 4.1. Ejecutar Seed desde Railway CLI
```bash
railway run python backend/manage.py seed_data
```

### 4.2. Crear Superusuario
```bash
railway run python backend/manage.py createsuperuser
```

---

## ✅ Paso 5: Verificar Despliegue

### 5.1. Verificar que el Servidor Esté Corriendo
1. En Railway, ve a **"Deployments"**
2. Verifica que el estado sea **"Success"** (verde)
3. Haz clic en el botón **"Open App"** para ver tu URL

### 5.2. Acceder al Admin
```
https://tu-proyecto.railway.app/admin/
```

### 5.3. Acceder a la API Docs
```
https://tu-proyecto.railway.app/api/docs/
```

### 5.4. Probar un Endpoint
```bash
curl https://tu-proyecto.railway.app/api/activos/
```

---

## 🔍 Solución de Problemas

### Error: "DisallowedHost at /"
**Causa**: `ALLOWED_HOSTS` no incluye tu dominio de Railway.

**Solución**:
```env
ALLOWED_HOSTS=*.railway.app,tu-proyecto.railway.app
```

### Error: "CSRF verification failed"
**Causa**: `CSRF_TRUSTED_ORIGINS` no incluye tu dominio HTTPS.

**Solución**:
```env
CSRF_TRUSTED_ORIGINS=https://tu-proyecto.railway.app
```

**IMPORTANTE**: Debe incluir `https://` al inicio.

### Error: "could not connect to server"
**Causa**: `DATABASE_URL` incorrecta o NeonTech no está accesible.

**Solución**:
1. Verifica que la `DATABASE_URL` sea correcta
2. Asegúrate de que incluya `?sslmode=require` al final
3. Verifica que NeonTech esté activo

### Error: "No module named 'whitenoise'"
**Causa**: Las dependencias no se instalaron correctamente.

**Solución**:
1. Verifica que `requirements.txt` esté en la raíz del proyecto
2. Railway debería instalar automáticamente
3. Si persiste, verifica los logs de build

### Error: "Static files not found"
**Causa**: Los archivos estáticos no se recolectaron.

**Solución**:
Agrega al Procfile:
```
release: python backend/manage.py collectstatic --noinput && python backend/manage.py migrate
web: gunicorn config.wsgi:application --log-file -
```

---

## 📊 Monitoreo y Logs

### Ver Logs en Tiempo Real
1. En Railway, ve a tu proyecto
2. Haz clic en **"View Logs"**
3. Verás los logs de Gunicorn y Django

### Logs Útiles
```bash
# Ver logs desde Railway CLI
railway logs

# Ver logs con filtro
railway logs --filter "ERROR"
```

---

## 🔒 Seguridad en Producción

### Checklist de Seguridad

✅ **DEBUG = False** en producción  
✅ **SECRET_KEY** única y segura  
✅ **ALLOWED_HOSTS** configurado correctamente  
✅ **CSRF_TRUSTED_ORIGINS** configurado con HTTPS  
✅ **DATABASE_URL** con SSL habilitado  
✅ **CORS_ALLOWED_ORIGINS** limitado a dominios específicos  
✅ **Contraseñas de admin** cambiadas  

### Cambiar Contraseñas en Producción
```bash
railway run python backend/manage.py changepassword admin
```

---

## 🎉 Resumen de Configuración

### Archivos Modificados/Creados
✅ **requirements.txt** - Dependencias de producción agregadas  
✅ **Procfile** - Comando de inicio para Railway  
✅ **config/settings.py** - Configuración dinámica para producción  
✅ **RAILWAY_DEPLOYMENT_GUIDE.md** - Esta guía  

### Variables de Entorno Requeridas
✅ **SECRET_KEY** - Clave secreta de Django  
✅ **DEBUG** - False en producción  
✅ **ALLOWED_HOSTS** - Dominios permitidos  
✅ **CSRF_TRUSTED_ORIGINS** - Orígenes CSRF confiables  
✅ **DATABASE_URL** - URL de conexión a NeonTech  

### Servicios Configurados
✅ **Railway** - Hosting de la aplicación  
✅ **NeonTech** - Base de datos PostgreSQL  
✅ **Gunicorn** - Servidor WSGI  
✅ **Whitenoise** - Archivos estáticos  

---

## 🚀 Próximos Pasos

1. ✅ **Configurar NeonTech** y obtener DATABASE_URL
2. ✅ **Crear proyecto en Railway** y conectar repositorio
3. ✅ **Configurar variables de entorno** en Railway
4. ✅ **Ejecutar migraciones** en producción
5. ✅ **Poblar datos iniciales** con seed_data
6. ✅ **Verificar que todo funcione** (admin + API)
7. ✅ **Configurar dominio personalizado** (opcional)
8. ✅ **Configurar CI/CD** para deploys automáticos

---

## 📞 Soporte

Si encuentras problemas:
1. Revisa los logs en Railway
2. Verifica las variables de entorno
3. Asegúrate de que NeonTech esté activo
4. Verifica que el Procfile esté en la raíz del proyecto
5. Consulta la documentación de Railway: https://docs.railway.app/


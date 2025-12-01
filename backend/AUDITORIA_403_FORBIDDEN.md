# 🔍 AUDITORÍA DE SEGURIDAD - ERROR 403 FORBIDDEN

## 📋 CONTEXTO

**Error:** 403 Forbidden al hacer GET a `/api/historial-movimientos/`  
**Entorno:** Backend Django REST Framework (Render) + Frontend Vue (Vercel)  
**Evidencia:** Header `Authorization: Bearer eyJ...` se envía correctamente (verificado en Network)

---

## ✅ PUNTO 1: CONFIGURACIÓN DE CORS Y CSRF

### **1.1 CORS_ALLOWED_ORIGINS** ✅

**Archivo:** `backend/config/settings.py` (líneas 206-207)

```python
CORS_ALLOWED_ORIGINS_STR = os.environ.get('CORS_ALLOWED_ORIGINS', 'http://localhost:5173,http://127.0.0.1:5173')
CORS_ALLOWED_ORIGINS = [origin.strip() for origin in CORS_ALLOWED_ORIGINS_STR.split(',') if origin.strip()]
```

**Estado:** ✅ **CORRECTO** - La configuración es correcta, pero necesitas verificar la variable de entorno en Render.

**Acción requerida:**
1. Ve a tu dashboard de Render → Tu servicio backend → Environment
2. Verifica que exista la variable: `CORS_ALLOWED_ORIGINS`
3. El valor debe ser tu dominio de Vercel **SIN SLASH AL FINAL**:
   ```
   https://tu-app.vercel.app
   ```
   ❌ **INCORRECTO:** `https://tu-app.vercel.app/`  
   ✅ **CORRECTO:** `https://tu-app.vercel.app`

4. Si tienes múltiples dominios, sepáralos con comas:
   ```
   https://tu-app.vercel.app,https://tu-dominio-custom.com
   ```

---

### **1.2 CSRF_TRUSTED_ORIGINS** ⚠️ **CRÍTICO**

**Archivo:** `backend/config/settings.py` (línea 47)

```python
CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', 'http://localhost').split(',')
```

**Estado:** ⚠️ **REQUIERE CONFIGURACIÓN EN PRODUCCIÓN**

**Problema:** Django 4+ requiere que los orígenes HTTPS estén en `CSRF_TRUSTED_ORIGINS` para aceptar requests.

**Acción requerida:**
1. Ve a Render → Environment Variables
2. Agrega/actualiza la variable: `CSRF_TRUSTED_ORIGINS`
3. El valor debe incluir **HTTPS** y tu dominio de backend de Render:
   ```
   https://tu-backend.onrender.com,https://tu-app.vercel.app
   ```

**Ejemplo completo:**
```bash
CSRF_TRUSTED_ORIGINS=https://sca-hospital-backend.onrender.com,https://sca-hospital-frontend.vercel.app
```

---

### **1.3 Orden de Middleware** ✅

**Archivo:** `backend/config/settings.py` (líneas 75-79)

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # PRIMERO
    'whitenoise.middleware.WhiteNoiseMiddleware',     # SEGUNDO
    'corsheaders.middleware.CorsMiddleware',          # TERCERO ✅
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',      # DESPUÉS DE CORS ✅
```

**Estado:** ✅ **CORRECTO** - `CorsMiddleware` está antes de `CommonMiddleware`.

---

### **1.4 CORS_ALLOW_CREDENTIALS** ✅

**Archivo:** `backend/config/settings.py` (línea 210)

```python
CORS_ALLOW_CREDENTIALS = True
```

**Estado:** ✅ **CORRECTO** - Permite enviar cookies y headers de autenticación.

---

## ✅ PUNTO 2: PERMISOS DE DRF

### **2.1 DEFAULT_PERMISSION_CLASSES** ⚠️ **POSIBLE PROBLEMA**

**Archivo:** `backend/config/settings.py` (líneas 227-229)

```python
'DEFAULT_PERMISSION_CLASSES': [
    'rest_framework.permissions.IsAuthenticatedOrReadOnly',
],
```

**Estado:** ⚠️ **PERMISIVO** - Permite lectura sin autenticación.

**Análisis:**
- Este permiso permite GET sin autenticación, pero los ViewSets individuales pueden sobrescribirlo.
- No es la causa del 403, ya que el ViewSet tiene permisos más restrictivos.

---

### **2.2 HistorialMovimientoViewSet Permissions** ✅ **CORRECTO**

**Archivo:** `backend/core/views.py` (línea 776)

```python
permission_classes = [IsAuthenticated, IsJefeOrAdminReadOnly]
```

**Estado:** ✅ **CORRECTO** - Requiere autenticación y permite lectura a Técnicos/Jefes.

**Permisos del ViewSet:**
- `IsAuthenticated`: Usuario debe estar autenticado ✅
- `IsJefeOrAdminReadOnly`: Permite GET a Técnicos, Jefes y Admin ✅

**Verificación del permiso personalizado:**
```python
# backend/core/permissions.py (líneas 84-86)
if rol_nombre in ['Técnico', 'Jefe de Departamento']:
    return request.method in permissions.SAFE_METHODS  # GET, HEAD, OPTIONS
```

**Conclusión:** Los permisos están correctos. El problema NO está aquí.

---

## ⚠️ PUNTO 3: VALIDEZ DEL TOKEN Y USUARIO

### **3.1 Configuración de SIMPLE_JWT** ✅

**Archivo:** `backend/config/settings.py` (líneas 249-250)

```python
'ACCESS_TOKEN_LIFETIME': timedelta(minutes=int(os.environ.get('JWT_ACCESS_TOKEN_LIFETIME', '60'))),
'REFRESH_TOKEN_LIFETIME': timedelta(minutes=int(os.environ.get('JWT_REFRESH_TOKEN_LIFETIME', '1440'))),
```

**Estado:** ✅ **CORRECTO**

**Configuración actual:**
- Access Token: 60 minutos (1 hora)
- Refresh Token: 1440 minutos (24 horas)

**Posible problema:** Si el usuario ha estado inactivo por más de 1 hora, el token expiró.

**Solución:**
1. En el frontend, implementa refresh automático del token
2. O aumenta el tiempo de vida del access token en producción:
   ```bash
   # En Render Environment Variables
   JWT_ACCESS_TOKEN_LIFETIME=480  # 8 horas
   ```

---

### **3.2 Usuario is_active** ⚠️ **VERIFICAR**

**Modelo:** `backend/core/models.py`

El modelo `Usuario` hereda de `AbstractUser`, que incluye el campo `is_active`.

**Posible problema:** Si el usuario tiene `is_active=False`, Django rechazará el token.

**Verificación:**
1. Accede al admin de Django: `https://tu-backend.onrender.com/admin/`
2. Ve a Core → Usuarios
3. Busca el usuario que está teniendo el error 403
4. Verifica que el checkbox **"Activo"** esté marcado ✅

**Comando para verificar desde shell:**
```python
python manage.py shell
>>> from core.models import Usuario
>>> user = Usuario.objects.get(username='nombre_usuario')
>>> print(f"is_active: {user.is_active}")
>>> print(f"rol: {user.rol.nombre_rol if user.rol else 'Sin rol'}")
```

---

## 🎯 DIAGNÓSTICO FINAL

### **Causas más probables del 403 (en orden de probabilidad):**

1. **⚠️ CSRF_TRUSTED_ORIGINS no configurado en Render** (90% probabilidad)
   - Django 4+ rechaza requests HTTPS si el origen no está en CSRF_TRUSTED_ORIGINS
   - **Solución:** Agregar variable de entorno en Render

2. **⚠️ CORS_ALLOWED_ORIGINS mal configurado** (70% probabilidad)
   - Dominio de Vercel no está en la lista
   - Slash al final del dominio
   - **Solución:** Verificar variable de entorno en Render

3. **⚠️ Token expirado** (50% probabilidad)
   - Usuario inactivo por más de 1 hora
   - **Solución:** Refrescar token o aumentar tiempo de vida

4. **⚠️ Usuario is_active=False** (30% probabilidad)
   - Usuario desactivado en el admin
   - **Solución:** Activar usuario en Django Admin

5. **⚠️ Rol del usuario no es Técnico/Jefe/Admin** (20% probabilidad)
   - Usuario tiene un rol diferente
   - **Solución:** Verificar rol en Django Admin

---

## 🚀 PLAN DE ACCIÓN INMEDIATO

### **Paso 1: Configurar variables de entorno en Render** ⚠️ **CRÍTICO**

```bash
# En Render Dashboard → Environment Variables

# 1. CSRF_TRUSTED_ORIGINS (CRÍTICO)
CSRF_TRUSTED_ORIGINS=https://tu-backend.onrender.com,https://tu-frontend.vercel.app

# 2. CORS_ALLOWED_ORIGINS (CRÍTICO)
CORS_ALLOWED_ORIGINS=https://tu-frontend.vercel.app

# 3. CORS_ALLOW_ALL (Desactivar en producción)
CORS_ALLOW_ALL=False

# 4. DEBUG (Desactivar en producción)
DEBUG=False

# 5. ALLOWED_HOSTS
ALLOWED_HOSTS=tu-backend.onrender.com,tu-frontend.vercel.app
```

**Después de agregar las variables:**
1. Guarda los cambios
2. Render reiniciará automáticamente el servicio
3. Espera 2-3 minutos a que el deploy termine

---

### **Paso 2: Verificar usuario en Django Admin**

1. Accede a: `https://tu-backend.onrender.com/admin/`
2. Login con superusuario
3. Ve a **Core → Usuarios**
4. Busca el usuario que tiene el error
5. Verifica:
   - ✅ **Activo** (is_active) está marcado
   - ✅ **Rol** es "Técnico", "Jefe de Departamento" o "Administrador"
   - ✅ **Usuario activo** (is_staff) NO necesita estar marcado

---

### **Paso 3: Probar con token fresco**

1. En el frontend, haz logout
2. Vuelve a hacer login
3. Esto generará un token nuevo
4. Intenta acceder a `/api/historial-movimientos/` nuevamente

---

### **Paso 4: Verificar logs de Render**

1. Ve a Render Dashboard → Tu servicio → Logs
2. Busca errores relacionados con CORS o CSRF:
   ```
   Forbidden (CSRF cookie not set.)
   Forbidden (CSRF token missing or incorrect.)
   Origin checking failed
   ```
3. Comparte los logs conmigo si encuentras errores

---

## 📝 CHECKLIST DE VERIFICACIÓN

- [ ] Variable `CSRF_TRUSTED_ORIGINS` configurada en Render con HTTPS
- [ ] Variable `CORS_ALLOWED_ORIGINS` configurada en Render sin slash final
- [ ] Variable `CORS_ALLOW_ALL=False` en producción
- [ ] Usuario tiene `is_active=True` en Django Admin
- [ ] Usuario tiene rol válido (Técnico/Jefe/Admin)
- [ ] Token no ha expirado (menos de 1 hora desde login)
- [ ] Logs de Render no muestran errores de CORS/CSRF



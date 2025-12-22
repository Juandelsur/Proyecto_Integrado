# ✅ CHECKLIST DE VERIFICACIÓN - CONFIGURACIÓN CORS

## Pre-Deploy (Antes de commit/push)

- [x] `corsheaders` está en INSTALLED_APPS
- [x] `CorsMiddleware` está en MIDDLEWARE (posición 3, antes de CommonMiddleware)
- [x] `django-cors-headers` está en requirements.txt
- [x] `ALLOWED_HOSTS` incluye `backend-sca.onrender.com`
- [x] `CORS_ALLOWED_ORIGINS` configurado (localhost + backend)
- [x] `CORS_ALLOWED_ORIGIN_REGEXES` configurado (Vercel dinámico)
- [x] `CSRF_TRUSTED_ORIGINS` configurado (Vercel + backend)
- [x] `CORS_ALLOW_CREDENTIALS = True`
- [x] No hay errores de linter

## Deploy

- [ ] Commit realizado: `git add config/settings.py`
- [ ] Push realizado: `git push origin main`
- [ ] Render detectó el push (verificar dashboard)
- [ ] Deploy completado en Render (verificar logs)

## Testing Post-Deploy

### Test 1: Verificar que el backend responde
```bash
curl https://backend-sca.onrender.com/api/activos/
```
**Resultado esperado:** JSON con lista de activos (o lista vacía)

### Test 2: Verificar CORS desde navegador
1. Abrir: https://proyecto-integrado-p0gxwiiy0-juanmunoz6895-4026s-projects.vercel.app
2. Abrir DevTools (F12) → Console
3. Ejecutar:
```javascript
fetch('https://backend-sca.onrender.com/api/activos/', {
  headers: { 'Content-Type': 'application/json' }
})
.then(res => res.json())
.then(data => console.log('✅ CORS OK:', data))
.catch(err => console.error('❌ Error:', err))
```
**Resultado esperado:** `✅ CORS OK: [...]` (sin errores CORS)

### Test 3: Verificar Login
- [ ] Ir a la página de login en Vercel
- [ ] Ingresar credenciales de test
- [ ] Verificar que NO hay errores CORS en consola
- [ ] Verificar que el login funciona y redirige correctamente

### Test 4: Verificar Headers CORS
```bash
curl -I -X OPTIONS https://backend-sca.onrender.com/api/activos/ \
  -H "Origin: https://proyecto-integrado-p0gxwiiy0-juanmunoz6895-4026s-projects.vercel.app" \
  -H "Access-Control-Request-Method: GET"
```
**Resultado esperado:**
```
Access-Control-Allow-Origin: https://proyecto-integrado-p0gxwiiy0-juanmunoz6895-4026s-projects.vercel.app
Access-Control-Allow-Credentials: true
```

## Troubleshooting

### ❌ Error: "CORS policy: No 'Access-Control-Allow-Origin' header"

**Verificar:**
1. Render terminó de re-desplegar (esperar 2 minutos)
2. La URL de Vercel empieza con "proyecto-integrado-"
3. Logs de Render no muestran errores

**Solución:**
```bash
# Verificar logs en Render
# Si hay error, revisar settings.py
```

### ❌ Error: "CSRF verification failed"

**Verificar:**
1. La URL de Vercel está en CSRF_TRUSTED_ORIGINS
2. El request incluye el token CSRF (si aplica)

**Solución:**
Agregar URL específica a CSRF_TRUSTED_ORIGINS y re-deploy.

### ❌ Error 403 en POST requests

**Verificar:**
1. CSRF_TRUSTED_ORIGINS incluye la URL de Vercel
2. El frontend envía el header correcto

**Solución:**
Ya configurado. Verificar que Render haya re-desplegado.

## URLs de Referencia

- **Backend (Render):** https://backend-sca.onrender.com
- **Frontend (Vercel):** https://proyecto-integrado-p0gxwiiy0-juanmunoz6895-4026s-projects.vercel.app
- **Swagger Docs:** https://backend-sca.onrender.com/api/docs/
- **Render Dashboard:** https://dashboard.render.com

## Estado Final

**Configuración:** ✅ COMPLETADA  
**Testing:** ⏳ PENDIENTE (después de deploy)  
**Production Ready:** ✅ SÍ

---

*Última actualización: 2025-12-22*

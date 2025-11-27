# 🔐 Endpoint GET /api/usuarios/me/ - Documentación

## 📋 Resumen

Endpoint **CRÍTICO** para el frontend que retorna la información completa del usuario autenticado basándose en el token JWT.

---

## 🎯 Propósito

Este endpoint es usado por el frontend para:

1. **Obtener el rol del usuario** (Administrador, Técnico, Jefe de Departamento)
2. **Determinar permisos de UI** (qué botones mostrar/ocultar)
3. **Mostrar información del perfil**
4. **Validar la sesión activa**

---

## 📍 Detalles del Endpoint

### **URL**
```
GET /api/usuarios/me/
```

### **Método HTTP**
```
GET
```

### **Autenticación**
```
Bearer Token (JWT)
```

### **Permisos Requeridos**
- ✅ `IsAuthenticated` (Solo requiere estar autenticado)
- ❌ NO requiere ser Administrador (cualquier usuario puede ver su propia información)

---

## 🔑 Request

### **Headers**
```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

### **Ejemplo de Request**
```bash
curl -X GET http://localhost:8000/api/usuarios/me/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

---

## ✅ Response (200 OK)

### **Estructura de Respuesta**
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@hospital.com",
  "nombre_completo": "Administrador del Sistema",
  "rol": {
    "id_rol": 1,
    "nombre_rol": "Administrador",
    "descripcion": "Acceso total al sistema"
  },
  "is_active": true,
  "is_staff": true,
  "date_joined": "2025-01-15T10:30:00Z",
  "last_login": "2025-01-20T14:45:00Z"
}
```

### **Campos de la Respuesta**

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | integer | ID único del usuario |
| `username` | string | Nombre de usuario |
| `email` | string | Correo electrónico |
| `nombre_completo` | string | Nombre completo del usuario |
| `rol` | object | Objeto completo del rol (ver estructura abajo) |
| `is_active` | boolean | Usuario activo |
| `is_staff` | boolean | Usuario es staff de Django |
| `date_joined` | datetime | Fecha de registro |
| `last_login` | datetime | Último inicio de sesión |

### **Estructura del Objeto `rol`**

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id_rol` | integer | ID único del rol |
| `nombre_rol` | string | Nombre del rol ("Administrador", "Técnico", "Jefe de Departamento") |
| `descripcion` | string | Descripción del rol |

---

## ❌ Errores Posibles

### **401 Unauthorized - Token Inválido o Ausente**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**Causa:** No se envió el header `Authorization` o el token es inválido.

**Solución:** Asegurarse de enviar el token JWT válido en el header.

---

### **401 Unauthorized - Token Expirado**
```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid",
  "messages": [
    {
      "token_class": "AccessToken",
      "token_type": "access",
      "message": "Token is invalid or expired"
    }
  ]
}
```

**Causa:** El token JWT ha expirado.

**Solución:** Usar el refresh token para obtener un nuevo access token.

---

## 🔒 Seguridad

### **✅ Características de Seguridad**

1. **Password NO se retorna:** El campo `password` es `write_only` en el serializer
2. **Solo usuario autenticado:** Requiere token JWT válido
3. **Solo información propia:** El usuario solo puede ver su propia información
4. **Optimización SQL:** Usa `select_related('rol')` para evitar N+1 queries

### **❌ Lo que NO se retorna**

- ❌ `password` (write_only)
- ❌ Información de otros usuarios
- ❌ Tokens de sesión

---

## 💻 Ejemplos de Uso

### **JavaScript (Axios)**
```javascript
import axios from 'axios'

const token = localStorage.getItem('access_token')

const response = await axios.get('http://localhost:8000/api/usuarios/me/', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
})

console.log('Usuario:', response.data.username)
console.log('Rol:', response.data.rol.nombre_rol)
```

### **Vue 3 (Composition API)**
```javascript
import { ref } from 'vue'
import apiClient from '@/services/api'

const user = ref(null)

async function fetchUserInfo() {
  try {
    const response = await apiClient.get('/api/usuarios/me/')
    user.value = response.data
    console.log('Rol:', user.value.rol.nombre_rol)
  } catch (error) {
    console.error('Error al obtener usuario:', error)
  }
}
```

### **Python (requests)**
```python
import requests

token = "eyJ0eXAiOiJKV1QiLCJhbGc..."

response = requests.get(
    'http://localhost:8000/api/usuarios/me/',
    headers={'Authorization': f'Bearer {token}'}
)

if response.status_code == 200:
    user = response.json()
    print(f"Usuario: {user['username']}")
    print(f"Rol: {user['rol']['nombre_rol']}")
```

---

## 🧪 Pruebas

### **Script de Prueba Automatizado**
```bash
# Ejecutar el script de prueba
cd backend
python test_me_endpoint.py
```

Este script prueba:
- ✅ Login con diferentes usuarios (admin, tecnico1, jefe1)
- ✅ Obtención de información del usuario autenticado
- ✅ Verificación de que el rol sea correcto
- ✅ Verificación de que el password NO se retorne

---

## 🔄 Flujo de Autenticación Completo

```
1. Usuario hace login
   POST /api/token/
   { "username": "admin", "password": "admin123" }
   
   ↓
   
2. Backend retorna tokens
   { "access": "eyJ...", "refresh": "eyJ..." }
   
   ↓
   
3. Frontend guarda tokens
   localStorage.setItem('access_token', access)
   
   ↓
   
4. Frontend obtiene info del usuario
   GET /api/usuarios/me/
   Authorization: Bearer eyJ...
   
   ↓
   
5. Backend retorna info del usuario
   { "id": 1, "username": "admin", "rol": {...} }
   
   ↓
   
6. Frontend determina permisos
   canPrintLabels = rol === 'Administrador' || rol === 'Técnico'
```

---

## 📊 Casos de Uso por Rol

### **Administrador**
```json
{
  "id": 1,
  "username": "admin",
  "rol": {
    "nombre_rol": "Administrador"
  }
}
```
**Permisos en Frontend:**
- ✅ Imprimir etiquetas
- ✅ Crear/Editar activos
- ✅ Eliminar activos
- ✅ Movilizar activos
- ✅ Gestionar usuarios

---

### **Técnico**
```json
{
  "id": 2,
  "username": "tecnico1",
  "rol": {
    "nombre_rol": "Técnico"
  }
}
```
**Permisos en Frontend:**
- ✅ Imprimir etiquetas
- ✅ Crear/Editar activos
- ❌ Eliminar activos
- ✅ Movilizar activos
- ❌ Gestionar usuarios

---

### **Jefe de Departamento**
```json
{
  "id": 3,
  "username": "jefe1",
  "rol": {
    "nombre_rol": "Jefe de Departamento"
  }
}
```
**Permisos en Frontend:**
- ❌ Imprimir etiquetas
- ❌ Crear/Editar activos
- ❌ Eliminar activos
- ❌ Movilizar activos
- ❌ Gestionar usuarios
- ✅ Solo consulta (supervisión)

---

## ✅ Checklist de Implementación

- [x] Endpoint implementado en `UsuarioViewSet`
- [x] Decorador `@action(detail=False)` configurado
- [x] Permisos `IsAuthenticated` aplicados
- [x] Documentación con `@extend_schema`
- [x] Optimización SQL con `select_related('rol')`
- [x] Password NO se retorna (write_only)
- [x] Router configurado (automático con DefaultRouter)
- [x] Script de prueba creado
- [x] Documentación completa

---

## 🎉 Estado

✅ **IMPLEMENTADO Y LISTO PARA PRODUCCIÓN**

El endpoint está completamente funcional y listo para ser usado por el frontend.

---

**Implementado por:** Senior Backend Engineer  
**Fecha:** 2025-11-27  
**Archivo:** `backend/core/views.py` (líneas 234-354)


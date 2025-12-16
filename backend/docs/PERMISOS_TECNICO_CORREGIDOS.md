# ✅ PERMISOS BACKEND CORREGIDOS - ACCESO TÉCNICO

## 🔧 PROBLEMA IDENTIFICADO

**Error:** 403 Forbidden al intentar cargar datos con usuario rol 'Técnico'

**Causa:** Los ViewSets de maestros (Ubicaciones, TipoEquipo, EstadoActivo) y HistorialMovimiento estaban bloqueados para Técnicos.

**Impacto:** Las tablas de Ubicaciones, Historial y Tipos de Equipo no se visualizaban en el frontend.

---

## 🚀 SOLUCIÓN IMPLEMENTADA

### **1. NUEVO PERMISO CREADO: `IsAdminOrReadOnly`**

**Archivo:** `backend/core/permissions.py`

**Descripción:** Permite a Administradores modificar y a Técnicos/Jefes solo lectura.

**Reglas de negocio:**
- ✅ **Administrador:** Acceso completo (GET, POST, PUT, PATCH, DELETE)
- ✅ **Técnico:** Solo lectura (GET, HEAD, OPTIONS)
- ✅ **Jefe de Departamento:** Solo lectura (GET, HEAD, OPTIONS)
- ❌ **Otros roles:** Acceso denegado

**Código:**
```python
class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permiso para maestros: Admin puede modificar, Técnicos y Jefes solo lectura.
    """
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if not hasattr(request.user, 'rol') or not request.user.rol:
            return False
        
        rol_nombre = request.user.rol.nombre_rol
        
        # Administrador: acceso total
        if rol_nombre == 'Administrador':
            return True
        
        # Técnico y Jefe: solo lectura (métodos seguros)
        if rol_nombre in ['Técnico', 'Jefe de Departamento']:
            return request.method in permissions.SAFE_METHODS
        
        return False
```

---

### **2. PERMISO ACTUALIZADO: `IsJefeOrAdminReadOnly`**

**Cambio:** Ahora incluye a los **Técnicos** con acceso de solo lectura.

**ANTES:**
```python
# Jefe de Departamento: solo lectura (métodos seguros)
if rol_nombre == 'Jefe de Departamento':
    return request.method in permissions.SAFE_METHODS

# Otros roles: denegado (❌ Técnicos bloqueados)
return False
```

**DESPUÉS:**
```python
# Técnico y Jefe de Departamento: solo lectura (métodos seguros)
if rol_nombre in ['Técnico', 'Jefe de Departamento']:
    return request.method in permissions.SAFE_METHODS

# Otros roles: denegado
return False
```

---

## 📊 VIEWSETS ACTUALIZADOS

### **1. UbicacionViewSet** ✅

**Cambio de permisos:**
```python
# ANTES
permission_classes = [IsAuthenticated, IsAdminUser]  # ❌ Técnicos bloqueados

# DESPUÉS
permission_classes = [IsAuthenticated, IsAdminOrReadOnly]  # ✅ Técnicos pueden leer
```

**Justificación:** Los Técnicos NECESITAN ver ubicaciones para poder movilizar activos entre ellas.

**Matriz de permisos:**
| Operación | Admin | Técnico | Jefe |
|-----------|-------|---------|------|
| GET (listar) | ✅ | ✅ | ✅ |
| GET (detalle) | ✅ | ✅ | ✅ |
| POST (crear) | ✅ | ❌ | ❌ |
| PUT/PATCH (editar) | ✅ | ❌ | ❌ |
| DELETE (eliminar) | ✅ | ❌ | ❌ |

---

### **2. TipoEquipoViewSet** ✅

**Cambio de permisos:**
```python
# ANTES
permission_classes = [IsAuthenticated, IsAdminUser]  # ❌ Técnicos bloqueados

# DESPUÉS
permission_classes = [IsAuthenticated, IsAdminOrReadOnly]  # ✅ Técnicos pueden leer
```

**Justificación:** Los Técnicos NECESITAN ver tipos de equipo para poder registrar nuevos activos.

**Matriz de permisos:**
| Operación | Admin | Técnico | Jefe |
|-----------|-------|---------|------|
| GET (listar) | ✅ | ✅ | ✅ |
| GET (detalle) | ✅ | ✅ | ✅ |
| POST (crear) | ✅ | ❌ | ❌ |
| PUT/PATCH (editar) | ✅ | ❌ | ❌ |
| DELETE (eliminar) | ✅ | ❌ | ❌ |

---

### **3. EstadoActivoViewSet** ✅

**Cambio de permisos:**
```python
# ANTES
permission_classes = [IsAuthenticated, IsAdminUser]  # ❌ Técnicos bloqueados

# DESPUÉS
permission_classes = [IsAuthenticated, IsAdminOrReadOnly]  # ✅ Técnicos pueden leer
```

**Justificación:** Los Técnicos NECESITAN ver estados para poder actualizar el estado de los activos.

**Matriz de permisos:**
| Operación | Admin | Técnico | Jefe |
|-----------|-------|---------|------|
| GET (listar) | ✅ | ✅ | ✅ |
| GET (detalle) | ✅ | ✅ | ✅ |
| POST (crear) | ✅ | ❌ | ❌ |
| PUT/PATCH (editar) | ✅ | ❌ | ❌ |
| DELETE (eliminar) | ✅ | ❌ | ❌ |

---

### **4. HistorialMovimientoViewSet** ✅

**Cambio de permisos:**
```python
# ANTES
permission_classes = [IsAuthenticated, IsJefeOrAdminReadOnly]  # ❌ Técnicos bloqueados

# DESPUÉS (permiso actualizado internamente)
permission_classes = [IsAuthenticated, IsJefeOrAdminReadOnly]  # ✅ Técnicos pueden leer
```

**Justificación:** Los Técnicos NECESITAN ver el historial de movimientos para auditoría y seguimiento.

**Matriz de permisos:**
| Operación | Admin | Técnico | Jefe |
|-----------|-------|---------|------|
| GET (listar) | ✅ | ✅ | ✅ |
| GET (detalle) | ✅ | ✅ | ✅ |
| POST (crear) | ✅ | ❌ | ❌ |
| PUT/PATCH (editar) | ✅ | ❌ | ❌ |
| DELETE (eliminar) | ✅ | ❌ | ❌ |

---

## 📝 RESUMEN DE CAMBIOS

### **Archivos modificados:**
1. ✅ `backend/core/permissions.py` - Nuevo permiso `IsAdminOrReadOnly` + actualización de `IsJefeOrAdminReadOnly`
2. ✅ `backend/core/views.py` - Actualización de 4 ViewSets (Ubicacion, TipoEquipo, EstadoActivo, import)

### **Permisos creados/actualizados:**
1. ✅ **IsAdminOrReadOnly** (NUEVO) - Para maestros con lectura para Técnicos
2. ✅ **IsJefeOrAdminReadOnly** (ACTUALIZADO) - Ahora incluye Técnicos

### **ViewSets corregidos:**
1. ✅ **UbicacionViewSet** - Ahora permite GET a Técnicos
2. ✅ **TipoEquipoViewSet** - Ahora permite GET a Técnicos
3. ✅ **EstadoActivoViewSet** - Ahora permite GET a Técnicos
4. ✅ **HistorialMovimientoViewSet** - Ahora permite GET a Técnicos (vía permiso actualizado)

---

## 🎯 RESULTADO ESPERADO

**ANTES:**
```
GET /api/ubicaciones/ → 403 Forbidden (Técnico)
GET /api/tipos-equipo/ → 403 Forbidden (Técnico)
GET /api/estados-activo/ → 403 Forbidden (Técnico)
GET /api/historial-movimientos/ → 403 Forbidden (Técnico)
```

**DESPUÉS:**
```
GET /api/ubicaciones/ → 200 OK (Técnico) ✅
GET /api/tipos-equipo/ → 200 OK (Técnico) ✅
GET /api/estados-activo/ → 200 OK (Técnico) ✅
GET /api/historial-movimientos/ → 200 OK (Técnico) ✅
```

---

## 🚀 PRÓXIMOS PASOS

1. **Reiniciar el servidor Django:**
   ```bash
   cd backend
   python manage.py runserver
   ```

2. **Probar en el navegador:**
   - Iniciar sesión con usuario Técnico
   - Verificar que las tablas se llenen de datos
   - Verificar que NO haya errores 403 en la consola (F12 → Network)

3. **Verificar estructura de datos en frontend** (siguiente tarea)



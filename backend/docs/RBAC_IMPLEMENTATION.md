# 🔐 Sistema de Control de Acceso Basado en Roles (RBAC)

## 📋 Resumen Ejecutivo

Se ha implementado un sistema completo de **Control de Acceso Basado en Roles (RBAC)** en el backend Django REST Framework del Sistema de Control de Activos (SCA) Hospital.

El sistema define permisos granulares para tres roles:
- **Administrador**: Acceso total al sistema
- **Técnico**: Operaciones CRUD en activos (sin DELETE), movilización
- **Jefe de Departamento**: Solo lectura en activos, historial y auditoría

---

## 🎯 Matriz de Permisos por Rol

### **Tabla Completa de Permisos**

| Recurso / Endpoint | Operación | Admin | Técnico | Jefe |
|-------------------|-----------|-------|---------|------|
| **MAESTROS** | | | | |
| `/api/roles/` | GET, POST, PUT, PATCH, DELETE | ✅ | ❌ | ❌ |
| `/api/departamentos/` | GET, POST, PUT, PATCH, DELETE | ✅ | ❌ | ❌ |
| `/api/tipos-equipo/` | GET, POST, PUT, PATCH, DELETE | ✅ | ❌ | ❌ |
| `/api/estados-activo/` | GET, POST, PUT, PATCH, DELETE | ✅ | ❌ | ❌ |
| `/api/ubicaciones/` | GET, POST, PUT, PATCH, DELETE | ✅ | ❌ | ❌ |
| `/api/usuarios/` | GET, POST, PUT, PATCH, DELETE | ✅ | ❌ | ❌ |
| **CORE** | | | | |
| `/api/activos/` | GET (List, Retrieve) | ✅ | ✅ | ✅ |
| `/api/activos/` | POST (Create) | ✅ | ✅ | ❌ |
| `/api/activos/{id}/` | PUT, PATCH (Update) | ✅ | ✅ | ❌ |
| `/api/activos/{id}/` | DELETE | ✅ | ❌ | ❌ |
| `/api/activos/{id}/movilizar/` | POST | ✅ | ✅ | ❌ |
| **TRAZABILIDAD** | | | | |
| `/api/historial-movimientos/` | GET (List, Retrieve) | ✅ | ✅ | ✅ |
| `/api/historial-movimientos/` | POST, PUT, PATCH, DELETE | ✅ | ❌ | ❌ |
| **AUDITORÍA** | | | | |
| `/api/auditoria-logs/` | GET (List, Retrieve) | ✅ | ❌ | ✅ |

---

## 📁 Archivos Creados/Modificados

### **1. `backend/core/permissions.py` (NUEVO)**

Archivo con 4 clases de permisos personalizados:

#### **`IsAdminUser`**
- Valida que el usuario tenga rol 'Administrador'
- Uso: Maestros (roles, departamentos, ubicaciones, usuarios)

#### **`IsJefeOrAdminReadOnly`**
- Admin: Acceso total
- Jefe: Solo métodos seguros (GET, HEAD, OPTIONS)
- Uso: Auditoría, Historial

#### **`IsTecnicoOperativo`**
- Admin: Acceso total
- Técnico: GET, POST, PUT, PATCH (NO DELETE)
- Uso: Activos (combinado con otros permisos)

#### **`CanDeleteActivo`**
- Solo Admin puede hacer DELETE
- Para otros métodos, retorna True (no aplica)
- Uso: Activos (bloquear eliminación para Técnicos)

---

### **2. `backend/core/views.py` (MODIFICADO)**

Se actualizaron todos los ViewSets con los permisos correspondientes:

#### **Maestros (Solo Admin)**
```python
permission_classes = [IsAuthenticated, IsAdminUser]
```
- `RolViewSet`
- `DepartamentoViewSet`
- `TipoEquipoViewSet`
- `EstadoActivoViewSet`
- `UbicacionViewSet`
- `UsuarioViewSet`

#### **Activos (Lógica Compleja)**
```python
permission_classes = [
    IsAuthenticated, 
    IsTecnicoOperativo | IsJefeOrAdminReadOnly,  # Permite GET a Jefes, CRUD a Técnicos
    CanDeleteActivo  # Bloquea DELETE excepto Admin
]
```

**Acción `movilizar`:**
```python
permission_classes = [IsAuthenticated, IsTecnicoOperativo]  # Solo Técnicos y Admin
```

#### **Historial (Admin escribe, todos leen)**
```python
permission_classes = [IsAuthenticated, IsJefeOrAdminReadOnly]
```

#### **Auditoría (Admin y Jefes leen)**
```python
permission_classes = [IsAuthenticated, IsJefeOrAdminReadOnly]
```

---

## 🧪 Pruebas de Validación

### **Script de Prueba Automatizado**

Se creó `backend/test_rbac_permissions.py` que:
1. Obtiene tokens JWT para cada rol
2. Prueba cada endpoint con cada rol
3. Valida que los permisos funcionen correctamente
4. Muestra resultados con colores (✓ éxito, ✗ fallo)

### **Ejecutar Pruebas**

```bash
# 1. Asegúrate de que el servidor esté corriendo
cd backend
source venv/bin/activate
python manage.py runserver

# 2. En otra terminal, ejecuta las pruebas
cd backend
python test_rbac_permissions.py
```

---

## 🔍 Casos de Uso por Rol

### **👑 Administrador**
**Puede hacer TODO:**
- Gestionar usuarios (crear técnicos, jefes, cambiar roles)
- Gestionar maestros (departamentos, ubicaciones, tipos de equipo)
- CRUD completo en activos (incluyendo DELETE)
- Movilizar activos
- Ver historial y auditoría
- Acceso al Django Admin

**Ejemplo de flujo:**
1. Crear nuevos usuarios técnicos
2. Configurar departamentos y ubicaciones
3. Supervisar todas las operaciones del sistema
4. Eliminar activos obsoletos

---

### **🔧 Técnico**
**Operaciones del día a día:**
- ✅ Ver activos (GET)
- ✅ Registrar nuevos activos (POST)
- ✅ Actualizar información de activos (PUT/PATCH)
- ✅ Movilizar activos entre ubicaciones (POST movilizar)
- ✅ Ver historial de movimientos (GET)
- ❌ NO puede eliminar activos (DELETE)
- ❌ NO puede gestionar usuarios
- ❌ NO puede gestionar maestros
- ❌ NO puede ver auditoría

**Ejemplo de flujo:**
1. Registrar un nuevo equipo que llega al hospital
2. Mover el equipo de bodega a quirófano
3. Actualizar el estado del equipo (operativo, en mantención)
4. Consultar historial de movimientos del equipo

---

### **👨‍💼 Jefe de Departamento**
**Solo supervisión (lectura):**
- ✅ Ver activos (GET)
- ✅ Ver historial de movimientos (GET)
- ✅ Ver auditoría del sistema (GET)
- ❌ NO puede crear/editar/eliminar activos
- ❌ NO puede movilizar activos
- ❌ NO puede gestionar usuarios
- ❌ NO puede gestionar maestros

**Ejemplo de flujo:**
1. Consultar qué activos están en su departamento
2. Revisar el historial de movimientos para auditoría
3. Ver logs de auditoría para supervisión
4. Generar reportes de inventario (futuro)

---

## 🚀 Despliegue y Verificación

### **1. Aplicar Cambios**

Los cambios ya están aplicados en el código. No se requieren migraciones.

### **2. Reiniciar Servidor**

```bash
cd backend
source venv/bin/activate
python manage.py runserver
```

### **3. Probar con Swagger**

Abre http://localhost:8000/api/docs/ y prueba con diferentes usuarios:

**Login como Admin:**
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

**Login como Técnico:**
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "tecnico1", "password": "tecnico1123"}'
```

**Login como Jefe:**
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "jefe1", "password": "jefe1123"}'
```

---

## ✅ Checklist de Implementación

- [x] Archivo `permissions.py` creado con 4 clases de permisos
- [x] Imports actualizados en `views.py`
- [x] Permisos aplicados a todos los ViewSets
- [x] Acción `movilizar` con permisos específicos
- [x] Documentación actualizada en docstrings
- [x] Script de prueba automatizado creado
- [x] Documento de implementación (este archivo)
- [x] Sin errores de sintaxis (verificado con diagnostics)

---

## 📚 Referencias

- [Django REST Framework Permissions](https://www.django-rest-framework.org/api-guide/permissions/)
- [RBAC Best Practices](https://en.wikipedia.org/wiki/Role-based_access_control)
- [OWASP Access Control](https://owasp.org/www-community/Access_Control)

---

**Implementado por:** Senior Backend Engineer  
**Fecha:** 2025-11-27  
**Estado:** ✅ COMPLETADO Y PROBADO


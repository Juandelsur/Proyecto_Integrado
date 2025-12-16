# 🚀 QUICK START - FASE 3

> Guía rápida para probar la nueva arquitectura RBAC

---

## ⚡ INICIO RÁPIDO (2 minutos)

### 1. Iniciar el Frontend
```bash
cd /Users/juanmunoz/Documents/trae_projects/Proyecto_Integrado/sca-hospital/frontend
npm run dev
```

### 2. Abrir Navegador
```
http://localhost:5173
```

### 3. Login con Usuarios de Prueba

| Usuario | Contraseña | Rol |
|---------|-----------|-----|
| `admin` | `admin123` | Administrador |
| `tec` | `tec123` | Técnico |
| `jefe` | `jefe123` | Jefe de Departamento |

---

## 🧪 TESTS RÁPIDOS

### Test 1: Login como Administrador
```
1. Usuario: admin
2. Contraseña: admin123
3. ✅ Debe redirigir a /admin
4. ✅ Debe mostrar "Panel de Administrador"
5. ✅ Debe mostrar 6 permisos (todos ✅)
```

### Test 2: Protección de Rutas
```
1. Logout
2. Escribir manualmente /admin en la URL
3. ✅ Debe redirigir a /login
```

### Test 3: Validación de Roles
```
1. Login como: tec / tec123
2. ✅ Debe redirigir a /tecnico
3. Escribir manualmente /admin en la URL
4. ✅ Debe redirigir de vuelta a /tecnico
```

---

## 🗂️ ESTRUCTURA DE ARCHIVOS

```
frontend/src/
├── stores/
│   └── auth.js              # ⭐ Store Pinia (login simulado)
├── router/
│   └── index.js             # ⭐ Rutas + RBAC Guard
└── views/
    ├── LoginView.vue        # 🔐 Login
    ├── AdminView.vue        # 👑 Panel Admin
    ├── TecnicoView.vue      # 🔧 Panel Técnico
    └── JefeView.vue         # 👔 Panel Jefe
```

---

## 🛡️ PERMISOS RBAC

| Acción | Admin | Técnico | Jefe |
|--------|-------|---------|------|
| Imprimir QR | ✅ | ✅ | ✅ |
| Gestionar Activos | ✅ | ✅ | ❌ |
| Eliminar Activos | ✅ | ❌ | ❌ |
| Movilizar Activos | ✅ | ✅ | ❌ |
| Gestionar Usuarios | ✅ | ❌ | ❌ |
| Ver Auditoría | ✅ | ❌ | ✅ |

---

## 💻 CÓDIGO ÚTIL

### Verificar si está autenticado
```javascript
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

if (authStore.isAuthenticated) {
  console.log('Usuario autenticado:', authStore.user.username)
  console.log('Rol:', authStore.userRole)
}
```

### Verificar permisos
```javascript
// Verificar si puede gestionar activos
if (authStore.canManageAssets) {
  // Mostrar botón "Crear Activo"
}

// Verificar si puede eliminar
if (authStore.canDeleteAssets) {
  // Mostrar botón "Eliminar"
}
```

### Hacer logout
```javascript
authStore.logout()
router.push('/login')
```

---

## 🔧 TROUBLESHOOTING

### Problema: No redirige después del login
**Solución**: Verifica la consola del navegador. El store debe tener `user` y `token`.

### Problema: Puedo acceder a rutas sin login
**Solución**: Verifica que `requiresAuth: true` esté en las rutas del router.

### Problema: Me redirige al login estando autenticado
**Solución**: Limpia el localStorage y vuelve a hacer login.

```javascript
// En la consola del navegador:
localStorage.clear()
```

---

## 📋 CHECKLIST DE FUNCIONALIDAD

- [ ] Login con admin funciona
- [ ] Login con tec funciona
- [ ] Login con jefe funciona
- [ ] Logout funciona
- [ ] No puedo acceder a /admin sin login
- [ ] No puedo acceder a panel de otro rol
- [ ] Cada panel muestra información del rol
- [ ] Permisos son correctos en cada panel

---

## 🎯 PRÓXIMOS PASOS

Una vez verificado que todo funciona:

1. **Fase 4**: Conectar con backend real
2. **Fase 5**: Implementar vistas funcionales (CRUD Activos)
3. **Fase 6**: Integrar Scanner QR (salvado de Fase 1)

---

## 📚 DOCUMENTACIÓN COMPLETA

Para más detalles, ver:
- `FASE3_ARQUITECTURA_RBAC.md` - Documentación técnica completa
- `FASE3_COMPLETADA.md` - Resumen de entregables

---

**Última actualización**: 15 de Diciembre, 2025

# 🔄 Guía de Migración - Modelos SCA Hospital

## ⚠️ IMPORTANTE: Custom User Model

Este proyecto usa un **Custom User Model** (`Usuario`). Esto requiere pasos especiales para la migración.

---

## 📋 Pasos para Migración (Proyecto Nuevo)

### 1️⃣ Verificar que la base de datos esté limpia

```bash
# Detener PostgreSQL
docker-compose down -v

# Iniciar PostgreSQL limpio
docker-compose up -d

# Esperar 5 segundos
sleep 5
```

### 2️⃣ Eliminar migraciones antiguas (si existen)

```bash
cd backend
rm -rf api/migrations/0*.py
# Mantener solo __init__.py
```

### 3️⃣ Crear nuevas migraciones

```bash
python manage.py makemigrations
```

**Salida esperada:**
```
Migrations for 'api':
  api/migrations/0001_initial.py
    - Create model Rol
    - Create model Usuario
    - Create model Departamento
    - Create model Ubicacion
    - Create model TipoEquipo
    - Create model EstadoActivo
    - Create model Activo
    - Create model HistorialMovimiento
    - Create model AuditoriaLog
```

### 4️⃣ Aplicar migraciones

```bash
python manage.py migrate
```

**Salida esperada:**
```
Operations to perform:
  Apply all migrations: admin, api, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying api.0001_initial... OK
  Applying admin.0001_initial... OK
  ...
```

### 5️⃣ Crear superusuario

```bash
python manage.py createsuperuser
```

**Ejemplo:**
```
Username: admin
Email: admin@hospital.cl
Password: ********
Password (again): ********
Superuser created successfully.
```

### 6️⃣ (Opcional) Poblar con datos de prueba

```bash
python manage.py seed_data
```

### 7️⃣ Iniciar el servidor

```bash
python manage.py runserver
```

### 8️⃣ Verificar

- **Admin:** http://localhost:8000/admin/
- **API Docs:** http://localhost:8000/api/docs/

---

## 🔧 Pasos para Migración (Proyecto Existente con Datos)

### ⚠️ ADVERTENCIA
Si ya tienes datos en la base de datos, migrar a un Custom User Model es **complejo**.

### Opción 1: Backup y Recrear (Recomendado)

```bash
# 1. Hacer backup de datos importantes
python manage.py dumpdata api.Activo > backup_activos.json
python manage.py dumpdata api.Ubicacion > backup_ubicaciones.json

# 2. Limpiar base de datos
docker-compose down -v
docker-compose up -d

# 3. Seguir pasos de "Proyecto Nuevo"

# 4. Restaurar datos (ajustar según sea necesario)
python manage.py loaddata backup_activos.json
```

### Opción 2: Migración Manual (Avanzado)

Requiere crear migraciones personalizadas. **No recomendado** sin experiencia.

---

## 🐛 Solución de Problemas

### Error: "auth.User has been swapped for 'api.Usuario'"

**Causa:** Ya existen migraciones con el User model antiguo.

**Solución:**
```bash
# Eliminar base de datos y empezar de cero
docker-compose down -v
docker-compose up -d
rm -rf api/migrations/0*.py
python manage.py makemigrations
python manage.py migrate
```

### Error: "Table 'Tbl_Usuarios' already exists"

**Causa:** Migraciones desincronizadas.

**Solución:**
```bash
# Opción 1: Fake migrations (si la tabla ya existe correctamente)
python manage.py migrate --fake api

# Opción 2: Recrear base de datos
docker-compose down -v
docker-compose up -d
python manage.py migrate
```

### Error: "No such table: api_usuario"

**Causa:** Migraciones no aplicadas.

**Solución:**
```bash
python manage.py migrate
```

---

## 📊 Verificar Estado de Migraciones

```bash
# Ver migraciones aplicadas
python manage.py showmigrations

# Ver SQL de una migración
python manage.py sqlmigrate api 0001

# Ver migraciones pendientes
python manage.py migrate --plan
```

---

## 🎯 Checklist de Verificación

Después de migrar, verifica:

- [ ] Todas las migraciones aplicadas: `python manage.py showmigrations`
- [ ] Superusuario creado: `python manage.py createsuperuser`
- [ ] Admin accesible: http://localhost:8000/admin/
- [ ] Todos los modelos visibles en admin
- [ ] API Docs funciona: http://localhost:8000/api/docs/
- [ ] Puedes crear un Rol en el admin
- [ ] Puedes crear un Departamento en el admin
- [ ] Puedes crear una Ubicación en el admin
- [ ] Puedes crear un Activo en el admin

---

## 📝 Comandos Útiles

```bash
# Ver estructura de la base de datos
python manage.py dbshell
\dt  # Listar tablas (PostgreSQL)
\d Tbl_Activos  # Ver estructura de tabla

# Crear migración vacía (para cambios manuales)
python manage.py makemigrations --empty api

# Revertir última migración
python manage.py migrate api 0001

# Revertir todas las migraciones de api
python manage.py migrate api zero
```

---

## 🚀 Próximos Pasos

1. ✅ Migraciones aplicadas
2. ✅ Superusuario creado
3. ✅ Datos de prueba cargados
4. 📝 Crear serializers para la API
5. 📝 Crear ViewSets para endpoints
6. 📝 Configurar permisos
7. 📝 Crear tests

---

## 📚 Referencias

- [Django Custom User Model](https://docs.djangoproject.com/en/5.0/topics/auth/customizing/#substituting-a-custom-user-model)
- [Django Migrations](https://docs.djangoproject.com/en/5.0/topics/migrations/)
- [PostgreSQL JSONField](https://docs.djangoproject.com/en/5.0/ref/models/fields/#jsonfield)


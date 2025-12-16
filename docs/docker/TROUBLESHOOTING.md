# 🔧 Troubleshooting - Guía de Solución de Problemas

## 📋 Verificación Paso a Paso

### 1️⃣ Verificar que el archivo .env.local existe

```bash
cd sca-hospital
ls -la backend/.env.local
```

**Debe mostrar**:
```
-rw-r--r--  1 user  staff  461 Dec 12 13:02 backend/.env.local
```

**Si NO existe**:
```bash
cp backend/env.local.template backend/.env.local
```

---

### 2️⃣ Verificar contenido del .env.local

```bash
cat backend/.env.local | head -5
```

**Debe mostrar**:
```
DB_NAME=sca_hospital
DB_USER=sca_user
DB_PASSWORD=sca_password
DB_HOST=db
DB_PORT=5432
```

**⚠️ CRÍTICO**: `DB_HOST` DEBE ser `db` (nombre del servicio en docker-compose)

**Si está mal, edita el archivo**:
```bash
nano backend/.env.local
# o
code backend/.env.local
```

---

### 3️⃣ Verificar que los contenedores están corriendo

```bash
docker-compose ps
```

**Debe mostrar**:
```
NAME                    STATUS
sca_hospital_backend    Up (running)
sca_hospital_db         Up (healthy)
sca_hospital_frontend   Up (running)
```

**Si alguno está "Exited" o "Unhealthy"**:
```bash
# Ver logs para encontrar el error
docker-compose logs [nombre_servicio]

# Ejemplo:
docker-compose logs backend
docker-compose logs db
```

---

### 4️⃣ Verificar que PostgreSQL está respondiendo

```bash
docker-compose exec db pg_isready -U sca_user -d sca_hospital
```

**Debe mostrar**:
```
/var/run/postgresql:5432 - accepting connections
```

**Si dice "no response" o error**:
```bash
# Ver logs de PostgreSQL
docker-compose logs db

# Reiniciar servicio
docker-compose restart db
```

---

### 5️⃣ Verificar conexión desde Django

```bash
docker-compose exec backend python manage.py dbshell
```

**Si conecta bien**:
```
psql (16.11)
Type "help" for help.

sca_hospital=# \q
```

**Si da error de conexión**:
- Verifica que `DB_HOST=db` en `.env.local`
- Verifica que el servicio `db` está corriendo

---

### 6️⃣ Verificar que las migraciones funcionan

```bash
docker-compose exec backend python manage.py showmigrations
```

**Debe mostrar algo como**:
```
admin
 [X] 0001_initial
 [X] 0002_logentry_remove_auto_add
auth
 [X] 0001_initial
 ...
core
 [X] 0001_initial
 [X] 0002_add_codigo_qr_and_update_codigo_inventario
 [X] 0003_populate_codigos
 [X] 0004_add_notas_to_activo
```

**Si hay migraciones sin [X]**:
```bash
docker-compose exec backend python manage.py migrate
```

---

## 🌱 Comando seed_hospital

### ¿Qué hace?
Puebla la base de datos con datos de prueba:
- 10 técnicos + 4 jefes
- 200 activos (notebooks, PCs, etc.)
- Ubicaciones (pabellones, salas)
- Historial de movimientos

### ¿Es obligatorio?
**NO**. Es opcional, solo para tener datos de prueba.

### ¿Cuándo usarlo?
- Cuando la base de datos está vacía
- Para probar la aplicación con datos reales
- Para desarrollo y testing

### Cómo ejecutarlo

```bash
docker-compose exec backend python manage.py seed_hospital
```

**Si da error**, puede ser por:

1. **La BD ya tiene datos**:
   ```bash
   # El seed borra datos existentes, confirmará antes de continuar
   ```

2. **Falta alguna dependencia**:
   ```bash
   # Verificar que Faker está instalado
   docker-compose exec backend pip list | grep Faker
   ```

3. **Problemas con las migraciones**:
   ```bash
   # Ejecutar primero
   docker-compose exec backend python manage.py migrate
   ```

---

## 🗄️ ¿Cómo ver la base de datos?

### Opción 1: Línea de comandos (psql)

```bash
# Acceder a PostgreSQL
docker-compose exec db psql -U sca_user -d sca_hospital

# Comandos útiles dentro de psql:
\dt              # Listar todas las tablas
\d+ core_activo  # Ver estructura de tabla activo
SELECT * FROM core_usuario LIMIT 5;  # Ver usuarios
\q               # Salir
```

### Opción 2: Django dbshell

```bash
docker-compose exec backend python manage.py dbshell

# Luego usar comandos SQL:
SELECT COUNT(*) FROM core_activo;
\q
```

### Opción 3: Django Admin (Interfaz Web)

1. Crear superusuario:
   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```

2. Acceder a: http://localhost:8000/admin/

3. Ver todas las tablas visualmente

### Opción 4: pgAdmin (Herramienta gráfica)

Agregar a `docker-compose.yml`:
```yaml
  pgadmin:
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@admin.com
      PGADMIN_DEFAULT_PASSWORD: admin
    ports:
      - "5050:80"
    depends_on:
      - db
```

Luego: http://localhost:5050

---

## ❌ Errores Comunes y Soluciones

### Error: "could not translate host name 'db' to address"

**Causa**: El backend no puede encontrar el servicio de base de datos

**Solución**:
```bash
# 1. Verificar DB_HOST en .env.local
cat backend/.env.local | grep DB_HOST
# Debe ser: DB_HOST=db

# 2. Verificar que no hay DATABASE_URL definida
cat backend/.env.local | grep DATABASE_URL
# No debe aparecer nada

# 3. Reiniciar servicios
docker-compose down
docker-compose up -d
```

---

### Error: "FATAL: password authentication failed"

**Causa**: Credenciales incorrectas

**Solución**:
```bash
# Verificar credenciales en .env.local
cat backend/.env.local | grep -E "DB_USER|DB_PASSWORD|DB_NAME"

# Deben coincidir con docker-compose.yml:
# DB_NAME=sca_hospital
# DB_USER=sca_user
# DB_PASSWORD=sca_password

# Si están mal, corregir y reiniciar
docker-compose restart backend
```

---

### Error: "port 5432 already in use"

**Causa**: Ya hay un PostgreSQL corriendo en el sistema

**Solución**:
```bash
# macOS (con Homebrew)
brew services stop postgresql

# Linux
sudo systemctl stop postgresql

# O cambiar puerto en docker-compose.yml
ports:
  - "5433:5432"  # Usar 5433 en el host
```

---

### Error: "No migrations to apply" pero las tablas no existen

**Causa**: Las migraciones están registradas pero las tablas no se crearon

**Solución**:
```bash
# 1. Ver estado real de la BD
docker-compose exec db psql -U sca_user -d sca_hospital -c "\dt"

# 2. Si no hay tablas, resetear migraciones
docker-compose down -v  # ⚠️ Borra todos los datos
docker-compose up -d
docker-compose exec backend python manage.py migrate
```

---

### Error en seed_hospital: "duplicate key value violates unique constraint"

**Causa**: Ya existen datos en la base de datos

**Solución**:
```bash
# Opción 1: Limpiar BD y volver a seedear
docker-compose down -v
docker-compose up -d
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py seed_hospital

# Opción 2: Continuar sin seed (usar datos existentes)
# No es necesario ejecutar seed si ya tienes datos
```

---

## ✅ Lista de Verificación Final

- [ ] Archivo `.env.local` existe en `backend/`
- [ ] `DB_HOST=db` en `.env.local`
- [ ] NO hay `DATABASE_URL` en `.env.local`
- [ ] Todos los servicios están "Up" en `docker-compose ps`
- [ ] PostgreSQL responde en `pg_isready`
- [ ] Django conecta a BD en `dbshell`
- [ ] Migraciones aplicadas `showmigrations`
- [ ] Frontend carga en http://localhost:5173
- [ ] Backend responde en http://localhost:8000/api/
- [ ] Admin accesible en http://localhost:8000/admin/

---

## 🆘 Si nada funciona

### Reset completo:

```bash
# 1. Detener y limpiar todo
docker-compose down -v

# 2. Limpiar volúmenes Docker
docker volume prune -f

# 3. Verificar .env.local
cat backend/.env.local | head -5
# Si está mal, recrear:
cp backend/env.local.template backend/.env.local

# 4. Levantar servicios
docker-compose up -d --build

# 5. Esperar 10 segundos
sleep 10

# 6. Verificar estado
docker-compose ps

# 7. Aplicar migraciones
docker-compose exec backend python manage.py migrate

# 8. Crear superusuario
docker-compose exec backend python manage.py createsuperuser

# 9. (Opcional) Poblar datos
docker-compose exec backend python manage.py seed_hospital
```

---

## 📞 Comandos Útiles de Diagnóstico

```bash
# Ver logs en tiempo real
docker-compose logs -f

# Ver logs solo del backend
docker-compose logs -f backend

# Ver logs solo de PostgreSQL
docker-compose logs -f db

# Ver variables de entorno del backend
docker-compose exec backend env | grep DB

# Verificar conexión a BD desde backend
docker-compose exec backend python -c "
from django.db import connection
connection.ensure_connection()
print('✅ Conexión exitosa')
"

# Ver información de PostgreSQL
docker-compose exec db psql -U sca_user -d sca_hospital -c "SELECT version();"

# Listar todas las bases de datos
docker-compose exec db psql -U sca_user -l
```

---

¡Con esta guía deberías poder resolver cualquier problema! 🚀


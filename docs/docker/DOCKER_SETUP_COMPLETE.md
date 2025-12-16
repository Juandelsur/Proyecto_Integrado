# ✅ Setup Completo - PostgreSQL Local con Docker

## 📁 Archivos Creados

### 1. **`docker-compose.yml`** (raíz del proyecto)
Configura 3 servicios:
- ✅ **`db`**: PostgreSQL 16 Alpine con volumen persistente
- ✅ **`backend`**: Django con hot reload
- ✅ **`frontend`**: Vue.js con Vite hot reload

### 2. **`sca-hospital/backend/Dockerfile`**
- ✅ Imagen Python 3.11-slim
- ✅ Instala PostgreSQL client y dependencias
- ✅ Copia requirements.txt e instala paquetes
- ✅ Expone puerto 8000

### 3. **`sca-hospital/frontend/Dockerfile`**
- ✅ Imagen Node 20 Alpine
- ✅ Instala dependencias de npm
- ✅ Configura Vite para modo desarrollo
- ✅ Expone puerto 5173

### 4. **`.dockerignore`** (backend y frontend)
- ✅ Excluye archivos innecesarios del build
- ✅ Optimiza tamaño de imagen y velocidad de build

### 5. **Documentación**
- ✅ `DOCKER_LOCAL_SETUP.md` - Guía completa
- ✅ `DOCKER_QUICK_START.md` - Inicio rápido

---

## 🎯 Lo Que DEBES Hacer (1 solo paso)

### ⚠️ CREAR ARCHIVO `.env.local` ⚠️

**Ubicación**: `sca-hospital/backend/.env.local`

**Contenido** (copiar exactamente):

```env
# Database
DB_NAME=sca_hospital
DB_USER=sca_user
DB_PASSWORD=sca_password
DB_HOST=db
DB_PORT=5432

# Django
SECRET_KEY=django-insecure-local-development-key-change-in-production-12345678
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,backend
CSRF_TRUSTED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,http://localhost:8000

# CORS
CORS_ALLOW_ALL=True
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# JWT
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440
```

**Comando rápido** (ejecutar desde la raíz del proyecto):

```bash
cat > sca-hospital/backend/.env.local << 'EOF'
DB_NAME=sca_hospital
DB_USER=sca_user
DB_PASSWORD=sca_password
DB_HOST=db
DB_PORT=5432
SECRET_KEY=django-insecure-local-development-key-change-in-production-12345678
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,backend
CSRF_TRUSTED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,http://localhost:8000
CORS_ALLOW_ALL=True
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440
EOF
```

---

## 🚀 Comandos para Iniciar

```bash
# 1. Levantar todos los servicios
docker-compose up -d

# 2. Ejecutar migraciones
docker-compose exec backend python manage.py migrate

# 3. Crear superusuario
docker-compose exec backend python manage.py createsuperuser

# 4. (Opcional) Poblar datos de prueba
docker-compose exec backend python manage.py seed_hospital
```

**Listo!** Ahora puedes acceder a:
- 🌐 Frontend: http://localhost:5173
- 🔧 Backend API: http://localhost:8000/api/
- 👤 Admin: http://localhost:8000/admin/
- 📚 API Docs: http://localhost:8000/api/schema/swagger-ui/

---

## 🔑 Características Clave

### ✅ Volumen Persistente
```yaml
volumes:
  postgres_data:
    driver: local
```
- Los datos de PostgreSQL persisten entre reinicios
- Ubicación: volumen Docker llamado `postgres_data`
- Para eliminar datos: `docker-compose down -v`

### ✅ Healthcheck
```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U sca_user -d sca_hospital"]
  interval: 10s
  timeout: 5s
  retries: 5
```
- El backend espera a que PostgreSQL esté listo
- Evita errores de conexión al iniciar

### ✅ Depends On
```yaml
depends_on:
  db:
    condition: service_healthy
```
- Django no inicia hasta que PostgreSQL esté saludable
- Orden garantizado de inicio de servicios

### ✅ Hot Reload
- **Backend**: Cambios en archivos `.py` se reflejan automáticamente
- **Frontend**: Cambios en archivos `.vue`, `.js` se reflejan automáticamente
- No necesitas reiniciar los contenedores al desarrollar

---

## 🔄 Comparación: Antes vs Ahora

### Antes (Neon en la nube):
```env
DATABASE_URL=postgresql://user:pass@ep-cool-name-123456.us-east-1.aws.neon.tech/neondb?sslmode=require
```
- Base de datos en la nube (Neon)
- Requiere conexión a internet
- SSL obligatorio
- Datos en servidor remoto

### Ahora (PostgreSQL local):
```env
DB_HOST=db
DB_NAME=sca_hospital
DB_USER=sca_user
DB_PASSWORD=sca_password
DB_PORT=5432
```
- Base de datos local en Docker
- No requiere internet (excepto para pull de imagen)
- Sin SSL
- Datos locales y persistentes

### Tu `settings.py` soporta AMBOS:
```python
if os.environ.get('DATABASE_URL'):
    # PRODUCCIÓN: Usa DATABASE_URL (Neon con SSL)
    DATABASES = { ... }
else:
    # DESARROLLO: Usa variables DB_* (PostgreSQL local)
    DATABASES = { ... }
```

**Para cambiar entre ambos:**
- **Desarrollo local**: Usa `.env.local` sin `DATABASE_URL`
- **Producción**: Define `DATABASE_URL` en Render/Railway

---

## 📊 Arquitectura del Sistema

```
┌─────────────────────────────────────────────────┐
│           Docker Compose Network                │
│                                                 │
│  ┌─────────────┐    ┌──────────────┐           │
│  │             │    │              │           │
│  │  Frontend   │───▶│   Backend    │           │
│  │  (Vue.js)   │    │   (Django)   │           │
│  │  Port: 5173 │    │   Port: 8000 │           │
│  │             │    │              │           │
│  └─────────────┘    └──────┬───────┘           │
│                            │                    │
│                            ▼                    │
│                     ┌──────────────┐            │
│                     │              │            │
│                     │  PostgreSQL  │            │
│                     │  Port: 5432  │            │
│                     │              │            │
│                     └──────┬───────┘            │
│                            │                    │
│                            ▼                    │
│                  ┌──────────────────┐           │
│                  │  postgres_data   │           │
│                  │  (Volume)        │           │
│                  └──────────────────┘           │
│                                                 │
└─────────────────────────────────────────────────┘

Host Machine:
- localhost:5173 → Frontend
- localhost:8000 → Backend
- localhost:5432 → PostgreSQL
```

---

## 🛠️ Comandos Útiles

### Ver logs
```bash
docker-compose logs -f           # Todos los servicios
docker-compose logs -f backend   # Solo backend
docker-compose logs -f db        # Solo base de datos
```

### Reiniciar servicios
```bash
docker-compose restart           # Todos
docker-compose restart backend   # Solo backend
```

### Ejecutar comandos en el backend
```bash
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py shell
```

### Acceder a PostgreSQL
```bash
# Shell de PostgreSQL
docker-compose exec db psql -U sca_user -d sca_hospital

# Comandos útiles dentro de psql:
\dt          # Listar tablas
\d+ tabla    # Describir tabla
\q           # Salir
```

### Limpiar todo
```bash
docker-compose down              # Detener contenedores
docker-compose down -v           # Detener y eliminar volúmenes (⚠️ BORRA DATOS)
docker system prune              # Limpiar caché de Docker
```

---

## 🐛 Troubleshooting

### 1. Puerto 5432 ocupado
```bash
# Verificar qué usa el puerto
lsof -i :5432

# Detener PostgreSQL local (macOS)
brew services stop postgresql

# O cambiar puerto en docker-compose.yml
ports:
  - "5433:5432"  # Usar 5433 en el host
```

### 2. Backend no conecta a DB
```bash
# Verificar que DB esté saludable
docker-compose ps

# Debe mostrar: db (healthy)

# Si no, ver logs
docker-compose logs db

# Verificar manualmente
docker-compose exec db pg_isready -U sca_user -d sca_hospital
```

### 3. Migraciones fallan
```bash
# Eliminar contenedores y volúmenes
docker-compose down -v

# Reconstruir todo
docker-compose up -d --build

# Ejecutar migraciones nuevamente
docker-compose exec backend python manage.py migrate
```

### 4. Frontend no carga
```bash
# Ver logs del frontend
docker-compose logs -f frontend

# Verificar que Vite esté corriendo
docker-compose exec frontend npm run dev
```

### 5. Permisos en volúmenes (Linux)
```bash
# Si tienes problemas de permisos
sudo chown -R $USER:$USER ./sca-hospital
```

---

## 🎓 Conceptos Importantes

### ¿Por qué `DB_HOST=db`?
En Docker Compose, los servicios se comunican por nombre. El servicio `backend` puede acceder al servicio `db` usando el hostname `db`.

### ¿Por qué no usar `DATABASE_URL`?
`DATABASE_URL` es para conexiones a bases de datos remotas (como Neon). Para desarrollo local, es más simple usar variables separadas (`DB_NAME`, `DB_USER`, etc.).

### ¿Los datos persisten?
Sí, gracias al volumen `postgres_data`. Los datos persisten entre reinicios de contenedores. Para eliminar datos: `docker-compose down -v`.

### ¿Puedo usar pgAdmin?
Sí, puedes agregar pgAdmin al `docker-compose.yml`:

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

Luego accede a http://localhost:5050

---

## ✅ Checklist de Verificación

- [ ] Archivo `.env.local` creado en `sca-hospital/backend/`
- [ ] Variables de entorno correctas (especialmente `DB_HOST=db`)
- [ ] Docker Desktop corriendo (macOS/Windows)
- [ ] Puerto 5432 libre (no hay PostgreSQL local corriendo)
- [ ] Ejecutar `docker-compose up -d`
- [ ] Ejecutar `docker-compose ps` (todos deben estar "Up")
- [ ] Ejecutar migraciones
- [ ] Crear superusuario
- [ ] Acceder a http://localhost:8000/admin/
- [ ] Acceder a http://localhost:5173/

---

## 📚 Documentación Relacionada

- **`DOCKER_LOCAL_SETUP.md`** - Guía detallada completa
- **`DOCKER_QUICK_START.md`** - Inicio rápido con comandos esenciales
- **`sca-hospital/backend/SETUP_INSTRUCTIONS.md`** - Setup original del proyecto
- **Docker Compose Docs**: https://docs.docker.com/compose/
- **PostgreSQL Docs**: https://www.postgresql.org/docs/

---

## 🎉 ¡Todo Listo!

Tu proyecto ahora tiene:
- ✅ PostgreSQL local en Docker
- ✅ Datos persistentes entre reinicios
- ✅ Hot reload en backend y frontend
- ✅ Configuración lista para desarrollo
- ✅ Fácil de resetear y reiniciar
- ✅ No más dependencia de Neon para desarrollo

**Siguiente paso**: Crear el archivo `.env.local` y ejecutar `docker-compose up -d`

¡Feliz desarrollo! 🚀


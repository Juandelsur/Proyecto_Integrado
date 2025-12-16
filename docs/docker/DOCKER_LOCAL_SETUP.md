# 🐳 Configuración Local con Docker - PostgreSQL

## ✅ Archivos Creados

### 1. `docker-compose.yml` (Raíz del proyecto)

Se ha creado un archivo `docker-compose.yml` con:
- **Servicio `db`**: PostgreSQL 16 Alpine con volumen persistente
- **Servicio `backend`**: Django conectado a PostgreSQL
- **Servicio `frontend`**: Vue.js 
- **Volumen persistente** `postgres_data` para no perder datos

---

## 📝 Configuración Requerida

### 2. Crear archivo `.env.local` en `sca-hospital/backend/`

**IMPORTANTE**: Crea manualmente el archivo `.env.local` dentro de `sca-hospital/backend/` con el siguiente contenido:

```env
# =============================================================================
# DATABASE CONFIGURATION (PostgreSQL local en Docker)
# =============================================================================

DB_NAME=sca_hospital
DB_USER=sca_user
DB_PASSWORD=sca_password
DB_HOST=db
DB_PORT=5432

# =============================================================================
# DJANGO CONFIGURATION
# =============================================================================

SECRET_KEY=django-insecure-local-development-key-change-in-production-12345678
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,backend
CSRF_TRUSTED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,http://localhost:8000

# =============================================================================
# CORS CONFIGURATION
# =============================================================================

CORS_ALLOW_ALL=True
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# =============================================================================
# JWT CONFIGURATION
# =============================================================================

JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440
```

---

## 🚀 Uso de Docker Compose

### Levantar todos los servicios:
```bash
docker-compose up -d
```

### Ver logs:
```bash
docker-compose logs -f
```

### Solo base de datos (si quieres correr Django localmente sin Docker):
```bash
docker-compose up -d db
```

Y en ese caso, cambiar en `.env.local`:
```env
DB_HOST=localhost  # En lugar de 'db'
```

### Detener servicios:
```bash
docker-compose down
```

### Detener y eliminar volúmenes (⚠️ BORRA TODOS LOS DATOS):
```bash
docker-compose down -v
```

---

## 🔧 Comandos Útiles

### Ejecutar migraciones:
```bash
docker-compose exec backend python manage.py migrate
```

### Crear superusuario:
```bash
docker-compose exec backend python manage.py createsuperuser
```

### Poblar base de datos con datos de prueba:
```bash
docker-compose exec backend python manage.py seed_hospital
```

### Acceder a la shell de PostgreSQL:
```bash
docker-compose exec db psql -U sca_user -d sca_hospital
```

### Ver logs del backend:
```bash
docker-compose logs -f backend
```

### Reiniciar un servicio específico:
```bash
docker-compose restart backend
```

---

## 📊 Puertos Expuestos

- **PostgreSQL**: `localhost:5432`
- **Backend (Django)**: `http://localhost:8000`
- **Frontend (Vue)**: `http://localhost:5173`

---

## 🔐 Credenciales de PostgreSQL

Por defecto (puedes cambiarlas en `docker-compose.yml` y `.env.local`):

- **Base de datos**: `sca_hospital`
- **Usuario**: `sca_user`
- **Contraseña**: `sca_password`
- **Host**: `db` (dentro de Docker) o `localhost` (fuera de Docker)
- **Puerto**: `5432`

---

## ⚠️ Notas Importantes

1. **NO subas `.env.local` a Git** (ya debe estar en `.gitignore`)
2. **NO defines `DATABASE_URL`** en `.env.local` (eso es solo para producción con Neon)
3. El volumen `postgres_data` persiste los datos entre reinicios
4. El `healthcheck` en PostgreSQL asegura que el backend espere a que la BD esté lista
5. Si tienes problemas de conexión, asegúrate que el puerto 5432 no esté ocupado:
   ```bash
   lsof -i :5432
   ```

---

## 🔄 Migrando de Neon a PostgreSQL Local

Tu `settings.py` ya está configurado para soportar ambos:

- **Producción (Neon)**: Usa `DATABASE_URL` con SSL
- **Desarrollo Local**: Usa variables `DB_*` sin `DATABASE_URL`

Para cambiar entre ambos, simplemente:

1. **Desarrollo local**: Usa `.env.local` (sin `DATABASE_URL`)
2. **Producción**: Define `DATABASE_URL` en Render/Railway

---

## 🐛 Troubleshooting

### Backend no puede conectar a la base de datos:
```bash
# Verifica que PostgreSQL esté corriendo:
docker-compose ps

# Verifica logs de PostgreSQL:
docker-compose logs db

# Verifica que el healthcheck pase:
docker-compose exec db pg_isready -U sca_user -d sca_hospital
```

### Puerto 5432 ya está en uso:
```bash
# Detén cualquier PostgreSQL local:
brew services stop postgresql@14  # macOS con Homebrew
sudo systemctl stop postgresql    # Linux

# O cambia el puerto en docker-compose.yml:
ports:
  - "5433:5432"  # Usar 5433 en el host
```

### Permisos de archivos:
```bash
# Si tienes problemas de permisos con volúmenes:
docker-compose down -v
docker volume prune
docker-compose up -d
```

---

## ✅ Verificar que Todo Funciona

```bash
# 1. Levantar servicios
docker-compose up -d

# 2. Esperar unos segundos y verificar que estén corriendo
docker-compose ps

# 3. Ver logs para detectar errores
docker-compose logs -f

# 4. Probar conexión a PostgreSQL
docker-compose exec db psql -U sca_user -d sca_hospital -c "SELECT version();"

# 5. Ejecutar migraciones
docker-compose exec backend python manage.py migrate

# 6. Crear superusuario
docker-compose exec backend python manage.py createsuperuser

# 7. Poblar datos de prueba (opcional)
docker-compose exec backend python manage.py seed_hospital

# 8. Acceder al admin de Django
# http://localhost:8000/admin

# 9. Acceder a la API
# http://localhost:8000/api/

# 10. Acceder al frontend
# http://localhost:5173
```

---

## 🎯 Resumen

**Antes** (Neon en la nube):
```env
DATABASE_URL=postgresql://user:pass@neon.tech/db?sslmode=require
```

**Ahora** (PostgreSQL local en Docker):
```env
DB_NAME=sca_hospital
DB_USER=sca_user
DB_PASSWORD=sca_password
DB_HOST=db
DB_PORT=5432
```

¡Tu proyecto ahora usa PostgreSQL local con datos persistentes! 🎉


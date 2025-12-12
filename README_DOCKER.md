# 🐳 PostgreSQL Local con Docker - Guía Rápida

## 🎯 Objetivo

Configurar un entorno de desarrollo local con PostgreSQL en Docker, reemplazando la conexión a Neon (PostgreSQL en la nube) para desarrollo local.

---

## 🚀 Opción 1: Setup Automático (Recomendado)

### Linux / macOS:
```bash
cd sca-hospital
./setup-docker.sh
```

### Windows:
```cmd
cd sca-hospital
setup-docker.bat
```

El script automáticamente:
- ✅ Verifica Docker
- ✅ Crea archivo `.env.local`
- ✅ Construye imágenes
- ✅ Levanta servicios
- ✅ Ejecuta migraciones
- ✅ Opcionalmente crea superusuario y datos de prueba

---

## 📝 Opción 2: Setup Manual

### 1. Crear archivo `.env.local`

Ve a la carpeta `sca-hospital` y copia el archivo template:
```bash
cd sca-hospital
cp backend/env.local.template backend/.env.local
```

O créalo manualmente en `backend/.env.local`:
```env
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
```

### 2. Levantar servicios

Desde la carpeta `sca-hospital`:
```bash
cd sca-hospital
docker-compose up -d
```

### 3. Ejecutar migraciones

```bash
docker-compose exec backend python manage.py migrate
```

### 4. Crear superusuario

```bash
docker-compose exec backend python manage.py createsuperuser
```

### 5. (Opcional) Poblar datos de prueba

```bash
docker-compose exec backend python manage.py seed_hospital
```

---

## 🌐 Acceder a la Aplicación

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000/api/
- **Admin Django**: http://localhost:8000/admin/
- **API Docs (Swagger)**: http://localhost:8000/api/schema/swagger-ui/
- **PostgreSQL**: localhost:5432

---

## 📚 Documentación Completa

- **`DOCKER_SETUP_COMPLETE.md`** - Documentación completa y detallada
- **`DOCKER_QUICK_START.md`** - Inicio rápido con comandos esenciales
- **`DOCKER_LOCAL_SETUP.md`** - Guía detallada con troubleshooting

---

## 🛠️ Comandos Más Usados

```bash
# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down

# Reiniciar servicios
docker-compose restart

# Ejecutar comando en backend
docker-compose exec backend python manage.py <comando>

# Acceder a shell de PostgreSQL
docker-compose exec db psql -U sca_user -d sca_hospital

# Reconstruir imágenes
docker-compose build --no-cache

# Eliminar TODO (incluyendo datos)
docker-compose down -v
```

---

## 📦 Archivos Creados

### Configuración Docker:
- ✅ `sca-hospital/docker-compose.yml` - Orquestación de servicios
- ✅ `sca-hospital/backend/Dockerfile` - Imagen Django
- ✅ `sca-hospital/frontend/Dockerfile` - Imagen Vue.js
- ✅ `sca-hospital/backend/.dockerignore` - Archivos excluidos del build
- ✅ `sca-hospital/frontend/.dockerignore` - Archivos excluidos del build

### Configuración Aplicación:
- ✅ `sca-hospital/backend/env.local.template` - Template de variables de entorno
- ⚠️ `sca-hospital/backend/.env.local` - **DEBES CREAR ESTE ARCHIVO**

### Scripts de Setup:
- ✅ `sca-hospital/setup-docker.sh` - Setup automático (Linux/macOS)
- ✅ `sca-hospital/setup-docker.bat` - Setup automático (Windows)

### Documentación:
- ✅ `README_DOCKER.md` - Esta guía
- ✅ `DOCKER_SETUP_COMPLETE.md` - Guía completa
- ✅ `DOCKER_QUICK_START.md` - Quick start
- ✅ `DOCKER_LOCAL_SETUP.md` - Setup detallado

---

## 🔑 Servicios en docker-compose.yml

```yaml
services:
  db:              # PostgreSQL 16 Alpine
  backend:         # Django (depende de db)
  frontend:        # Vue.js + Vite (depende de backend)

volumes:
  postgres_data:   # Datos persistentes de PostgreSQL
```

---

## ⚠️ Importante

1. **NO subas `.env.local` a Git** (ya está en `.gitignore`)
2. **Cambia el `SECRET_KEY`** en producción
3. **Usa `DATABASE_URL`** solo en producción (Neon)
4. **Usa variables `DB_*`** para desarrollo local
5. **Los datos persisten** gracias al volumen `postgres_data`

---

## 🆚 Desarrollo vs Producción

| Aspecto | Desarrollo (Local) | Producción (Neon) |
|---------|-------------------|-------------------|
| Base de datos | PostgreSQL en Docker | Neon PostgreSQL |
| Configuración | `.env.local` | Variables en Render |
| Host DB | `db` (nombre servicio) | URL de Neon |
| SSL | No necesario | Requerido |
| Variable | `DB_HOST`, `DB_NAME`, etc. | `DATABASE_URL` |

Tu `settings.py` detecta automáticamente cuál usar:
- Si existe `DATABASE_URL` → Usa Neon (producción)
- Si no existe → Usa variables `DB_*` (desarrollo)

---

## 🐛 Problemas Comunes

### Puerto 5432 ocupado
```bash
# macOS
brew services stop postgresql

# Cambiar puerto en docker-compose.yml
ports:
  - "5433:5432"
```

### Backend no conecta
```bash
# Verificar estado
docker-compose ps

# Ver logs
docker-compose logs db backend
```

### Resetear todo
```bash
docker-compose down -v
docker-compose up -d --build
docker-compose exec backend python manage.py migrate
```

---

## ✅ Verificación Rápida

```bash
# 1. Servicios corriendo
docker-compose ps
# Todos deben estar "Up" y db debe estar "healthy"

# 2. PostgreSQL responde
docker-compose exec db pg_isready -U sca_user -d sca_hospital
# Debe responder: "sca_hospital - accepting connections"

# 3. Backend responde
curl http://localhost:8000/api/
# Debe responder con JSON

# 4. Frontend carga
curl http://localhost:5173/
# Debe responder con HTML
```

---

## 📞 ¿Necesitas Ayuda?

1. Revisa `DOCKER_SETUP_COMPLETE.md` para troubleshooting detallado
2. Verifica logs: `docker-compose logs -f`
3. Verifica estado: `docker-compose ps`
4. Resetea todo: `docker-compose down -v && docker-compose up -d --build`

---

## 🎉 ¡Listo!

Ahora tienes un entorno de desarrollo completo con:
- ✅ PostgreSQL local
- ✅ Django con hot reload
- ✅ Vue.js con hot reload
- ✅ Datos persistentes
- ✅ Fácil de resetear

**Próximo paso**: Ejecutar el script de setup o crear `.env.local` manualmente.

¡Feliz desarrollo! 🚀


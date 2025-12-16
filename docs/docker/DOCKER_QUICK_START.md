# 🚀 Quick Start - Docker Local Setup

## 📋 Pasos Rápidos

### 1️⃣ Crear archivo de configuración

Crea el archivo `sca-hospital/backend/.env.local` con este contenido:

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

### 2️⃣ Levantar servicios

```bash
docker-compose up -d
```

### 3️⃣ Ejecutar migraciones

```bash
docker-compose exec backend python manage.py migrate
```

### 4️⃣ Crear superusuario

```bash
docker-compose exec backend python manage.py createsuperuser
```

### 5️⃣ (Opcional) Poblar datos de prueba

```bash
docker-compose exec backend python manage.py seed_hospital
```

### 6️⃣ Acceder a la aplicación

- **Backend API**: http://localhost:8000/api/
- **Admin Django**: http://localhost:8000/admin/
- **Frontend Vue**: http://localhost:5173/
- **API Docs (Swagger)**: http://localhost:8000/api/schema/swagger-ui/

---

## 🛑 Detener servicios

```bash
docker-compose down
```

---

## 🔄 Solo base de datos (Django local, no Docker)

Si prefieres correr Django fuera de Docker pero quieres usar PostgreSQL en Docker:

### 1. Levantar solo la base de datos:
```bash
docker-compose up -d db
```

### 2. Cambiar en `.env.local`:
```env
DB_HOST=localhost  # En lugar de 'db'
```

### 3. Activar entorno virtual y correr Django:
```bash
cd sca-hospital/backend
source venv/bin/activate  # En Linux/macOS
# o
venv\Scripts\activate     # En Windows

python manage.py runserver
```

---

## 📝 Comandos útiles

```bash
# Ver logs en tiempo real
docker-compose logs -f

# Ver logs solo del backend
docker-compose logs -f backend

# Reiniciar un servicio
docker-compose restart backend

# Ejecutar comando en el backend
docker-compose exec backend python manage.py <comando>

# Acceder a shell de Django
docker-compose exec backend python manage.py shell

# Acceder a PostgreSQL
docker-compose exec db psql -U sca_user -d sca_hospital

# Ver contenedores corriendo
docker-compose ps

# Detener y eliminar TODO (⚠️ BORRA DATOS)
docker-compose down -v
```

---

## ✅ ¿Qué incluye este setup?

- ✅ PostgreSQL 16 Alpine (ligero y rápido)
- ✅ Django Backend con hot reload
- ✅ Vue Frontend con Vite hot reload
- ✅ Volumen persistente para la base de datos
- ✅ Healthcheck para PostgreSQL
- ✅ Variables de entorno configuradas
- ✅ Configuración lista para desarrollo

---

## 🎯 Diferencias: Producción vs Desarrollo

| Aspecto | Producción (Neon) | Desarrollo (Docker) |
|---------|------------------|---------------------|
| Base de datos | Neon PostgreSQL (nube) | PostgreSQL local |
| Configuración | `DATABASE_URL` | Variables `DB_*` |
| SSL | Requerido | No necesario |
| Archivo config | Variables en Render | `.env.local` |
| DEBUG | `False` | `True` |
| CORS | Orígenes específicos | Todos permitidos |

---

## 🐛 Problemas comunes

### Puerto 5432 ocupado
```bash
# macOS con Homebrew
brew services stop postgresql

# Linux
sudo systemctl stop postgresql

# O cambiar puerto en docker-compose.yml
```

### Backend no conecta a DB
```bash
# Verificar que DB esté lista
docker-compose exec db pg_isready -U sca_user -d sca_hospital

# Ver logs de DB
docker-compose logs db
```

### Permisos en volúmenes
```bash
docker-compose down -v
docker volume prune
docker-compose up -d
```

---

¡Listo! Tu entorno de desarrollo local está configurado. 🎉


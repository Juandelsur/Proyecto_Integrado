# 🏥 SCA - Sistema de Control de Activos Hospitalarios (Backend)

**API RESTful para la gestión integral de inventario, trazabilidad de activos y auditoría del Hospital Regional.**

Este backend proporciona una API robusta y escalable construida con Django 5 y Django REST Framework, diseñada para gestionar el ciclo de vida completo de los activos hospitalarios, desde su registro hasta su baja, con trazabilidad completa y auditoría de todas las operaciones.

---

## 📋 Tabla de Contenidos

- [Stack Tecnológico](#-stack-tecnológico)
- [Características Principales](#-características-principales)
- [Instalación y Configuración Local](#-instalación-y-configuración-local)
- [Variables de Entorno](#-variables-de-entorno)
- [Comandos de Gestión](#-comandos-de-gestión)
- [Documentación de la API](#-documentación-de-la-api)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Despliegue en Producción](#-despliegue-en-producción)
- [Autores](#-autores)

---

## 🛠️ Stack Tecnológico

### Lenguajes y Frameworks
- **Python 3.11+** - Lenguaje de programación principal
- **Django 5.x** - Framework web de alto nivel
- **Django REST Framework 3.14+** - Toolkit para construir APIs RESTful
- **djangorestframework-simplejwt 5.3+** - Autenticación JWT

### Base de Datos
- **PostgreSQL 15+** - Base de datos relacional
- **psycopg2-binary** - Adaptador de PostgreSQL para Python
- **NeonTech** - PostgreSQL serverless para producción

### Documentación y Herramientas
- **drf-spectacular 0.27+** - Generación automática de documentación OpenAPI 3.0
- **django-cors-headers 4.0+** - Manejo de CORS para frontend

### Servidor y Despliegue
- **Gunicorn 21.2+** - Servidor WSGI para producción
- **WhiteNoise 6.6+** - Servicio de archivos estáticos en producción
- **Render** - Plataforma de despliegue (Web Service)
- **python-dotenv 1.0+** - Gestión de variables de entorno

---

## ✨ Características Principales

### 🔐 Autenticación y Seguridad
- **JWT (JSON Web Tokens)** para autenticación stateless
- **Permisos granulares** con `IsAuthenticated` en todos los endpoints
- **Auditoría completa** de todas las operaciones críticas
- **SSL/TLS** requerido en producción (NeonTech)

### 📊 Gestión de Activos
- **CRUD completo** para activos hospitalarios
- **Trazabilidad** de movimientos entre ubicaciones
- **Historial completo** de cambios y movimientos
- **Serialización híbrida** (IDs en escritura, objetos completos en lectura)

### ⚡ Optimización y Performance
- **Select Related** para evitar N+1 queries
- **Paginación automática** (20 items por página)
- **Compresión de archivos estáticos** con WhiteNoise
- **Connection pooling** para PostgreSQL (conn_max_age=600)

### 📖 Documentación Automática
- **Swagger UI** interactivo en `/api/docs/`
- **ReDoc** en `/api/schema/redoc/`
- **OpenAPI 3.0 Schema** en `/api/schema/`

---

## 🚀 Instalación y Configuración Local

### Requisitos Previos
- **Python 3.11 o superior**
- **PostgreSQL 15+** (o Docker con `docker-compose.yml` en la raíz del proyecto)
- **Git**

### Paso 1: Clonar el Repositorio
```bash
git clone <URL_DEL_REPO>
cd Proyecto_Integrado/backend
```

### Paso 2: Crear y Activar Entorno Virtual

**En Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**En macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar Dependencias
```bash
pip install -r requirements.txt
```

### Paso 4: Configurar Variables de Entorno
Crea un archivo `.env` en la carpeta `backend/` con el siguiente contenido:

```env
# Configuración de Django
DEBUG=True
SECRET_KEY=tu-clave-secreta-super-segura-aqui-cambiar-en-produccion

# Base de Datos Local (Docker)
DB_NAME=sca_hospital
DB_USER=sca_user
DB_PASSWORD=sca_password
DB_HOST=localhost
DB_PORT=5432

# Base de Datos Producción (NeonTech)
# DATABASE_URL=postgresql://user:password@host:5432/database?sslmode=require

# CORS (Frontend)
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# CSRF (Producción)
CSRF_TRUSTED_ORIGINS=https://tu-dominio.onrender.com

# JWT Tokens (Opcional - Valores por defecto)
ACCESS_TOKEN_LIFETIME_MINUTES=60
REFRESH_TOKEN_LIFETIME_DAYS=7
```

### Paso 5: Levantar Base de Datos (Docker)
Desde la raíz del proyecto:
```bash
docker-compose up -d
```

### Paso 6: Ejecutar Migraciones
```bash
python manage.py migrate
```

### Paso 7: Poblar Base de Datos con Datos de Prueba
```bash
python manage.py seed_data
```

Este comando crea automáticamente:
- ✅ 2 Roles (Administrador, Técnico)
- ✅ 2 Usuarios de prueba
- ✅ 2 Departamentos (Urgencias, UCI)
- ✅ 4 Ubicaciones
- ✅ 3 Tipos de Equipo (Monitor, Desfibrilador, Camilla)
- ✅ 3 Estados (Operativo, En Mantención, De Baja)
- ✅ 5 Activos de ejemplo

### Paso 8: Crear Superusuario (Opcional)
```bash
python manage.py createsuperuser
```

### Paso 9: Iniciar Servidor de Desarrollo
```bash
python manage.py runserver
```

✅ **El backend estará disponible en:** `http://localhost:8000`

---

## 🔑 Variables de Entorno

### Variables Requeridas

| Variable | Descripción | Ejemplo | Requerido |
|----------|-------------|---------|-----------|
| `DEBUG` | Modo debug (True/False) | `False` | ✅ |
| `SECRET_KEY` | Clave secreta de Django | `django-insecure-...` | ✅ |
| `DATABASE_URL` | URL de conexión a PostgreSQL (Producción) | `postgresql://user:pass@host:5432/db` | ⚠️ Producción |
| `DB_NAME` | Nombre de la base de datos (Local) | `sca_hospital` | ⚠️ Local |
| `DB_USER` | Usuario de PostgreSQL (Local) | `sca_user` | ⚠️ Local |
| `DB_PASSWORD` | Contraseña de PostgreSQL (Local) | `sca_password` | ⚠️ Local |
| `DB_HOST` | Host de PostgreSQL (Local) | `localhost` | ⚠️ Local |
| `DB_PORT` | Puerto de PostgreSQL (Local) | `5432` | ⚠️ Local |

### Variables Opcionales

| Variable | Descripción | Valor por Defecto |
|----------|-------------|-------------------|
| `CORS_ALLOWED_ORIGINS` | Orígenes permitidos para CORS | `http://localhost:5173` |
| `CSRF_TRUSTED_ORIGINS` | Orígenes confiables para CSRF | `https://tu-dominio.onrender.com` |
| `ACCESS_TOKEN_LIFETIME_MINUTES` | Duración del token de acceso JWT | `60` (1 hora) |
| `REFRESH_TOKEN_LIFETIME_DAYS` | Duración del token de refresco JWT | `7` (7 días) |

---

## 🎯 Comandos de Gestión

### Migraciones de Base de Datos

**Crear migraciones:**
```bash
python manage.py makemigrations
```

**Aplicar migraciones:**
```bash
python manage.py migrate
```

**Ver estado de migraciones:**
```bash
python manage.py showmigrations
```

### Datos de Prueba

**Poblar base de datos con datos de prueba:**
```bash
python manage.py seed_data
```

Este comando personalizado (`seed_data`) es **fundamental para desarrollo y testing**. Ejecuta las siguientes operaciones:

1. **Limpia datos existentes** (opcional, con confirmación)
2. **Crea roles de usuario:**
   - Administrador (permisos completos)
   - Técnico (permisos limitados)
3. **Crea usuarios de prueba:**
   - `admin` / `admin123` (Administrador)
   - `tecnico` / `tecnico123` (Técnico)
4. **Crea departamentos:**
   - Urgencias
   - UCI (Unidad de Cuidados Intensivos)
5. **Crea ubicaciones:**
   - Sala 101, Box 3 (Urgencias)
   - Sala UCI-A, Box UCI-1 (UCI)
6. **Crea tipos de equipo:**
   - Monitor de Signos Vitales
   - Desfibrilador
   - Camilla Eléctrica
7. **Crea estados de activo:**
   - Operativo
   - En Mantención
   - De Baja
8. **Crea activos de ejemplo:**
   - 5 activos con códigos de inventario, números de serie, marcas y modelos

**Ventajas:**
- ✅ Configuración instantánea del entorno de desarrollo
- ✅ Datos consistentes para testing
- ✅ Evita crear datos manualmente
- ✅ Idempotente (puede ejecutarse múltiples veces)

### Gestión de Usuarios

**Crear superusuario:**
```bash
python manage.py createsuperuser
```

**Cambiar contraseña de usuario:**
```bash
python manage.py changepassword <username>
```

### Servidor de Desarrollo

**Iniciar servidor:**
```bash
python manage.py runserver
```

**Iniciar en puerto específico:**
```bash
python manage.py runserver 8080
```

**Iniciar en todas las interfaces:**
```bash
python manage.py runserver 0.0.0.0:8000
```

### Utilidades

**Abrir shell interactivo de Django:**
```bash
python manage.py shell
```

**Verificar configuración del proyecto:**
```bash
python manage.py check
```

**Recolectar archivos estáticos (producción):**
```bash
python manage.py collectstatic --noinput
```

---

## 📖 Documentación de la API

### Acceso a la Documentación Interactiva

Una vez que el servidor esté corriendo, puedes acceder a la documentación automática de la API:

#### 🔷 Swagger UI (Recomendado)
**URL:** `http://localhost:8000/api/docs/`

Interfaz interactiva que permite:
- ✅ Explorar todos los endpoints disponibles
- ✅ Ver esquemas de request/response
- ✅ Probar endpoints directamente desde el navegador
- ✅ Ver ejemplos de uso
- ✅ Autenticarse con JWT

#### 🔷 ReDoc
**URL:** `http://localhost:8000/api/schema/redoc/`

Documentación estática y elegante con:
- ✅ Vista de tres columnas
- ✅ Búsqueda rápida
- ✅ Navegación por tags

#### 🔷 OpenAPI Schema (JSON)
**URL:** `http://localhost:8000/api/schema/`

Esquema OpenAPI 3.0 en formato JSON para:
- ✅ Generación de clientes automáticos
- ✅ Importar en Postman/Insomnia
- ✅ Validación de contratos

### Autenticación JWT

Todos los endpoints (excepto `/api/token/` y `/api/token/refresh/`) requieren autenticación JWT.

#### 1. Obtener Token de Acceso

**Endpoint:** `POST /api/token/`

**Request:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### 2. Usar Token en Requests

Incluye el token en el header `Authorization`:

```bash
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Ejemplo con cURL:**
```bash
curl -H "Authorization: Bearer <tu_token>" http://localhost:8000/api/activos/
```

#### 3. Refrescar Token

**Endpoint:** `POST /api/token/refresh/`

**Request:**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response:**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Endpoints Principales

#### 🔹 Maestros
- `GET/POST /api/roles/` - Gestión de roles
- `GET/POST /api/departamentos/` - Gestión de departamentos
- `GET/POST /api/tipos-equipo/` - Gestión de tipos de equipo
- `GET/POST /api/estados-activo/` - Gestión de estados de activo

#### 🔹 Core
- `GET/POST /api/ubicaciones/` - Gestión de ubicaciones
- `GET/POST /api/usuarios/` - Gestión de usuarios
- `GET/POST /api/activos/` - Gestión de activos (CRUD completo)
- `POST /api/activos/{id}/movilizar/` - Movilizar activo entre ubicaciones

#### 🔹 Trazabilidad
- `GET/POST /api/historial-movimientos/` - Historial de movimientos de activos

#### 🔹 Auditoría
- `GET /api/auditoria-logs/` - Logs de auditoría (solo lectura)

### Ejemplo de Uso Completo

**1. Autenticarse:**
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

**2. Listar activos:**
```bash
curl http://localhost:8000/api/activos/ \
  -H "Authorization: Bearer <tu_token>"
```

**3. Crear un activo:**
```bash
curl -X POST http://localhost:8000/api/activos/ \
  -H "Authorization: Bearer <tu_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "codigo_inventario": "ACT-2024-001",
    "numero_serie": "SN123456",
    "marca": "HP",
    "modelo": "EliteBook 840 G8",
    "tipo_id": 1,
    "estado_id": 1,
    "ubicacion_actual_id": 1
  }'
```

**4. Movilizar un activo:**
```bash
curl -X POST http://localhost:8000/api/activos/1/movilizar/ \
  -H "Authorization: Bearer <tu_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "id_ubicacion_destino": 2,
    "notas": "Traslado por mantenimiento preventivo"
  }'
```

---

## 📁 Estructura del Proyecto

```
backend/
├── config/                      # Configuración del proyecto Django
│   ├── __init__.py
│   ├── settings.py             # Configuración principal (CRÍTICO)
│   ├── urls.py                 # URLs principales del proyecto
│   ├── wsgi.py                 # Punto de entrada WSGI (Gunicorn)
│   └── asgi.py                 # Punto de entrada ASGI (futuro)
│
├── core/                        # App principal del sistema
│   ├── migrations/             # Migraciones de base de datos
│   ├── management/             # Comandos personalizados
│   │   └── commands/
│   │       └── seed_data.py    # Comando para poblar DB
│   ├── __init__.py
│   ├── admin.py                # Configuración del panel de admin
│   ├── apps.py                 # Configuración de la app
│   ├── models.py               # Modelos de datos (9 modelos)
│   ├── serializers.py          # Serializers DRF (9 serializers)
│   ├── views.py                # ViewSets DRF (9 viewsets)
│   ├── urls.py                 # URLs de la API
│   └── tests.py                # Tests unitarios
│
├── venv/                        # Entorno virtual (no versionado)
├── .env                         # Variables de entorno (no versionado)
├── .env.example                 # Plantilla de variables de entorno
├── manage.py                    # CLI de Django
├── requirements.txt             # Dependencias de Python
├── Procfile                     # Configuración para Render
└── README.md                    # Este archivo
```

### Modelos de Datos (core/models.py)

El sistema cuenta con **9 modelos principales**:

1. **Rol** - Roles de usuario (Administrador, Técnico, Supervisor)
2. **Usuario** - Usuarios del sistema (extiende AbstractUser)
3. **Departamento** - Departamentos del hospital
4. **Ubicacion** - Ubicaciones físicas dentro de departamentos
5. **TipoEquipo** - Tipos de equipos/activos
6. **EstadoActivo** - Estados de los activos (Operativo, En Mantención, De Baja)
7. **Activo** - Activos hospitalarios (entidad central)
8. **HistorialMovimiento** - Trazabilidad de movimientos de activos
9. **AuditoriaLog** - Logs de auditoría del sistema

---

## 🚀 Despliegue en Producción

### Plataforma: Render

El proyecto está configurado para desplegarse en **Render** como un **Web Service**.

### Configuración en Render

#### 1. Crear Web Service

1. Conecta tu repositorio de GitHub a Render
2. Selecciona el repositorio del proyecto
3. Configura el servicio:
   - **Name:** `sca-hospital-backend`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r backend/requirements.txt`
   - **Start Command:** `gunicorn config.wsgi:application --log-file -`
   - **Root Directory:** `backend`

#### 2. Variables de Entorno en Render

Configura las siguientes variables en el dashboard de Render:

```env
DEBUG=False
SECRET_KEY=<genera-una-clave-secreta-segura>
DATABASE_URL=<url-de-neontech-postgresql>
CORS_ALLOWED_ORIGINS=https://tu-frontend.vercel.app
CSRF_TRUSTED_ORIGINS=https://sca-hospital-backend.onrender.com
```

#### 3. Base de Datos: NeonTech

1. Crea una cuenta en [NeonTech](https://neon.tech/)
2. Crea un nuevo proyecto PostgreSQL
3. Copia la **Connection String** (DATABASE_URL)
4. Pégala en las variables de entorno de Render

**Formato de DATABASE_URL:**
```
postgresql://user:password@host.neon.tech:5432/database?sslmode=require
```

#### 4. Despliegue Automático

Render detectará automáticamente el `Procfile` y desplegará el proyecto:

```
web: gunicorn config.wsgi:application --log-file -
```

#### 5. Ejecutar Migraciones en Producción

Después del primer despliegue, ejecuta las migraciones desde la consola de Render:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_data  # Opcional: datos de prueba
```

### Características de Producción

- ✅ **Gunicorn** como servidor WSGI
- ✅ **WhiteNoise** para servir archivos estáticos
- ✅ **SSL/TLS** requerido para conexiones a PostgreSQL
- ✅ **Connection pooling** (conn_max_age=600)
- ✅ **CORS** configurado para frontend
- ✅ **CSRF** protección habilitada
- ✅ **DEBUG=False** por defecto

### Monitoreo y Logs

**Ver logs en tiempo real:**
```bash
# Desde el dashboard de Render, sección "Logs"
```

**Verificar salud del servicio:**
```bash
curl https://sca-hospital-backend.onrender.com/api/activos/
```

---

## 👥 Autores

Este proyecto fue desarrollado por el equipo de estudiantes de Ingeniería en Informática del **Instituto Profesional AIEP**:

- **Matias Arias** - Backend Developer & Database Architect
- **Juan Muñoz** - Full Stack Developer & DevOps Engineer
- **Julio Villegas** - Frontend Developer & UI/UX Designer

### Institución
**Instituto Profesional AIEP**
Proyecto Integrado - Ingeniería en Informática
Año 2024

---

## 📄 Licencia

Este proyecto es de uso académico y está desarrollado como parte del Proyecto Integrado de la carrera de Ingeniería en Informática.

---

## 🆘 Soporte y Contacto

Para reportar problemas o solicitar ayuda:

1. **Issues:** Abre un issue en el repositorio de GitHub
2. **Documentación adicional:** Revisa los archivos `.md` en la carpeta `backend/`
3. **Contacto directo:** Contacta a los autores del proyecto

---

## 📚 Recursos Adicionales

### Documentación Oficial
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [drf-spectacular](https://drf-spectacular.readthedocs.io/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

### Guías del Proyecto
- `ADMIN_AND_SEED_GUIDE.md` - Guía del panel de administración
- `API_DOCUMENTATION.md` - Documentación detallada de la API
- `MODELS_DOCUMENTATION.md` - Documentación de modelos de datos
- `RAILWAY_DEPLOYMENT_GUIDE.md` - Guía de despliegue alternativa

---

**¡Gracias por usar el Sistema de Control de Activos Hospitalarios!** 🏥✨



# 🚀 Backend SCA - Guía de Configuración

## 📋 Requisitos Previos

- **Python 3.10+** (Compatible con MacOS M1 y Windows)
- **PostgreSQL** (via Docker)
- **Git**

---

## 🔧 Configuración Inicial

### 1️⃣ Clonar el Repositorio

```bash
git clone <repository-url>
cd sca-hospital
```

### 2️⃣ Iniciar PostgreSQL con Docker

Desde la raíz del proyecto:

```bash
docker-compose up -d
```

Verificar que el contenedor esté corriendo:

```bash
docker ps
```

### 3️⃣ Configurar el Entorno Virtual

#### En MacOS / Linux:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

#### En Windows:

```bash
cd backend
python -m venv venv
venv\Scripts\activate
```

### 4️⃣ Instalar Dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Nota:** Usamos `psycopg2-binary` para evitar problemas de compilación en Windows y MacOS M1.

### 5️⃣ Configurar Variables de Entorno

El archivo `.env` ya está creado con valores por defecto. Si necesitas modificarlo:

```bash
cp .env.example .env
# Editar .env según tu configuración
```

### 6️⃣ Ejecutar Migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7️⃣ Crear Superusuario (Opcional)

```bash
python manage.py createsuperuser
```

### 8️⃣ Iniciar el Servidor

```bash
python manage.py runserver
```

El servidor estará disponible en: `http://localhost:8000`

---

## 📚 Endpoints Disponibles

### Admin
- **Django Admin:** `http://localhost:8000/admin/`

### API REST
- **Activos:** `http://localhost:8000/api/activos/`
- **Ubicaciones:** `http://localhost:8000/api/ubicaciones/`

### Autenticación JWT
- **Obtener Token:** `POST http://localhost:8000/api/auth/token/`
- **Refrescar Token:** `POST http://localhost:8000/api/auth/token/refresh/`
- **Verificar Token:** `POST http://localhost:8000/api/auth/token/verify/`

### Documentación API
- **Swagger UI:** `http://localhost:8000/api/docs/`
- **ReDoc:** `http://localhost:8000/api/redoc/`
- **Schema JSON:** `http://localhost:8000/api/schema/`

---

## 🧪 Ejecutar Tests

```bash
python manage.py test
```

---

## 🛠️ Comandos Útiles

### Ver logs de PostgreSQL
```bash
docker logs sca_db_local
```

### Detener PostgreSQL
```bash
docker-compose down
```

### Limpiar base de datos
```bash
docker-compose down -v
docker-compose up -d
python manage.py migrate
```

### Generar nuevo SECRET_KEY
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

---

## 🐛 Solución de Problemas

### Error: "psycopg2 not found"
```bash
pip install psycopg2-binary
```

### Error: "Connection refused" (PostgreSQL)
Verificar que Docker esté corriendo:
```bash
docker ps
docker-compose up -d
```

### Error: "Port 8000 already in use"
```bash
# Matar el proceso en el puerto 8000
# MacOS/Linux:
lsof -ti:8000 | xargs kill -9

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

---

## 📦 Estructura del Proyecto

```
backend/
├── api/                    # App principal
├── config/                 # Configuración Django
│   ├── settings.py        # Configuración robusta con dotenv
│   └── urls.py            # URLs con JWT y documentación
├── manage.py
├── requirements.txt       # Dependencias con versiones flexibles
├── .env                   # Variables de entorno (NO commitear)
├── .env.example          # Plantilla de variables
└── SETUP.md              # Esta guía
```

---

## 👥 Equipo

Compatible con:
- ✅ MacOS (Intel y M1/M2)
- ✅ Windows 10/11
- ✅ Linux

---

## 📝 Notas Importantes

1. **NUNCA** commitear el archivo `.env`
2. Usar `psycopg2-binary` para evitar problemas de compilación
3. Mantener el entorno virtual activado durante el desarrollo
4. Ejecutar migraciones después de cada cambio en modelos
5. Documentar cambios en la API usando docstrings

---

## 🔗 Enlaces Útiles

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [drf-spectacular](https://drf-spectacular.readthedocs.io/)
- [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/)


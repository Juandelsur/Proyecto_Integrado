# ⚡ Quick Start - Backend SCA

## 🎯 Instalación Rápida

### Opción 1: Script Automático (Recomendado)

#### MacOS / Linux:
```bash
cd backend
chmod +x setup.sh
./setup.sh
```

#### Windows:
```bash
cd backend
setup.bat
```

---

### Opción 2: Instalación Manual

#### 1. Iniciar PostgreSQL
```bash
# Desde la raíz del proyecto
docker-compose up -d
```

#### 2. Crear y activar entorno virtual

**MacOS/Linux:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
```

#### 3. Instalar dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Configurar variables de entorno
```bash
# El archivo .env ya está creado con valores por defecto
# Si necesitas modificarlo, edita backend/.env
```

#### 5. Ejecutar migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 6. (Opcional) Crear superusuario
```bash
python manage.py createsuperuser
```

#### 7. Iniciar servidor
```bash
python manage.py runserver
```

---

## 🌐 URLs Disponibles

| Servicio | URL |
|----------|-----|
| **Admin Django** | http://localhost:8000/admin/ |
| **API Activos** | http://localhost:8000/api/activos/ |
| **API Ubicaciones** | http://localhost:8000/api/ubicaciones/ |
| **Swagger UI** | http://localhost:8000/api/docs/ |
| **ReDoc** | http://localhost:8000/api/redoc/ |
| **Schema JSON** | http://localhost:8000/api/schema/ |
| **JWT Token** | http://localhost:8000/api/auth/token/ |
| **JWT Refresh** | http://localhost:8000/api/auth/token/refresh/ |

---

## 🔑 Autenticación JWT

### Obtener Token:
```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "tu_usuario", "password": "tu_password"}'
```

### Usar Token en Requests:
```bash
curl http://localhost:8000/api/activos/ \
  -H "Authorization: Bearer TU_ACCESS_TOKEN"
```

---

## 📦 Dependencias Instaladas

- ✅ Django 5.x
- ✅ Django REST Framework
- ✅ Simple JWT (Autenticación)
- ✅ drf-spectacular (Documentación API)
- ✅ django-cors-headers (CORS)
- ✅ psycopg2-binary (PostgreSQL)
- ✅ python-dotenv (Variables de entorno)

---

## 🛠️ Comandos Útiles

```bash
# Activar entorno virtual
source venv/bin/activate  # MacOS/Linux
venv\Scripts\activate     # Windows

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver

# Ejecutar tests
python manage.py test

# Ver logs de PostgreSQL
docker logs sca_db_local

# Detener PostgreSQL
docker-compose down
```

---

## 📚 Documentación Completa

Ver **SETUP.md** para documentación detallada y solución de problemas.

---

## ✅ Checklist de Verificación

- [ ] Python 3.10+ instalado
- [ ] Docker instalado y corriendo
- [ ] PostgreSQL iniciado con `docker-compose up -d`
- [ ] Entorno virtual creado y activado
- [ ] Dependencias instaladas
- [ ] Migraciones ejecutadas
- [ ] Servidor corriendo en http://localhost:8000
- [ ] Swagger UI accesible en http://localhost:8000/api/docs/

---

## 🆘 Problemas Comunes

### Error: "psycopg2 not found"
```bash
pip install psycopg2-binary
```

### Error: "Connection refused"
```bash
docker-compose up -d
# Esperar 5 segundos
python manage.py migrate
```

### Error: "Port 8000 already in use"
```bash
# MacOS/Linux
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

---

## 🎉 ¡Listo!

Tu backend está configurado y listo para desarrollo.

**Próximo paso:** Abre http://localhost:8000/api/docs/ para explorar la API.


# 🚀 Instrucciones de Configuración del Backend SCA Hospital

## ✅ Requisitos Previos

- Python 3.9 o superior
- PostgreSQL 12 o superior (o SQLite para desarrollo)
- pip (gestor de paquetes de Python)

---

## 📦 Paso 1: Instalar Dependencias

### Opción A: Usando pip directamente

```bash
cd backend
pip3 install -r requirements.txt
```

### Opción B: Usando entorno virtual (RECOMENDADO)

```bash
cd backend

# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
# En macOS/Linux:
source venv/bin/activate

# En Windows:
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

**Salida esperada**:
```
Collecting Django>=5.0,<5.3
Collecting python-dotenv>=1.0.0
Collecting psycopg2-binary>=2.9.0
Collecting djangorestframework>=3.14.0
Collecting djangorestframework-simplejwt>=5.3.0
Collecting drf-spectacular>=0.27.0
Collecting django-cors-headers>=4.0.0
...
Successfully installed Django-5.0.x ...
```

---

## 🗄️ Paso 2: Configurar Base de Datos

### Opción A: PostgreSQL (PRODUCCIÓN)

1. **Crear base de datos**:
```bash
# Conectar a PostgreSQL
psql -U postgres

# Crear base de datos
CREATE DATABASE sca_hospital;

# Crear usuario
CREATE USER sca_user WITH PASSWORD 'sca_password';

# Otorgar permisos
GRANT ALL PRIVILEGES ON DATABASE sca_hospital TO sca_user;

# Salir
\q
```

2. **Configurar variables de entorno**:
```bash
# Crear archivo .env en backend/
cd backend
touch .env
```

3. **Editar .env**:
```env
# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=sca_hospital
DB_USER=sca_user
DB_PASSWORD=sca_password
DB_HOST=localhost
DB_PORT=5432

# Django
SECRET_KEY=tu-clave-secreta-super-segura-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# JWT
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Opción B: SQLite (DESARROLLO)

1. **Configurar variables de entorno**:
```bash
cd backend
touch .env
```

2. **Editar .env**:
```env
# Database (SQLite)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# Django
SECRET_KEY=tu-clave-secreta-super-segura-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# JWT
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

---

## 🔧 Paso 3: Aplicar Migraciones

```bash
cd backend

# Crear migraciones
python3 manage.py makemigrations

# Aplicar migraciones
python3 manage.py migrate
```

**Salida esperada**:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, core, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying core.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying sessions.0001_initial... OK
  ...
```

---

## 🌱 Paso 4: Poblar Base de Datos

```bash
python3 manage.py seed_data
```

**Salida esperada**:
```
🚀 Iniciando poblado de base de datos...

📋 Creando Roles...
   ✓ Rol "Administrador" creado
   ✓ Rol "Técnico" creado

👥 Creando Usuarios...
   ✓ Superusuario "admin" creado (password: admin123)
   ✓ Usuario "juan" creado (password: juan123)

...

======================================================================
✅ POBLADO COMPLETADO CON ÉXITO
======================================================================
```

---

## 🚀 Paso 5: Iniciar Servidor

```bash
python3 manage.py runserver
```

**Salida esperada**:
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
January 15, 2024 - 10:30:00
Django version 5.0, using settings 'config.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

---

## ✅ Paso 6: Verificar Instalación

### 1. Admin Panel
- URL: http://localhost:8000/admin/
- Usuario: admin
- Password: admin123

### 2. API Documentation
- Swagger: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/

### 3. API Endpoints
- Activos: http://localhost:8000/api/activos/
- Ubicaciones: http://localhost:8000/api/ubicaciones/
- Usuarios: http://localhost:8000/api/usuarios/

---

## 🔍 Solución de Problemas

### Error: "No module named 'dotenv'"
```bash
pip3 install python-dotenv
```

### Error: "No module named 'rest_framework'"
```bash
pip3 install djangorestframework
```

### Error: "No module named 'psycopg2'"
```bash
pip3 install psycopg2-binary
```

### Error: "FATAL: database does not exist"
Asegúrate de haber creado la base de datos en PostgreSQL.

### Error: "django.db.utils.OperationalError"
Verifica las credenciales en el archivo .env.

---

## 📚 Comandos Útiles

### Ver migraciones pendientes
```bash
python3 manage.py showmigrations
```

### Crear superusuario manualmente
```bash
python3 manage.py createsuperuser
```

### Limpiar base de datos
```bash
python3 manage.py flush
```

### Volver a poblar
```bash
python3 manage.py seed_data --force
```

### Abrir shell de Django
```bash
python3 manage.py shell
```

---

## ✅ Checklist de Instalación

- [ ] Python 3.9+ instalado
- [ ] PostgreSQL instalado (o usar SQLite)
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Archivo .env creado y configurado
- [ ] Base de datos creada (si usas PostgreSQL)
- [ ] Migraciones aplicadas (`python manage.py migrate`)
- [ ] Datos poblados (`python manage.py seed_data`)
- [ ] Servidor iniciado (`python manage.py runserver`)
- [ ] Admin accesible (http://localhost:8000/admin/)
- [ ] API Docs accesible (http://localhost:8000/api/docs/)

---

## 🎉 ¡Listo!

Tu backend del SCA Hospital está configurado y listo para usar.

**Próximos pasos**:
1. Explora el admin panel
2. Prueba los endpoints en Swagger
3. Moviliza un activo usando la API
4. Verifica la trazabilidad en el historial
5. Revisa los logs de auditoría


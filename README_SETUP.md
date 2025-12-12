# ✅ Configuración Actualizada - Docker PostgreSQL

## 📍 Ubicación Correcta de Archivos

Todos los archivos de Docker están ahora en la carpeta **`sca-hospital`**:

```
sca-hospital/
├── docker-compose.yml      ← Archivo principal
├── setup-docker.sh         ← Script Linux/macOS
├── setup-docker.bat        ← Script Windows
├── INICIO_RAPIDO.txt       ← Guía rápida
├── README_DOCKER.md        ← Esta guía
│
├── backend/
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── env.local.template
│   └── .env.local          ← DEBES CREAR
│
└── frontend/
    ├── Dockerfile
    └── .dockerignore
```

---

## 🚀 Cómo Empezar (3 pasos)

### 1️⃣ Ve a la carpeta correcta
```bash
cd sca-hospital
```

### 2️⃣ Crea el archivo .env.local
```bash
cp backend/env.local.template backend/.env.local
```

### 3️⃣ Levanta los servicios
```bash
# Opción A: Script automático (recomendado)
./setup-docker.sh

# Opción B: Manual
docker-compose up -d
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
```

---

## 🌐 URLs de Acceso

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/
- Docs: http://localhost:8000/api/schema/swagger-ui/

---

## ⚠️ Importante

**TODOS los comandos de docker-compose deben ejecutarse desde `sca-hospital`**

```bash
# ✅ Correcto
cd sca-hospital
docker-compose up -d

# ❌ Incorrecto  
cd Proyecto_Integrado
docker-compose up -d
```

---

## 📝 Comandos Útiles

```bash
# Ver logs
docker-compose logs -f

# Detener
docker-compose down

# Reiniciar
docker-compose restart

# Ejecutar comando Django
docker-compose exec backend python manage.py <comando>
```

---

¡Listo para desarrollar! 🚀


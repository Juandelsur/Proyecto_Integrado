# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

**Sistema de Control de Activos (SCA) - Hospital Regional**

A full-stack hospital asset tracking system with QR code-based inventory management, role-based access control (RBAC), and complete audit trail functionality.

**Tech Stack:**
- **Backend:** Django 5.2 + Django REST Framework + PostgreSQL
- **Frontend:** Vue 3 + Vuetify 3 + Pinia + Vite
- **Auth:** JWT (djangorestframework-simplejwt)
- **Database:** PostgreSQL 16 (Docker containerized)
- **Documentation:** drf-spectacular (OpenAPI/Swagger)

---

## Development Commands

### Docker Environment (Recommended)

All Docker commands must be run from the `sca-hospital` directory:

```bash
# Quick setup (automated)
./setup-docker.sh         # macOS/Linux
setup-docker.bat          # Windows

# Manual setup
docker-compose up -d
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser

# View logs
docker-compose logs -f [service]    # service: db, backend, frontend

# Stop services
docker-compose down

# Restart services
docker-compose restart [service]

# Execute Django commands
docker-compose exec backend python manage.py <command>
```

**Services:**
- Database: `http://localhost:5432` (PostgreSQL)
- Backend API: `http://localhost:8000`
- Frontend: `http://localhost:5173`

### Backend (Django)

Navigate to `backend/` directory first:

```bash
# Create/activate virtual environment
python3 -m venv venv
source venv/bin/activate          # macOS/Linux
.\venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Database operations
python manage.py migrate
python manage.py makemigrations

# Create superuser
python manage.py createsuperuser

# Seed test data (200 assets, 10 technicians, 4 managers)
python manage.py seed_hospital

# Run development server
python manage.py runserver

# Run tests
python backend/test_me_endpoint.py
python backend/test_rbac_permissions.py

# Static files
python manage.py collectstatic --noinput
```

### Frontend (Vue.js)

Navigate to `frontend/` directory first:

```bash
# Install dependencies
npm install

# Development server (with hot reload)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Code quality
npm run lint              # ESLint
npm run format            # Prettier

# Unit tests
npm run test:unit         # Vitest
```

---

## Architecture Overview

### Database Schema

**Core Models (8 tables):**
1. `Tbl_Roles` - User roles (Admin, Técnico, Jefe de Departamento)
2. `Tbl_Usuarios` - Custom User model extending Django's AbstractUser
3. `Tbl_Departamentos` - Hospital departments (Urgencias, UCI, etc.)
4. `Tbl_Ubicaciones` - Specific locations with auto-generated QR codes (LOC-XXXXXX)
5. `Tbl_Tipos_Equipo` - Asset types (Monitor, Computer, etc.)
6. `Tbl_Estados_Activo` - Asset states (Operativo, En Mantención, etc.)
7. `Tbl_Activos` - Central assets table with auto-generated inventory codes (INV-YY-XXXXXX)
8. `Tbl_Historial_Movimientos` - Complete movement tracking
9. `Tbl_Auditoria_Logs` - JSONField-based audit logs (replaces MongoDB)

**Key Features:**
- All foreign keys use explicit `db_column='fk_id_...'` naming
- `on_delete=models.PROTECT` for referential integrity
- Auto-generated unique codes with collision handling
- Indexed fields for performance (codigo_inventario, numero_serie, timestamps)

### Backend Architecture

**Structure:**
```
backend/
├── config/              # Project settings & main URLs
│   ├── settings.py      # Environment-based configuration
│   ├── urls.py          # JWT auth + API docs + admin
│   └── wsgi.py
├── core/                # Main app (all business logic here)
│   ├── models.py        # 9 models with explicit db_column FKs
│   ├── serializers.py   # Hybrid read/write serializers
│   ├── views.py         # ViewSets with RBAC permissions
│   ├── urls.py          # RESTful router configuration
│   ├── permissions.py   # Custom RBAC permission classes
│   ├── admin.py         # Django admin customization
│   └── management/
│       └── commands/
│           └── seed_hospital.py  # Test data seeding
└── requirements.txt
```

**API Structure (DefaultRouter):**
- `/api/roles/`, `/api/departamentos/`, `/api/tipos-equipo/`, `/api/estados-activo/` - Master data
- `/api/ubicaciones/` - Locations with QR codes
- `/api/usuarios/` - User management + `/api/usuarios/me/` endpoint
- `/api/activos/` - **Central resource** (asset CRUD)
- `/api/historial-movimientos/` - Movement tracking
- `/api/auditoria-logs/` - Audit logs (read-only)

**Authentication:**
- JWT tokens via `/api/auth/token/` (login)
- `/api/auth/token/refresh/` (refresh access token)
- `/api/auth/token/verify/` (verify token validity)

**API Documentation:**
- Swagger UI: `http://localhost:8000/api/docs/`
- ReDoc: `http://localhost:8000/api/redoc/`
- OpenAPI Schema: `http://localhost:8000/api/schema/`

### Frontend Architecture

**Structure:**
```
frontend/src/
├── App.vue
├── main.js              # Vuetify 3 + Pinia + Router setup
├── services/
│   ├── api.js           # Axios instance with JWT interceptors
│   ├── activosService.js
│   ├── authService.js
│   └── ubicacionesService.js
├── stores/              # Pinia state management
│   ├── auth.js          # Auth state + RBAC permissions computed
│   └── activos.js
├── router/
│   └── index.js         # Vue Router with auth guards
├── views/
│   ├── LoginView.vue
│   ├── HomeView.vue
│   ├── admin/           # Admin views
│   └── technician/      # Technician mobile-optimized views
├── layouts/
│   └── LayoutTecnico.vue
└── components/
```

**Key Frontend Patterns:**
- Vuetify 3 Material Design components
- Pinia stores for state management
- Axios interceptors auto-attach JWT tokens from localStorage
- Route guards check `requiresAuth`, `requiresPermission`, `requiresRole`
- QR scanning using `html5-qrcode` library
- QR generation using `qrcode` library

---

## Role-Based Access Control (RBAC)

**3 Roles Defined:**

### 1. Administrador
- **Permissions:** Full system access
- **Can:** Create/edit/delete assets, users, master data; print labels; move assets; view audit logs
- **Backend Permission Classes:** `IsAdminUser`

### 2. Técnico (Technician)
- **Permissions:** Operational asset management
- **Can:** Create/edit assets, move assets, print labels
- **Cannot:** Delete assets, manage users, view audit logs
- **Backend Permission Classes:** `IsTecnicoOperativo` + `CanDeleteActivo` (blocks DELETE)

### 3. Jefe de Departamento (Department Manager)
- **Permissions:** Read-only supervision
- **Can:** View assets, print labels, view audit logs
- **Cannot:** Create/edit/delete assets, move assets, manage users
- **Backend Permission Classes:** `IsJefeOrAdminReadOnly`, `IsAdminOrReadOnly`

**Implementation:**
- Backend: Custom permission classes in `core/permissions.py`
- Frontend: Computed properties in `stores/auth.js` (canManageAssets, canMoveAssets, etc.)
- Route protection: `router/index.js` guards check permissions before navigation

---

## Important Patterns & Conventions

### Serializer Hybrid Pattern (Read/Write)

Serializers use hybrid approach for foreign keys:
- **Write (POST/PUT):** Accept `{field}_id` (e.g., `departamento_id: 1`)
- **Read (GET):** Return full nested object (e.g., `departamento: {id: 1, nombre_departamento: "Urgencias"}`)

Example from `UbicacionSerializer`:
```python
# Write-only: accepts ID
departamento_id = serializers.PrimaryKeyRelatedField(
    queryset=Departamento.objects.all(),
    source='departamento',
    write_only=True
)

# Read-only: returns full object
departamento = DepartamentoSerializer(read_only=True)
```

### Auto-Generated Unique Codes

Both `Ubicacion` and `Activo` models generate unique codes automatically:
- **Ubicaciones:** `LOC-{6-char-hex}` (e.g., LOC-A1B2C3)
- **Activos:** `INV-{YY}-{6-char-hex}` (e.g., INV-25-F8A1B2)

Implementation uses collision detection loop (max 100 attempts) in model's `save()` method.

### Environment Configuration

**Backend (.env.local):**
- Use `backend/env.local.template` as template
- Required vars: `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`
- Docker: `DB_HOST=db`, Local: `DB_HOST=localhost`

**Frontend (.env.development / .env.production):**
- `VITE_API_URL` - Backend API URL (default: `http://localhost:8000`)

### File Path References

When referencing code:
- Backend: Use relative paths from `backend/` (e.g., `core/models.py`, `config/settings.py`)
- Frontend: Use relative paths from `frontend/` (e.g., `src/stores/auth.js`, `src/views/LoginView.vue`)

---

## Testing

**Backend Tests:**
- `backend/test_me_endpoint.py` - Tests `/api/usuarios/me/` endpoint with all roles
- `backend/test_rbac_permissions.py` - Tests permission classes

Run with: `python backend/test_me_endpoint.py` (requires Django setup)

**Frontend Tests:**
- Unit tests: `npm run test:unit` (Vitest + @vue/test-utils)
- Linting: `npm run lint`

---

## Common Workflows

### Adding a New Asset
1. POST to `/api/activos/` with `numero_serie`, `marca`, `modelo`, `tipo_id`, `estado_id`, `ubicacion_actual_id`
2. Backend auto-generates `codigo_inventario` (INV-YY-XXXXXX)
3. Frontend redirects to asset detail view

### Moving an Asset
1. Create entry in `/api/historial-movimientos/` with `activo_id`, `ubicacion_origen_id`, `ubicacion_destino_id`, `usuario_registra_id`, `tipo_movimiento`
2. Update `ubicacion_actual` on the asset via PATCH `/api/activos/{id}/`
3. Timestamp and user are auto-recorded

### QR Code Workflow
1. Scan QR code using technician scanner view
2. Parse code to extract asset `codigo_inventario` or location `codigo_qr`
3. Fetch asset/location via API
4. Display confirmation screen
5. Submit movement with current location

---

## Admin Credentials

**Default Superuser:**
- Username: `admin`
- Password: `admin123`

**Test Users (after seed_hospital):**
- `tecnico1` to `tecnico10` (password: `tecnico1123`, etc.)
- `jefe1` to `jefe4` (password: `jefe1123`, etc.)

---

## Git Workflow

**Branch Structure:**
- `main` - Production-ready code
- `develop` - Integration branch
- Individual branches: `julio`, `mati`, `juan`

**Rules:**
- Never commit directly to `main` or `develop`
- Always pull from `develop` before starting work: `git pull origin develop`
- Push to personal branch: `git push origin <your-branch>`

---

## Troubleshooting

### Port Already in Use
```bash
# Check what's using port 5432 (PostgreSQL)
lsof -i :5432

# Kill process
kill -9 <PID>
```

### Docker Issues
```bash
# Clean restart
docker-compose down -v    # Remove volumes
docker-compose up -d --build

# Reset database
docker-compose down -v
docker-compose up -d
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py seed_hospital
```

### CORS Errors
- Verify backend is running on port 8000
- Check `CORS_ALLOWED_ORIGINS` in backend `.env.local`
- Check `VITE_API_URL` in frontend `.env.development`

### JWT Token Expired
Frontend automatically handles via interceptor in `services/api.js` - redirects to login on 401

---

## Additional Documentation

- `README.md` - Quick start guide
- `README_DOCKER.md` - Docker setup guide
- `README_SETUP.md` - Setup instructions
- `CAMBIOS_REALIZADOS.md` - Change log
- `backend/ME_ENDPOINT_DOCUMENTATION.md` - `/me/` endpoint docs
- `backend/RBAC_IMPLEMENTATION.md` - RBAC system details

# CONTEXTO TÉCNICO DEL SISTEMA - SCA Hospital

**Stack:** Vue 3 + Vuetify 3 + Django REST Framework + PostgreSQL  
**Fecha de Generación:** 2024

---

## 1. MAPA DE DATOS: Modelos Django ↔ v-model Frontend

### 1.1 Modelo: `Activo` (Tbl_Activos)

**Campos del Modelo Django:**
```python
- id: AutoField (PK, read_only)
- codigo_inventario: CharField(max_length=20, unique, editable=False, auto-generated)
- numero_serie: CharField(max_length=100, unique, db_index=True)
- marca: CharField(max_length=100)
- modelo: CharField(max_length=100)
- fecha_alta: DateTimeField(auto_now_add=True, read_only)
- tipo: ForeignKey(TipoEquipo, db_column='fk_id_tipo', PROTECT)
- estado: ForeignKey(EstadoActivo, db_column='fk_id_estado', PROTECT)
- ubicacion_actual: ForeignKey(Ubicacion, db_column='fk_id_ubicacion_actual', PROTECT)
- notas: TextField(blank=True, null=True)
```

**v-model Frontend (POST/PUT):**
```javascript
{
  numero_serie: String,        // v-model="form.numero_serie"
  marca: String,               // v-model="form.marca"
  modelo: String,              // v-model="form.modelo"
  tipo_id: Number,             // v-model="form.tipo_id" (NO tipo, es tipo_id)
  estado_id: Number,           // v-model="form.estado_id" (NO estado, es estado_id)
  ubicacion_actual_id: Number, // v-model="form.ubicacion_actual_id" (NO ubicacion_actual)
  notas: String | null         // v-model="form.notas"
}
```

**v-model Frontend (GET - Respuesta):**
```javascript
{
  id: Number,
  codigo_inventario: String,   // Generado automáticamente, NO enviar en POST
  numero_serie: String,
  marca: String,
  modelo: String,
  fecha_alta: String,           // ISO 8601 format
  tipo: {                       // Objeto completo (read_only)
    id: Number,
    nombre_tipo: String
  },
  estado: {                     // Objeto completo (read_only)
    id: Number,
    nombre_estado: String
  },
  ubicacion_actual: {           // Objeto completo (read_only)
    id: Number,
    nombre_ubicacion: String,
    codigo_qr: String,
    departamento: {
      id: Number,
      nombre_departamento: String
    },
    total_activos: Number
  },
  notas: String | null
}
```

**CRÍTICO:** 
- En escritura (POST/PUT) usar `tipo_id`, `estado_id`, `ubicacion_actual_id` (números)
- En lectura (GET) recibir `tipo`, `estado`, `ubicacion_actual` (objetos)
- `codigo_inventario` se genera automáticamente, NO enviar en POST

---

### 1.2 Modelo: `Usuario` (Tbl_Usuarios)

**Campos del Modelo Django:**
```python
- id: AutoField (PK, read_only)
- username: CharField(unique, inherited from AbstractUser)
- password: CharField(write_only, hashed automatically)
- email: EmailField(inherited from AbstractUser)
- nombre_completo: CharField(max_length=200)
- rol: ForeignKey(Rol, db_column='fk_id_rol', PROTECT, null=True, blank=True)
- is_active: BooleanField(inherited)
- is_staff: BooleanField(inherited)
- date_joined: DateTimeField(auto_now_add=True, read_only)
- last_login: DateTimeField(read_only)
```

**v-model Frontend (POST/PUT):**
```javascript
{
  username: String,            // v-model="form.username"
  password: String,            // v-model="form.password" (write_only, se hashea)
  email: String,              // v-model="form.email"
  nombre_completo: String,    // v-model="form.nombre_completo"
  rol_id: Number | null,      // v-model="form.rol_id" (NO rol, es rol_id)
  is_active: Boolean,         // v-model="form.is_active"
  is_staff: Boolean           // v-model="form.is_staff"
}
```

**v-model Frontend (GET - Respuesta):**
```javascript
{
  id: Number,
  username: String,
  email: String,
  nombre_completo: String,
  rol: {                       // Objeto completo (read_only)
    id: Number,
    nombre_rol: String
  },
  is_active: Boolean,
  is_staff: Boolean,
  date_joined: String,         // ISO 8601 format
  last_login: String | null   // ISO 8601 format
}
```

**CRÍTICO:**
- `password` es write_only, NUNCA se devuelve en GET
- En escritura usar `rol_id` (número), en lectura recibir `rol` (objeto)

---

### 1.3 Modelo: `Ubicacion` (Tbl_Ubicaciones)

**Campos del Modelo Django:**
```python
- id: AutoField (PK, read_only)
- nombre_ubicacion: CharField(max_length=100)
- codigo_qr: CharField(max_length=20, unique, editable=False, auto-generated)
- departamento: ForeignKey(Departamento, db_column='fk_id_departamento', PROTECT)
```

**v-model Frontend (POST/PUT):**
```javascript
{
  nombre_ubicacion: String,   // v-model="form.nombre_ubicacion"
  departamento_id: Number     // v-model="form.departamento_id" (NO departamento)
}
```

**v-model Frontend (GET - Respuesta):**
```javascript
{
  id: Number,
  nombre_ubicacion: String,
  codigo_qr: String,          // Generado automáticamente (LOC-{HEX})
  departamento: {             // Objeto completo (read_only)
    id: Number,
    nombre_departamento: String
  },
  total_activos: Number        // Calculado (read_only)
}
```

---

### 1.4 Modelo: `HistorialMovimiento` (Tbl_Historial_Movimientos)

**Campos del Modelo Django:**
```python
- id: AutoField (PK, read_only)
- activo: ForeignKey(Activo, db_column='fk_id_activo', PROTECT)
- usuario_registra: ForeignKey(Usuario, db_column='fk_id_usuario_registra', PROTECT)
- ubicacion_origen: ForeignKey(Ubicacion, db_column='fk_id_ubicacion_origen', PROTECT)
- ubicacion_destino: ForeignKey(Ubicacion, db_column='fk_id_ubicacion_destino', PROTECT)
- fecha_movimiento: DateTimeField(auto_now_add=True, read_only)
- tipo_movimiento: CharField(choices=['TRASLADO', 'ASIGNACION', 'DEVOLUCION', 'MANTENIMIENTO', 'RETORNO', 'BAJA'])
- comentarios: TextField(null=True, blank=True)
```

**v-model Frontend (POST - Movilización):**
```javascript
{
  id_ubicacion_destino: Number, // v-model="form.id_ubicacion_destino" (min_value=1)
  notas: String | null          // v-model="form.notas" (max_length=500, optional)
}
```

**v-model Frontend (GET - Respuesta):**
```javascript
{
  id: Number,
  codigo_activo: String,        // activo.codigo_inventario (read_only)
  activo: {                     // Objeto activo (read_only)
    id: Number,
    codigo_inventario: String,
    marca: String,
    modelo: String
  },
  nombre_usuario: String,       // usuario_registra.nombre_completo (read_only)
  usuario_registra: {           // Objeto usuario (read_only)
    id: Number,
    username: String,
    nombre_completo: String
  },
  codigo_origen: String,         // ubicacion_origen.codigo_qr (read_only)
  ubicacion_origen: {            // Objeto ubicación origen (read_only)
    id: Number,
    nombre_ubicacion: String,
    codigo_qr: String,
    departamento: String
  },
  codigo_destino: String,        // ubicacion_destino.codigo_qr (read_only)
  ubicacion_destino: {           // Objeto ubicación destino (read_only)
    id: Number,
    nombre_ubicacion: String,
    codigo_qr: String,
    departamento: String
  },
  fecha_movimiento: String,       // ISO 8601 format
  tipo_movimiento: String,        // 'TRASLADO' | 'ASIGNACION' | 'DEVOLUCION' | 'MANTENIMIENTO' | 'RETORNO' | 'BAJA'
  comentarios: String | null
}
```

---

### 1.5 Modelos Maestros (Solo Lectura en Frontend)

**Rol (Tbl_Roles):**
```javascript
{
  id: Number,
  nombre_rol: String  // 'Administrador' | 'Técnico' | 'Jefe de Departamento'
}
```

**Departamento (Tbl_Departamentos):**
```javascript
{
  id: Number,
  nombre_departamento: String
}
```

**TipoEquipo (Tbl_Tipos_Equipo):**
```javascript
{
  id: Number,
  nombre_tipo: String  // 'Computador' | 'Monitor' | 'Impresora' | etc.
}
```

**EstadoActivo (Tbl_Estados_Activo):**
```javascript
{
  id: Number,
  nombre_estado: String  // 'Operativo' | 'En Mantención' | 'En Reparación' | 'De Baja'
}
```

---

## 2. LÓGICA DE VALIDACIÓN: Serializers ↔ Vuetify Rules

### 2.1 ActivoSerializer - Validaciones Backend

**Ubicación:** `backend/core/serializers.py:266`

**Validaciones Automáticas (Django REST Framework):**
```python
# Campos requeridos (required=True por defecto en ModelSerializer)
- numero_serie: required, max_length=100, unique=True
- marca: required, max_length=100
- modelo: required, max_length=100
- tipo_id: required (PrimaryKeyRelatedField)
- estado_id: required (PrimaryKeyRelatedField)
- ubicacion_actual_id: required (PrimaryKeyRelatedField)
- notas: optional (blank=True, null=True)

# Validaciones de Foreign Keys
- tipo_id: Debe existir en TipoEquipo.objects.all()
- estado_id: Debe existir en EstadoActivo.objects.all()
- ubicacion_actual_id: Debe existir en Ubicacion.objects.all()
```

**Vuetify Rules Frontend (Equivalente):**
```javascript
const rules = {
  numero_serie: [
    (v) => !!v || 'El número de serie es requerido',
    (v) => (v && v.length <= 100) || 'Máximo 100 caracteres',
    // Validación de unicidad debe hacerse en el backend
  ],
  marca: [
    (v) => !!v || 'La marca es requerida',
    (v) => (v && v.length <= 100) || 'Máximo 100 caracteres'
  ],
  modelo: [
    (v) => !!v || 'El modelo es requerido',
    (v) => (v && v.length <= 100) || 'Máximo 100 caracteres'
  ],
  tipo_id: [
    (v) => !!v || 'El tipo de equipo es requerido',
    (v) => Number.isInteger(Number(v)) || 'Debe ser un ID válido'
  ],
  estado_id: [
    (v) => !!v || 'El estado es requerido',
    (v) => Number.isInteger(Number(v)) || 'Debe ser un ID válido'
  ],
  ubicacion_actual_id: [
    (v) => !!v || 'La ubicación actual es requerida',
    (v) => Number.isInteger(Number(v)) || 'Debe ser un ID válido'
  ],
  notas: [
    (v) => !v || v.length <= 500 || 'Máximo 500 caracteres'
  ]
}
```

---

### 2.2 UsuarioSerializer - Validaciones Backend

**Ubicación:** `backend/core/serializers.py:183`

**Validaciones Automáticas:**
```python
- username: required, unique=True (validado por Django)
- password: required, write_only=True (se hashea en create())
- email: required, valid email format (validado por Django)
- nombre_completo: required, max_length=200
- rol_id: optional (allow_null=True, required=False)
- is_active: BooleanField (default=True)
- is_staff: BooleanField (default=False)
```

**Vuetify Rules Frontend:**
```javascript
const rules = {
  username: [
    (v) => !!v || 'El nombre de usuario es requerido',
    (v) => (v && v.length >= 3) || 'Mínimo 3 caracteres',
    (v) => /^[a-zA-Z0-9_]+$/.test(v) || 'Solo letras, números y guión bajo'
  ],
  password: [
    (v) => !!v || 'La contraseña es requerida',
    (v) => (v && v.length >= 8) || 'Mínimo 8 caracteres'
  ],
  email: [
    (v) => !!v || 'El email es requerido',
    (v) => /.+@.+\..+/.test(v) || 'Email inválido'
  ],
  nombre_completo: [
    (v) => !!v || 'El nombre completo es requerido',
    (v) => (v && v.length <= 200) || 'Máximo 200 caracteres'
  ],
  rol_id: [
    (v) => !v || Number.isInteger(Number(v)) || 'Debe ser un ID válido'
  ]
}
```

---

### 2.3 MovilizacionInputSerializer - Validaciones Backend

**Ubicación:** `backend/core/serializers.py:639`

**Validaciones:**
```python
- id_ubicacion_destino: required, IntegerField, min_value=1
  + Validación custom: validate_id_ubicacion_destino() verifica que exista en DB
- notas: optional, CharField, allow_blank=True, max_length=500
```

**Vuetify Rules Frontend:**
```javascript
const rules = {
  id_ubicacion_destino: [
    (v) => !!v || 'La ubicación destino es requerida',
    (v) => Number.isInteger(Number(v)) || 'Debe ser un número entero',
    (v) => Number(v) >= 1 || 'Debe ser mayor a 0'
  ],
  notas: [
    (v) => !v || v.length <= 500 || 'Máximo 500 caracteres'
  ]
}
```

---

### 2.4 UbicacionSerializer - Validaciones Backend

**Ubicación:** `backend/core/serializers.py:107`

**Validaciones:**
```python
- nombre_ubicacion: required, max_length=100
- departamento_id: required (PrimaryKeyRelatedField)
- codigo_qr: auto-generated, read_only
```

**Vuetify Rules Frontend:**
```javascript
const rules = {
  nombre_ubicacion: [
    (v) => !!v || 'El nombre de la ubicación es requerido',
    (v) => (v && v.length <= 100) || 'Máximo 100 caracteres'
  ],
  departamento_id: [
    (v) => !!v || 'El departamento es requerido',
    (v) => Number.isInteger(Number(v)) || 'Debe ser un ID válido'
  ]
}
```

---

## 3. CONFIGURACIÓN DE VUETIFY

**Ubicación:** `frontend/src/main.js:19-40`

**Configuración Completa:**
```javascript
const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'light',  // ⚠️ SOLO TEMA LIGHT CONFIGURADO
    themes: {
      light: {
        colors: {
          primary: '#1565C0',    // Azul Hospital
          secondary: '#0D47A1',  // Azul Oscuro
          success: '#4CAF50',     // Verde
          error: '#F44336',       // Rojo
          warning: '#FF9800',     // Naranja
          info: '#2196F3',        // Azul Info
        },
      },
      // ⚠️ NO HAY TEMA DARK CONFIGURADO
    },
  },
  icons: {
    defaultSet: 'mdi',  // Material Design Icons
  },
})
```

**Variables de Color Disponibles:**
```javascript
// Uso en componentes Vue
color="primary"    // #1565C0
color="secondary"  // #0D47A1
color="success"    // #4CAF50
color="error"      // #F44336
color="warning"    // #FF9800
color="info"       // #2196F3
```

**CRÍTICO:**
- Solo tema `light` está configurado
- No existe tema `dark` en la configuración
- Colores globales definidos en `themes.light.colors`

---

## 4. FLUJO DE AXIOS/FETCH

### 4.1 Configuración Base

**Ubicación:** `frontend/src/services/api.js`

**Instancia Axios:**
```javascript
const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: baseURL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})
```

**Variables de Entorno:**
```bash
# Desarrollo local
VITE_API_URL=http://localhost:8000

# Producción
VITE_API_URL=https://backend-sca.onrender.com
```

---

### 4.2 Interceptor de Request (Autenticación)

**Ubicación:** `frontend/src/services/api.js:31-45`

**Código:**
```javascript
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)
```

**Headers Enviados:**
```javascript
{
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Bearer {token}'  // Si existe access_token en localStorage
}
```

**CRÍTICO:**
- Token se obtiene de `localStorage.getItem('access_token')`
- Formato: `Bearer {token}`
- Se agrega automáticamente a TODAS las peticiones si existe

---

### 4.3 Interceptor de Response (Manejo de Errores)

**Ubicación:** `frontend/src/services/api.js:48-86`

**Código:**
```javascript
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response) {
      switch (error.response.status) {
        case 401:
          localStorage.removeItem('access_token')
          // Redirigir al login (comentado, implementar si es necesario)
          break
        case 403:
          console.error('Acceso prohibido')
          break
        case 404:
          console.error('Recurso no encontrado')
          break
        case 500:
          console.error('Error interno del servidor')
          break
      }
    }
    return Promise.reject(error)
  }
)
```

**Acciones por Código HTTP:**
- `401`: Elimina `access_token` del localStorage
- `403`: Log de error (acceso prohibido)
- `404`: Log de error (recurso no encontrado)
- `500`: Log de error (error interno)

---

### 4.4 Endpoints Principales

**Base URL:** `/api/`

**Endpoints Activos:**
```javascript
GET    /api/activos/                    // Lista paginada
GET    /api/activos/{id}/                // Detalle
POST   /api/activos/                     // Crear
PUT    /api/activos/{id}/                 // Actualizar completo
PATCH  /api/activos/{id}/                 // Actualizar parcial
DELETE /api/activos/{id}/                // Eliminar
POST   /api/activos/{id}/movilizar/      // Movilizar activo
```

**Endpoints Usuarios:**
```javascript
GET    /api/usuarios/                    // Lista
GET    /api/usuarios/me/                 // Usuario actual
GET    /api/usuarios/{id}/               // Detalle
POST   /api/usuarios/                    // Crear
PUT    /api/usuarios/{id}/               // Actualizar
```

**Endpoints Autenticación:**
```javascript
POST   /api/auth/token/                  // Login (obtener tokens)
POST   /api/auth/token/refresh/          // Refresh token
POST   /api/auth/token/verify/            // Verificar token
```

**Endpoints Maestros:**
```javascript
GET    /api/roles/                       // Lista de roles
GET    /api/departamentos/               // Lista de departamentos
GET    /api/ubicaciones/                 // Lista de ubicaciones
GET    /api/tipos-equipo/                // Lista de tipos
GET    /api/estados-activo/              // Lista de estados
```

---

## 5. ESTADO GLOBAL: PINIA STORES

### 5.1 Store: `auth` (Autenticación)

**Ubicación:** `frontend/src/stores/auth.js`

**Estado (State):**
```javascript
const token = ref(localStorage.getItem('access_token') || null)
const refreshToken = ref(localStorage.getItem('refresh_token') || null)
const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))
```

**Getters (Computed):**
```javascript
isAuthenticated: computed(() => !!token.value && !!user.value)
userRole: computed(() => user.value?.rol?.nombre_rol || null)
isAdmin: computed(() => userRole.value === 'Administrador')
isTecnico: computed(() => userRole.value === 'Técnico')
isJefe: computed(() => userRole.value === 'Jefe de Departamento')
```

**Permisos RBAC (Computed):**
```javascript
canPrintLabels: computed(() => isAuthenticated.value)  // ✅ TODOS los roles
canManageAssets: computed(() => isAdmin.value || isTecnico.value)  // ✅ Admin, Técnico
canDeleteAssets: computed(() => isAdmin.value)  // ✅ Solo Admin
canMoveAssets: computed(() => isAdmin.value || isTecnico.value)  // ✅ Admin, Técnico
canManageUsers: computed(() => isAdmin.value)  // ✅ Solo Admin
canViewAudit: computed(() => isAdmin.value || isJefe.value)  // ✅ Admin, Jefe
```

**Acciones (Actions):**
```javascript
async login(username, password) {
  // Simulado para desarrollo (FASE 3)
  // Usuarios de prueba:
  // - admin / admin123 -> Administrador
  // - tec / tec123 -> Técnico
  // - jefe / jefe123 -> Jefe de Departamento
  
  // Guarda tokens en localStorage y estado
  // Retorna: { success: boolean, message?: string }
}

async fetchUserInfo() {
  // GET /api/usuarios/me/
  // Actualiza user.value y localStorage
}

function logout() {
  // Limpia token, refreshToken, user
  // Elimina de localStorage: access_token, refresh_token, user
}
```

**Uso en Componentes:**
```javascript
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

// Verificar autenticación
if (authStore.isAuthenticated) { ... }

// Verificar permisos
if (authStore.canManageAssets) { ... }

// Acceder a rol
const role = authStore.userRole  // 'Administrador' | 'Técnico' | 'Jefe de Departamento'
```

---

### 5.2 Store: `activos` (Gestión de Activos)

**Ubicación:** `frontend/src/stores/activos.js`

**Estado (State):**
```javascript
const activos = ref([])  // Array de activos
const activoActual = ref(null)  // Activo seleccionado
const loading = ref(false)  // Estado de carga
const error = ref(null)  // Mensaje de error
const pagination = ref({
  count: 0,
  next: null,
  previous: null,
  currentPage: 1
})
```

**Getters (Computed):**
```javascript
totalActivos: computed(() => pagination.value.count)
hasNextPage: computed(() => pagination.value.next !== null)
hasPreviousPage: computed(() => pagination.value.previous !== null)
```

**Acciones (Actions):**
```javascript
async fetchActivos(params = {}) {
  // GET /api/activos/ con params (page, search, ordering)
  // Actualiza: activos.value, pagination.value
  // Parámetros: { page?: number, search?: string, ordering?: string }
}

async fetchActivoById(id) {
  // GET /api/activos/{id}/
  // Actualiza: activoActual.value
  // Retorna: objeto activo completo
}

async addActivo(activoData) {
  // POST /api/activos/
  // activoData: { numero_serie, marca, modelo, tipo_id, estado_id, ubicacion_actual_id, notas? }
  // Agrega a activos.value (unshift)
  // Retorna: activo creado
}

async editActivo(id, activoData) {
  // PUT /api/activos/{id}/
  // Actualiza en activos.value y activoActual.value si coincide
  // Retorna: activo actualizado
}

async removeActivo(id) {
  // DELETE /api/activos/{id}/
  // Elimina de activos.value
  // Limpia activoActual.value si coincide
}

async moverActivo(id, movimientoData) {
  // POST /api/activos/{id}/movilizar/
  // movimientoData: { id_ubicacion_destino: number, notas?: string }
  // Recarga activo con fetchActivoById(id)
  // Retorna: resultado del movimiento
}

function clearState() {
  // Limpia: activos, activoActual, error, pagination
}
```

**Uso en Componentes:**
```javascript
import { useActivosStore } from '@/stores/activos'

const activosStore = useActivosStore()

// Cargar lista
await activosStore.fetchActivos({ page: 1, search: 'HP' })

// Acceder a datos
const lista = activosStore.activos
const total = activosStore.totalActivos
const isLoading = activosStore.loading
const errorMsg = activosStore.error

// Crear activo
await activosStore.addActivo({
  numero_serie: 'SN123456',
  marca: 'HP',
  modelo: 'EliteBook 840 G8',
  tipo_id: 1,
  estado_id: 1,
  ubicacion_actual_id: 1
})
```

---

## 6. ESTRUCTURAS DE OBJETOS CRÍTICAS

### 6.1 Payload POST /api/activos/

```javascript
{
  numero_serie: "SN123456",        // String, required, unique
  marca: "HP",                     // String, required, max_length=100
  modelo: "EliteBook 840 G8",      // String, required, max_length=100
  tipo_id: 1,                      // Number, required (FK)
  estado_id: 1,                    // Number, required (FK)
  ubicacion_actual_id: 1,          // Number, required (FK)
  notas: "Equipo nuevo"            // String | null, optional, max_length=500
}
```

### 6.2 Payload POST /api/activos/{id}/movilizar/

```javascript
{
  id_ubicacion_destino: 5,          // Number, required, min_value=1
  notas: "Traslado por mantenimiento"  // String | null, optional, max_length=500
}
```

### 6.3 Respuesta GET /api/activos/{id}/

```javascript
{
  id: 1,
  codigo_inventario: "INV-25-A1B2C3",  // String, auto-generated
  numero_serie: "SN123456",
  marca: "HP",
  modelo: "EliteBook 840 G8",
  fecha_alta: "2024-01-15T10:30:00Z",  // ISO 8601
  tipo: {
    id: 1,
    nombre_tipo: "Computador"
  },
  estado: {
    id: 1,
    nombre_estado: "Operativo"
  },
  ubicacion_actual: {
    id: 1,
    nombre_ubicacion: "Sala 101",
    codigo_qr: "LOC-F8A1B2",
    departamento: {
      id: 1,
      nombre_departamento: "Urgencias"
    },
    total_activos: 5
  },
  notas: "Equipo nuevo"
}
```

### 6.4 Respuesta GET /api/activos/ (Paginada)

```javascript
{
  count: 100,                       // Total de activos
  next: "http://localhost:8000/api/activos/?page=2",
  previous: null,
  results: [
    // Array de objetos activo (misma estructura que GET /api/activos/{id}/)
  ]
}
```

---

## 7. NOMBRES DE VARIABLES Y CONSTANTES

### 7.1 LocalStorage Keys

```javascript
localStorage.getItem('access_token')    // Token JWT
localStorage.getItem('refresh_token')   // Refresh token
localStorage.getItem('user')             // JSON string del usuario
```

### 7.2 Roles del Sistema

```javascript
'Administrador'
'Técnico'
'Jefe de Departamento'
```

### 7.3 Tipos de Movimiento

```javascript
'TRASLADO'
'ASIGNACION'
'DEVOLUCION'
'MANTENIMIENTO'
'RETORNO'
'BAJA'
```

### 7.4 Nombres de Tablas en DB

```python
Tbl_Roles
Tbl_Usuarios
Tbl_Departamentos
Tbl_Ubicaciones
Tbl_Tipos_Equipo
Tbl_Estados_Activo
Tbl_Activos
Tbl_Historial_Movimientos
Tbl_Auditoria_Logs
```

### 7.5 Nombres de Columnas FK en DB

```python
fk_id_rol                  # Usuario.rol
fk_id_departamento          # Ubicacion.departamento
fk_id_tipo                  # Activo.tipo
fk_id_estado                # Activo.estado
fk_id_ubicacion_actual      # Activo.ubicacion_actual
fk_id_activo                # HistorialMovimiento.activo
fk_id_usuario_registra      # HistorialMovimiento.usuario_registra
fk_id_ubicacion_origen      # HistorialMovimiento.ubicacion_origen
fk_id_ubicacion_destino     # HistorialMovimiento.ubicacion_destino
fk_id_usuario               # AuditoriaLog.usuario
```

---

## 8. CONFIGURACIÓN DJANGO

### 8.1 User Model

```python
# settings.py
AUTH_USER_MODEL = 'core.Usuario'
```

### 8.2 Serializers - Patrón Híbrido

**CRÍTICO:** Todos los serializers con Foreign Keys usan patrón híbrido:
- **Escritura (POST/PUT):** Campos `{campo}_id` (PrimaryKeyRelatedField, write_only)
- **Lectura (GET):** Campos `{campo}` (Serializer anidado, read_only)

**Ejemplo ActivoSerializer:**
```python
tipo_id = PrimaryKeyRelatedField(write_only=True)      # POST/PUT
tipo = TipoEquipoSerializer(read_only=True)             # GET
```

---

## 9. VALIDACIONES CRÍTICAS

### 9.1 Backend - Validaciones Automáticas

- **Unique constraints:** `numero_serie`, `codigo_inventario`, `username`
- **Foreign Key validation:** Todos los `{campo}_id` deben existir en sus tablas
- **Required fields:** Validados automáticamente por ModelSerializer
- **Custom validation:** `MovilizacionInputSerializer.validate_id_ubicacion_destino()`

### 9.2 Frontend - Validaciones Vuetify

- **Required:** `rules.required = (v) => !!v || 'Este campo es requerido'`
- **Max length:** Validar según `max_length` del modelo
- **Email format:** `/.+@.+\..+/.test(v)`
- **Integer validation:** `Number.isInteger(Number(v))`
- **Min value:** `Number(v) >= 1`

---

## 10. CÓDIGOS AUTO-GENERADOS

### 10.1 Código de Inventario (Activo)

**Formato:** `INV-{YY}-{HEX}`  
**Ejemplo:** `INV-25-A1B2C3`  
**Generación:** Automática en `Activo.save()`  
**Validación:** Unique constraint en DB

### 10.2 Código QR (Ubicacion)

**Formato:** `LOC-{HEX}`  
**Ejemplo:** `LOC-F8A1B2`  
**Generación:** Automática en `Ubicacion.save()`  
**Validación:** Unique constraint en DB

---

**FIN DEL DOCUMENTO**


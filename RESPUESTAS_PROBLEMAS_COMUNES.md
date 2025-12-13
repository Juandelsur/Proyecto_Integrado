# 🎯 Respuestas a Problemas Comunes - Audio del Compañero

## 📝 Problemas Reportados

### 1. "El .env tuve que renombrarlo porque el backend lo buscaba como .env.local"

**✅ EN NUESTRA CONFIGURACIÓN ESTO YA ESTÁ CORRECTO**

El `docker-compose.yml` busca específicamente `.env.local`:
```yaml
env_file:
  - ./backend/.env.local
```

**Para tu compañero**: Debe usar `.env.local`, NO `.env`

**Comando para verificar**:
```bash
ls -la backend/.env.local
```

---

### 2. "La base de datos en Docker la buscamos como 'db' pero en el .env estaba como host o algo así"

**✅ EN NUESTRA CONFIGURACIÓN ESTO YA ESTÁ CORRECTO**

**Explicación del problema**:
- En `docker-compose.yml`, el servicio se llama `db`:
  ```yaml
  services:
    db:  ← Este es el nombre del servicio
  ```

- En `.env.local`, la variable `DB_HOST` DEBE ser `db`:
  ```bash
  DB_HOST=db  ← Debe coincidir con el nombre del servicio
  ```

**Si está mal configurado**:
```bash
# Ver el contenido actual
cat backend/.env.local | grep DB_HOST

# Si dice algo como:
# DB_HOST=localhost
# o
# DB_HOST=postgres
# o cualquier otra cosa

# Debe cambiarse a:
# DB_HOST=db
```

**Para editar**:
```bash
nano backend/.env.local
# o
code backend/.env.local
```

---

### 3. "Los tres servicios están activos... pero no sé si la base de datos tenía que mostrar algo"

**✅ ES NORMAL QUE LA BASE DE DATOS NO MUESTRE UNA INTERFAZ**

PostgreSQL es un servicio de base de datos, **no tiene interfaz web por defecto**.

**Cómo verificar que la base de datos funciona**:

```bash
# Opción 1: Verificar con pg_isready
docker-compose exec db pg_isready -U sca_user -d sca_hospital
# Debe responder: "/var/run/postgresql:5432 - accepting connections"

# Opción 2: Entrar a PostgreSQL
docker-compose exec db psql -U sca_user -d sca_hospital
# Si conecta, verás el prompt: sca_hospital=#

# Opción 3: Ver las tablas creadas
docker-compose exec db psql -U sca_user -d sca_hospital -c "\dt"
# Debe mostrar la lista de tablas (después de migrate)
```

**Interfaces gráficas para ver la BD** (opcionales):
1. **Django Admin**: http://localhost:8000/admin/ (después de crear superusuario)
2. **pgAdmin4**: Agregar servicio al docker-compose
3. **DBeaver**: Aplicación externa que se conecta a localhost:5432

---

### 4. "El comando seed no sé para qué es... el migrate funcionó bien"

**✅ EL SEED ES OPCIONAL - SIRVE PARA POBLAR DATOS DE PRUEBA**

#### ¿Qué hace `seed_hospital`?

El comando `python manage.py seed_hospital` crea datos de prueba en la base de datos:

**Crea**:
- ✅ **14 usuarios** (10 técnicos + 4 jefes de departamento)
- ✅ **200 activos** (notebooks, PCs, mouses, discos, impresoras)
- ✅ **Ubicaciones** (Pabellón Central, Sala de Emergencias, etc.)
- ✅ **Departamentos** (TI, Mantenimiento, etc.)
- ✅ **Historial de movimientos** (1-3 movimientos por activo)

#### ¿Es obligatorio?
**NO**. Es completamente opcional.

#### ¿Cuándo usarlo?
- Para tener datos con los que probar la aplicación
- Si la base de datos está vacía
- Para ver cómo funciona el sistema con datos reales

#### ¿Qué pasa si no lo uso?
- La base de datos estará vacía
- Tendrás que crear manualmente:
  - Usuarios (técnicos, jefes)
  - Activos (equipos)
  - Ubicaciones
  - Movimientos

#### ¿Por qué puede fallar el seed?

**Razones comunes**:

1. **La BD ya tiene datos**:
   ```bash
   # El seed borra datos existentes, verifica antes
   docker-compose exec backend python manage.py shell
   >>> from core.models import Activo
   >>> Activo.objects.count()
   200  # Si hay datos, preguntará si quieres borrarlos
   ```

2. **Faltan dependencias**:
   ```bash
   # Verificar que Faker está instalado
   docker-compose exec backend pip list | grep Faker
   # Debe mostrar: Faker  38.2.0
   ```

3. **Migraciones no aplicadas**:
   ```bash
   # Ejecutar primero
   docker-compose exec backend python manage.py migrate
   ```

4. **Permisos o problemas de BD**:
   ```bash
   # Ver logs para el error específico
   docker-compose logs backend
   ```

#### Cómo ejecutar el seed correctamente

```bash
# Paso 1: Asegurarse que las migraciones están aplicadas
docker-compose exec backend python manage.py migrate

# Paso 2: Ejecutar el seed
docker-compose exec backend python manage.py seed_hospital

# Salida esperada:
# ======================================================================
#   SEED HOSPITAL - Sistema de Control de Activos
# ======================================================================
# 
# [1/8] 🔄 Limpiando base de datos...
# ⚠️  ADVERTENCIA: Esto borrará TODOS los datos existentes.
# ¿Estás seguro? (yes/no): yes
# ✅ Base de datos limpiada
# 
# [2/8] 👥 Creando roles y usuarios...
# ✅ 14 usuarios creados
# 
# [3/8] 🏢 Creando departamentos...
# ✅ 6 departamentos creados
# 
# ... etc ...
```

---

## 🔍 Resumen de Diferencias

| Aspecto | Tu Compañero | Nuestra Config |
|---------|--------------|----------------|
| Nombre archivo | `.env` → tuvo que renombrar | `.env.local` desde el inicio ✅ |
| Variable host | Tenía nombre incorrecto | `DB_HOST=db` correcto ✅ |
| Entender seed | No sabía qué hacía | Explicado claramente ✅ |
| Ver BD | Pensaba que debía "mostrar algo" | Explicado cómo acceder ✅ |

---

## 📋 Checklist para tu Compañero

**Envíale esto**:

```bash
# 1. Verificar archivo .env.local
cd sca-hospital
ls -la backend/.env.local
# ✅ Debe existir

# 2. Verificar contenido (especialmente DB_HOST)
cat backend/.env.local | grep DB_HOST
# ✅ Debe decir: DB_HOST=db

# 3. Verificar que NO hay DATABASE_URL
cat backend/.env.local | grep DATABASE_URL
# ✅ No debe mostrar nada

# 4. Verificar servicios corriendo
docker-compose ps
# ✅ Todos deben estar "Up"

# 5. Verificar PostgreSQL
docker-compose exec db pg_isready -U sca_user -d sca_hospital
# ✅ Debe responder: "accepting connections"

# 6. Ver las tablas de la BD
docker-compose exec db psql -U sca_user -d sca_hospital -c "\dt"
# ✅ Debe mostrar lista de tablas

# 7. Crear superusuario (obligatorio para admin)
docker-compose exec backend python manage.py createsuperuser

# 8. (Opcional) Poblar datos de prueba
docker-compose exec backend python manage.py seed_hospital
```

---

## 🎓 Explicación para Principiantes

### ¿Por qué `DB_HOST=db`?

En Docker Compose, los servicios se comunican entre sí usando **sus nombres**.

```yaml
services:
  db:        ← Este es un "hostname" dentro de Docker
    ...
  
  backend:   ← Este servicio puede llamar al otro como "db"
    ...
```

Es como si en tu red local tuvieras:
- Computador 1: nombre `db`
- Computador 2: nombre `backend`

El `backend` puede conectarse a `db` porque Docker crea una **red interna** donde los nombres de servicios funcionan como hostnames.

**Por eso**:
- Dentro de Docker: `DB_HOST=db` ✅
- Fuera de Docker (tu máquina): `DB_HOST=localhost` ✅

---

### ¿Por qué `.env.local` y no `.env`?

Para separar ambientes:
- `.env` → Configuración general
- `.env.local` → Configuración específica de desarrollo local
- `.env.production` → Configuración de producción

En nuestro caso, usamos `.env.local` para dejar claro que es para **desarrollo local con Docker**.

---

### ¿Qué hace el comando `migrate`?

Crea las **tablas en la base de datos** según los modelos de Django:

```python
# models.py
class Activo(models.Model):
    codigo_inventario = models.CharField(...)
    nombre = models.CharField(...)
    ...
```

`migrate` convierte esto en SQL:
```sql
CREATE TABLE core_activo (
    id BIGSERIAL PRIMARY KEY,
    codigo_inventario VARCHAR(50),
    nombre VARCHAR(255),
    ...
);
```

---

### ¿Qué hace el comando `seed_hospital`?

**Llena las tablas** con datos de prueba:

```sql
-- Sin seed (tablas vacías):
SELECT COUNT(*) FROM core_activo;
-- Resultado: 0

-- Con seed:
SELECT COUNT(*) FROM core_activo;
-- Resultado: 200
```

**Analogía**:
- `migrate` = Construir un edificio (estructura)
- `seed` = Amueblar el edificio (contenido)

---

## 💡 Tips Adicionales

### Ver contenido de la base de datos sin comandos

1. Crear superusuario:
   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```

2. Ir a: http://localhost:8000/admin/

3. Ver todas las tablas visualmente

### Si el seed falla

```bash
# Ver el error específico
docker-compose logs backend | tail -50

# Errores comunes y soluciones:
# - "duplicate key": BD ya tiene datos → usar docker-compose down -v
# - "Faker not found": Reinstalar dependencias → docker-compose build --no-cache
# - "table doesn't exist": Aplicar migraciones → docker-compose exec backend python manage.py migrate
```

---

¿Necesitas que explique algo más en detalle? 🚀


# 🏥 Sistema de Control de Activos (SCA) - Hospital Regional

Este es el repositorio oficial del proyecto. La arquitectura está basada en **Django (Backend)** y **Vue 3 (Frontend)**, con base de datos **PostgreSQL** contenerizada en Docker.

---

## 🛠️ Pre-requisitos
Antes de empezar, asegúrate de tener instalado en tu computador:
1.  **Git**
2.  **Docker Desktop** (Debe estar abierto y corriendo)
3.  **Python 3.11+**
4.  **Node.js** (LTS)

---

## 🚀 Guía de Inicio Rápido

Sigue estos pasos en orden para levantar el entorno de desarrollo.

### 1. Clonar el repositorio
Abre tu terminal (PowerShell o CMD) y descarga el proyecto:

```bash
git clone <URL_DEL_REPO>
cd Proyecto_Integrado
```

### 2. Levantar la Base de Datos (Docker)
Esto iniciará un contenedor con PostgreSQL 15 configurado y listo en el puerto 5432.
*Asegúrate de tener Docker Desktop abierto.*

```bash
docker-compose up -d
```

### 3. Configurar el Backend (Django)
Abre una **nueva terminal** y navega a la carpeta backend:

```bash
cd backend
```

**Crear y activar el entorno virtual:**

* **En Windows:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
* **En Mac/Linux:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

**Instalar dependencias y correr el servidor:**

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
✅ *El Backend quedará corriendo en: `http://localhost:8000`*

### 4. Configurar el Frontend (Vue.js)
Abre una **nueva terminal**, vuelve a la raíz y entra a frontend:

```bash
cd frontend
npm install
npm run dev
```
✅ *El Frontend quedará corriendo en: `http://localhost:5173`*

---

## 🔑 Accesos y Credenciales

Una vez que todo esté corriendo, puedes acceder a:

* **Aplicación Web (Vue):** [http://localhost:5173](http://localhost:5173)
* **API Browser (Django):** [http://localhost:8000/api/activos/](http://localhost:8000/api/activos/)
* **Panel de Administración:** [http://localhost:8000/admin/](http://localhost:8000/admin/)

**Credenciales de Superusuario (Admin):**
* **Usuario:** `admin`
* **Contraseña:** `admin123`

---

## 🌳 Flujo de Trabajo con Git

Para mantener el orden, sigamos estas reglas:

1.  **NUNCA trabajar directo en `main` o `develop`.**
2.  Cada integrante tiene su propia rama. Antes de empezar a trabajar, cámbiate a ella:
    ```bash
    git checkout julio   # (o mati / juan)
    ```
3.  **Actualízate:** Antes de tirar código, trae los últimos cambios de develop a tu rama:
    ```bash
    git pull origin develop
    ```
4.  **Guardar cambios:**
    ```bash
    git add .
    git commit -m "Descripción de lo que hiciste"
    git push origin <tu_rama>
    ```

---

## 🆘 Solución de Problemas Comunes

* **Error: "Port 5432 is already allocated"**: Tienes otro Postgres corriendo en tu PC. Ciérralo o mata el proceso antes de hacer `docker-compose up`.
* **Error: "No se reconoce el comando 'venv'"**: Asegúrate de haber instalado Python correctamente y agregado al PATH (en Windows).
* **Error de CORS en el navegador**: Asegúrate de que el Backend esté corriendo en el puerto 8000.
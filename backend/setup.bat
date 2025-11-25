@echo off
REM ==============================================================================
REM Script de Inicialización del Backend SCA
REM Compatible con Windows
REM ==============================================================================

echo.
echo ========================================
echo   Backend SCA - Configuracion Inicial
echo ========================================
echo.

REM Verificar Python
echo [1/9] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado
    pause
    exit /b 1
)
echo [OK] Python encontrado
echo.

REM Verificar Docker
echo [2/9] Verificando Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker no esta instalado
    pause
    exit /b 1
)
echo [OK] Docker encontrado
echo.

REM Crear entorno virtual
echo [3/9] Creando entorno virtual...
if not exist "venv" (
    python -m venv venv
    echo [OK] Entorno virtual creado
) else (
    echo [INFO] Entorno virtual ya existe
)
echo.

REM Activar entorno virtual
echo [4/9] Activando entorno virtual...
call venv\Scripts\activate.bat
echo [OK] Entorno virtual activado
echo.

REM Actualizar pip
echo [5/9] Actualizando pip...
python -m pip install --upgrade pip --quiet
echo [OK] pip actualizado
echo.

REM Instalar dependencias
echo [6/9] Instalando dependencias...
pip install -r requirements.txt --quiet
echo [OK] Dependencias instaladas
echo.

REM Verificar archivo .env
echo [7/9] Verificando archivo .env...
if not exist ".env" (
    echo [INFO] Archivo .env no encontrado, copiando desde .env.example
    copy .env.example .env
    echo [OK] Archivo .env creado
) else (
    echo [OK] Archivo .env existe
)
echo.

REM Iniciar PostgreSQL con Docker
echo [8/9] Iniciando PostgreSQL con Docker...
cd ..
docker-compose up -d
cd backend
echo [OK] PostgreSQL iniciado
echo.

REM Esperar a que PostgreSQL este listo
echo Esperando a que PostgreSQL este listo...
timeout /t 5 /nobreak >nul
echo [OK] PostgreSQL listo
echo.

REM Ejecutar migraciones
echo [9/9] Ejecutando migraciones...
python manage.py makemigrations
python manage.py migrate
echo [OK] Migraciones completadas
echo.

REM Preguntar si crear superusuario
echo.
set /p CREATE_SUPER="Deseas crear un superusuario? (s/n): "
if /i "%CREATE_SUPER%"=="s" (
    python manage.py createsuperuser
)
echo.

REM Resumen
echo ========================================
echo   Configuracion completada exitosamente
echo ========================================
echo.
echo Proximos pasos:
echo 1. Activar el entorno virtual: venv\Scripts\activate
echo 2. Iniciar el servidor: python manage.py runserver
echo.
echo URLs disponibles:
echo    - Admin: http://localhost:8000/admin/
echo    - API: http://localhost:8000/api/
echo    - Swagger: http://localhost:8000/api/docs/
echo    - ReDoc: http://localhost:8000/api/redoc/
echo.
echo Ver SETUP.md para mas informacion
echo.
pause


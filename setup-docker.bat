@echo off
REM ==============================================================================
REM Script de Setup Rápido para Docker Local - PostgreSQL (Windows)
REM ==============================================================================
REM Este script automatiza el setup inicial del entorno de desarrollo local
REM con PostgreSQL en Docker.
REM ==============================================================================

echo.
echo ========================================
echo 🚀 Setup de Docker Local - SCA Hospital
echo ========================================
echo.

REM ==============================================================================
REM 1. Verificar que Docker esté corriendo
REM ==============================================================================
echo 📦 Verificando Docker...
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Docker no está corriendo.
    echo Por favor inicia Docker Desktop y vuelve a ejecutar este script.
    pause
    exit /b 1
)
echo ✅ Docker está corriendo
echo.

REM ==============================================================================
REM 2. Crear archivo .env.local si no existe
REM ==============================================================================
set ENV_FILE=backend\.env.local
set ENV_TEMPLATE=backend\env.local.template

if exist "%ENV_FILE%" (
    echo ⚠️  El archivo .env.local ya existe.
    set /p OVERWRITE="¿Deseas sobrescribirlo? (y/N): "
    if /i not "%OVERWRITE%"=="y" (
        echo Manteniendo archivo existente.
    ) else (
        echo 🔧 Creando archivo .env.local...
        copy /y "%ENV_TEMPLATE%" "%ENV_FILE%" >nul
        echo ✅ Archivo .env.local creado
    )
) else (
    echo 🔧 Creando archivo .env.local...
    copy /y "%ENV_TEMPLATE%" "%ENV_FILE%" >nul
    echo ✅ Archivo .env.local creado
)
echo.

REM ==============================================================================
REM 3. Detener contenedores existentes (si los hay)
REM ==============================================================================
echo 🛑 Deteniendo contenedores existentes (si los hay)...
docker-compose down >nul 2>&1
echo ✅ Contenedores detenidos
echo.

REM ==============================================================================
REM 4. Construir imágenes
REM ==============================================================================
echo 🔨 Construyendo imágenes de Docker...
docker-compose build --no-cache
echo ✅ Imágenes construidas
echo.

REM ==============================================================================
REM 5. Levantar servicios
REM ==============================================================================
echo 🚀 Levantando servicios (db, backend, frontend)...
docker-compose up -d
echo ✅ Servicios iniciados
echo.

REM ==============================================================================
REM 6. Esperar a que PostgreSQL esté listo
REM ==============================================================================
echo ⏳ Esperando a que PostgreSQL esté listo...
timeout /t 10 /nobreak >nul
docker-compose exec -T db pg_isready -U sca_user -d sca_hospital >nul 2>&1
if errorlevel 1 (
    echo ⚠️  PostgreSQL aún se está iniciando, espera unos segundos más...
    timeout /t 5 /nobreak >nul
)
echo ✅ PostgreSQL está listo
echo.

REM ==============================================================================
REM 7. Ejecutar migraciones
REM ==============================================================================
echo 📊 Ejecutando migraciones de Django...
docker-compose exec -T backend python manage.py migrate
echo ✅ Migraciones ejecutadas
echo.

REM ==============================================================================
REM 8. Recolectar archivos estáticos
REM ==============================================================================
echo 📦 Recolectando archivos estáticos...
docker-compose exec -T backend python manage.py collectstatic --noinput >nul 2>&1
echo ✅ Archivos estáticos recolectados
echo.

REM ==============================================================================
REM 9. Preguntar si desea crear superusuario
REM ==============================================================================
echo 👤 ¿Deseas crear un superusuario ahora?
set /p CREATE_SUPERUSER="(y/N): "
if /i "%CREATE_SUPERUSER%"=="y" (
    docker-compose exec backend python manage.py createsuperuser
    echo ✅ Superusuario creado
) else (
    echo Puedes crear un superusuario más tarde con:
    echo   docker-compose exec backend python manage.py createsuperuser
)
echo.

REM ==============================================================================
REM 10. Preguntar si desea poblar datos de prueba
REM ==============================================================================
echo 📝 ¿Deseas poblar la base de datos con datos de prueba?
set /p SEED_DATA="(y/N): "
if /i "%SEED_DATA%"=="y" (
    docker-compose exec -T backend python manage.py seed_hospital
    echo ✅ Datos de prueba cargados
) else (
    echo Puedes poblar datos de prueba más tarde con:
    echo   docker-compose exec backend python manage.py seed_hospital
)
echo.

REM ==============================================================================
REM FINALIZADO
REM ==============================================================================
echo.
echo ==============================================
echo 🎉 ¡Setup completado exitosamente!
echo ==============================================
echo.
echo 📍 Accede a tu aplicación en:
echo.
echo   🌐 Frontend (Vue.js):  http://localhost:5173
echo   🔧 Backend API:        http://localhost:8000/api/
echo   👤 Django Admin:       http://localhost:8000/admin/
echo   📚 API Docs:           http://localhost:8000/api/schema/swagger-ui/
echo.
echo 📝 Comandos útiles:
echo.
echo   # Ver logs en tiempo real
echo   docker-compose logs -f
echo.
echo   # Detener servicios
echo   docker-compose down
echo.
echo   # Reiniciar servicios
echo   docker-compose restart
echo.
echo   # Ejecutar comandos en el backend
echo   docker-compose exec backend python manage.py ^<comando^>
echo.
echo   # Acceder a PostgreSQL
echo   docker-compose exec db psql -U sca_user -d sca_hospital
echo.
echo ==============================================
echo.
pause


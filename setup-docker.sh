#!/bin/bash

# ==============================================================================
# Script de Setup Rápido para Docker Local - PostgreSQL
# ==============================================================================
# Este script automatiza el setup inicial del entorno de desarrollo local
# con PostgreSQL en Docker.
# ==============================================================================

set -e  # Detener si hay algún error

echo "🚀 Setup de Docker Local - SCA Hospital"
echo "========================================"
echo ""

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# ==============================================================================
# 1. Verificar que Docker esté corriendo
# ==============================================================================
echo "📦 Verificando Docker..."
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Error: Docker no está corriendo.${NC}"
    echo "Por favor inicia Docker Desktop y vuelve a ejecutar este script."
    exit 1
fi
echo -e "${GREEN}✅ Docker está corriendo${NC}"
echo ""

# ==============================================================================
# 2. Crear archivo .env.local si no existe
# ==============================================================================
ENV_FILE="backend/.env.local"
ENV_TEMPLATE="backend/env.local.template"

if [ -f "$ENV_FILE" ]; then
    echo -e "${YELLOW}⚠️  El archivo .env.local ya existe.${NC}"
    read -p "¿Deseas sobrescribirlo? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Manteniendo archivo existente."
    else
        echo "🔧 Creando archivo .env.local..."
        cp "$ENV_TEMPLATE" "$ENV_FILE"
        echo -e "${GREEN}✅ Archivo .env.local creado${NC}"
    fi
else
    echo "🔧 Creando archivo .env.local..."
    cp "$ENV_TEMPLATE" "$ENV_FILE"
    echo -e "${GREEN}✅ Archivo .env.local creado${NC}"
fi
echo ""

# ==============================================================================
# 3. Detener contenedores existentes (si los hay)
# ==============================================================================
echo "🛑 Deteniendo contenedores existentes (si los hay)..."
docker-compose down > /dev/null 2>&1 || true
echo -e "${GREEN}✅ Contenedores detenidos${NC}"
echo ""

# ==============================================================================
# 4. Construir imágenes
# ==============================================================================
echo "🔨 Construyendo imágenes de Docker..."
docker-compose build --no-cache
echo -e "${GREEN}✅ Imágenes construidas${NC}"
echo ""

# ==============================================================================
# 5. Levantar servicios
# ==============================================================================
echo "🚀 Levantando servicios (db, backend, frontend)..."
docker-compose up -d
echo -e "${GREEN}✅ Servicios iniciados${NC}"
echo ""

# ==============================================================================
# 6. Esperar a que PostgreSQL esté listo
# ==============================================================================
echo "⏳ Esperando a que PostgreSQL esté listo..."
for i in {1..30}; do
    if docker-compose exec -T db pg_isready -U sca_user -d sca_hospital > /dev/null 2>&1; then
        echo -e "${GREEN}✅ PostgreSQL está listo${NC}"
        break
    fi
    if [ $i -eq 30 ]; then
        echo -e "${RED}❌ Error: PostgreSQL no respondió a tiempo${NC}"
        echo "Ejecuta: docker-compose logs db"
        exit 1
    fi
    sleep 1
done
echo ""

# ==============================================================================
# 7. Ejecutar migraciones
# ==============================================================================
echo "📊 Ejecutando migraciones de Django..."
docker-compose exec -T backend python manage.py migrate
echo -e "${GREEN}✅ Migraciones ejecutadas${NC}"
echo ""

# ==============================================================================
# 8. Recolectar archivos estáticos
# ==============================================================================
echo "📦 Recolectando archivos estáticos..."
docker-compose exec -T backend python manage.py collectstatic --noinput > /dev/null 2>&1
echo -e "${GREEN}✅ Archivos estáticos recolectados${NC}"
echo ""

# ==============================================================================
# 9. Preguntar si desea crear superusuario
# ==============================================================================
echo "👤 ¿Deseas crear un superusuario ahora?"
read -p "(y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker-compose exec backend python manage.py createsuperuser
    echo -e "${GREEN}✅ Superusuario creado${NC}"
else
    echo "Puedes crear un superusuario más tarde con:"
    echo "  docker-compose exec backend python manage.py createsuperuser"
fi
echo ""

# ==============================================================================
# 10. Preguntar si desea poblar datos de prueba
# ==============================================================================
echo "📝 ¿Deseas poblar la base de datos con datos de prueba?"
read -p "(y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker-compose exec -T backend python manage.py seed_hospital
    echo -e "${GREEN}✅ Datos de prueba cargados${NC}"
else
    echo "Puedes poblar datos de prueba más tarde con:"
    echo "  docker-compose exec backend python manage.py seed_hospital"
fi
echo ""

# ==============================================================================
# FINALIZADO
# ==============================================================================
echo ""
echo "=============================================="
echo -e "${GREEN}🎉 ¡Setup completado exitosamente!${NC}"
echo "=============================================="
echo ""
echo "📍 Accede a tu aplicación en:"
echo ""
echo "  🌐 Frontend (Vue.js):  http://localhost:5173"
echo "  🔧 Backend API:        http://localhost:8000/api/"
echo "  👤 Django Admin:       http://localhost:8000/admin/"
echo "  📚 API Docs:           http://localhost:8000/api/schema/swagger-ui/"
echo ""
echo "📝 Comandos útiles:"
echo ""
echo "  # Ver logs en tiempo real"
echo "  docker-compose logs -f"
echo ""
echo "  # Detener servicios"
echo "  docker-compose down"
echo ""
echo "  # Reiniciar servicios"
echo "  docker-compose restart"
echo ""
echo "  # Ejecutar comandos en el backend"
echo "  docker-compose exec backend python manage.py <comando>"
echo ""
echo "  # Acceder a PostgreSQL"
echo "  docker-compose exec db psql -U sca_user -d sca_hospital"
echo ""
echo "=============================================="
echo ""


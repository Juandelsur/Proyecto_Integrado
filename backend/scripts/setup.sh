#!/bin/bash

# ==============================================================================
# Script de Inicialización del Backend SCA
# Compatible con MacOS y Linux
# ==============================================================================

set -e  # Detener en caso de error

echo "🚀 Iniciando configuración del Backend SCA..."
echo ""

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar Python
echo "📦 Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 no está instalado${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python $(python3 --version) encontrado${NC}"
echo ""

# Verificar Docker
echo "🐳 Verificando Docker..."
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker no está instalado${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Docker encontrado${NC}"
echo ""

# Crear entorno virtual
echo "🔧 Creando entorno virtual..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✅ Entorno virtual creado${NC}"
else
    echo -e "${YELLOW}⚠️  Entorno virtual ya existe${NC}"
fi
echo ""

# Activar entorno virtual
echo "🔌 Activando entorno virtual..."
source venv/bin/activate
echo -e "${GREEN}✅ Entorno virtual activado${NC}"
echo ""

# Actualizar pip
echo "⬆️  Actualizando pip..."
pip install --upgrade pip --quiet
echo -e "${GREEN}✅ pip actualizado${NC}"
echo ""

# Instalar dependencias
echo "📚 Instalando dependencias..."
pip install -r requirements.txt --quiet
echo -e "${GREEN}✅ Dependencias instaladas${NC}"
echo ""

# Verificar archivo .env
echo "🔐 Verificando archivo .env..."
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  Archivo .env no encontrado, copiando desde .env.example${NC}"
    cp .env.example .env
    echo -e "${GREEN}✅ Archivo .env creado${NC}"
else
    echo -e "${GREEN}✅ Archivo .env existe${NC}"
fi
echo ""

# Iniciar PostgreSQL con Docker
echo "🐘 Iniciando PostgreSQL con Docker..."
cd ..
docker-compose up -d
cd backend
echo -e "${GREEN}✅ PostgreSQL iniciado${NC}"
echo ""

# Esperar a que PostgreSQL esté listo
echo "⏳ Esperando a que PostgreSQL esté listo..."
sleep 5
echo -e "${GREEN}✅ PostgreSQL listo${NC}"
echo ""

# Ejecutar migraciones
echo "🔄 Ejecutando migraciones..."
python manage.py makemigrations
python manage.py migrate
echo -e "${GREEN}✅ Migraciones completadas${NC}"
echo ""

# Preguntar si crear superusuario
echo ""
read -p "¿Deseas crear un superusuario? (s/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[SsYy]$ ]]; then
    python manage.py createsuperuser
fi
echo ""

# Resumen
echo "=============================================="
echo -e "${GREEN}✅ ¡Configuración completada exitosamente!${NC}"
echo "=============================================="
echo ""
echo "📝 Próximos pasos:"
echo "1. Activar el entorno virtual: source venv/bin/activate"
echo "2. Iniciar el servidor: python manage.py runserver"
echo ""
echo "🌐 URLs disponibles:"
echo "   - Admin: http://localhost:8000/admin/"
echo "   - API: http://localhost:8000/api/"
echo "   - Swagger: http://localhost:8000/api/docs/"
echo "   - ReDoc: http://localhost:8000/api/redoc/"
echo ""
echo "📚 Ver SETUP.md para más información"
echo ""


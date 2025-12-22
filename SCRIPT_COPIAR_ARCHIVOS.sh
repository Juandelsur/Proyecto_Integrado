#!/bin/bash

# ============================================================================
# SCRIPT DE MIGRACIÓN AUTOMÁTICA - FEATURE-LOGIN A MAIN
# ============================================================================
# Descripción: Copia automáticamente todos los archivos .vue necesarios
#              desde la rama origin/feature-login sin afectar tu trabajo actual
# Autor: Senior Frontend Architect
# Fecha: 22 Diciembre 2025
# ============================================================================

set -e  # Salir si hay algún error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Contadores
SUCCESS_COUNT=0
ERROR_COUNT=0

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

print_header() {
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
    ((SUCCESS_COUNT++))
}

print_error() {
    echo -e "${RED}✗${NC} $1"
    ((ERROR_COUNT++))
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Función para copiar un archivo desde la rama feature-login
copy_file_from_feature() {
    local source_path=$1
    local dest_path=$2
    
    # Crear directorio destino si no existe
    mkdir -p "$(dirname "$dest_path")"
    
    # Copiar archivo usando git show
    if git show "origin/feature-login:$source_path" > "$dest_path" 2>/dev/null; then
        print_success "$dest_path"
        return 0
    else
        print_error "$dest_path (no encontrado en feature-login)"
        return 1
    fi
}

# ============================================================================
# INICIO DEL SCRIPT
# ============================================================================

print_header "🚀 SCRIPT DE MIGRACIÓN AUTOMÁTICA - FEATURE-LOGIN"

print_info "Este script copiará 27 archivos .vue necesarios desde origin/feature-login"
print_warning "Asegúrate de haber hecho commit de tus cambios actuales antes de continuar"
echo ""
read -p "¿Continuar? (s/n): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Ss]$ ]]; then
    print_error "Operación cancelada por el usuario"
    exit 1
fi

# ============================================================================
# VERIFICACIONES PREVIAS
# ============================================================================

print_header "🔍 VERIFICACIONES PREVIAS"

# Verificar que estamos en el directorio correcto
if [ ! -d "frontend/src" ]; then
    print_error "No se encuentra el directorio frontend/src"
    print_info "Asegúrate de ejecutar este script desde la raíz del proyecto"
    exit 1
fi
print_success "Directorio del proyecto verificado"

# Verificar que existe la rama feature-login
if ! git rev-parse --verify origin/feature-login >/dev/null 2>&1; then
    print_error "La rama origin/feature-login no existe"
    print_info "Ejecuta: git fetch origin"
    exit 1
fi
print_success "Rama origin/feature-login encontrada"

# ============================================================================
# CREAR ESTRUCTURA DE DIRECTORIOS
# ============================================================================

print_header "📁 CREANDO ESTRUCTURA DE DIRECTORIOS"

mkdir -p frontend/src/views/admin/gestion
mkdir -p frontend/src/views/technician/activos

print_success "Directorios creados correctamente"

# ============================================================================
# COPIAR ARCHIVOS - VISTAS ADMIN GESTIÓN
# ============================================================================

print_header "📂 COPIANDO VISTAS ADMIN - GESTIÓN (7 archivos)"

copy_file_from_feature "frontend/src/views/admin/gestion/GestionActivos.vue" \
    "frontend/src/views/admin/gestion/GestionActivos.vue"

copy_file_from_feature "frontend/src/views/admin/gestion/GestionEstadoActivo.vue" \
    "frontend/src/views/admin/gestion/GestionEstadoActivo.vue"

copy_file_from_feature "frontend/src/views/admin/gestion/GestionDepartamentos.vue" \
    "frontend/src/views/admin/gestion/GestionDepartamentos.vue"

copy_file_from_feature "frontend/src/views/admin/gestion/GestionRoles.vue" \
    "frontend/src/views/admin/gestion/GestionRoles.vue"

copy_file_from_feature "frontend/src/views/admin/gestion/GestionTipoEquipo.vue" \
    "frontend/src/views/admin/gestion/GestionTipoEquipo.vue"

copy_file_from_feature "frontend/src/views/admin/gestion/GestionUbicaciones.vue" \
    "frontend/src/views/admin/gestion/GestionUbicaciones.vue"

copy_file_from_feature "frontend/src/views/admin/gestion/GestionUsuarios.vue" \
    "frontend/src/views/admin/gestion/GestionUsuarios.vue"

# ============================================================================
# COPIAR ARCHIVOS - VISTAS ADMIN REPORTES
# ============================================================================

print_header "📂 COPIANDO VISTAS ADMIN - REPORTES (6 archivos)"

copy_file_from_feature "frontend/src/views/admin/AssetListView.vue" \
    "frontend/src/views/admin/AssetListView.vue"

copy_file_from_feature "frontend/src/views/admin/AssetDetailView.vue" \
    "frontend/src/views/admin/AssetDetailView.vue"

copy_file_from_feature "frontend/src/views/admin/PrintQRsView.vue" \
    "frontend/src/views/admin/PrintQRsView.vue"

copy_file_from_feature "frontend/src/views/admin/HistorialView.vue" \
    "frontend/src/views/admin/HistorialView.vue"

copy_file_from_feature "frontend/src/views/admin/ReportesView.vue" \
    "frontend/src/views/admin/ReportesView.vue"

copy_file_from_feature "frontend/src/views/admin/AuditoriaView.vue" \
    "frontend/src/views/admin/AuditoriaView.vue"

# ============================================================================
# COPIAR ARCHIVOS - VISTAS TÉCNICO
# ============================================================================

print_header "📂 COPIANDO VISTAS TÉCNICO (8 archivos)"

copy_file_from_feature "frontend/src/views/technician/ScannerView.vue" \
    "frontend/src/views/technician/ScannerView.vue"

copy_file_from_feature "frontend/src/views/technician/PrintLabelsView.vue" \
    "frontend/src/views/technician/PrintLabelsView.vue"

copy_file_from_feature "frontend/src/views/technician/CreateAssetView.vue" \
    "frontend/src/views/technician/CreateAssetView.vue"

copy_file_from_feature "frontend/src/views/technician/EditAssetSearchView.vue" \
    "frontend/src/views/technician/EditAssetSearchView.vue"

copy_file_from_feature "frontend/src/views/technician/MovimientoTecnicoView.vue" \
    "frontend/src/views/technician/MovimientoTecnicoView.vue"

copy_file_from_feature "frontend/src/views/technician/MovementSuccessView.vue" \
    "frontend/src/views/technician/MovementSuccessView.vue"

copy_file_from_feature "frontend/src/views/technician/SettingsView.vue" \
    "frontend/src/views/technician/SettingsView.vue"

copy_file_from_feature "frontend/src/views/technician/QRScannerDemoView.vue" \
    "frontend/src/views/technician/QRScannerDemoView.vue"

# ============================================================================
# COPIAR ARCHIVOS - VISTAS TÉCNICO ACTIVOS
# ============================================================================

print_header "📂 COPIANDO VISTAS TÉCNICO - ACTIVOS (2 archivos)"

copy_file_from_feature "frontend/src/views/technician/activos/CrearActivoView.vue" \
    "frontend/src/views/technician/activos/CrearActivoView.vue"

copy_file_from_feature "frontend/src/views/technician/activos/EditarActivoView.vue" \
    "frontend/src/views/technician/activos/EditarActivoView.vue"

# ============================================================================
# COPIAR ARCHIVOS - VISTAS COMPARTIDAS
# ============================================================================

print_header "📂 COPIANDO VISTAS COMPARTIDAS (4 archivos)"

copy_file_from_feature "frontend/src/views/AssetEditView.vue" \
    "frontend/src/views/AssetEditView.vue"

copy_file_from_feature "frontend/src/views/AssetCreateView.vue" \
    "frontend/src/views/AssetCreateView.vue"

copy_file_from_feature "frontend/src/views/AssetMoveView.vue" \
    "frontend/src/views/AssetMoveView.vue"

copy_file_from_feature "frontend/src/views/ImprimirQrView.vue" \
    "frontend/src/views/ImprimirQrView.vue"

# ============================================================================
# RESUMEN FINAL
# ============================================================================

print_header "📊 RESUMEN DE LA OPERACIÓN"

echo -e "${GREEN}✓ Archivos copiados exitosamente: $SUCCESS_COUNT${NC}"
if [ $ERROR_COUNT -gt 0 ]; then
    echo -e "${RED}✗ Archivos con errores: $ERROR_COUNT${NC}"
fi

echo ""
print_info "Total esperado: 27 archivos"
print_info "Total procesado: $((SUCCESS_COUNT + ERROR_COUNT)) archivos"

if [ $ERROR_COUNT -eq 0 ]; then
    echo ""
    print_header "✅ MIGRACIÓN COMPLETADA CON ÉXITO"
    echo ""
    print_info "Próximos pasos:"
    echo "  1. Instalar dependencias: cd frontend && npm install jspdf@^3.0.4 jspdf-autotable@^5.0.2 xlsx@^0.18.5"
    echo "  2. Activar router migrado: mv frontend/src/router/index.js frontend/src/router/index_OLD.js"
    echo "                             mv frontend/src/router/index_MIGRADO.js frontend/src/router/index.js"
    echo "  3. Probar aplicación: npm run dev"
    echo ""
else
    echo ""
    print_warning "Algunos archivos no se pudieron copiar"
    print_info "Revisa la lista de errores arriba y cópialos manualmente"
    echo ""
fi

print_header "🎉 SCRIPT FINALIZADO"


#!/bin/bash

# ==============================================================================
# Script de Deploy: Configuración CORS para Vercel
# ==============================================================================
# 
# Este script commitea y pushea la configuración CORS a Render
# Render detectará el push automáticamente y re-desplegará el backend
# 
# Uso: ./deploy-cors.sh
# ==============================================================================

set -e  # Exit on error

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║                                                                      ║"
echo "║         🚀 DEPLOY: Configuración CORS para Vercel                    ║"
echo "║                                                                      ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

# Verificar que estamos en el directorio backend
if [ ! -f "config/settings.py" ]; then
    echo "❌ Error: No se encuentra config/settings.py"
    echo "   Asegúrate de ejecutar este script desde el directorio 'backend/'"
    exit 1
fi

echo "✓ Directorio verificado: backend/"
echo ""

# Verificar que hay cambios en settings.py
if git diff --quiet config/settings.py; then
    echo "⚠️  No hay cambios en config/settings.py"
    echo "   ¿Ya hiciste commit anteriormente?"
    read -p "¿Continuar de todas formas? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✓ Cambios detectados en config/settings.py"
fi

echo ""
echo "📋 Cambios a commitear:"
echo "   • config/settings.py (configuración CORS/CSRF)"
echo ""

# Mostrar diff (primeras 30 líneas)
echo "📝 Preview de cambios:"
git diff config/settings.py | head -30
echo "   ..."
echo ""

# Confirmar con el usuario
read -p "¿Proceder con commit y push? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Deploy cancelado por el usuario"
    exit 1
fi

echo ""
echo "🔄 Staging archivos..."
git add config/settings.py

echo "✓ Archivos staged"
echo ""

echo "💾 Creando commit..."
git commit -m "feat: Configurar CORS para Vercel con estrategia híbrida dinámica

- Agregar backend-sca.onrender.com a ALLOWED_HOSTS
- Configurar CORS_ALLOWED_ORIGINS (localhost + backend)
- Configurar CORS_ALLOWED_ORIGIN_REGEXES (Vercel dinámico)
- Configurar CSRF_TRUSTED_ORIGINS (Vercel + backend)
- Habilitar CORS_ALLOW_CREDENTIALS para JWT

Estrategia híbrida:
1. Lista blanca específica para local y backend
2. Regex dinámico para todas las URLs de Vercel (previews + prod)
3. CSRF protection para operaciones sensibles

Refs: #cors #vercel #deploy"

echo "✓ Commit creado"
echo ""

echo "🚀 Pushing a origin main..."
git push origin main

echo "✓ Push completado"
echo ""

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║                                                                      ║"
echo "║                    ✅ DEPLOY INICIADO                                ║"
echo "║                                                                      ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""
echo "📊 Estado:"
echo "   • Commit: ✅ Completado"
echo "   • Push:   ✅ Completado"
echo "   • Render: ⏳ Detectando cambios..."
echo ""
echo "🔗 Próximos pasos:"
echo "   1. Ir a: https://dashboard.render.com"
echo "   2. Seleccionar servicio: backend-sca"
echo "   3. Verificar en 'Logs' que el deploy inició"
echo "   4. Esperar 1-2 minutos"
echo "   5. Probar desde Vercel"
echo ""
echo "🧪 Testing rápido (después de 2 minutos):"
echo "   Abrir DevTools en Vercel y ejecutar:"
echo ""
echo "   fetch('https://backend-sca.onrender.com/api/activos/', {"
echo "     headers: { 'Content-Type': 'application/json' }"
echo "   })"
echo "   .then(res => res.json())"
echo "   .then(data => console.log('✅ CORS OK:', data))"
echo ""
echo "🎉 ¡Listo!"

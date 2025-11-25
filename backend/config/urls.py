"""
URL Configuration for SCA Hospital Backend.

Incluye rutas para:
- Admin de Django
- API REST (ViewSets)
- Autenticación JWT
- Documentación API (Swagger/ReDoc)
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from api.views import ActivoViewSet, UbicacionViewSet

# ==============================================================================
# ROUTER CONFIGURATION
# ==============================================================================

# El Router crea las URLs automáticamente para los ViewSets
router = DefaultRouter()
router.register(r'activos', ActivoViewSet, basename='activo')
router.register(r'ubicaciones', UbicacionViewSet, basename='ubicacion')

# ==============================================================================
# URL PATTERNS
# ==============================================================================

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # API REST
    path('api/', include(router.urls)),

    # JWT Authentication
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
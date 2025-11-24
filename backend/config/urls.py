from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import ActivoViewSet, UbicacionViewSet

# El Router crea las URLs automáticamente
router = DefaultRouter()
router.register(r'activos', ActivoViewSet)
router.register(r'ubicaciones', UbicacionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
from rest_framework import serializers
from .models import Activo, Ubicacion

class UbicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ubicacion
        fields = '__all__'

class ActivoSerializer(serializers.ModelSerializer):
    # Esto agrega el nombre de la ubicación al JSON para que sea legible
    nombre_ubicacion = serializers.ReadOnlyField(source='ubicacion.nombre_ubicacion')

    class Meta:
        model = Activo
        fields = '__all__'
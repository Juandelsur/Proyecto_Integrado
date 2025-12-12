# =============================================================================
# Dockerfile para Django Backend - SCA Hospital
# =============================================================================

FROM python:3.11-slim

# Evitar que Python genere archivos .pyc y habilitar modo unbuffered
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema para PostgreSQL y otras herramientas
RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements y instalar dependencias de Python
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el código del proyecto
COPY . /app/

# Exponer puerto 8000 para Django
EXPOSE 8000

# Comando por defecto (puede ser sobrescrito en docker-compose.yml)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


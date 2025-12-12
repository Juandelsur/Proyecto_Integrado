# =============================================================================
# Dockerfile para Vue.js Frontend - SCA Hospital
# =============================================================================

FROM node:20-alpine

# Establecer directorio de trabajo
WORKDIR /app

# Copiar package.json y package-lock.json
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar el código del proyecto
COPY . .

# Exponer puerto 5173 (Vite default)
EXPOSE 5173

# Comando para modo desarrollo (con hot reload)
# Vite necesita --host 0.0.0.0 para ser accesible desde fuera del contenedor
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]


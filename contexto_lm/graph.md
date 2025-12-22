Aquí tienes el bloque procesado para **Indicadores de Carga y Progreso**.

Estos componentes son vitales para la UX en aplicaciones con latencia de red (Backend Calls). He agrupado ambos porque suelen convivir: uno para estados globales (linear) y otro para elementos puntuales (circular).

---

# v-progress-linear, v-progress-circular

### Ejemplo de Uso (Sinergia: Tarjeta de Carga de Archivos)

Este ejemplo combina una barra lineal para el progreso total y un loader circular para indicar procesamiento individual.

```html
<script setup>
import { ref, onMounted } from 'vue'

const uploadProgress = ref(0)
const isProcessing = ref(false)

// Simulación de carga
onMounted(() => {
  const interval = setInterval(() => {
    if (uploadProgress.value < 100) {
      uploadProgress.value += 10
    } else {
      clearInterval(interval)
      isProcessing.value = true // Cambia a estado "Procesando"
    }
  }, 500)
})
</script>

<template>
  <v-card width="400" title="Subiendo Documentos" subtitle="Por favor no cierre la ventana">
    <v-card-text>
      
      <div class="d-flex justify-space-between mb-1">
        <span>Progreso General</span>
        <span>{{ uploadProgress }}%</span>
      </div>
      <v-progress-linear
        v-model="uploadProgress"
        color="primary"
        height="10"
        striped
        rounded
      ></v-progress-linear>

      <v-divider class="my-4"></v-divider>

      <div class="d-flex align-center">
        <v-progress-circular
          v-if="isProcessing"
          indeterminate
          color="success"
          size="24"
          width="3"
          class="mr-3"
        ></v-progress-circular>
        
        <div class="text-body-2">
          <span v-if="!isProcessing">Subiendo datos al servidor...</span>
          <span v-else class="text-success font-weight-bold">Procesando y guardando en DB...</span>
        </div>
      </div>

    </v-card-text>
  </v-card>
</template>

```

---

# v-progress-linear

Barra horizontal. Ideal para colocar en la parte superior de tablas (`loading` prop), diálogos o tarjetas.

### API Props

| Prop | Tipo | Default | Descripción |
| --- | --- | --- | --- |
| **model-value** | string/number | 0 | El porcentaje actual de progreso (0-100). |
| **indeterminate** | boolean | false | **Vital:** Si es `true`, la barra se anima constantemente sin mostrar un porcentaje específico (útil cuando no sabes cuánto tardará el backend). |
| **color** | string | undefined | Color de la barra (ej: 'primary', 'error'). |
| **height** | string/number | 4 | Grosor de la barra. |
| **striped** | boolean | false | Añade un patrón de rayas diagonales a la parte llena. |
| **stream** | boolean | false | Animación especial que indica que hay flujo de datos continuo. |
| **buffer-value** | string/number | 0 | Muestra una segunda barra más clara (útil para streaming de video o cargas en dos pasos). |
| **rounded** | boolean | false | Redondea los bordes de la barra. |
| **bg-color** | string | undefined | Color del fondo de la barra (la parte vacía). |

---

# v-progress-circular

Spinner circular. Ideal para botones (`loading`), iconos de estado o centrado en la pantalla durante la carga inicial.

### API Props

| Prop | Tipo | Default | Descripción |
| --- | --- | --- | --- |
| **indeterminate** | boolean | false | Si es `true`, gira infinitamente. Si es `false`, muestra el porcentaje estático basado en `model-value`. |
| **model-value** | string/number | 0 | Porcentaje de llenado (0-100). |
| **size** | string/number | 'default' | Diámetro del círculo en píxeles (ej: `size="32"`). |
| **width** | string/number | 4 | Grosor del trazo del círculo. |
| **color** | string | undefined | Color del trazo. |
| **bg-color** | string | undefined | Color del trazo de fondo (la parte vacía del círculo). |

### Slots

| Slot | Descripción |
| --- | --- |
| **default** | Contenido dentro del círculo (usualmente texto con el porcentaje). Solo visible si el círculo es lo suficientemente grande. |

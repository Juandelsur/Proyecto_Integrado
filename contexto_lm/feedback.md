Aquí tienes el último bloque procesado para el **Contexto de Feedback e Interacción**.

Este bloque es crucial para la "Sensación de Usuario" (UX). Como desarrollador Backend, a menudo descuidamos esto, pero un buen feedback (Loading states, Toasts, Confirmaciones) es la diferencia entre que el usuario piense que la app "se colgó" o que está "procesando".

---

# v-btn, v-dialog, v-snackbar, v-alert, v-chip, v-skeleton-loader

### Ejemplo de Uso (Sinergia: Flujo de Acción Destructiva)

Este patrón es el "Estándar de Oro" para acciones críticas (Borrar, Archivar, Enviar):

1. Botón inicial.
2. Diálogo de confirmación (previene clics accidentales).
3. Estado de carga (`loading`) mientras el backend responde.
4. Feedback final (`snackbar` o `alert`) con el resultado.

```html
<script setup>
import { ref } from 'vue'

const dialog = ref(false)
const deleting = ref(false)
const snackbar = ref(false)
const errorAlert = ref(false)

// Simulación de una llamada al Backend
const deleteUser = async () => {
  deleting.value = true
  errorAlert.value = false // Resetear errores previos
  
  setTimeout(() => {
    deleting.value = false
    dialog.value = false // Cerrar diálogo
    snackbar.value = true // Mostrar toast de éxito
    // Si fallara: errorAlert.value = true
  }, 2000)
}
</script>

<template>
  <v-container>
    <v-btn 
      color="error" 
      prepend-icon="mdi-delete" 
      @click="dialog = true"
    >
      Eliminar Cuenta
    </v-btn>

    <v-dialog v-model="dialog" max-width="500" persistent>
      <v-card>
        <v-card-title class="headline">¿Estás seguro?</v-card-title>
        
        <v-card-text>
          Esta acción no se puede deshacer. El usuario:
          <v-chip color="primary" label class="ml-2">
            <v-icon start icon="mdi-account"></v-icon>
            admin_user
          </v-chip>
          será eliminado permanentemente.

          <v-alert
            v-if="errorAlert"
            type="error"
            title="Error de Servidor"
            text="No se pudo eliminar el usuario. Intente más tarde."
            class="mt-4"
            variant="tonal"
          ></v-alert>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="dialog = false" :disabled="deleting">
            Cancelar
          </v-btn>
          <v-btn 
            color="error" 
            variant="flat" 
            :loading="deleting" 
            @click="deleteUser"
          >
            Confirmar Eliminación
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-snackbar
      v-model="snackbar"
      timeout="3000"
      color="success"
      location="bottom right"
    >
      Usuario eliminado correctamente
      <template v-slot:actions>
        <v-btn variant="text" @click="snackbar = false">Cerrar</v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

```

---

# v-btn

El componente de interacción principal.

### API Props

| Prop | Tipo | Default | Descripción |
| --- | --- | --- | --- |
| **color** | string | undefined | Color del botón (ej: 'primary', 'error', 'success'). |
| **variant** | string | 'elevated' | `'elevated'` (sólido con sombra), `'flat'` (sólido sin sombra), `'tonal'` (fondo suave), `'text'` (solo texto), `'outlined'` (solo borde). |
| **size** | string | 'default' | `'x-small'`, `'small'`, `'default'`, `'large'`, `'x-large'`. |
| **loading** | boolean | false | **Vital para Backend:** Reemplaza el texto con un spinner y deshabilita el clic. |
| **disabled** | boolean | false | Deshabilita el botón visual y funcionalmente. |
| **icon** | boolean/string | false | Si es `true`, el botón es redondo. Si pasas un string (ej: `icon="mdi-plus"`), actúa como un botón de icono. |
| **prepend-icon** | string | undefined | Icono antes del texto. |
| **append-icon** | string | undefined | Icono después del texto. |
| **block** | boolean | false | Ocupa el 100% del ancho disponible (útil en móviles o diálogos). |

---

# v-dialog

Ventana modal que se superpone al contenido. Se usa para confirmaciones, formularios complejos o mostrar detalles sin salir de la página.

### API Props

| Prop | Tipo | Default | Descripción |
| --- | --- | --- | --- |
| **model-value** | boolean | false | (v-model) Controla si el diálogo está visible o no. |
| **persistent** | boolean | false | Si es `true`, el diálogo **NO** se cierra al hacer clic afuera. Obliga al usuario a tomar una acción (Aceptar/Cancelar). |
| **width / max-width** | string/number | undefined | Controla el ancho. Recomendado usar `max-width="500"` para diálogos de texto. |
| **scrollable** | boolean | false | Si el contenido es muy largo, permite scroll dentro del diálogo manteniendo el título y los botones fijos. |
| **fullscreen** | boolean | false | Ocupa toda la pantalla (útil para formularios masivos en móviles). |
| **transition** | string | 'dialog-transition' | Animación de entrada/salida. |

### Slots

| Slot | Descripción |
| --- | --- |
| **default** | El contenido del diálogo (usualmente un `v-card`). |
| **activator** | Slot especial para colocar el componente que abre el diálogo (evita usar una variable `ref` manual, aunque para lógica compleja es mejor usar `v-model`). |

---

# v-snackbar

Notificación temporal (Toast) que aparece usualmente en la parte inferior. No interrumpe al usuario.

### API Props

| Prop | Tipo | Default | Descripción |
| --- | --- | --- | --- |
| **model-value** | boolean | false | (v-model) Controla la visibilidad. |
| **timeout** | number | 5000 | Tiempo en milisegundos antes de cerrarse solo. `-1` para mantenerlo abierto. |
| **color** | string | undefined | Color de fondo (ej: 'success' para éxito, 'error' para fallos). |
| **location** | string | 'bottom' | `'top'`, `'bottom'`, `'top right'`, etc. |
| **vertical** | boolean | false | Apila el contenido verticalmente (útil si el mensaje es largo y hay botones). |

---

# v-alert

Componente para comunicar estados importantes de forma prominente en la interfaz.

### API Props

| Prop | Tipo | Default | Descripción |
| --- | --- | --- | --- |
| **type** | string | undefined | `'success'`, `'info'`, `'warning'`, `'error'`. Al usar esto, Vuetify pone automáticamente el icono y color estándar. |
| **title** | string | undefined | Título en negrita. |
| **text** | string | undefined | Cuerpo del mensaje. |
| **closable** | boolean | false | Añade una "X" para cerrar la alerta. |
| **variant** | string | 'flat' | `'tonal'` (recomendado para dashboards modernos), `'outlined'`, `'elevated'`. |
| **prominent** | boolean | false | Hace el icono más grande y llamativo. |
| **density** | string | 'default' | `'compact'` reduce el padding. |

---

# v-skeleton-loader

Placeholder animado que simula la estructura del contenido mientras se cargan los datos. Mejora la percepción de velocidad.

### API Props

| Prop | Tipo | Default | Descripción |
| --- | --- | --- | --- |
| **loading** | boolean | false | Si es `true`, muestra el esqueleto. Si es `false`, muestra el contenido del slot `default`. |
| **type** | string | 'ossein' | Define la estructura a simular. Puedes combinar tipos separados por coma: `'card'`, `'table'`, `'list-item-avatar'`, `'article'`, `'table-heading, table-row-divider, table-row'`. |
| **elevation** | string/number | undefined | Sombra del contenedor del loader. |

---

# v-chip

Etiqueta compacta para mostrar información de atributos, categorías o filtros.

### API Props

| Prop | Tipo | Default | Descripción |
| --- | --- | --- | --- |
| **color** | string | undefined | Color del chip. |
| **label** | boolean | false | Si es `true`, el chip es rectangular con bordes ligeramente redondeados (mejor para datos técnicos). Si es `false`, es completamente redondo (estilo píldora). |
| **closable** | boolean | false | Muestra una "X" para eliminar el chip (útil para filtros activos). |
| **variant** | string | 'tonal' | Estilo visual. |
| **size** | string | 'default' | `'x-small'`, `'small'` (útil dentro de tablas). |

---

# v-icon

Renderiza iconos de Material Design Icons (MDI).

### API Props

| Prop | Tipo | Default | Descripción |
| --- | --- | --- | --- |
| **icon** | string | undefined | El nombre del icono (ej: `mdi-home`). |
| **size** | string/number | 'default' | Tamaño del icono. |
| **color** | string | undefined | Color del icono. |
| **start / end** | boolean | false | Añade margen automático si se usa dentro de un botón (start=izquierda, end=derecha). |

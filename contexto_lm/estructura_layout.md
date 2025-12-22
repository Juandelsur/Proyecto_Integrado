Aquí tienes el bloque procesado. He agrupado todo bajo la lógica de "Layout Estructural" (The Skeleton), ya que estos componentes funcionan como el sistema circulatorio y óseo de tu aplicación. El ejemplo de código es un **Dashboard completo** para que la IA entienda la jerarquía exacta.

---

# v-app-bar, v-navigation-drawer, v-main, v-container, v-row, v-col, v-spacer

### Ejemplo de Uso (Sinergia: Dashboard Layout)

Este ejemplo muestra la estructura canónica de una aplicación Vuetify (App Bar + Drawer + Main + Grid System).

```html
<script setup>
import { ref } from 'vue'

const drawer = ref(true) // Controla la visibilidad del menú lateral
</script>

<template>
  <v-app>
    <v-app-bar color="primary" density="compact" elevation="2">
      <template v-slot:prepend>
        <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      </template>

      <v-app-bar-title>Panel de Administración</v-app-bar-title>

      <v-spacer></v-spacer> <template v-slot:append>
        <v-btn icon="mdi-dots-vertical"></v-btn>
      </template>
    </v-app-bar>

    <v-navigation-drawer v-model="drawer" location="start" width="256">
      </v-navigation-drawer>

    <v-main>
      <v-container fluid> <v-row dense> <v-col cols="12" md="4">
            <v-card>Estadística 1</v-card>
          </v-col>

          <v-col cols="12" md="4">
            <v-card>Estadística 2</v-card>
          </v-col>

          <v-col cols="12" md="4">
            <v-card>Estadística 3</v-card>
          </v-col>

        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

```

---

# v-container

El contenedor raíz para el contenido. Centra el contenido horizontalmente y proporciona padding.

### API Props

| Prop | Tipo | Default | Descripción |
| --- | --- | --- | --- |
| **fluid** | boolean | false | Elimina el ancho máximo (max-width), ocupando el 100% del viewport disponible. Ideal para Dashboards. |
| **tag** | string | 'div' | Etiqueta HTML personalizada para el componente. |

---

# v-row

Un contenedor flex (flexbox container) para `v-col`.

### API Props

| Prop | Tipo | Default | Descripción |
| --- | --- | --- | --- |
| **dense** | boolean | false | Reduce el espacio (gutter) entre `v-col` componentes. Hace la interfaz más compacta. |
| **no-gutters** | boolean | false | Elimina completamente el espacio entre columnas. |
| **align** | string | null | Alineación vertical (align-items). Opciones: `start`, `center`, `end`, `baseline`, `stretch`. |
| **justify** | string | null | Alineación horizontal (justify-content). Opciones: `start`, `center`, `end`, `space-between`, `space-around`. |
| **align-content** | string | null | Gestiona el espacio vertical si hay múltiples líneas. |

---

# v-col

Las columnas del grid system. Deben ser hijos directos de `v-row`.

### API Props

| Prop | Tipo | Default | Descripción |
| --- | --- | --- | --- |
| **cols** | string/number | false | Número de columnas por defecto (escala de 1 a 12). "auto" ajusta al contenido. |
| **sm, md, lg, xl, xxl** | string/number | false | Define el número de columnas (1-12) específicamente para ese breakpoint. (Ej: `md="6"` ocupa mitad de pantalla en tablets/laptops). |
| **offset** | string/number | null | Número de columnas vacías a la izquierda (offset) por defecto. |
| **offset-sm/md/lg...** | string/number | null | Offset específico por breakpoint. |
| **align-self** | string | null | Sobrescribe la alineación vertical para esta columna específica (`start`, `center`, `end`). |

---

# v-app-bar

La barra de herramientas superior, usada para navegación, títulos y acciones globales. Se coloca siempre fuera de `v-main`.

### API Props

| Prop | Tipo | Default | Descripción |
| --- | --- | --- | --- |
| **color** | string | undefined | Color de fondo (ej: 'primary', 'surface', '#FFF'). |
| **density** | string | 'default' | Altura de la barra: `'default'` (64px), `'prominent'` (128px), `'comfortable'`, `'compact'`. |
| **elevation** | string/number | undefined | Sombra (0-24). |
| **flat** | boolean | false | Elimina la sombra (box-shadow). |
| **scroll-behavior** | string | undefined | Acción al hacer scroll: `'hide'`, `'elevate'`, `'collapse'`, `'fade-image'`. |
| **border** | boolean | false | Añade un borde inferior. |

### Slots

| Slot | Descripción |
| --- | --- |
| **prepend** | Ubicación izquierda (generalmente para el icono del menú o botón "atrás"). |
| **title** | Contenido del título. |
| **default** | Contenido central. |
| **append** | Ubicación derecha (acciones, perfil de usuario, dots menu). |
| **extension** | Slot debajo del contenido principal (útil para tabs). |

---

# v-navigation-drawer

El panel de navegación lateral (sidebar). Puede ser permanente, temporal (overlay) o "rail" (iconos solo).

### API Props

| Prop | Tipo | Default | Descripción |
| --- | --- | --- | --- |
| **model-value** | boolean | null | Controla la visibilidad (v-model). |
| **location** | string | 'start' | Lado de la pantalla: `'start'` (izquierda), `'end'` (derecha), `'top'`, `'bottom'`. |
| **permanent** | boolean | false | Siempre visible, ignora el tamaño de pantalla. |
| **temporary** | boolean | false | Se comporta como un overlay con fondo oscuro (scrim). Ideal para móviles. |
| **rail** | boolean | null | Modo minimizado (ancho reducido, usualmente 56px). |
| **expand-on-hover** | boolean | false | Se expande al pasar el mouse si está en modo `rail`. |
| **width** | string/number | 256 | Ancho del drawer. |
| **scrim** | string/boolean | true | El fondo oscuro cuando es temporal. |
| **sticky** | boolean | false | Mantiene el drawer visible al hacer scroll. |

### Slots

| Slot | Descripción |
| --- | --- |
| **prepend** | Área superior (ej: Perfil de usuario). |
| **default** | Área central (Listas de navegación). |
| **append** | Área inferior (ej: Botón de cerrar sesión). |

---

# v-main

El componente crítico de layout. Calcula dinámicamente el espacio disponible restando el tamaño de `v-app-bar` y `v-navigation-drawer`. Todo el contenido de la página debe ir dentro de él.

### API Props

| Prop | Tipo | Default | Descripción |
| --- | --- | --- | --- |
| **scrollable** | boolean | false | Define si el contenido interno tiene su propio scroll independiente. |

---

# v-spacer

Componente utilitario flexbox. Ocupa todo el espacio disponible entre dos componentes.

### Ejemplo

`<logo /> <v-spacer /> <boton-perfil />` (El logo a la izquierda, el botón a la derecha extrema).

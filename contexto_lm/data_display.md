Aquí tienes el bloque procesado para el **Contexto de Visualización de Datos**.

Este es quizás el bloque más importante para un Backend Developer, porque aquí es donde "aterrizan" tus datos JSON. He puesto un énfasis especial en `v-data-table-server` y cómo mapear sus eventos a una llamada API estándar (tipo Django REST Framework).

---

# v-data-table-server

La herramienta definitiva para mostrar grandes volúmenes de datos paginados desde el backend. **No** descarga todo de golpe; pide página por página.

### Ejemplo de Uso (Sinergia: Tabla Server-Side con Card y Buscador)

Este patrón conecta `update:options` (que detecta cambios de página o reordenamiento) directamente con tu función de llamada al API.

```html
<script setup>
import { ref } from 'vue'

const items = ref([])
const loading = ref(false)
const totalItems = ref(0) // Vital para que la tabla calcule cuántas páginas existen
const search = ref('')

// Definición de columnas
const headers = [
  { title: 'Nombre', key: 'name', align: 'start' },
  { title: 'Email', key: 'email', align: 'start' },
  { title: 'Rol', key: 'role', sortable: false },
  { title: 'Acciones', key: 'actions', sortable: false, align: 'end' },
]

// Esta función se ejecuta automáticamente al montar, cambiar página o cambiar orden
const loadItems = async ({ page, itemsPerPage, sortBy }) => {
  loading.value = true
  
  // Transformar formato de Vuetify a formato Django/Backend
  // Vuetify sortBy es array: [{ key: 'name', order: 'desc' }]
  // Django espera: ordering=-name
  const orderParam = sortBy.length ? (sortBy[0].order === 'desc' ? '-' : '') + sortBy[0].key : null;
  
  try {
    // Simulación de fetch
    // const res = await api.get(`/users?page=${page}&page_size=${itemsPerPage}&ordering=${orderParam}&search=${search.value}`)
    // items.value = res.data.results
    // totalItems.value = res.data.count
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <v-card flat title="Gestión de Usuarios">
    <template v-slot:text>
      <v-text-field
        v-model="search"
        label="Buscar..."
        prepend-inner-icon="mdi-magnify"
        variant="outlined"
        density="compact"
        hide-details
        single-line
      ></v-text-field>
    </template>

    <v-data-table-server
      v-model:items-per-page="itemsPerPage"
      :headers="headers"
      :items="items"
      :items-length="totalItems"
      :loading="loading"
      :search="search"
      item-value="id"
      @update:options="loadItems"
    >
      <template v-slot:item.role="{ item }">
        <v-chip color="primary" size="small">{{ item.role }}</v-chip>
      </template>

      <template v-slot:item.actions="{ item }">
        <v-btn icon="mdi-pencil" size="small" variant="text"></v-btn>
      </template>
    </v-data-table-server>
  </v-card>
</template>

```

### API Props

| Prop | Tipo | Default | Descripción |
| --- | --- | --- | --- |
| **items** | array | [] | Los datos *actuales* de la página visible (no todos los datos de la DB). |
| **items-length** | number | undefined | **OBLIGATORIO**. El total de registros en la base de datos (obtenido del `count` de Django). Sin esto, la paginación no funciona. |
| **headers** | array | undefined | Array de objetos `{ title, key, align, sortable }` que define las columnas. |
| **loading** | boolean | false | Muestra una barra de progreso lineal arriba de la tabla. |
| **items-per-page** | number | 10 | Cuántas filas mostrar por página. |
| **page** | number | 1 | La página actual (1-indexed). |
| **sort-by** | array | [] | Estado actual del ordenamiento. |
| **search** | string | undefined | String de búsqueda. Nota: En server-side, debes pasar esto manualmente a tu API. |
| **multi-sort** | boolean | false | Permite ordenar por múltiples columnas a la vez. |
| **hover** | boolean | false | Resalta la fila cuando el mouse pasa por encima. |
| **density** | string | 'default' | Altura de filas: `'default'`, `'comfortable'`, `'compact'`. |

### Slots

| Slot | Descripción |
| --- | --- |
| **item.[key]** | Permite personalizar una celda específica. Ej: `item.status` para poner un icono en vez de texto. Recibe el objeto `{ item }`. |
| **top** | Espacio arriba de la tabla (ideal para filtros o botones de "Nuevo"). |
| **no-data** | Contenido a mostrar si el array `items` está vacío. |

### Eventos Clave

| Evento | Descripción |
| --- | --- |
| **update:options** | **EL MÁS IMPORTANTE**. Se dispara cuando cambia CUALQUIER cosa (página, items por página, orden). Te da un objeto `{ page, itemsPerPage, sortBy, groupBy, search }`. |

---

# v-card

El contenedor universal. En Material Design 3 (Vuetify 3), las cartas son más planas por defecto. Se usan para agrupar contenido relacionado.

### API Props

| Prop | Tipo | Default | Descripción |
| --- | --- | --- | --- |
| **title** | string | undefined | Título principal de la tarjeta. |
| **subtitle** | string | undefined | Subtítulo grisáceo. |
| **text** | string | undefined | Contenido del cuerpo (o usar el slot default). |
| **variant** | string | 'elevated' | `'elevated'` (sombra), `'flat'` (plano), `'outlined'` (borde), `'tonal'` (relleno suave). |
| **loading** | boolean | false | Muestra una barra de carga en el borde superior. |
| **elevation** | string/number | undefined | Nivel de sombra (0-24). |
| **disabled** | boolean | false | Reduce la opacidad y bloquea interacciones. |
| **link** | boolean | undefined | Hace que toda la tarjeta sea cliqueable (efecto hover). |

---

# v-list, v-list-item

Utilizados para: Menús laterales (Navigation Drawer), Listas de Configuración, o filas de detalles simples.

### Ejemplo de Uso (Lista de Detalles)

```html
<v-card width="300">
  <v-list lines="two"> <v-list-subheader>Ajustes</v-list-subheader>
    
    <v-list-item
      title="Notificaciones"
      subtitle="Gestionar alertas de correo"
      prepend-icon="mdi-bell"
      value="notifications"
    >
      <template v-slot:append>
        <v-switch color="primary" inset></v-switch>
      </template>
    </v-list-item>

    <v-list-item
      title="Cuenta"
      subtitle="Actualizar perfil"
      prepend-icon="mdi-account"
      link
    ></v-list-item>
  </v-list>
</v-card>

```

### API Props (v-list)

| Prop | Tipo | Default | Descripción |
| --- | --- | --- | --- |
| **lines** | string | 'one' | Altura de los items: `'one'`, `'two'` (título + subtítulo), `'three'`. |
| **nav** | boolean | false | Estilo especial para menús de navegación (bordes redondeados, más compacto). |
| **density** | string | 'default' | Espaciado vertical. |
| **select-strategy** | string | 'single-leaf' | Cómo se comportan las selecciones (single, multiple). |

### API Props (v-list-item)

| Prop | Tipo | Default | Descripción |
| --- | --- | --- | --- |
| **title** | string | undefined | Texto principal. |
| **subtitle** | string | undefined | Texto secundario (requiere `lines="two"` en el padre). |
| **prepend-icon** | string | undefined | Icono a la izquierda. |
| **append-icon** | string | undefined | Icono a la derecha (o usar slot `append` para botones). |
| **active** | boolean | undefined | Fuerza el estado "seleccionado". |
| **link** | boolean | undefined | Hace que el item sea cliqueable y tenga efecto hover. |
| **value** | any | undefined | El valor que retornará el `v-list` si se selecciona este item. |
| **to** | string | undefined | Integra Vue Router (como un `<router-link>`). |

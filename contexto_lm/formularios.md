Aquí tienes el bloque procesado para el **Contexto de Formularios**. He diseñado el ejemplo de sinergia simulando un "Formulario de Creación de Usuario", que es el caso de uso más común donde conviven todos estos elementos.

He limpiado agresivamente las tablas para dejar solo lo que usará `Cursor` para construir tu Dashboard (ignorando props oscuras de diseño que casi nunca se tocan manualmente).

---

# v-form, v-text-field, v-select, v-autocomplete, v-checkbox, v-switch

### Ejemplo de Uso (Sinergia: Formulario Completo)

Este ejemplo muestra cómo `v-form` orquesta la validación de múltiples tipos de inputs. Nota el uso de `variant="outlined"` y `density="compact"`, que es el estándar estético para Dashboards de administración modernos.

```html
<script setup>
import { ref } from 'vue'

const valid = ref(false)
const form = ref(null)

// Datos del formulario
const userData = ref({
  name: '',
  email: '',
  role: null,
  city: null,
  notifications: true,
  terms: false
})

// Opciones simuladas
const roles = [
  { title: 'Administrador', value: 'admin' },
  { title: 'Editor', value: 'editor' }
]
const cities = ['Temuco', 'Santiago', 'Valparaíso']

// Reglas de validación simples
const rules = {
  required: value => !!value || 'Este campo es obligatorio',
  email: value => /.+@.+\..+/.test(value) || 'E-mail debe ser válido',
}

const submit = async () => {
  const { valid } = await form.value.validate()
  if (valid) {
    console.log("Enviando al Backend:", userData.value)
  }
}
</script>

<template>
  <v-card class="pa-4">
    <v-form ref="form" v-model="valid" @submit.prevent="submit">
      
      <v-row>
        <v-col cols="12" md="6">
          <v-text-field
            v-model="userData.name"
            label="Nombre Completo"
            :rules="[rules.required]"
            variant="outlined"
            density="compact"
            prepend-inner-icon="mdi-account"
          ></v-text-field>
        </v-col>

        <v-col cols="12" md="6">
          <v-select
            v-model="userData.role"
            :items="roles"
            item-title="title"
            item-value="value"
            label="Rol de Usuario"
            variant="outlined"
            density="compact"
            :rules="[rules.required]"
          ></v-select>
        </v-col>

        <v-col cols="12">
          <v-autocomplete
            v-model="userData.city"
            :items="cities"
            label="Buscar Ciudad"
            variant="outlined"
            density="compact"
            clearable
            no-data-text="No se encontraron ciudades"
          ></v-autocomplete>
        </v-col>

        <v-col cols="12" md="6">
          <v-switch
            v-model="userData.notifications"
            label="Recibir notificaciones por correo"
            color="primary"
            inset
            hide-details
          ></v-switch>
        </v-col>

        <v-col cols="12" md="6">
          <v-checkbox
            v-model="userData.terms"
            label="Acepto los términos y condiciones"
            :rules="[rules.required]"
            color="primary"
            hide-details
          ></v-checkbox>
        </v-col>
      </v-row>

      <v-btn type="submit" color="primary" :disabled="!valid" class="mt-4">
        Guardar Usuario
      </v-btn>
    </v-form>
  </v-card>
</template>

```

---

# v-form

Contenedor lógico que provee validación a todos los inputs hijos.

### API Props

| Prop | Tipo | Default | Descripción |
| --- | --- | --- | --- |
| **model-value** | boolean | null | `v-model`. Es `true` si todos los inputs dentro son válidos. |
| **fast-fail** | boolean | false | Detiene la validación apenas encuentra el primer error (ahorra recursos). |
| **validate-on** | string | 'input' | Cuándo validar: `'input'`, `'blur'`, `'submit'`, `'lazy'`. |
| **disabled** | boolean | false | Deshabilita todos los inputs dentro del formulario. |
| **readonly** | boolean | false | Pone todos los inputs en modo solo lectura. |

### Métodos Expuestos (Exposed)

*Accesibles vía ref (ej: `form.value.validate()`)*

* **validate()**: Ejecuta la validación de todos los campos. Retorna una promesa `{ valid: boolean, errors: [] }`.
* **reset()**: Limpia los valores y los errores.
* **resetValidation()**: Limpia solo los errores, mantiene los valores escritos.

---

# v-text-field

El input estándar para texto, números, contraseñas, etc.

### API Props

| Prop | Tipo | Default | Descripción |
| --- | --- | --- | --- |
| **label** | string | undefined | El texto flotante que describe el campo. |
| **variant** | string | 'filled' | Estilo visual: `'outlined'` (Recomendado Dashboard), `'filled'`, `'underlined'`, `'plain'`. |
| **density** | string | 'default' | Altura: `'default'`, `'comfortable'`, `'compact'` (Recomendado Dashboard). |
| **rules** | array | [] | Array de funciones para validación. Si retorna `true` pasa, si retorna `string` muestra el error. |
| **type** | string | 'text' | Tipo HTML: `'text'`, `'password'`, `'number'`, `'email'`. |
| **clearable** | boolean | false | Muestra un icono (X) para borrar el contenido. |
| **prepend-inner-icon** | string | undefined | Icono dentro del input, a la izquierda (ej: lupa, usuario). |
| **append-inner-icon** | string | undefined | Icono dentro del input, a la derecha (ej: ojo password). |
| **hide-details** | boolean/'auto' | false | Oculta el espacio reservado para errores/hints. Úsalo en 'auto' para tablas densas. |
| **hint** | string | undefined | Texto de ayuda debajo del input. |

---

# v-select

Dropdown para seleccionar opciones de una lista predefinida. No permite buscar (para eso usa Autocomplete).

### API Props

| Prop | Tipo | Default | Descripción |
| --- | --- | --- | --- |
| **items** | array | [] | Array de strings u objetos con las opciones. |
| **item-title** | string | 'title' | La propiedad del objeto a mostrar como texto (ej: 'nombre_producto'). |
| **item-value** | string | 'value' | La propiedad del objeto a guardar en el v-model (ej: 'id_producto'). |
| **multiple** | boolean | false | Permite seleccionar varios items. |
| **chips** | boolean | false | Muestra las selecciones como "chips" (etiquetas) en vez de texto separado por comas. |
| **return-object** | boolean | false | Si es true, el v-model guarda el objeto completo, no solo el `item-value`. |
| **variant / density** | string | - | Igual que v-text-field. |

---

# v-autocomplete

Similar a v-select, pero permite al usuario escribir para filtrar o buscar remotamente (API).

### API Props

| Prop | Tipo | Default | Descripción |
| --- | --- | --- | --- |
| **items** | array | [] | Igual que v-select. |
| **auto-select-first** | boolean | false | Resalta automáticamente la primera coincidencia al buscar. |
| **loading** | boolean | false | Muestra una barra de carga (útil para búsquedas asíncronas en API). |
| **no-data-text** | string | - | Texto a mostrar si la búsqueda no arroja resultados. |
| **search** | string | undefined | (v-model:search) Variable para capturar lo que el usuario está escribiendo mientras busca.Vital para búsquedas remotas en Django. Usar junto con @update:search |
| **clear-on-select** | boolean | false | Borra el texto de búsqueda al seleccionar un item (útil en selección múltiple). |

---

# v-checkbox

Input booleano para selecciones binarias (Sí/No).

### API Props

| Prop | Tipo | Default | Descripción |
| --- | --- | --- | --- |
| **label** | string | undefined | Texto junto a la casilla. |
| **model-value** | any | undefined | El valor enlazado. |
| **false-value** | any | undefined | Valor a enviar cuando no está marcado (útil si el backend espera 0 en vez de false). |
| **true-value** | any | undefined | Valor a enviar cuando está marcado (útil si el backend espera 1 en vez de true). |
| **indeterminate** | boolean | false | Estado visual "ni marcado ni desmarcado" (guión). |

---

# v-switch

Variante visual del checkbox, estilo interruptor de encendido/apagado.

### API Props

| Prop | Tipo | Default | Descripción |
| --- | --- | --- | --- |
| **inset** | boolean | false | Hace que el botón (thumb) esté dentro de la barra (track). Estilo iOS/Moderno. |
| **color** | string | undefined | Color cuando está activo (ej: 'primary', 'success'). |
| **loading** | boolean | false | Muestra un spinner de carga dentro del switch. |
| **flat** | boolean | false | Quita la sombra del botón circular. |

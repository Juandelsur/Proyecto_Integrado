# REGLAS DE ORO: FRONTEND (VUE 3 + VUETIFY + DJANGO)
> Este archivo define las restricciones técnicas obligatorias para generar código en este proyecto.

## 1. COMPOSITION API ESTRICTA
- Usa SIEMPRE `<script setup>`.
- **PROHIBIDO** usar Options API (`data()`, `methods: {}`, `mounted()`).
- Usa `const` y `ref`/`reactive` para el estado.
- Para llamadas a API, usa `async/await` dentro de bloques `try/catch`.

## 2. SINTAXIS VUETIFY 3 (NO ALUCINAR V2)
Las IAs suelen confundir versiones. Reglas absolutas:
- **Grid System:** Solo existen `<v-row>` y `<v-col cols="12" md="6">`. (PROHIBIDO: `<v-flex>`, `xs12`, `<v-layout>`).
- **Inputs:** Usa `variant="outlined"` y `density="compact"`. (PROHIBIDO: `outlined` como booleano, `dense` como booleano).
- **Tablas:** Usa `<v-data-table-server>`. La paginación es `v-model:items-per-page`. (PROHIBIDO: `pagination.sync`).
- **Iconos:** Usa `mdi-` (ej: `prepend-icon="mdi-home"`). No uses clases `fa fa-home`.

## 3. INTEGRACIÓN V-DATA-TABLE-SERVER CON DJANGO
Al implementar tablas server-side, transforma SIEMPRE los parámetros de Vuetify a Django así:
- **Paginación:** `page` (Vuetify) -> `page` (Django).
- **Límite:** `itemsPerPage` (Vuetify) -> `page_size` (Django).
- **Ordenamiento:**
  - Vuetify entrega Array: `[{ key: 'name', order: 'desc' }]`
  - Django espera String: `ordering: '-name'` (Guión para descendente).
- **Búsqueda:** `search` -> `search` (Django Filter).

## 4. SEGURIDAD DE RENDERIZADO (Null Safety)
- El backend es asíncrono. **Nunca asumas que los datos existen al montar el componente.**
- Usa Optional Chaining: `item?.cliente?.nombre` en lugar de `item.cliente.nombre`.
- Usa `<v-skeleton-loader>` o `v-if="!loading"` para evitar pantallas blancas mientras carga.

## 5. ESTILOS Y COLORES
- No inventes CSS (`style="..."`).
- Usa las clases de utilidad de Vuetify: `class="mb-4"`, `class="text-h5"`, `class="d-flex justify-center"`.
- Colores: Usa props `color="primary"` o `color="error"`. No uses Hexadecimales directos.

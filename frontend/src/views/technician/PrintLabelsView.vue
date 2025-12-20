<template>
  <div class="print-labels-view">
    <!-- TABS DE SELECCIÓN DE ACTIVOS -->
    <v-card class="mb-4">
      <v-tabs v-model="activeTab" bg-color="primary" dark>
        <v-tab value="activos">
          <v-icon start>mdi-checkbox-multiple-marked</v-icon>
          Por Activos
        </v-tab>
        <v-tab value="ubicaciones">
          <v-icon start>mdi-map-marker-multiple</v-icon>
          Por Ubicaciones
        </v-tab>
        <v-tab value="manual">
          <v-icon start>mdi-keyboard</v-icon>
          Manual
        </v-tab>
      </v-tabs>

      <v-window v-model="activeTab">
        <!-- TAB 1: POR ACTIVOS -->
        <v-window-item value="activos">
          <v-card-text>
            <!-- Filtros -->
            <v-row class="mb-4">
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="filtros.busqueda"
                  label="Buscar activo"
                  prepend-inner-icon="mdi-magnify"
                  variant="outlined"
                  density="comfortable"
                  clearable
                  hint="Buscar por código, marca, modelo o número de serie"
                  persistent-hint
                ></v-text-field>
              </v-col>

              <v-col cols="12" sm="6" md="3">
                <v-select
                  v-model="filtros.marca"
                  :items="marcasDisponibles"
                  label="Marca"
                  variant="outlined"
                  density="comfortable"
                  clearable
                ></v-select>
              </v-col>

              <v-col cols="12" sm="6" md="3">
                <v-select
                  v-model="filtros.tipoEquipo"
                  :items="tiposEquipo"
                  item-title="nombre_tipo"
                  item-value="id"
                  label="Tipo de Equipo"
                  variant="outlined"
                  density="comfortable"
                  clearable
                ></v-select>
              </v-col>

              <v-col cols="12" md="6">
                <v-select
                  v-model="filtros.ubicacion"
                  :items="ubicaciones"
                  item-title="nombre_ubicacion"
                  item-value="id"
                  label="Ubicación Actual"
                  variant="outlined"
                  density="comfortable"
                  clearable
                ></v-select>
              </v-col>

              <v-col cols="12" md="6">
                <v-btn
                  color="secondary"
                  variant="outlined"
                  block
                  @click="limpiarFiltros"
                >
                  <v-icon start>mdi-filter-off</v-icon>
                  Limpiar Filtros
                </v-btn>
              </v-col>
            </v-row>

            <!-- Resumen y Selección -->
            <v-card variant="tonal" color="primary" class="mb-4" v-if="activosFiltrados.length > 0">
              <v-card-text>
                <v-row align="center">
                  <v-col cols="12" md="8">
                    <div class="d-flex align-center gap-3">
                      <v-chip color="primary" variant="elevated">
                        {{ activosSeleccionados.length }} de {{ activosFiltrados.length }} seleccionados
                      </v-chip>
                      
                      <v-checkbox
                        v-model="seleccionarTodosActivos"
                        label="Seleccionar todos"
                        hide-details
                        @update:model-value="toggleSeleccionarTodosActivos"
                      ></v-checkbox>
                    </div>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>

            <!-- Tabla de Activos -->
            <v-data-table
              v-model="activosSeleccionados"
              :headers="headersActivos"
              :items="activosFiltrados"
              :loading="loadingActivos"
              show-select
              item-value="id"
              class="elevation-1"
              :items-per-page="10"
            >
              <template v-slot:loading>
                <v-skeleton-loader type="table-row@10"></v-skeleton-loader>
              </template>

              <template v-slot:no-data>
                <div class="text-center py-8">
                  <v-icon size="64" color="grey">mdi-package-variant</v-icon>
                  <p class="text-h6 mt-4">No hay activos disponibles</p>
                </div>
              </template>

              <template v-slot:item.nombre="{ item }">
                <span class="font-weight-medium">{{ item.marca }} {{ item.modelo }}</span>
              </template>

              <template v-slot:item.ubicacion="{ item }">
                <v-chip size="small" color="info" variant="tonal">
                  {{ item.ubicacion_actual?.nombre_ubicacion || 'Sin ubicación' }}
                </v-chip>
              </template>

              <template v-slot:item.estado="{ item }">
                <v-chip 
                  size="small" 
                  :color="getEstadoColor(item.estado?.nombre_estado)"
                  variant="tonal"
                >
                  {{ item.estado?.nombre_estado || 'Sin estado' }}
                </v-chip>
              </template>
            </v-data-table>

            <v-card-actions class="mt-4">
              <v-spacer></v-spacer>
              <v-btn
                color="primary"
                size="large"
                :disabled="activosSeleccionados.length === 0"
                @click="agregarSeleccionadosACola"
              >
                <v-icon start>mdi-plus-circle</v-icon>
                Agregar {{ activosSeleccionados.length }} Seleccionados a Cola
              </v-btn>
            </v-card-actions>
          </v-card-text>
        </v-window-item>

        <!-- TAB 2: POR UBICACIONES -->
        <v-window-item value="ubicaciones">
          <v-card-text>
            <!-- Filtros de Ubicación -->
            <v-row class="mb-4">
              <v-col cols="12" md="4">
                <v-select
                  v-model="filtros.departamento"
                  :items="departamentos"
                  item-title="nombre_departamento"
                  item-value="id"
                  label="Departamento"
                  variant="outlined"
                  density="comfortable"
                  clearable
                  prepend-inner-icon="mdi-office-building"
                  @update:model-value="onDepartamentoChange"
                ></v-select>
              </v-col>

              <v-col cols="12" md="4">
                <v-select
                  v-model="filtros.ubicacion"
                  :items="ubicacionesFiltradas"
                  item-title="nombre_ubicacion"
                  item-value="id"
                  label="Ubicación"
                  variant="outlined"
                  density="comfortable"
                  clearable
                  prepend-inner-icon="mdi-map-marker"
                  :disabled="!filtros.departamento"
                  @update:model-value="cargarActivosPorUbicacion"
                >
                  <template v-slot:prepend-item>
                    <v-list-item
                      title="Todas las ubicaciones"
                      @click="seleccionarTodasLasUbicaciones"
                    >
                      <template v-slot:prepend>
                        <v-icon>mdi-select-all</v-icon>
                      </template>
                    </v-list-item>
                    <v-divider class="mb-2"></v-divider>
                  </template>
                </v-select>
              </v-col>

              <v-col cols="12" md="4">
                <v-text-field
                  v-model="filtros.busquedaActivo"
                  label="Buscar activo en ubicación"
                  prepend-inner-icon="mdi-magnify"
                  variant="outlined"
                  density="comfortable"
                  clearable
                  :disabled="!filtros.ubicacion && activosPorUbicacion.length === 0"
                ></v-text-field>
              </v-col>
            </v-row>

            <!-- Resumen y Selección de Activos por Ubicación -->
            <v-card variant="tonal" color="success" class="mb-4" v-if="activosPorUbicacionFiltrados.length > 0">
              <v-card-text>
                <v-row align="center">
                  <v-col cols="12" md="8">
                    <div class="d-flex align-center gap-3">
                      <v-chip color="success" variant="elevated">
                        {{ activosPorUbicacionSeleccionados.length }} de {{ activosPorUbicacionFiltrados.length }} seleccionados
                      </v-chip>
                      
                      <v-checkbox
                        v-model="seleccionarTodosUbicacion"
                        label="Seleccionar todos"
                        hide-details
                        @update:model-value="toggleSeleccionarTodosUbicacion"
                      ></v-checkbox>
                    </div>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>

            <!-- Mensaje cuando no hay ubicación seleccionada -->
            <v-alert
              v-if="!filtros.ubicacion && activosPorUbicacion.length === 0"
              type="info"
              variant="tonal"
              class="mb-4"
            >
              <v-icon start>mdi-information</v-icon>
              Selecciona un departamento y una ubicación para ver los activos disponibles.
            </v-alert>

            <!-- Loading State -->
            <div v-if="loadingActivosUbicacion" class="loading-container">
              <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
              <p class="mt-3 text-h6">Cargando activos...</p>
            </div>

            <!-- Lista de Activos por Ubicación -->
            <v-card v-else-if="activosPorUbicacionFiltrados.length > 0">
              <v-card-title class="text-h6 font-weight-bold d-flex justify-space-between">
                <span>Activos en Ubicación</span>
                <span class="text-subtitle-2 text-grey">{{ activosPorUbicacionFiltrados.length }} activos</span>
              </v-card-title>

              <v-divider></v-divider>

              <v-list>
                <v-list-item
                  v-for="activo in activosPorUbicacionFiltrados"
                  :key="activo.id"
                  :value="activo.id"
                >
                  <template v-slot:prepend>
                    <v-checkbox
                      :model-value="isActivoUbicacionSeleccionado(activo.id)"
                      @update:model-value="toggleActivoUbicacion(activo)"
                      hide-details
                    ></v-checkbox>
                  </template>

                  <v-list-item-title class="font-weight-medium">
                    {{ activo.marca }} {{ activo.modelo }}
                  </v-list-item-title>

                  <v-list-item-subtitle>
                    <div class="d-flex align-center gap-2 flex-wrap mt-1">
                      <v-chip size="small" variant="tonal">
                        {{ activo.codigo_inventario }}
                      </v-chip>
                      <v-chip 
                        size="small" 
                        :color="getEstadoColor(activo.estado?.nombre_estado)"
                        variant="tonal"
                      >
                        {{ activo.estado?.nombre_estado || 'Sin estado' }}
                      </v-chip>
                    </div>
                  </v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </v-card>

            <!-- Empty State -->
            <v-card v-else-if="filtros.ubicacion">
              <v-card-text class="text-center py-8">
                <v-icon size="64" color="grey-lighten-1">mdi-inbox</v-icon>
                <p class="text-h6 mt-4">No hay activos en esta ubicación</p>
                <p class="text-body-2 text-grey">Intenta seleccionar otra ubicación</p>
              </v-card-text>
            </v-card>

            <v-card-actions class="mt-4" v-if="activosPorUbicacionSeleccionados.length > 0">
              <v-spacer></v-spacer>
              <v-btn
                color="success"
                size="large"
                @click="agregarActivosUbicacionACola"
              >
                <v-icon start>mdi-plus-circle</v-icon>
                Agregar {{ activosPorUbicacionSeleccionados.length }} Activos a Cola
              </v-btn>
            </v-card-actions>
          </v-card-text>
        </v-window-item>

        <!-- TAB 3: MANUAL -->
        <v-window-item value="manual">
          <v-card-text>
            <v-alert type="info" variant="tonal" class="mb-4">
              <v-icon start>mdi-information</v-icon>
              Ingresa los códigos de inventario manualmente. Presiona Enter después de cada código.
            </v-alert>

            <v-combobox
              v-model="codigosManuales"
              label="Códigos de Inventario"
              prepend-inner-icon="mdi-barcode"
              variant="outlined"
              chips
              multiple
              closable-chips
              hint="Escribe un código y presiona Enter. Ejemplo: INV-25-A1B2C3"
              persistent-hint
            ></v-combobox>

            <v-card-actions class="mt-4">
              <v-spacer></v-spacer>
              <v-btn
                color="error"
                variant="outlined"
                @click="codigosManuales = []"
                :disabled="codigosManuales.length === 0"
              >
                <v-icon start>mdi-delete</v-icon>
                Limpiar
              </v-btn>
              <v-btn
                color="primary"
                size="large"
                :disabled="codigosManuales.length === 0"
                @click="agregarCodigosManuales"
              >
                <v-icon start>mdi-plus-circle</v-icon>
                Agregar {{ codigosManuales.length }} Códigos
              </v-btn>
            </v-card-actions>
          </v-card-text>
        </v-window-item>
      </v-window>
    </v-card>

    <!-- COLA DE IMPRESIÓN -->
    <v-card v-if="colaImpresion.length > 0" class="mb-4">
      <v-card-title class="d-flex align-center">
        <v-icon start color="success">mdi-printer-check</v-icon>
        Cola de Impresión ({{ colaImpresion.length }} activos)
        <v-spacer></v-spacer>
        <v-btn
          color="error"
          variant="text"
          size="small"
          @click="limpiarCola"
        >
          <v-icon start>mdi-delete-sweep</v-icon>
          Limpiar Cola
        </v-btn>
      </v-card-title>

      <v-card-text>
        <v-chip-group column>
          <v-chip
            v-for="activo in colaImpresion"
            :key="activo.id"
            closable
            @click:close="removerDeCola(activo.id)"
            color="primary"
            variant="outlined"
          >
            {{ activo.codigo_inventario }} - {{ activo.marca }} {{ activo.modelo }}
          </v-chip>
        </v-chip-group>
      </v-card-text>
    </v-card>

    <!-- BOTÓN FLOTANTE DE VISTA PREVIA -->
    <v-btn
      v-if="colaImpresion.length > 0"
      class="fab-preview"
      color="success"
      size="x-large"
      elevation="8"
      @click="abrirVistaPrevia"
    >
      <v-icon start>mdi-printer-eye</v-icon>
      Vista Previa / Imprimir ({{ colaImpresion.length }})
    </v-btn>

    <!-- DIÁLOGO DE VISTA PREVIA E IMPRESIÓN -->
    <v-dialog
      v-model="dialogVistaPrevia"
      fullscreen
      transition="dialog-bottom-transition"
    >
      <v-card>
        <v-toolbar color="primary" dark>
          <v-btn icon @click="cerrarVistaPrevia">
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-toolbar-title>Vista Previa de Etiquetas ({{ colaImpresion.length }} activos)</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="imprimirEtiquetas">
            <v-icon start>mdi-printer</v-icon>
            Imprimir Ahora
          </v-btn>
        </v-toolbar>

        <v-card-text class="pa-4">
          <!-- Área de Impresión -->
          <div id="print-area" class="print-container">
            <div
              v-for="activo in colaImpresion"
              :key="activo.id"
              class="etiqueta-card"
            >
              <!-- Contenido de la Etiqueta -->
              <div class="etiqueta-content">
                <!-- Izquierda: Nombre del Activo (70%) -->
                <div class="etiqueta-nombre">
                  <span class="nombre-text">{{ activo.marca }} {{ activo.modelo }}</span>
                </div>

                <!-- Derecha: QR + Código Vertical (30%) -->
                <div class="etiqueta-qr-section">
                  <!-- QR Code -->
                  <div class="qr-container">
                    <img
                      v-if="activo.qrDataUrl"
                      :src="activo.qrDataUrl"
                      alt="QR Code"
                      class="qr-image"
                    />
                    <div v-else class="qr-placeholder">
                      <v-icon size="40">mdi-qrcode</v-icon>
                    </div>
                  </div>

                  <!-- Código Vertical -->
                  <div class="codigo-vertical">
                    <span>{{ activo.codigo_inventario }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </v-card-text>
      </v-card>
    </v-dialog>

    <!-- SNACKBAR -->
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="3000"
    >
      {{ snackbar.text }}
    </v-snackbar>
  </div>
</template>

<script setup>
/**
 * ============================================================================
 * PRINT LABELS VIEW - IMPRESIÓN DE ETIQUETAS QR
 * ============================================================================
 *
 * Vista mejorada con búsqueda por ubicación desde el backend.
 * Tres modos de selección: Por Activos, Por Ubicaciones, Manual.
 * Genera etiquetas con diseño industrial (3 por fila) listas para impresión.
 */

import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/services/api'
import QRCode from 'qrcode'

// ============================================================================
// COMPOSABLES
// ============================================================================

const router = useRouter()

// ============================================================================
// STATE - TABS Y FILTROS
// ============================================================================

const activeTab = ref('ubicaciones')

const filtros = ref({
  busqueda: '',
  marca: null,
  tipoEquipo: null,
  ubicacion: null,
  departamento: null,
  busquedaUbicacion: '',
  busquedaActivo: ''
})

// ============================================================================
// STATE - DATOS DE LA API
// ============================================================================

const activos = ref([])
const ubicaciones = ref([])
const departamentos = ref([])
const tiposEquipo = ref([])
const activosPorUbicacion = ref([])

const loadingActivos = ref(false)
const loadingUbicaciones = ref(false)
const loadingActivosUbicacion = ref(false)

// ============================================================================
// STATE - SELECCIÓN Y COLA
// ============================================================================

const activosSeleccionados = ref([])
const activosPorUbicacionSeleccionados = ref([])
const codigosManuales = ref([])
const colaImpresion = ref([])

const seleccionarTodosActivos = ref(false)
const seleccionarTodosUbicacion = ref(false)

// ============================================================================
// STATE - VISTA PREVIA
// ============================================================================

const dialogVistaPrevia = ref(false)

// ============================================================================
// STATE - NOTIFICACIONES
// ============================================================================

const snackbar = ref({
  show: false,
  text: '',
  color: 'success'
})

// ============================================================================
// COMPUTED - HEADERS DE TABLAS
// ============================================================================

const headersActivos = computed(() => [
  { title: 'Nombre', key: 'nombre', sortable: true },
  { title: 'Código', key: 'codigo_inventario', sortable: true },
  { title: 'Marca', key: 'marca', sortable: true },
  { title: 'Ubicación', key: 'ubicacion', sortable: false },
  { title: 'Estado', key: 'estado', sortable: false }
])

// ============================================================================
// COMPUTED - FILTROS
// ============================================================================

const activosFiltrados = computed(() => {
  let resultado = activos.value

  // Filtro por búsqueda de texto
  if (filtros.value.busqueda) {
    const termino = filtros.value.busqueda.toLowerCase()
    resultado = resultado.filter(activo => {
      return (
        activo.codigo_inventario?.toLowerCase().includes(termino) ||
        activo.marca?.toLowerCase().includes(termino) ||
        activo.modelo?.toLowerCase().includes(termino) ||
        activo.numero_serie?.toLowerCase().includes(termino)
      )
    })
  }

  // Filtro por marca
  if (filtros.value.marca) {
    resultado = resultado.filter(a => a.marca === filtros.value.marca)
  }

  // Filtro por tipo de equipo
  if (filtros.value.tipoEquipo) {
    resultado = resultado.filter(a => a.tipo?.id === filtros.value.tipoEquipo)
  }

  // Filtro por ubicación
  if (filtros.value.ubicacion) {
    resultado = resultado.filter(a => a.ubicacion_actual?.id === filtros.value.ubicacion)
  }

  return resultado
})

const ubicacionesFiltradas = computed(() => {
  if (!filtros.value.departamento) return []
  
  return ubicaciones.value.filter(
    ub => ub.departamento?.id === filtros.value.departamento
  )
})

const activosPorUbicacionFiltrados = computed(() => {
  let resultado = activosPorUbicacion.value

  // Filtrar por búsqueda de texto
  if (filtros.value.busquedaActivo) {
    const termino = filtros.value.busquedaActivo.toLowerCase()
    resultado = resultado.filter(activo => {
      return (
        activo.codigo_inventario?.toLowerCase().includes(termino) ||
        activo.marca?.toLowerCase().includes(termino) ||
        activo.modelo?.toLowerCase().includes(termino) ||
        activo.numero_serie?.toLowerCase().includes(termino)
      )
    })
  }

  return resultado
})

const marcasDisponibles = computed(() => {
  const marcas = [...new Set(activos.value.map(a => a.marca).filter(Boolean))]
  return marcas.sort()
})

// ============================================================================
// MÉTODOS - API
// ============================================================================

async function fetchActivos() {
  loadingActivos.value = true
  try {
    const response = await apiClient.get('/api/activos/', {
      params: { page_size: 1000 }
    })
    activos.value = Array.isArray(response.data) 
      ? response.data 
      : response.data.results || []
    
    console.log(`✅ Cargados ${activos.value.length} activos`)
  } catch (error) {
    console.error('Error al cargar activos:', error)
    mostrarNotificacion('Error al cargar activos', 'error')
  } finally {
    loadingActivos.value = false
  }
}

async function fetchUbicaciones() {
  loadingUbicaciones.value = true
  try {
    const response = await apiClient.get('/api/ubicaciones/', {
      params: { page_size: 1000 }
    })
    ubicaciones.value = Array.isArray(response.data) 
      ? response.data 
      : response.data.results || []
    
    console.log(`✅ Cargadas ${ubicaciones.value.length} ubicaciones`)
  } catch (error) {
    console.error('Error al cargar ubicaciones:', error)
    mostrarNotificacion('Error al cargar ubicaciones', 'error')
  } finally {
    loadingUbicaciones.value = false
  }
}

async function fetchDepartamentos() {
  try {
    const response = await apiClient.get('/api/departamentos/', {
      params: { page_size: 1000 }
    })
    departamentos.value = Array.isArray(response.data) 
      ? response.data 
      : response.data.results || []
    
    console.log(`✅ Cargados ${departamentos.value.length} departamentos`)
  } catch (error) {
    console.error('Error al cargar departamentos:', error)
    mostrarNotificacion('Error al cargar departamentos', 'error')
  }
}

async function fetchTiposEquipo() {
  try {
    const response = await apiClient.get('/api/tipos-equipo/', {
      params: { page_size: 1000 }
    })
    tiposEquipo.value = Array.isArray(response.data) 
      ? response.data 
      : response.data.results || []
    
    console.log(`✅ Cargados ${tiposEquipo.value.length} tipos de equipo`)
  } catch (error) {
    console.error('Error al cargar tipos de equipo:', error)
    mostrarNotificacion('Error al cargar tipos de equipo', 'error')
  }
}

/**
 * Carga los activos filtrados por ubicación
 */
async function cargarActivosPorUbicacion() {
  if (!filtros.value.ubicacion) {
    activosPorUbicacion.value = []
    activosPorUbicacionSeleccionados.value = []
    return
  }

  loadingActivosUbicacion.value = true
  try {
    const response = await apiClient.get('/api/activos/', {
      params: {
        ubicacion_actual: filtros.value.ubicacion,
        page_size: 1000
      }
    })
    
    activosPorUbicacion.value = Array.isArray(response.data) 
      ? response.data 
      : response.data.results || []

    console.log(`✅ Cargados ${activosPorUbicacion.value.length} activos de la ubicación ${filtros.value.ubicacion}`)

    // Limpiar selección al cambiar ubicación
    activosPorUbicacionSeleccionados.value = []
    seleccionarTodosUbicacion.value = false

    // Si hay paginación, obtener todas las páginas
    if (response.data.next) {
      await cargarTodasLasPaginasUbicacion(response.data.next)
    }

  } catch (error) {
    console.error('Error al cargar activos por ubicación:', error)
    mostrarNotificacion('Error al cargar activos de la ubicación', 'error')
    activosPorUbicacion.value = []
  } finally {
    loadingActivosUbicacion.value = false
  }
}

/**
 * Carga todas las páginas si la API está paginada (para ubicación)
 */
async function cargarTodasLasPaginasUbicacion(nextUrl) {
  try {
    while (nextUrl) {
      const response = await apiClient.get(nextUrl)
      const nuevosActivos = Array.isArray(response.data) 
        ? response.data 
        : response.data.results || []
      activosPorUbicacion.value = [...activosPorUbicacion.value, ...nuevosActivos]
      nextUrl = response.data.next || null
    }
  } catch (error) {
    console.error('Error al cargar páginas adicionales:', error)
  }
}

/**
 * Selecciona todas las ubicaciones del departamento
 */
async function seleccionarTodasLasUbicaciones() {
  filtros.value.ubicacion = null
  
  if (!filtros.value.departamento) return

  loadingActivosUbicacion.value = true
  try {
    const ubicacionesIds = ubicacionesFiltradas.value.map(ub => ub.id)
    
    const promises = ubicacionesIds.map(ubicacionId => 
      apiClient.get('/api/activos/', {
        params: {
          ubicacion_actual: ubicacionId,
          page_size: 1000
        }
      })
    )

    const responses = await Promise.all(promises)
    
    activosPorUbicacion.value = []
    responses.forEach(response => {
      const activosUbicacion = Array.isArray(response.data) 
        ? response.data 
        : response.data.results || []
      activosPorUbicacion.value = [...activosPorUbicacion.value, ...activosUbicacion]
    })

    console.log(`✅ Cargados ${activosPorUbicacion.value.length} activos de todas las ubicaciones del departamento`)
    
    activosPorUbicacionSeleccionados.value = []
    seleccionarTodosUbicacion.value = false

  } catch (error) {
    console.error('Error al cargar activos de todas las ubicaciones:', error)
    mostrarNotificacion('Error al cargar activos', 'error')
  } finally {
    loadingActivosUbicacion.value = false
  }
}

/**
 * Al cambiar departamento, limpiar ubicación y activos
 */
function onDepartamentoChange() {
  filtros.value.ubicacion = null
  activosPorUbicacion.value = []
  activosPorUbicacionSeleccionados.value = []
  seleccionarTodosUbicacion.value = false
}

// ============================================================================
// MÉTODOS - GESTIÓN DE COLA
// ============================================================================

function agregarSeleccionadosACola() {
  const nuevosActivos = activos.value.filter(a =>
    activosSeleccionados.value.includes(a.id) &&
    !colaImpresion.value.some(c => c.id === a.id)
  )

  colaImpresion.value.push(...nuevosActivos)
  activosSeleccionados.value = []
  seleccionarTodosActivos.value = false
  
  mostrarNotificacion(`${nuevosActivos.length} activos agregados a la cola`, 'success')
}

function agregarActivosUbicacionACola() {
  const nuevosActivos = activosPorUbicacionSeleccionados.value.filter(activo =>
    !colaImpresion.value.some(c => c.id === activo.id)
  )

  colaImpresion.value.push(...nuevosActivos)
  activosPorUbicacionSeleccionados.value = []
  seleccionarTodosUbicacion.value = false
  
  mostrarNotificacion(`${nuevosActivos.length} activos agregados a la cola`, 'success')
}

async function agregarCodigosManuales() {
  let agregados = 0
  
  for (const codigo of codigosManuales.value) {
    const activo = activos.value.find(a =>
      a.codigo_inventario === codigo &&
      !colaImpresion.value.some(c => c.id === a.id)
    )

    if (activo) {
      colaImpresion.value.push(activo)
      agregados++
    }
  }

  if (agregados > 0) {
    mostrarNotificacion(`${agregados} activos agregados a la cola`, 'success')
  } else {
    mostrarNotificacion('No se encontraron activos con los códigos ingresados', 'warning')
  }

  codigosManuales.value = []
}

function removerDeCola(activoId) {
  colaImpresion.value = colaImpresion.value.filter(a => a.id !== activoId)
  mostrarNotificacion('Activo removido de la cola', 'info')
}

function limpiarCola() {
  colaImpresion.value = []
  mostrarNotificacion('Cola de impresión limpiada', 'info')
}

function limpiarFiltros() {
  filtros.value = {
    busqueda: '',
    marca: null,
    tipoEquipo: null,
    ubicacion: null,
    departamento: null,
    busquedaUbicacion: '',
    busquedaActivo: ''
  }
}

// ============================================================================
// MÉTODOS - SELECCIÓN
// ============================================================================

function toggleSeleccionarTodosActivos() {
  if (seleccionarTodosActivos.value) {
    activosSeleccionados.value = activosFiltrados.value.map(a => a.id)
  } else {
    activosSeleccionados.value = []
  }
}

function isActivoUbicacionSeleccionado(activoId) {
  return activosPorUbicacionSeleccionados.value.some(a => a.id === activoId)
}

function toggleActivoUbicacion(activo) {
  const index = activosPorUbicacionSeleccionados.value.findIndex(a => a.id === activo.id)
  
  if (index > -1) {
    activosPorUbicacionSeleccionados.value.splice(index, 1)
  } else {
    activosPorUbicacionSeleccionados.value.push(activo)
  }

  // Actualizar estado de "seleccionar todos"
  seleccionarTodosUbicacion.value = 
    activosPorUbicacionSeleccionados.value.length === activosPorUbicacionFiltrados.value.length
}

function toggleSeleccionarTodosUbicacion() {
  if (seleccionarTodosUbicacion.value) {
    activosPorUbicacionSeleccionados.value = [...activosPorUbicacionFiltrados.value]
  } else {
    activosPorUbicacionSeleccionados.value = []
  }
}

// ============================================================================
// MÉTODOS - GENERACIÓN DE QR CODES
// ============================================================================

async function generarQRCode(codigo) {
  try {
    const qrDataUrl = await QRCode.toDataURL(codigo, {
      width: 120,
      margin: 1,
      color: {
        dark: '#000000',
        light: '#FFFFFF'
      }
    })
    return qrDataUrl
  } catch (error) {
    console.error('Error al generar QR:', error)
    return ''
  }
}

async function generarQRsParaCola() {
  mostrarNotificacion('Generando códigos QR...', 'info')
  
  for (const activo of colaImpresion.value) {
    if (!activo.qrDataUrl) {
      activo.qrDataUrl = await generarQRCode(activo.codigo_inventario)
    }
  }
  
  mostrarNotificacion('Códigos QR generados correctamente', 'success')
}

// ============================================================================
// MÉTODOS - VISTA PREVIA E IMPRESIÓN
// ============================================================================

async function abrirVistaPrevia() {
  await generarQRsParaCola()
  dialogVistaPrevia.value = true
}

function cerrarVistaPrevia() {
  dialogVistaPrevia.value = false
}

function imprimirEtiquetas() {
  window.print()
  mostrarNotificacion('Enviando a impresión...', 'success')
}

// ============================================================================
// MÉTODOS - HELPERS
// ============================================================================

function getEstadoColor(estado) {
  const colores = {
    'Operativo': 'success',
    'En Reparación': 'warning',
    'En Bodega TI': 'info',
    'De Baja': 'error'
  }
  return colores[estado] || 'grey'
}

function mostrarNotificacion(text, color = 'success') {
  snackbar.value = {
    show: true,
    text,
    color
  }
}

// ============================================================================
// WATCHERS
// ============================================================================

watch(activosSeleccionados, (newVal) => {
  seleccionarTodosActivos.value = newVal.length === activosFiltrados.value.length && newVal.length > 0
})

// ============================================================================
// LIFECYCLE HOOKS
// ============================================================================

onMounted(async () => {
  await Promise.all([
    fetchActivos(),
    fetchUbicaciones(),
    fetchDepartamentos(),
    fetchTiposEquipo()
  ])
})

</script>

<style scoped>
/* ============================================================================
   CONTENEDOR PRINCIPAL
   ============================================================================ */

.print-labels-view {
  min-height: calc(100vh - 112px);
  background: #f5f7fa;
  padding: 1rem;
  padding-bottom: 100px; /* Espacio para el FAB */
}

/* ============================================================================
   LOADING STATE
   ============================================================================ */

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 1rem;
  color: #666;
}

/* ============================================================================
   BOTÓN FLOTANTE DE VISTA PREVIA
   ============================================================================ */

.fab-preview {
  position: fixed !important;
  bottom: 80px !important;
  right: 24px !important;
  z-index: 1000 !important;
}

/* ============================================================================
   CONTENEDOR DE ETIQUETAS (GRID 3 COLUMNAS)
   ============================================================================ */

.print-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  padding: 20px;
  background: white;
}

/* ============================================================================
   TARJETA DE ETIQUETA INDIVIDUAL
   ============================================================================ */

.etiqueta-card {
  border: 1px dashed #000;
  padding: 8px;
  page-break-inside: avoid;
  min-height: 80px;
  display: flex;
  align-items: center;
}

.etiqueta-content {
  display: flex;
  width: 100%;
  align-items: center;
  gap: 8px;
}

/* ============================================================================
   NOMBRE DEL ACTIVO (IZQUIERDA - 70%)
   ============================================================================ */

.etiqueta-nombre {
  flex: 0 0 70%;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  padding-left: 8px;
}

.nombre-text {
  font-size: 14px;
  font-weight: bold;
  line-height: 1.2;
  text-align: left;
  word-wrap: break-word;
}

/* ============================================================================
   SECCIÓN QR + CÓDIGO (DERECHA - 30%)
   ============================================================================ */

.etiqueta-qr-section {
  flex: 0 0 30%;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 4px;
}

.qr-container {
  flex-shrink: 0;
}

.qr-image {
  width: 60px;
  height: 60px;
  display: block;
}

.qr-placeholder {
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  border: 1px dashed #999;
}

/* ============================================================================
   CÓDIGO VERTICAL (ROTADO 90 GRADOS)
   ============================================================================ */

.codigo-vertical {
  writing-mode: vertical-rl;
  text-orientation: mixed;
  font-size: 10px;
  font-weight: bold;
  letter-spacing: 1px;
  white-space: nowrap;
  padding: 4px 0;
}

/* ============================================================================
   UTILIDADES
   ============================================================================ */

.gap-3 {
  gap: 1rem;
}

/* ============================================================================
   RESPONSIVE - TABLETS Y MÓVILES
   ============================================================================ */

@media (max-width: 960px) {
  .print-container {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 600px) {
  .print-container {
    grid-template-columns: 1fr;
  }

  .fab-preview {
    bottom: 70px !important;
    right: 16px !important;
  }

  .print-labels-view {
    padding: 0.75rem;
  }
}

/* ============================================================================
   ESTILOS DE IMPRESIÓN (@media print)
   ============================================================================ */

@media print {
  /* Ocultar todo excepto el área de impresión */
  body * {
    visibility: hidden;
  }

  #print-area,
  #print-area * {
    visibility: visible;
  }

  #print-area {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
  }

  /* Ajustar márgenes de página */
  @page {
    margin: 10mm;
    size: A4;
  }

  /* Asegurar que las etiquetas no se corten */
  .etiqueta-card {
    page-break-inside: avoid;
    break-inside: avoid;
  }

  /* Mantener el grid de 3 columnas en impresión */
  .print-container {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
  }
}
</style>
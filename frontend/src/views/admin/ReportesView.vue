<template>
  <div class="reportes-content">
    <!-- ====================================================================
         HEADER
         ==================================================================== -->
    <v-card variant="tonal" color="primary" class="mb-4">
      <v-card-text>
        <h2 class="text-h5 font-weight-bold mb-1">Reportes del Sistema</h2>
        <p class="text-subtitle-1 mb-0">Genera informes detallados de activos y movimientos</p>
      </v-card-text>
    </v-card>

    <!-- ====================================================================
         REPORTES DE INVENTARIO
         ==================================================================== -->
    <v-card class="mb-4">
      <v-card-title class="text-h6 font-weight-bold d-flex align-center">
        <v-icon class="mr-2" color="blue">mdi-clipboard-list</v-icon>
        Reportes de Inventario
      </v-card-title>
      <v-card-text>
        <v-row>
          <v-col
            v-for="(reporte, index) in reportesInventario"
            :key="index"
            cols="12"
            sm="6"
            md="4"
          >
            <v-card
              class="reporte-card"
              elevation="2"
              @click="abrirDialogoReporte(reporte)"
            >
              <v-card-text class="text-center pa-6">
                <v-avatar
                  :color="reporte.color"
                  size="64"
                  class="mb-4"
                >
                  <v-icon size="32" color="white">
                    {{ reporte.icon }}
                  </v-icon>
                </v-avatar>
                
                <h3 class="text-h6 font-weight-bold mb-2">
                  {{ reporte.nombre }}
                </h3>
                
                <p class="text-body-2 text-grey-darken-1">
                  {{ reporte.descripcion }}
                </p>
              </v-card-text>

              <v-divider></v-divider>

              <v-card-actions class="pa-3">
                <v-btn
                  block
                  :color="reporte.color"
                  variant="text"
                >
                  Generar
                  <v-icon end>mdi-file-download</v-icon>
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- ====================================================================
         REPORTES DE MOVIMIENTOS
         ==================================================================== -->
    <v-card class="mb-4">
      <v-card-title class="text-h6 font-weight-bold d-flex align-center">
        <v-icon class="mr-2" color="teal">mdi-swap-horizontal</v-icon>
        Reportes de Movimientos
      </v-card-title>
      <v-card-text>
        <v-row>
          <v-col
            v-for="(reporte, index) in reportesMovimientos"
            :key="index"
            cols="12"
            sm="6"
            md="4"
          >
            <v-card
              class="reporte-card"
              elevation="2"
              @click="abrirDialogoReporte(reporte)"
            >
              <v-card-text class="text-center pa-6">
                <v-avatar
                  :color="reporte.color"
                  size="64"
                  class="mb-4"
                >
                  <v-icon size="32" color="white">
                    {{ reporte.icon }}
                  </v-icon>
                </v-avatar>
                
                <h3 class="text-h6 font-weight-bold mb-2">
                  {{ reporte.nombre }}
                </h3>
                
                <p class="text-body-2 text-grey-darken-1">
                  {{ reporte.descripcion }}
                </p>
              </v-card-text>

              <v-divider></v-divider>

              <v-card-actions class="pa-3">
                <v-btn
                  block
                  :color="reporte.color"
                  variant="text"
                >
                  Generar
                  <v-icon end>mdi-file-download</v-icon>
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- ====================================================================
         REPORTES DE MANTENIMIENTO
         ==================================================================== -->
    <v-card class="mb-4">
      <v-card-title class="text-h6 font-weight-bold d-flex align-center">
        <v-icon class="mr-2" color="orange">mdi-wrench</v-icon>
        Reportes de Mantenimiento
      </v-card-title>
      <v-card-text>
        <v-row>
          <v-col
            v-for="(reporte, index) in reportesMantenimiento"
            :key="index"
            cols="12"
            sm="6"
            md="4"
          >
            <v-card
              class="reporte-card"
              elevation="2"
              @click="abrirDialogoReporte(reporte)"
            >
              <v-card-text class="text-center pa-6">
                <v-avatar
                  :color="reporte.color"
                  size="64"
                  class="mb-4"
                >
                  <v-icon size="32" color="white">
                    {{ reporte.icon }}
                  </v-icon>
                </v-avatar>
                
                <h3 class="text-h6 font-weight-bold mb-2">
                  {{ reporte.nombre }}
                </h3>
                
                <p class="text-body-2 text-grey-darken-1">
                  {{ reporte.descripcion }}
                </p>
              </v-card-text>

              <v-divider></v-divider>

              <v-card-actions class="pa-3">
                <v-btn
                  block
                  :color="reporte.color"
                  variant="text"
                >
                  Generar
                  <v-icon end>mdi-file-download</v-icon>
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- ====================================================================
         REPORTES DE ASIGNACIÓN
         ==================================================================== -->
    <v-card class="mb-4">
      <v-card-title class="text-h6 font-weight-bold d-flex align-center">
        <v-icon class="mr-2" color="purple">mdi-account-check</v-icon>
        Reportes de Asignación
      </v-card-title>
      <v-card-text>
        <v-row>
          <v-col
            v-for="(reporte, index) in reportesAsignacion"
            :key="index"
            cols="12"
            sm="6"
            md="4"
          >
            <v-card
              class="reporte-card"
              elevation="2"
              @click="abrirDialogoReporte(reporte)"
            >
              <v-card-text class="text-center pa-6">
                <v-avatar
                  :color="reporte.color"
                  size="64"
                  class="mb-4"
                >
                  <v-icon size="32" color="white">
                    {{ reporte.icon }}
                  </v-icon>
                </v-avatar>
                
                <h3 class="text-h6 font-weight-bold mb-2">
                  {{ reporte.nombre }}
                </h3>
                
                <p class="text-body-2 text-grey-darken-1">
                  {{ reporte.descripcion }}
                </p>
              </v-card-text>

              <v-divider></v-divider>

              <v-card-actions class="pa-3">
                <v-btn
                  block
                  :color="reporte.color"
                  variant="text"
                >
                  Generar
                  <v-icon end>mdi-file-download</v-icon>
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- ====================================================================
         DIÁLOGO CONFIGURAR REPORTE
         ==================================================================== -->
    <v-dialog v-model="dialogoReporte" max-width="600px">
      <v-card>
        <v-card-title class="text-h5 pa-4" :class="`bg-${reporteSeleccionado?.color} text-white`">
          <v-icon start>{{ reporteSeleccionado?.icon }}</v-icon>
          {{ reporteSeleccionado?.nombre }}
        </v-card-title>
        
        <v-card-text class="pa-4">
          <p class="mb-4 text-body-1">{{ reporteSeleccionado?.descripcion }}</p>

          <!-- Filtros según tipo de reporte -->
          <div v-if="reporteSeleccionado?.filtros">
            
            <!-- Filtro de Estado -->
            <v-select
              v-if="reporteSeleccionado.filtros.includes('estado')"
              v-model="configuracion.estado"
              :items="estados"
              item-title="nombre_estado"
              item-value="id"
              label="Estado"
              variant="outlined"
              density="comfortable"
              prepend-inner-icon="mdi-state-machine"
              clearable
              class="mb-3"
            ></v-select>

            <!-- Filtro de Ubicación -->
            <v-select
              v-if="reporteSeleccionado.filtros.includes('ubicacion')"
              v-model="configuracion.ubicacion"
              :items="ubicaciones"
              item-title="nombre_ubicacion"
              item-value="id"
              label="Ubicación"
              variant="outlined"
              density="comfortable"
              prepend-inner-icon="mdi-map-marker"
              clearable
              class="mb-3"
            ></v-select>

            <!-- Filtro de Tipo de Equipo -->
            <v-select
              v-if="reporteSeleccionado.filtros.includes('tipo')"
              v-model="configuracion.tipo"
              :items="tiposEquipo"
              item-title="nombre_tipo"
              item-value="id"
              label="Tipo de Equipo"
              variant="outlined"
              density="comfortable"
              prepend-inner-icon="mdi-devices"
              clearable
              class="mb-3"
            ></v-select>

            <!-- Filtro de Departamento -->
            <v-select
              v-if="reporteSeleccionado.filtros.includes('departamento')"
              v-model="configuracion.departamento"
              :items="departamentos"
              item-title="nombre_departamento"
              item-value="id"
              label="Departamento"
              variant="outlined"
              density="comfortable"
              prepend-inner-icon="mdi-office-building"
              clearable
              class="mb-3"
            ></v-select>

            <!-- Filtro de Período -->
            <v-select
              v-if="reporteSeleccionado.filtros.includes('periodo')"
              v-model="configuracion.periodo"
              :items="periodos"
              label="Período"
              variant="outlined"
              density="comfortable"
              prepend-inner-icon="mdi-calendar-range"
              class="mb-3"
            ></v-select>

            <!-- Filtro de Usuario -->
            <v-select
              v-if="reporteSeleccionado.filtros.includes('usuario')"
              v-model="configuracion.usuario"
              :items="usuarios"
              item-title="nombre_completo"
              item-value="id"
              label="Usuario"
              variant="outlined"
              density="comfortable"
              prepend-inner-icon="mdi-account"
              clearable
              class="mb-3"
            ></v-select>

            <!-- Filtro de Activo específico -->
            <v-autocomplete
              v-if="reporteSeleccionado.filtros.includes('activo')"
              v-model="configuracion.activo"
              :items="activos"
              :item-title="item => `${item.codigo_inventario} - ${item.marca} ${item.modelo}`"
              item-value="id"
              label="Activo específico"
              variant="outlined"
              density="comfortable"
              prepend-inner-icon="mdi-laptop"
              clearable
              class="mb-3"
            ></v-autocomplete>

            <!-- Filtro de Rango de fechas personalizado -->
            <v-row v-if="reporteSeleccionado.filtros.includes('fechas')">
              <v-col cols="6">
                <v-text-field
                  v-model="configuracion.fechaDesde"
                  label="Fecha desde"
                  type="date"
                  variant="outlined"
                  density="comfortable"
                  prepend-inner-icon="mdi-calendar"
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  v-model="configuracion.fechaHasta"
                  label="Fecha hasta"
                  type="date"
                  variant="outlined"
                  density="comfortable"
                  prepend-inner-icon="mdi-calendar"
                ></v-text-field>
              </v-col>
            </v-row>
          </div>

          <!-- Formato de exportación -->
          <v-divider class="my-4"></v-divider>
          
          <v-select
            v-model="configuracion.formato"
            :items="formatos"
            label="Formato de exportación"
            variant="outlined"
            density="comfortable"
            prepend-inner-icon="mdi-file"
          ></v-select>
        </v-card-text>

        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn
            variant="text"
            @click="dialogoReporte = false"
          >
            Cancelar
          </v-btn>
          <v-btn
            :color="reporteSeleccionado?.color"
            @click="generarReporte"
            :loading="generandoReporte"
          >
            <v-icon start>mdi-download</v-icon>
            Generar Reporte
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- ====================================================================
         SNACKBAR
         ==================================================================== -->
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
 * REPORTES DEL SISTEMA
 * ============================================================================
 *
 * Vista para generar diferentes tipos de reportes:
 * - Inventario
 * - Movimientos
 * - Mantenimiento
 * - Asignación
 */

import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/services/api'

// ============================================================================
// COMPOSABLES
// ============================================================================

const router = useRouter()

// ============================================================================
// STATE
// ============================================================================

const reportesInventario = ref([
  {
    nombre: 'Inventario Completo',
    descripcion: 'Lista detallada de todos los activos',
    icon: 'mdi-format-list-bulleted',
    color: 'blue',
    tipo: 'inventario_completo',
    filtros: []
  },
  {
    nombre: 'Activos por Estado',
    descripcion: 'Agrupados por operativos, mantenimiento, bodega, baja',
    icon: 'mdi-state-machine',
    color: 'indigo',
    tipo: 'por_estado',
    filtros: ['estado']
  },
  {
    nombre: 'Activos por Ubicación',
    descripcion: 'Ver qué hay en cada ubicación física',
    icon: 'mdi-map-marker',
    color: 'cyan',
    tipo: 'por_ubicacion',
    filtros: ['ubicacion']
  },
  {
    nombre: 'Activos por Tipo',
    descripcion: 'Computadores, impresoras, monitores, etc.',
    icon: 'mdi-devices',
    color: 'teal',
    tipo: 'por_tipo',
    filtros: ['tipo']
  },
  {
    nombre: 'Activos por Departamento',
    descripcion: 'Qué tiene cada departamento',
    icon: 'mdi-office-building',
    color: 'green',
    tipo: 'por_departamento',
    filtros: ['departamento']
  }
])

const reportesMovimientos = ref([
  {
    nombre: 'Movimientos por Período',
    descripcion: 'Últimos 7 días, mes, año',
    icon: 'mdi-calendar-range',
    color: 'purple',
    tipo: 'movimientos_periodo',
    filtros: ['periodo', 'fechas']
  },
  {
    nombre: 'Movimientos por Usuario',
    descripcion: 'Quién ha registrado más movimientos',
    icon: 'mdi-account-clock',
    color: 'deep-purple',
    tipo: 'movimientos_usuario',
    filtros: ['usuario', 'periodo']
  },
  {
    nombre: 'Activos Más Movidos',
    descripcion: 'Identificar equipos con muchos traslados',
    icon: 'mdi-trending-up',
    color: 'pink',
    tipo: 'activos_mas_movidos',
    filtros: ['periodo']
  },
  {
    nombre: 'Historial de Activo',
    descripcion: 'Trazabilidad completa de un activo',
    icon: 'mdi-history',
    color: 'light-blue',
    tipo: 'historial_activo',
    filtros: ['activo']
  }
])

const reportesMantenimiento = ref([
  {
    nombre: 'Activos en Mantenimiento',
    descripcion: 'Lista actual de equipos en mantenimiento',
    icon: 'mdi-wrench-clock',
    color: 'amber',
    tipo: 'en_mantenimiento',
    filtros: []
  },
  {
    nombre: 'Historial de Mantenimientos',
    descripcion: 'Filtra por día, mes, año',
    icon: 'mdi-clipboard-text-clock',
    color: 'orange',
    tipo: 'historial_mantenimientos',
    filtros: ['periodo', 'fechas']
  },
  {
    nombre: 'Tiempo Promedio',
    descripcion: 'Métricas de eficiencia en mantenimiento',
    icon: 'mdi-chart-timeline',
    color: 'deep-orange',
    tipo: 'tiempo_promedio',
    filtros: ['periodo']
  },
  {
    nombre: 'Mantenimientos Frecuentes',
    descripcion: 'Identificar problemas recurrentes',
    icon: 'mdi-alert-circle',
    color: 'red',
    tipo: 'mantenimientos_frecuentes',
    filtros: ['periodo']
  }
])

const reportesAsignacion = ref([
  {
    nombre: 'Activos Sin Asignar',
    descripcion: 'Disponibles en bodega',
    icon: 'mdi-package-variant',
    color: 'blue-grey',
    tipo: 'sin_asignar',
    filtros: ['ubicacion']
  }
])

// Datos para filtros
const estados = ref([])
const ubicaciones = ref([])
const tiposEquipo = ref([])
const departamentos = ref([])
const usuarios = ref([])
const activos = ref([])

const periodos = [
  { title: 'Últimos 7 días', value: '7dias' },
  { title: 'Últimos 30 días', value: '30dias' },
  { title: 'Último mes', value: 'mes' },
  { title: 'Último trimestre', value: 'trimestre' },
  { title: 'Último año', value: 'año' },
  { title: 'Personalizado', value: 'personalizado' }
]

const formatos = [
  { title: 'Excel (.xlsx)', value: 'excel' },
  { title: 'PDF', value: 'pdf' },
  { title: 'CSV', value: 'csv' }
]

// Estado del diálogo
const dialogoReporte = ref(false)
const reporteSeleccionado = ref(null)
const generandoReporte = ref(false)

const configuracion = ref({
  estado: null,
  ubicacion: null,
  tipo: null,
  departamento: null,
  periodo: '30dias',
  usuario: null,
  activo: null,
  fechaDesde: null,
  fechaHasta: null,
  formato: 'excel'
})

const snackbar = ref({
  show: false,
  text: '',
  color: 'success'
})

// ============================================================================
// MÉTODOS - API
// ============================================================================

/**
 * Carga todos los datos necesarios para los filtros
 */
async function cargarDatosFiltros() {
  try {
    const [
      responseEstados,
      responseUbicaciones,
      responseTipos,
      responseDepartamentos,
      responseUsuarios,
      responseActivos
    ] = await Promise.all([
      apiClient.get('/api/estados-activo/', { params: { page_size: 1000 } }),
      apiClient.get('/api/ubicaciones/', { params: { page_size: 1000 } }),
      apiClient.get('/api/tipos-equipo/', { params: { page_size: 1000 } }),
      apiClient.get('/api/departamentos/', { params: { page_size: 1000 } }),
      apiClient.get('/api/usuarios/', { params: { page_size: 1000 } }),
      apiClient.get('/api/activos/', { params: { page_size: 1000 } })
    ])

    estados.value = responseEstados.data.results || responseEstados.data || []
    ubicaciones.value = responseUbicaciones.data.results || responseUbicaciones.data || []
    tiposEquipo.value = responseTipos.data.results || responseTipos.data || []
    departamentos.value = responseDepartamentos.data.results || responseDepartamentos.data || []
    usuarios.value = responseUsuarios.data.results || responseUsuarios.data || []
    activos.value = responseActivos.data.results || responseActivos.data || []

  } catch (error) {
    console.error('Error al cargar datos de filtros:', error)
  }
}

// ============================================================================
// MÉTODOS - UI
// ============================================================================

/**
 * Abre el diálogo de configuración del reporte
 */
function abrirDialogoReporte(reporte) {
  reporteSeleccionado.value = reporte
  
  // Resetear configuración
  configuracion.value = {
    estado: null,
    ubicacion: null,
    tipo: null,
    departamento: null,
    periodo: '30dias',
    usuario: null,
    activo: null,
    fechaDesde: null,
    fechaHasta: null,
    formato: 'excel'
  }
  
  dialogoReporte.value = true
}

/**
 * Genera el reporte con la configuración seleccionada
 */
async function generarReporte() {
  generandoReporte.value = true
  
  try {
    // TODO: Implementar llamada al endpoint de reportes
    // const response = await apiClient.post('/api/reportes/', {
    //   tipo: reporteSeleccionado.value.tipo,
    //   configuracion: configuracion.value
    // })
    
    // Simular generación
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    // mostrarNotificacion(`Reporte "${reporteSeleccionado.value.nombre}" generado correctamente`, 'success')
    mostrarNotificacion(`Funcion en Desarrollo`, 'error')
    dialogoReporte.value = false
    
    console.log('Generando reporte:', {
      tipo: reporteSeleccionado.value.tipo,
      config: configuracion.value
    })
    
  } catch (error) {
    console.error('Error al generar reporte:', error)
    mostrarNotificacion('Error al generar el reporte', 'error')
  } finally {
    generandoReporte.value = false
  }
}

/**
 * Muestra una notificación
 */
function mostrarNotificacion(text, color = 'success') {
  snackbar.value = {
    show: true,
    text,
    color
  }
}

// ============================================================================
// LIFECYCLE HOOKS
// ============================================================================

onMounted(async () => {
  await cargarDatosFiltros()
})

</script>

<style scoped>
/* ============================================================================
   CONTENEDOR PRINCIPAL
   ============================================================================ */

.reportes-content {
  min-height: calc(100vh - 112px);
  background: #f5f7fa;
  padding: 1rem;
  padding-bottom: 80px;
}

/* ============================================================================
   TARJETAS DE REPORTES
   ============================================================================ */

.reporte-card {
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  height: 100%;
  border-radius: 12px !important;
}

.reporte-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15) !important;
}

.reporte-card:active {
  transform: translateY(-4px);
}

/* ============================================================================
   RESPONSIVE ADJUSTMENTS
   ============================================================================ */

@media (max-width: 600px) {
  .reportes-content {
    padding: 0.75rem;
  }
}

@media (min-width: 960px) {
  .reportes-content {
    max-width: 1400px;
    margin: 0 auto;
  }
}
</style>
<template>
  <div class="jefe-home-content">
    <!-- ====================================================================
         INDICADOR DE CARGA
         ==================================================================== -->
    <div v-if="loading" class="text-center py-8">
      <v-progress-circular
        indeterminate
        color="primary"
        size="64"
      ></v-progress-circular>
      <p class="text-h6 mt-4">Cargando estadísticas...</p>
    </div>

    <!-- ====================================================================
         CONTENIDO PRINCIPAL (Solo se muestra cuando NO está cargando)
         ==================================================================== -->
    <div v-else>
      <!-- ====================================================================
           1. TARJETA DE BIENVENIDA
           ==================================================================== -->
      <v-card variant="tonal" color="primary" class="mb-4">
        <v-card-text>
          <h2 class="text-h5 font-weight-bold mb-1">Bienvenido, {{ userName }}</h2>
          <p class="text-subtitle-1 mb-0">{{ fechaActual }}</p>
          <p class="text-caption mt-1">Jefe de Departamento - Dashboard Ejecutivo</p>
        </v-card-text>
      </v-card>

    <!-- ====================================================================
         2. KPIs SUPERIORES - 4 TARJETAS
         ==================================================================== -->
    <v-row class="mb-4">
      <v-col
        v-for="(kpi, index) in kpis"
        :key="index"
        cols="6"
        md="3"
      >
        <v-card :color="kpi.color" dark elevation="4" class="kpi-card">
          <v-card-text>
            <div class="d-flex justify-space-between align-start">
              <v-icon size="40" class="kpi-icon">{{ kpi.icon }}</v-icon>
              <div class="text-right">
                <div class="text-h4 font-weight-bold">{{ kpi.value }}</div>
                <div class="text-caption mt-1">{{ kpi.label }}</div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- ====================================================================
         3. GRÁFICOS - BAR Y DOUGHNUT
         ==================================================================== -->
    <v-row class="mb-4">
      <!-- Gráfico de Barras: Activos por Departamento -->
      <v-col cols="12" md="6">
        <v-card elevation="2">
          <v-card-title class="text-h6 font-weight-bold">
            <v-icon class="mr-2">mdi-chart-bar</v-icon>
            Activos por Departamento
          </v-card-title>
          <v-card-text>
            <div class="chart-container">
              <Bar :data="barChartData" :options="barChartOptions" />
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Gráfico de Dona: Estado de Salud -->
      <v-col cols="12" md="6">
        <v-card elevation="2">
          <v-card-title class="text-h6 font-weight-bold">
            <v-icon class="mr-2">mdi-chart-donut</v-icon>
            Estado de Salud de Activos
          </v-card-title>
          <v-card-text>
            <div class="chart-container">
              <Doughnut :data="doughnutChartData" :options="doughnutChartOptions" />
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    </div>
    <!-- Fin del contenido principal -->
  </div>
</template>

<script setup>
/**
 * ============================================================================
 * JEFE DE DEPARTAMENTO - DASHBOARD EJECUTIVO
 * ============================================================================
 *
 * Dashboard de alto impacto visual con Vue-Chartjs:
 * 1. KPIs superiores (Total, Operativos, Reparación, De Baja)
 * 2. Gráfico de Barras: Activos por Departamento
 * 3. Gráfico de Dona: Estado de Salud
 * 4. Botones de acciones rápidas
 *
 * LIBRERÍAS: chart.js + vue-chartjs (ya instaladas)
 */

import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import apiClient from '@/services/api'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  ArcElement,
  CategoryScale,
  LinearScale
} from 'chart.js'
import { Bar, Doughnut } from 'vue-chartjs'

// ============================================================================
// REGISTRAR COMPONENTES DE CHART.JS (CRÍTICO PARA EVITAR ERRORES)
// ============================================================================
ChartJS.register(Title, Tooltip, Legend, BarElement, ArcElement, CategoryScale, LinearScale)

// ============================================================================
// COMPOSABLES
// ============================================================================
const router = useRouter()
const authStore = useAuthStore()

// ============================================================================
// STATE - DATOS REALES DESDE LA API
// ============================================================================

// Estado de carga
const loading = ref(true)
const error = ref(null)

// KPIs Superiores (se llenarán con datos reales)
const kpis = ref([
  {
    label: 'Total Activos',
    value: 0,
    icon: 'mdi-desktop-classic',
    color: 'blue'
  },
  {
    label: 'Operativos',
    value: 0,
    icon: 'mdi-check-circle',
    color: 'green'
  },
  {
    label: 'En Reparación',
    value: 0,
    icon: 'mdi-wrench',
    color: 'amber'
  },
  {
    label: 'De Baja',
    value: 0,
    icon: 'mdi-close-circle',
    color: 'red'
  }
])

// Datos para el gráfico de barras (Activos por Departamento) - Se llenarán con datos reales
const barChartData = ref({
  labels: [],
  datasets: [
    {
      label: 'Cantidad de Activos',
      data: [],
      backgroundColor: [],
      borderColor: [],
      borderWidth: 2
    }
  ]
})

// Paleta de colores para los gráficos
const colorPalette = [
  { bg: 'rgba(33, 150, 243, 0.7)', border: 'rgba(33, 150, 243, 1)' },    // Azul
  { bg: 'rgba(76, 175, 80, 0.7)', border: 'rgba(76, 175, 80, 1)' },      // Verde
  { bg: 'rgba(255, 152, 0, 0.7)', border: 'rgba(255, 152, 0, 1)' },      // Naranja
  { bg: 'rgba(156, 39, 176, 0.7)', border: 'rgba(156, 39, 176, 1)' },    // Púrpura
  { bg: 'rgba(244, 67, 54, 0.7)', border: 'rgba(244, 67, 54, 1)' },      // Rojo
  { bg: 'rgba(0, 188, 212, 0.7)', border: 'rgba(0, 188, 212, 1)' },      // Cyan
  { bg: 'rgba(255, 193, 7, 0.7)', border: 'rgba(255, 193, 7, 1)' },      // Amarillo
  { bg: 'rgba(96, 125, 139, 0.7)', border: 'rgba(96, 125, 139, 1)' }     // Gris
]

const barChartOptions = ref({
  responsive: true,
  maintainAspectRatio: true,
  plugins: {
    legend: {
      display: false
    },
    title: {
      display: false
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      ticks: {
        stepSize: 2
      }
    }
  }
})

// Datos para el gráfico de dona (Estado de Salud) - Se llenarán con datos reales
const doughnutChartData = ref({
  labels: [],
  datasets: [
    {
      label: 'Estado de Activos',
      data: [],
      backgroundColor: [],
      borderColor: [],
      borderWidth: 2
    }
  ]
})

// Mapa de colores por estado
const estadoColors = {
  'Operativo': { bg: 'rgba(76, 175, 80, 0.8)', border: 'rgba(76, 175, 80, 1)' },
  'En Reparación': { bg: 'rgba(255, 193, 7, 0.8)', border: 'rgba(255, 193, 7, 1)' },
  'En Mantención': { bg: 'rgba(255, 152, 0, 0.8)', border: 'rgba(255, 152, 0, 1)' },
  'En Bodega': { bg: 'rgba(33, 150, 243, 0.8)', border: 'rgba(33, 150, 243, 1)' },
  'De Baja': { bg: 'rgba(244, 67, 54, 0.8)', border: 'rgba(244, 67, 54, 1)' }
}

const doughnutChartOptions = ref({
  responsive: true,
  maintainAspectRatio: true,
  plugins: {
    legend: {
      position: 'bottom',
      labels: {
        padding: 15,
        font: {
          size: 12
        }
      }
    },
    title: {
      display: false
    }
  }
})

// ============================================================================
// COMPUTED PROPERTIES
// ============================================================================

/**
 * Obtiene el nombre del usuario desde el store
 */
const userName = computed(() => {
  return authStore.user?.nombre_completo || authStore.user?.username || 'Jefe'
})

/**
 * Genera la fecha actual formateada en español
 */
const fechaActual = computed(() => {
  const fecha = new Date()
  const opciones = {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }

  return fecha.toLocaleDateString('es-ES', opciones)
    .split(' ')
    .map((palabra, index) => index === 0 ? palabra.charAt(0).toUpperCase() + palabra.slice(1) : palabra)
    .join(' ')
})

// ============================================================================
// METHODS - API
// ============================================================================

/**
 * Carga las estadísticas del dashboard desde la API
 */
async function fetchDashboardData() {
  loading.value = true
  error.value = null

  try {
    console.log('📊 Cargando estadísticas del dashboard...')

    const response = await apiClient.get('/api/dashboard/stats/')
    const data = response.data

    console.log('✅ Estadísticas recibidas:', data)

    // ================================================================
    // 1. ACTUALIZAR KPIs
    // ================================================================
    kpis.value[0].value = data.kpis.total
    kpis.value[1].value = data.kpis.operativos
    kpis.value[2].value = data.kpis.en_reparacion
    kpis.value[3].value = data.kpis.de_baja

    // ================================================================
    // 2. ACTUALIZAR GRÁFICO DE BARRAS (Activos por Departamento)
    // ================================================================
    if (data.activos_por_departamento && data.activos_por_departamento.length > 0) {
      barChartData.value.labels = data.activos_por_departamento.map(item => item.departamento)
      barChartData.value.datasets[0].data = data.activos_por_departamento.map(item => item.cantidad)

      // Asignar colores dinámicamente
      const backgroundColors = []
      const borderColors = []

      data.activos_por_departamento.forEach((_, index) => {
        const colorIndex = index % colorPalette.length
        backgroundColors.push(colorPalette[colorIndex].bg)
        borderColors.push(colorPalette[colorIndex].border)
      })

      barChartData.value.datasets[0].backgroundColor = backgroundColors
      barChartData.value.datasets[0].borderColor = borderColors
    }

    // ================================================================
    // 3. ACTUALIZAR GRÁFICO DE DONA (Estado de Salud)
    // ================================================================
    if (data.estado_salud && data.estado_salud.length > 0) {
      doughnutChartData.value.labels = data.estado_salud.map(item => item.estado)
      doughnutChartData.value.datasets[0].data = data.estado_salud.map(item => item.cantidad)

      // Asignar colores según el estado
      const backgroundColors = []
      const borderColors = []

      data.estado_salud.forEach(item => {
        const colors = estadoColors[item.estado] || {
          bg: 'rgba(158, 158, 158, 0.8)',
          border: 'rgba(158, 158, 158, 1)'
        }
        backgroundColors.push(colors.bg)
        borderColors.push(colors.border)
      })

      doughnutChartData.value.datasets[0].backgroundColor = backgroundColors
      doughnutChartData.value.datasets[0].borderColor = borderColors
    }

  } catch (err) {
    console.error('❌ Error al cargar estadísticas:', err)
    error.value = 'No se pudieron cargar las estadísticas. Verifica tu conexión.'

    // Mostrar alerta al usuario
    alert('Error al cargar las estadísticas del dashboard. Por favor, recarga la página.')
  } finally {
    loading.value = false
  }
}

// ============================================================================
// METHODS - NAVEGACIÓN
// ============================================================================

/**
 * Navega a una ruta específica
 */
function navigateTo(path) {
  router.push(path)
}

// ============================================================================
// LIFECYCLE HOOKS
// ============================================================================

/**
 * Al montar el componente, cargar datos reales desde la API
 */
onMounted(async () => {
  console.log('🚀 Dashboard Jefe de Departamento - Iniciando carga de datos...')
  await fetchDashboardData()
})


</script>

<style scoped>
/* ============================================================================
   CONTENEDOR PRINCIPAL
   ============================================================================ */

.jefe-home-content {
  min-height: calc(100vh - 112px);
  background: #f5f7fa;
  padding: 1rem;
  padding-bottom: 80px;
}

/* ============================================================================
   KPI CARDS
   ============================================================================ */

.kpi-card {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  height: 100%;
  cursor: pointer;
}

.kpi-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.25) !important;
}

.kpi-card:active {
  transform: translateY(-2px);
}

.kpi-icon {
  opacity: 0.9;
}

/* ============================================================================
   CHART CONTAINERS
   ============================================================================ */

.chart-container {
  position: relative;
  height: 300px;
  padding: 1rem 0;
}

/* ============================================================================
   RESPONSIVE ADJUSTMENTS
   ============================================================================ */

@media (max-width: 600px) {
  .jefe-home-content {
    padding: 0.75rem;
  }

  .chart-container {
    height: 250px;
  }
}

@media (min-width: 960px) {
  .jefe-home-content {
    max-width: 1400px;
    margin: 0 auto;
  }

  .chart-container {
    height: 350px;
  }
}
</style>


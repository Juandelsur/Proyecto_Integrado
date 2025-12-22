<template>
  <div class="jefe-home-content">
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

    <!-- ====================================================================
         4. BOTONES DE ACCIONES RÁPIDAS
         ==================================================================== -->
    <v-card elevation="2">
      <v-card-title class="text-h6 font-weight-bold">
        <v-icon class="mr-2">mdi-lightning-bolt</v-icon>
        Acciones Rápidas
      </v-card-title>
      <v-card-text>
        <v-row>
          <v-col cols="12" sm="4">
            <v-btn
              block
              size="large"
              color="primary"
              variant="tonal"
              prepend-icon="mdi-qrcode-scan"
              @click="navigateTo('/tecnico/scan')"
            >
              Scanner QR
            </v-btn>
          </v-col>
          <v-col cols="12" sm="4">
            <v-btn
              block
              size="large"
              color="success"
              variant="tonal"
              prepend-icon="mdi-printer"
              @click="navigateTo('/jefe/imprimir-qr')"
            >
              Imprimir QR
            </v-btn>
          </v-col>
          <v-col cols="12" sm="4">
            <v-btn
              block
              size="large"
              color="info"
              variant="tonal"
              prepend-icon="mdi-file-chart"
              @click="navigateTo('/jefe/reportes')"
            >
              Ver Reportes
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
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
// STATE - DATOS MOCK PARA LOS GRÁFICOS
// ============================================================================

// KPIs Superiores
const kpis = ref([
  {
    label: 'Total Activos',
    value: 42,
    icon: 'mdi-desktop-classic',
    color: 'blue'
  },
  {
    label: 'Operativos',
    value: 35,
    icon: 'mdi-check-circle',
    color: 'green'
  },
  {
    label: 'En Reparación',
    value: 5,
    icon: 'mdi-wrench',
    color: 'amber'
  },
  {
    label: 'De Baja',
    value: 2,
    icon: 'mdi-close-circle',
    color: 'red'
  }
])

// Datos para el gráfico de barras (Activos por Departamento)
const barChartData = ref({
  labels: ['UCI', 'Laboratorio', 'Radiología', 'Urgencias', 'Pediatría', 'Cirugía'],
  datasets: [
    {
      label: 'Cantidad de Activos',
      data: [6, 5, 8, 4, 7, 12],
      backgroundColor: [
        'rgba(33, 150, 243, 0.7)',   // Azul
        'rgba(76, 175, 80, 0.7)',    // Verde
        'rgba(255, 152, 0, 0.7)',    // Naranja
        'rgba(156, 39, 176, 0.7)',   // Púrpura
        'rgba(244, 67, 54, 0.7)',    // Rojo
        'rgba(0, 188, 212, 0.7)'     // Cyan
      ],
      borderColor: [
        'rgba(33, 150, 243, 1)',
        'rgba(76, 175, 80, 1)',
        'rgba(255, 152, 0, 1)',
        'rgba(156, 39, 176, 1)',
        'rgba(244, 67, 54, 1)',
        'rgba(0, 188, 212, 1)'
      ],
      borderWidth: 2
    }
  ]
})

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

// Datos para el gráfico de dona (Estado de Salud)
const doughnutChartData = ref({
  labels: ['Operativos', 'En Reparación', 'En Bodega', 'De Baja'],
  datasets: [
    {
      label: 'Estado de Activos',
      data: [35, 5, 0, 2],
      backgroundColor: [
        'rgba(76, 175, 80, 0.8)',    // Verde
        'rgba(255, 193, 7, 0.8)',    // Amarillo
        'rgba(33, 150, 243, 0.8)',   // Azul
        'rgba(244, 67, 54, 0.8)'     // Rojo
      ],
      borderColor: [
        'rgba(76, 175, 80, 1)',
        'rgba(255, 193, 7, 1)',
        'rgba(33, 150, 243, 1)',
        'rgba(244, 67, 54, 1)'
      ],
      borderWidth: 2
    }
  ]
})

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
// METHODS
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
 * Al montar el componente, se pueden cargar datos reales desde la API
 * Por ahora usamos datos mock
 */
onMounted(() => {
  console.log('Dashboard Jefe de Departamento cargado')
  // TODO: Aquí se pueden cargar datos reales desde la API
  // await fetchDashboardData()
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


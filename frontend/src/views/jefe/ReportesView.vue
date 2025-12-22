<template>
  <div class="reportes-content">
    <!-- ====================================================================
         TARJETA DE TÍTULO
         ==================================================================== -->
    <v-card variant="tonal" color="info" class="mb-4">
      <v-card-text>
        <h2 class="text-h5 font-weight-bold mb-1">
          <v-icon class="mr-2">mdi-file-chart</v-icon>
          Reportes y Análisis
        </h2>
        <p class="text-subtitle-1 mb-0">Visualiza estadísticas y genera reportes personalizados</p>
      </v-card-text>
    </v-card>

    <!-- ====================================================================
         FILTROS DE REPORTES
         ==================================================================== -->
    <v-card class="mb-4" elevation="2">
      <v-card-title class="text-h6 font-weight-bold">
        Filtros de Búsqueda
      </v-card-title>
      <v-card-text>
        <v-row>
          <v-col cols="12" md="4">
            <v-select
              label="Tipo de Reporte"
              :items="tiposReporte"
              variant="outlined"
              density="comfortable"
              prepend-inner-icon="mdi-file-document"
            ></v-select>
          </v-col>
          <v-col cols="12" md="4">
            <v-select
              label="Departamento"
              :items="departamentos"
              variant="outlined"
              density="comfortable"
              prepend-inner-icon="mdi-office-building"
            ></v-select>
          </v-col>
          <v-col cols="12" md="4">
            <v-select
              label="Período"
              :items="periodos"
              variant="outlined"
              density="comfortable"
              prepend-inner-icon="mdi-calendar"
            ></v-select>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <v-btn
              block
              color="primary"
              size="large"
              prepend-icon="mdi-magnify"
            >
              Generar Reporte
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- ====================================================================
         REPORTES RÁPIDOS
         ==================================================================== -->
    <v-card elevation="2">
      <v-card-title class="text-h6 font-weight-bold">
        Reportes Rápidos
      </v-card-title>
      <v-card-text>
        <v-row>
          <v-col
            v-for="(reporte, index) in reportesRapidos"
            :key="index"
            cols="12"
            sm="6"
            md="4"
          >
            <v-card
              :color="reporte.color"
              dark
              elevation="4"
              class="reporte-card"
              @click="generarReporte(reporte.tipo)"
            >
              <v-card-text>
                <div class="text-center">
                  <v-icon size="48" class="mb-3">{{ reporte.icon }}</v-icon>
                  <div class="text-h6 font-weight-bold mb-2">
                    {{ reporte.titulo }}
                  </div>
                  <div class="text-caption">
                    {{ reporte.descripcion }}
                  </div>
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// ============================================================================
// STATE
// ============================================================================

const tiposReporte = ref([
  'Inventario Completo',
  'Movimientos por Período',
  'Estado de Activos',
  'Activos por Departamento',
  'Historial de Mantenimiento'
])

const departamentos = ref([
  'Todos',
  'UCI',
  'Laboratorio',
  'Radiología',
  'Urgencias',
  'Pediatría',
  'Cirugía'
])

const periodos = ref([
  'Última Semana',
  'Último Mes',
  'Último Trimestre',
  'Último Año',
  'Personalizado'
])

const reportesRapidos = ref([
  {
    titulo: 'Inventario Actual',
    descripcion: 'Estado completo de todos los activos',
    icon: 'mdi-clipboard-list',
    color: 'blue',
    tipo: 'inventario'
  },
  {
    titulo: 'Movimientos Recientes',
    descripcion: 'Últimos 30 días de actividad',
    icon: 'mdi-swap-horizontal',
    color: 'green',
    tipo: 'movimientos'
  },
  {
    titulo: 'Activos en Reparación',
    descripcion: 'Equipos en mantenimiento',
    icon: 'mdi-wrench',
    color: 'amber',
    tipo: 'reparacion'
  }
])

// ============================================================================
// METHODS
// ============================================================================

function generarReporte(tipo) {
  console.log('Generando reporte:', tipo)
  // TODO: Implementar lógica de generación de reportes
  alert(`Generando reporte de tipo: ${tipo}`)
}
</script>

<style scoped>
.reportes-content {
  min-height: calc(100vh - 112px);
  background: #f5f7fa;
  padding: 1rem;
  padding-bottom: 80px;
}

.reporte-card {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
}

.reporte-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.25) !important;
}

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


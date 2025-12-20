<template>
  <div class="herramientas-content">
    <!-- ====================================================================
         HEADER
         ==================================================================== -->
    <v-card variant="tonal" color="primary" class="mb-4">
      <v-card-text>
        <h2 class="text-h5 font-weight-bold mb-1">Herramientas Adicionales</h2>
        <p class="text-subtitle-1 mb-0">Acciones especiales del sistema</p>
      </v-card-text>
    </v-card>

    <!-- ====================================================================
         GESTIÓN DE ACTIVIDAD
         ==================================================================== -->
    <v-card class="mb-4">
      <v-card-title class="text-h6 font-weight-bold">
        Gestión de Actividad
      </v-card-title>
      <v-card-text>
        <v-row>
          <v-col
            v-for="(herramienta, index) in herramientasActividad"
            :key="index"
            cols="12"
            sm="6"
            md="4"
          >
            <v-card
              class="herramienta-card"
              elevation="2"
              @click="navigateTo(herramienta.route)"
            >
              <v-card-text class="text-center pa-6">
                <v-avatar
                  :color="herramienta.color"
                  size="64"
                  class="mb-4"
                >
                  <v-icon size="32" color="white">
                    {{ herramienta.icon }}
                  </v-icon>
                </v-avatar>
                
                <h3 class="text-h6 font-weight-bold mb-2">
                  {{ herramienta.nombre }}
                </h3>
                
                <p class="text-body-2 text-grey-darken-1">
                  {{ herramienta.descripcion }}
                </p>
              </v-card-text>

              <v-divider></v-divider>

              <v-card-actions class="pa-3">
                <v-btn
                  block
                  :color="herramienta.color"
                  variant="text"
                >
                  Abrir
                  <v-icon end>mdi-arrow-right</v-icon>
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- ====================================================================
         HERRAMIENTAS DE IMPRESIÓN
         ==================================================================== -->
    <v-card class="mb-4">
      <v-card-title class="text-h6 font-weight-bold">
        Herramientas
      </v-card-title>
      <v-card-text>
        <v-row>
          <v-col
            v-for="(herramienta, index) in herramientasImpresion"
            :key="index"
            cols="12"
            sm="6"
            md="4"
          >
            <v-card
              class="herramienta-card"
              elevation="2"
              @click="manejarClick(herramienta)"
            >
              <v-card-text class="text-center pa-6">
                <v-avatar
                  :color="herramienta.color"
                  size="64"
                  class="mb-4"
                >
                  <v-icon size="32" color="white">
                    {{ herramienta.icon }}
                  </v-icon>
                </v-avatar>
                
                <h3 class="text-h6 font-weight-bold mb-2">
                  {{ herramienta.nombre }}
                </h3>
                
                <p class="text-body-2 text-grey-darken-1">
                  {{ herramienta.descripcion }}
                </p>
              </v-card-text>

              <v-divider></v-divider>

              <v-card-actions class="pa-3">
                <v-btn
                  block
                  :color="herramienta.color"
                  variant="text"
                >
                  Abrir
                  <v-icon end>mdi-arrow-right</v-icon>
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- ====================================================================
         MANTENIMIENTO DEL SISTEMA
         ==================================================================== -->
    <v-card class="mb-4">
      <v-card-title class="text-h6 font-weight-bold">
        Mantenimiento del Sistema
      </v-card-title>
      <v-card-text>
        <v-row>
          <v-col
            v-for="(herramienta, index) in herramientasMantenimiento"
            :key="index"
            cols="12"
            sm="6"
            md="4"
          >
            <v-card
              class="herramienta-card"
              elevation="2"
              @click="manejarClick(herramienta)"
            >
              <v-card-text class="text-center pa-6">
                <v-avatar
                  :color="herramienta.color"
                  size="64"
                  class="mb-4"
                >
                  <v-icon size="32" color="white">
                    {{ herramienta.icon }}
                  </v-icon>
                </v-avatar>
                
                <h3 class="text-h6 font-weight-bold mb-2">
                  {{ herramienta.nombre }}
                </h3>
                
                <p class="text-body-2 text-grey-darken-1">
                  {{ herramienta.descripcion }}
                </p>
              </v-card-text>

              <v-divider></v-divider>

              <v-card-actions class="pa-3">
                <v-btn
                  block
                  :color="herramienta.color"
                  variant="text"
                >
                  {{ herramienta.accion || 'Abrir' }}
                  <v-icon end>mdi-arrow-right</v-icon>
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- ====================================================================
         DIÁLOGO RESPALDO
         ==================================================================== -->
    <v-dialog v-model="dialogoRespaldo" max-width="500px">
      <v-card>
        <v-card-title class="text-h5 pa-4 bg-info text-white">
          <v-icon start>mdi-database-export</v-icon>
          Respaldo de Datos
        </v-card-title>
        
        <v-card-text class="pa-4">
          <p class="mb-3">¿Qué deseas exportar?</p>
          
          <v-radio-group v-model="tipoRespaldo">
            <v-radio
              label="Todos los datos"
              value="completo"
            ></v-radio>
            <v-radio
              label="Solo activos"
              value="activos"
            ></v-radio>
            <v-radio
              label="Solo usuarios"
              value="usuarios"
            ></v-radio>
            <v-radio
              label="Solo historial"
              value="historial"
            ></v-radio>
          </v-radio-group>
        </v-card-text>

        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn
            variant="text"
            @click="dialogoRespaldo = false"
          >
            Cancelar
          </v-btn>
          <v-btn
            color="info"
            @click="generarRespaldo"
          >
            Exportar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- ====================================================================
         SNACKBAR NOTIFICACIONES
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
 * HERRAMIENTAS ADICIONALES
 * ============================================================================
 *
 * Vista centralizada para acciones especiales y herramientas del sistema
 */

import { ref } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/services/api'

// ============================================================================
// COMPOSABLES
// ============================================================================

const router = useRouter()

// ============================================================================
// STATE
// ============================================================================

const herramientasActividad = ref([
  {
    nombre: 'Movimientos',
    descripcion: 'Registro de movimientos de activos',
    icon: 'mdi-swap-horizontal',
    color: 'blue',
    route: '/admin/movimientos'
  },
  {
    nombre: 'Historial',
    descripcion: 'Historial completo de cambios',
    icon: 'mdi-history',
    color: 'indigo',
    route: '/admin/historial'
  },
  {
    nombre: 'Reportes',
    descripcion: 'Generar reportes del sistema',
    icon: 'mdi-file-chart',
    color: 'teal',
    route: '/admin/reportes'
  }
])

const herramientasImpresion = ref([
  {
    nombre: 'Imprimir QR',
    descripcion: 'Generar etiquetas QR para activos',
    icon: 'mdi-qrcode',
    color: 'purple',
    route: '/admin/imprimir-qr'
  },
  {
    nombre: 'Auditoría',
    descripcion: 'Registro de acciones de usuarios',
    icon: 'mdi-clipboard-check',
    color: 'orange',
    route: '/admin/auditoria'
  }
])

const herramientasMantenimiento = ref([
  {
    nombre: 'Respaldo de Datos',
    descripcion: 'Exportar base de datos',
    icon: 'mdi-database-export',
    color: 'cyan',
    accion: 'Exportar',
    tipo: 'dialog',
    dialog: 'respaldo'
  },
  {
    nombre: 'Configuración',
    descripcion: 'Ajustes generales del sistema',
    icon: 'mdi-cog',
    color: 'amber',
    route: '/admin/configuracion'
  }
])

const dialogoRespaldo = ref(false)
const dialogoLimpiar = ref(false)
const tipoRespaldo = ref('completo')
const opcionesLimpiar = ref([])

const snackbar = ref({
  show: false,
  text: '',
  color: 'success'
})

// ============================================================================
// MÉTODOS - NAVEGACIÓN Y CLICKS
// ============================================================================

/**
 * Navega a una ruta específica
 */
function navigateTo(route) {
  router.push(route)
}

/**
 * Maneja el click en una herramienta
 */
function manejarClick(herramienta) {
  if (herramienta.tipo === 'dialog') {
    if (herramienta.dialog === 'respaldo') {
      abrirDialogoRespaldo()
    } else if (herramienta.dialog === 'limpiar') {
      abrirDialogoLimpiar()
    }
  } else if (herramienta.route) {
    navigateTo(herramienta.route)
  }
}

// ============================================================================
// MÉTODOS - DIÁLOGOS
// ============================================================================

/**
 * Abre el diálogo de respaldo
 */
function abrirDialogoRespaldo() {
  tipoRespaldo.value = 'completo'
  dialogoRespaldo.value = true
}

/**
 * Abre el diálogo de limpieza
 */
function abrirDialogoLimpiar() {
  opcionesLimpiar.value = []
  dialogoLimpiar.value = true
}

// ============================================================================
// MÉTODOS - ACCIONES
// ============================================================================

/**
 * Genera un respaldo de datos
 */
async function generarRespaldo() {
  try {
    // TODO: Implementar llamada al endpoint de respaldo
    // const response = await apiClient.post('/api/respaldo/', {
    //   tipo: tipoRespaldo.value
    // })
    
    mostrarNotificacion('Respaldo generado correctamente', 'success')
    dialogoRespaldo.value = false
    
    console.log('Generando respaldo:', tipoRespaldo.value)
    
  } catch (error) {
    console.error('Error al generar respaldo:', error)
    mostrarNotificacion('Error al generar el respaldo', 'error')
  }
}

/**
 * Limpia registros seleccionados
 */
async function limpiarRegistros() {
  try {
    // TODO: Implementar llamada al endpoint de limpieza
    // const response = await apiClient.post('/api/limpiar/', {
    //   opciones: opcionesLimpiar.value
    // })
    
    mostrarNotificacion('Registros limpiados correctamente', 'success')
    dialogoLimpiar.value = false
    opcionesLimpiar.value = []
    
    console.log('Limpiando:', opcionesLimpiar.value)
    
  } catch (error) {
    console.error('Error al limpiar registros:', error)
    mostrarNotificacion('Error al limpiar los registros', 'error')
  }
}

/**
 * Muestra una notificación snackbar
 */
function mostrarNotificacion(text, color = 'success') {
  snackbar.value = {
    show: true,
    text,
    color
  }
}

</script>

<style scoped>
/* ============================================================================
   CONTENEDOR PRINCIPAL
   ============================================================================ */

.herramientas-content {
  min-height: calc(100vh - 112px);
  background: #f5f7fa;
  padding: 1rem;
  padding-bottom: 80px;
}

/* ============================================================================
   TARJETAS DE HERRAMIENTAS
   ============================================================================ */

.herramienta-card {
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  height: 100%;
  border-radius: 12px !important;
}

.herramienta-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15) !important;
}

.herramienta-card:active {
  transform: translateY(-4px);
}

/* ============================================================================
   RESPONSIVE ADJUSTMENTS
   ============================================================================ */

@media (max-width: 600px) {
  .herramientas-content {
    padding: 0.75rem;
  }
}

@media (min-width: 960px) {
  .herramientas-content {
    max-width: 1400px;
    margin: 0 auto;
  }
}
</style>
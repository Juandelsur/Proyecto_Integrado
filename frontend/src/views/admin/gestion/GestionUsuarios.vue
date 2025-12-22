<template>
  <div class="crud-entidad-content">
    <!-- ====================================================================
         HEADER CON TÍTULO Y BOTÓN NUEVO
         ==================================================================== -->
    <div class="header-section">
      <h1 class="entity-title">Gestión de Usuarios</h1>
      <v-btn
        color="blue"
        size="large"
        class="btn-nuevo"
        prepend-icon="mdi-plus"
        @click="abrirModalCrear"
      >
        Nuevo
      </v-btn>
    </div>

    <!-- ====================================================================
         BARRA DE BÚSQUEDA Y FILTROS
         ==================================================================== -->
    <div class="search-section">
      <v-text-field
        v-model="busqueda"
        prepend-inner-icon="mdi-magnify"
        label="Buscar por nombre, username o email"
        variant="outlined"
        density="comfortable"
        clearable
        @input="filtrarRegistros"
        class="mb-3"
      ></v-text-field>

      <!-- Filtros Desplegables -->
      <v-row dense>
        <v-col cols="12" sm="4">
          <v-select
            v-model="filtroRol"
            :items="rolesDisponibles"
            item-title="nombre_rol"
            item-value="id"
            label="Filtrar por Rol"
            variant="outlined"
            density="comfortable"
            clearable
            prepend-inner-icon="mdi-account-key"
            @update:model-value="filtrarRegistros"
          ></v-select>
        </v-col>
        <v-col cols="12" sm="4">
          <v-select
            v-model="filtroActivo"
            :items="[
              { text: 'Activos', value: true },
              { text: 'Inactivos', value: false }
            ]"
            item-title="text"
            item-value="value"
            label="Filtrar por Estado"
            variant="outlined"
            density="comfortable"
            clearable
            prepend-inner-icon="mdi-account-check"
            @update:model-value="filtrarRegistros"
          ></v-select>
        </v-col>
        <v-col cols="12" sm="4">
          <v-select
            v-model="filtroStaff"
            :items="[
              { text: 'Staff', value: true },
              { text: 'No Staff', value: false }
            ]"
            item-title="text"
            item-value="value"
            label="Filtrar por Staff"
            variant="outlined"
            density="comfortable"
            clearable
            prepend-inner-icon="mdi-shield-account"
            @update:model-value="filtrarRegistros"
          ></v-select>
        </v-col>
      </v-row>

      <!-- Contador de resultados -->
      <div class="text-caption text-grey mt-2">
        Mostrando {{ registrosMostrados.length }} de {{ registrosFiltrados.length }} usuarios
      </div>
    </div>

    <!-- ====================================================================
         LOADING STATE
         ==================================================================== -->
    <div v-if="loading" class="loading-container">
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
      <p class="mt-3">Cargando usuarios...</p>
    </div>

    <!-- ====================================================================
         LISTA DE REGISTROS
         ==================================================================== -->
    <div v-else class="registros-lista">
      <div
        v-for="registro in registrosMostrados"
        :key="registro.id"
        class="registro-item"
      >
        <div class="registro-info">
          <div class="registro-nombre">
            {{ registro.nombre_completo }}
          </div>
          <div class="registro-detalles">
            <span class="detalle-username">@{{ registro.username }}</span>
            <span class="detalle-separador">•</span>
            <span class="detalle-rol">{{ registro.rol?.nombre_rol || 'Sin rol' }}</span>
            <span class="detalle-separador">•</span>
            <v-chip
              :color="registro.is_active ? 'success' : 'error'"
              size="x-small"
              class="ml-1"
            >
              {{ registro.is_active ? 'Activo' : 'Inactivo' }}
            </v-chip>
            <v-chip
              v-if="registro.is_staff"
              color="purple"
              size="x-small"
              class="ml-1"
            >
              Staff
            </v-chip>
          </div>
        </div>
        <div class="registro-acciones">
          <v-btn
            color="blue-grey-lighten-1"
            size="small"
            icon="mdi-eye"
            class="btn-accion"
            @click="abrirModalVer(registro)"
          ></v-btn>
          <v-btn
            color="yellow-darken-2"
            size="small"
            icon="mdi-pencil"
            class="btn-accion"
            @click="abrirModalEditar(registro)"
          ></v-btn>
          <v-btn
            color="red-lighten-1"
            size="small"
            icon="mdi-delete"
            class="btn-accion"
            @click="confirmarEliminar(registro)"
          ></v-btn>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="registrosMostrados.length === 0" class="empty-state">
        <v-icon size="64" color="grey-lighten-1">mdi-inbox</v-icon>
        <p>No hay usuarios disponibles</p>
      </div>

      <!-- Botón Cargar Más -->
      <div v-if="registrosFiltrados.length > registrosMostrados.length" class="load-more-section">
        <v-btn
          variant="outlined"
          color="primary"
          size="large"
          prepend-icon="mdi-refresh"
          @click="cargarMasRegistros"
        >
          Cargar más ({{ registrosFiltrados.length - registrosMostrados.length }} restantes)
        </v-btn>
      </div>
    </div>

    <!-- ====================================================================
         BOTÓN VOLVER
         ==================================================================== -->
    <div class="footer-section">
      <v-btn
        variant="outlined"
        size="large"
        prepend-icon="mdi-arrow-left"
        class="btn-volver"
        @click="volver"
      >
        Volver
      </v-btn>
    </div>

    <!-- ====================================================================
         MODAL VER DETALLES (SOLO LECTURA)
         ==================================================================== -->
    <v-dialog v-model="showViewModal" max-width="600px" scrollable>
      <v-card>
        <v-card-title class="text-h5 pa-4 bg-blue-grey-lighten-1 text-white">
          <v-icon start>mdi-account-details</v-icon>
          Detalles del Usuario
        </v-card-title>
        
        <v-card-text class="pa-4">
          <v-list lines="two" class="py-0">
            <v-list-item>
              <template v-slot:prepend>
                <v-icon color="primary">mdi-identifier</v-icon>
              </template>
              <v-list-item-title class="text-subtitle-2 text-grey-darken-1">
                ID
              </v-list-item-title>
              <v-list-item-subtitle class="text-body-1 text-black mt-1">
                {{ registroVer?.id || 'N/A' }}
              </v-list-item-subtitle>
            </v-list-item>

            <v-divider class="my-2"></v-divider>

            <v-list-item>
              <template v-slot:prepend>
                <v-icon color="primary">mdi-account</v-icon>
              </template>
              <v-list-item-title class="text-subtitle-2 text-grey-darken-1">
                Nombre de Usuario
              </v-list-item-title>
              <v-list-item-subtitle class="text-body-1 text-black mt-1">
                @{{ registroVer?.username || 'N/A' }}
              </v-list-item-subtitle>
            </v-list-item>

            <v-divider class="my-2"></v-divider>

            <v-list-item>
              <template v-slot:prepend>
                <v-icon color="primary">mdi-account-circle</v-icon>
              </template>
              <v-list-item-title class="text-subtitle-2 text-grey-darken-1">
                Nombre Completo
              </v-list-item-title>
              <v-list-item-subtitle class="text-body-1 text-black mt-1">
                {{ registroVer?.nombre_completo || 'N/A' }}
              </v-list-item-subtitle>
            </v-list-item>

            <v-divider class="my-2"></v-divider>

            <v-list-item>
              <template v-slot:prepend>
                <v-icon color="primary">mdi-email</v-icon>
              </template>
              <v-list-item-title class="text-subtitle-2 text-grey-darken-1">
                Correo Electrónico
              </v-list-item-title>
              <v-list-item-subtitle class="text-body-1 text-black mt-1">
                {{ registroVer?.email || 'N/A' }}
              </v-list-item-subtitle>
            </v-list-item>

            <v-divider class="my-2"></v-divider>

            <v-list-item>
              <template v-slot:prepend>
                <v-icon color="primary">mdi-account-key</v-icon>
              </template>
              <v-list-item-title class="text-subtitle-2 text-grey-darken-1">
                Rol
              </v-list-item-title>
              <v-list-item-subtitle class="text-body-1 text-black mt-1">
                {{ registroVer?.rol?.nombre_rol || 'Sin rol' }}
              </v-list-item-subtitle>
            </v-list-item>

            <v-divider class="my-2"></v-divider>

            <v-list-item>
              <template v-slot:prepend>
                <v-icon color="primary">mdi-check-circle</v-icon>
              </template>
              <v-list-item-title class="text-subtitle-2 text-grey-darken-1">
                Estado
              </v-list-item-title>
              <v-list-item-subtitle class="mt-1">
                <v-chip
                  :color="registroVer?.is_active ? 'success' : 'error'"
                  size="small"
                >
                  {{ registroVer?.is_active ? 'Activo' : 'Inactivo' }}
                </v-chip>
              </v-list-item-subtitle>
            </v-list-item>

            <v-divider class="my-2"></v-divider>

            <v-list-item>
              <template v-slot:prepend>
                <v-icon color="primary">mdi-shield-account</v-icon>
              </template>
              <v-list-item-title class="text-subtitle-2 text-grey-darken-1">
                Staff
              </v-list-item-title>
              <v-list-item-subtitle class="mt-1">
                <v-chip
                  :color="registroVer?.is_staff ? 'purple' : 'grey'"
                  size="small"
                >
                  {{ registroVer?.is_staff ? 'Sí' : 'No' }}
                </v-chip>
              </v-list-item-subtitle>
            </v-list-item>

            <v-divider class="my-2"></v-divider>

            <v-list-item>
              <template v-slot:prepend>
                <v-icon color="primary">mdi-calendar-plus</v-icon>
              </template>
              <v-list-item-title class="text-subtitle-2 text-grey-darken-1">
                Fecha de Registro
              </v-list-item-title>
              <v-list-item-subtitle class="text-body-1 text-black mt-1">
                {{ formatearFecha(registroVer?.date_joined) }}
              </v-list-item-subtitle>
            </v-list-item>

            <v-divider class="my-2"></v-divider>

            <v-list-item>
              <template v-slot:prepend>
                <v-icon color="primary">mdi-login</v-icon>
              </template>
              <v-list-item-title class="text-subtitle-2 text-grey-darken-1">
                Último Inicio de Sesión
              </v-list-item-title>
              <v-list-item-subtitle class="text-body-1 text-black mt-1">
                {{ formatearFecha(registroVer?.last_login) || 'Nunca' }}
              </v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </v-card-text>

        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            @click="showViewModal = false"
          >
            Cerrar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- ====================================================================
         MODAL CREAR/EDITAR
         ==================================================================== -->
    <v-dialog v-model="showModal" max-width="700px" scrollable>
      <v-card>
        <v-card-title class="text-h5 pa-4 bg-primary text-white">
          <v-icon start>mdi-account-cog</v-icon>
          {{ modoEdicion ? 'Editar Usuario' : 'Nuevo Usuario' }}
        </v-card-title>
        
        <v-card-text class="pa-4">
          <v-form ref="formRef">
            <!-- Username -->
            <v-text-field
              v-model="formulario.username"
              label="Nombre de Usuario *"
              variant="outlined"
              density="comfortable"
              prepend-inner-icon="mdi-account"
              :rules="[v => !!v || 'Campo requerido']"
              :readonly="modoEdicion"
              :hint="modoEdicion ? 'El username no se puede modificar' : 'Único e inmutable'"
              persistent-hint
              class="mb-2"
            ></v-text-field>

            <!-- Nombre Completo -->
            <v-text-field
              v-model="formulario.nombre_completo"
              label="Nombre Completo *"
              variant="outlined"
              density="comfortable"
              prepend-inner-icon="mdi-account-circle"
              :rules="[v => !!v || 'Campo requerido']"
              class="mb-2"
            ></v-text-field>

            <!-- Email -->
            <v-text-field
              v-model="formulario.email"
              label="Correo Electrónico *"
              variant="outlined"
              density="comfortable"
              prepend-inner-icon="mdi-email"
              type="email"
              :rules="[
                v => !!v || 'Campo requerido',
                v => /.+@.+\..+/.test(v) || 'Email inválido'
              ]"
              class="mb-2"
            ></v-text-field>

            <!-- Contraseña -->
            <v-text-field
              v-model="formulario.password"
              :label="modoEdicion ? 'Nueva Contraseña (dejar vacío para no cambiar)' : 'Contraseña *'"
              variant="outlined"
              density="comfortable"
              prepend-inner-icon="mdi-lock"
              :append-inner-icon="mostrarPassword ? 'mdi-eye' : 'mdi-eye-off'"
              :type="mostrarPassword ? 'text' : 'password'"
              :rules="modoEdicion ? [] : [v => !!v || 'Campo requerido', v => (v && v.length >= 6) || 'Mínimo 6 caracteres']"
              @click:append-inner="mostrarPassword = !mostrarPassword"
              hint="Mínimo 6 caracteres"
              persistent-hint
              class="mb-2"
            ></v-text-field>

            <!-- Rol -->
            <v-select
              v-model="formulario.rol_id"
              :items="roles"
              item-title="nombre_rol"
              item-value="id"
              label="Rol *"
              variant="outlined"
              density="comfortable"
              prepend-inner-icon="mdi-account-key"
              :rules="[v => !!v || 'Campo requerido']"
              class="mb-2"
            ></v-select>

            <!-- Switches en una fila -->
            <v-row dense class="mt-2">
              <v-col cols="6">
                <v-switch
                  v-model="formulario.is_active"
                  label="Usuario Activo"
                  color="success"
                  hide-details
                ></v-switch>
              </v-col>
              <v-col cols="6">
                <v-switch
                  v-model="formulario.is_staff"
                  label="Staff"
                  color="purple"
                  hide-details
                ></v-switch>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>

        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn
            variant="text"
            @click="cerrarModal"
          >
            Cancelar
          </v-btn>
          <v-btn
            color="primary"
            @click="guardar"
          >
            {{ modoEdicion ? 'Actualizar' : 'Crear' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- ====================================================================
         MODAL CONFIRMAR ELIMINACIÓN
         ==================================================================== -->
    <v-dialog v-model="showDeleteDialog" max-width="400px">
      <v-card>
        <v-card-title class="text-h5 pa-4">
          <v-icon start color="error">mdi-alert-circle</v-icon>
          Confirmar Eliminación
        </v-card-title>
        
        <v-card-text class="pa-4">
          ¿Estás seguro de que deseas eliminar este usuario?
          <br><br>
          <strong>{{ registroAEliminar?.nombre_completo }}</strong>
          <br>
          <span class="text-grey">@{{ registroAEliminar?.username }}</span>
          <br><br>
          <v-alert type="warning" density="compact" class="mt-2">
            Esta acción no se puede deshacer.
          </v-alert>
        </v-card-text>

        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn
            variant="text"
            @click="showDeleteDialog = false"
          >
            Cancelar
          </v-btn>
          <v-btn
            color="red"
            @click="eliminar"
          >
            Eliminar
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
 * GESTIÓN DE USUARIOS - CRUD COMPLETO
 * ============================================================================
 *
 * Funcionalidades:
 * - Listar usuarios con paginación (20 por página)
 * - Filtros desplegables (Rol, Estado Activo, Staff)
 * - Búsqueda por nombre, username o email
 * - Ver detalles completos (modal solo lectura)
 * - Crear nuevo usuario
 * - Editar usuario existente (incluyendo cambio de contraseña)
 * - Eliminar usuario
 */

import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/services/api'

// ============================================================================
// COMPOSABLES
// ============================================================================

const router = useRouter()

// ============================================================================
// STATE
// ============================================================================

const registros = ref([])
const roles = ref([])
const loading = ref(false)
const showModal = ref(false)
const showViewModal = ref(false)
const showDeleteDialog = ref(false)
const modoEdicion = ref(false)
const registroAEliminar = ref(null)
const registroVer = ref(null)
const busqueda = ref('')
const formRef = ref(null)
const registrosPorPagina = ref(20)
const paginaActual = ref(1)
const mostrarPassword = ref(false)

// Filtros
const filtroRol = ref(null)
const filtroActivo = ref(null)
const filtroStaff = ref(null)

const snackbar = ref({
  show: false,
  text: '',
  color: 'success'
})

const formulario = ref({
  id: null,
  username: '',
  password: '',
  email: '',
  nombre_completo: '',
  rol_id: null,
  is_active: true,
  is_staff: false
})

// ============================================================================
// COMPUTED
// ============================================================================

/**
 * Obtiene los roles únicos disponibles para el filtro
 */
const rolesDisponibles = computed(() => {
  return roles.value
})

/**
 * Filtra los registros según la búsqueda y los filtros desplegables
 */
const registrosFiltrados = computed(() => {
  let resultado = registros.value

  // Filtro de búsqueda de texto
  if (busqueda.value) {
    const termino = busqueda.value.toLowerCase()
    resultado = resultado.filter(registro => {
      return (
        registro.nombre_completo?.toLowerCase().includes(termino) ||
        registro.username?.toLowerCase().includes(termino) ||
        registro.email?.toLowerCase().includes(termino)
      )
    })
  }

  // Filtro por rol
  if (filtroRol.value !== null) {
    resultado = resultado.filter(registro => 
      registro.rol?.id === filtroRol.value
    )
  }

  // Filtro por estado activo
  if (filtroActivo.value !== null) {
    resultado = resultado.filter(registro => 
      registro.is_active === filtroActivo.value
    )
  }

  // Filtro por staff
  if (filtroStaff.value !== null) {
    resultado = resultado.filter(registro => 
      registro.is_staff === filtroStaff.value
    )
  }

  return resultado
})

/**
 * Registros a mostrar con paginación (20 por defecto)
 */
const registrosMostrados = computed(() => {
  const limite = paginaActual.value * registrosPorPagina.value
  return registrosFiltrados.value.slice(0, limite)
})

// ============================================================================
// MÉTODOS - API
// ============================================================================

/**
 * Carga todos los usuarios desde la API
 */
async function cargarRegistros() {
  loading.value = true
  try {
    const response = await apiClient.get('/api/usuarios/', {
      params: { page_size: 1000 }
    })
    
    registros.value = Array.isArray(response.data) 
      ? response.data 
      : response.data.results || []

    // Si hay paginación, obtener todas las páginas
    if (response.data.next) {
      await cargarTodasLasPaginas(response.data.next)
    }
      
  } catch (error) {
    console.error('Error al cargar usuarios:', error)
    mostrarNotificacion('Error al cargar los usuarios', 'error')
  } finally {
    loading.value = false
  }
}

/**
 * Carga todas las páginas si la API está paginada
 */
async function cargarTodasLasPaginas(nextUrl) {
  try {
    while (nextUrl) {
      const response = await apiClient.get(nextUrl)
      const nuevosRegistros = Array.isArray(response.data) ? response.data : response.data.results || []
      registros.value = [...registros.value, ...nuevosRegistros]
      nextUrl = response.data.next || null
    }
  } catch (error) {
    console.error('Error al cargar páginas adicionales:', error)
  }
}

/**
 * Carga los roles para el select
 */
async function cargarRoles() {
  try {
    const response = await apiClient.get('/api/roles/', {
      params: { page_size: 1000 }
    })
    roles.value = Array.isArray(response.data) ? response.data : response.data.results || []
  } catch (error) {
    console.error('Error al cargar roles:', error)
  }
}

/**
 * Guarda un nuevo usuario o actualiza uno existente
 */
async function guardar() {
  // Validar formulario
  const { valid } = await formRef.value.validate()
  if (!valid) return

  try {
    // Preparar payload
    const payload = {
      username: formulario.value.username?.trim(),
      email: formulario.value.email?.trim(),
      nombre_completo: formulario.value.nombre_completo?.trim(),
      rol_id: formulario.value.rol_id,
      is_active: formulario.value.is_active,
      is_staff: formulario.value.is_staff
    }

    // Solo incluir password si se proporcionó
    if (formulario.value.password && formulario.value.password.trim() !== '') {
      payload.password = formulario.value.password
    }

    console.log('📤 Enviando payload:', payload)

    if (modoEdicion.value) {
      // Actualizar usuario existente
      await apiClient.put(
        `/api/usuarios/${formulario.value.id}/`,
        payload
      )
      mostrarNotificacion('Usuario actualizado correctamente', 'success')
    } else {
      // Crear nuevo usuario
      await apiClient.post('/api/usuarios/', payload)
      mostrarNotificacion('Usuario creado correctamente', 'success')
    }
    
    cerrarModal()
    await cargarRegistros()
    
  } catch (error) {
    console.error('❌ Error al guardar:', error)
    
    // Mostrar error detallado del servidor
    if (error.response?.data) {
      console.error('📥 Detalle del error:', error.response.data)
      
      let mensajeError = 'Error al guardar el usuario'
      
      if (typeof error.response.data === 'object') {
        const errores = []
        for (const [campo, mensajes] of Object.entries(error.response.data)) {
          if (Array.isArray(mensajes)) {
            errores.push(`${campo}: ${mensajes.join(', ')}`)
          } else {
            errores.push(`${campo}: ${mensajes}`)
          }
        }
        mensajeError = errores.join(' | ')
      }
      
      mostrarNotificacion(mensajeError, 'error')
    } else {
      mostrarNotificacion('Error al guardar el usuario', 'error')
    }
  }
}

/**
 * Elimina un usuario
 */
async function eliminar() {
  try {
    await apiClient.delete(`/api/usuarios/${registroAEliminar.value.id}/`)
    
    mostrarNotificacion('Usuario eliminado correctamente', 'success')
    showDeleteDialog.value = false
    registroAEliminar.value = null
    await cargarRegistros()
    
  } catch (error) {
    console.error('❌ Error al eliminar:', error)
    
    if (error.response?.status === 500 || error.response?.status === 400) {
      mostrarNotificacion(
        'No se puede eliminar este usuario. Puede estar relacionado con otros registros.', 
        'error'
      )
    } else {
      mostrarNotificacion('Error al eliminar el usuario', 'error')
    }
    
    showDeleteDialog.value = false
    registroAEliminar.value = null
  }
}

// ============================================================================
// MÉTODOS - UI
// ============================================================================

/**
 * Abre el modal para ver los detalles de un usuario (solo lectura)
 */
function abrirModalVer(registro) {
  registroVer.value = registro
  showViewModal.value = true
}

/**
 * Abre el modal para crear un nuevo usuario
 */
function abrirModalCrear() {
  modoEdicion.value = false
  formulario.value = {
    id: null,
    username: '',
    password: '',
    email: '',
    nombre_completo: '',
    rol_id: null,
    is_active: true,
    is_staff: false
  }
  showModal.value = true
}

/**
 * Abre el modal para editar un usuario existente
 */
function abrirModalEditar(registro) {
  modoEdicion.value = true
  formulario.value = {
    id: registro.id,
    username: registro.username,
    password: '', // Dejar vacío para no cambiar
    email: registro.email,
    nombre_completo: registro.nombre_completo,
    rol_id: registro.rol?.id || null,
    is_active: registro.is_active,
    is_staff: registro.is_staff
  }
  showModal.value = true
}

/**
 * Cierra el modal de crear/editar
 */
function cerrarModal() {
  showModal.value = false
  mostrarPassword.value = false
  if (formRef.value) {
    formRef.value.reset()
  }
}

/**
 * Abre el diálogo de confirmación para eliminar
 */
function confirmarEliminar(registro) {
  registroAEliminar.value = registro
  showDeleteDialog.value = true
}

/**
 * Filtra los registros (método auxiliar)
 */
function filtrarRegistros() {
  // Reiniciar la paginación cuando se aplica un filtro
  paginaActual.value = 1
}

/**
 * Carga más registros (incrementa la paginación)
 */
function cargarMasRegistros() {
  paginaActual.value++
}

/**
 * Formatea una fecha ISO a formato legible
 */
function formatearFecha(fecha) {
  if (!fecha) return 'N/A'
  
  try {
    const date = new Date(fecha)
    return date.toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch (error) {
    return fecha
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

/**
 * Vuelve a la página anterior
 */
function volver() {
  router.back()
}

// ============================================================================
// LIFECYCLE HOOKS
// ============================================================================

onMounted(async () => {
  await Promise.all([
    cargarRegistros(),
    cargarRoles()
  ])
})

</script>

<style scoped>
/* ============================================================================
   CONTENEDOR PRINCIPAL
   ============================================================================ */

.crud-entidad-content {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 1rem;
  max-width: 9000px;
  margin: 0 auto;
  padding-bottom: 2rem;
}

/* ============================================================================
   HEADER
   ============================================================================ */

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  gap: 1rem;
}

.entity-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.btn-nuevo {
  min-width: 120px;
  font-weight: 600;
}

/* ============================================================================
   BÚSQUEDA Y FILTROS
   ============================================================================ */

.search-section {
  margin-bottom: 1.5rem;
}

/* ============================================================================
   LISTA DE REGISTROS
   ============================================================================ */

.registros-lista {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 2rem;
}

.registro-item {
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  transition: all 0.2s ease;
}

.registro-item:hover {
  border-color: #1976d2;
  box-shadow: 0 2px 8px rgba(25, 118, 210, 0.15);
}

.registro-info {
  flex: 1;
  min-width: 0;
}

.registro-nombre {
  font-size: 1rem;
  color: #333;
  font-weight: 600;
  margin-bottom: 0.25rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.registro-detalles {
  font-size: 0.875rem;
  color: #666;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.detalle-username {
  font-family: monospace;
  background: #f5f5f5;
  padding: 0.125rem 0.5rem;
  border-radius: 4px;
}

.detalle-separador {
  color: #ccc;
}

.detalle-rol {
  color: #1976d2;
}

.registro-acciones {
  display: flex;
  gap: 0.5rem;
  flex-shrink: 0;
}

.btn-accion {
  min-width: 40px;
  height: 40px;
}

/* ============================================================================
   LOAD MORE
   ============================================================================ */

.load-more-section {
  display: flex;
  justify-content: center;
  margin-top: 1.5rem;
  padding: 1rem 0;
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
   EMPTY STATE
   ============================================================================ */

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 1rem;
  color: #999;
  gap: 1rem;
}

.empty-state p {
  font-size: 1rem;
  font-weight: 500;
}

/* ============================================================================
   FOOTER
   ============================================================================ */

.footer-section {
  display: flex;
  justify-content: flex-start;
  margin-top: 2rem;
}

.btn-volver {
  min-width: 120px;
  font-weight: 600;
}

/* ============================================================================
   RESPONSIVE
   ============================================================================ */

@media (max-width: 600px) {
  .crud-entidad-content {
    padding: 0.75rem;
  }

  .header-section {
    flex-direction: column;
    align-items: stretch;
  }

  .btn-nuevo {
    width: 100%;
  }

  .registro-item {
    flex-direction: column;
    align-items: stretch;
  }

  .registro-info {
    margin-bottom: 0.5rem;
  }

  .registro-acciones {
    justify-content: flex-end;
  }
}
</style>
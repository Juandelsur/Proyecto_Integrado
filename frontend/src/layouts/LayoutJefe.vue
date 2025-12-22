<template>
  <v-app>
    <v-app-bar color="primary" density="compact" elevation="2">
      <v-toolbar-title>SCA Hospital - Jefe</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn icon="mdi-logout" @click="logout" variant="text"></v-btn>
    </v-app-bar>

    <v-main class="bg-grey-lighten-4">
      <v-container fluid class="fill-height align-start pa-0">
        <router-view></router-view>
      </v-container>
    </v-main>

    <v-bottom-navigation
      v-model="activeTab"
      color="primary"
      active-color="primary"
      mode="shift"
      app 
      grow
      elevation="10"
    >
      <v-btn value="/jefe/home" to="/jefe/home">
        <v-icon>mdi-home</v-icon>
        <span>Inicio</span>
      </v-btn>

      <v-btn value="/jefe/scan" to="/jefe/scan">
        <v-icon>mdi-qrcode-scan</v-icon>
        <span>Escanear</span>
      </v-btn>

      <v-btn value="/jefe/reportes" to="/jefe/reportes">
        <v-icon>mdi-file-chart</v-icon>
        <span>Reportes</span>
      </v-btn>
    </v-bottom-navigation>
  </v-app>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const activeTab = ref('/jefe/home') // Valor por defecto

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

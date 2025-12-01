import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

// Importar estilos globales
import './assets/main.css'

// ============================================================================
// VUETIFY 3 CONFIGURATION
// ============================================================================
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          primary: '#1565C0', // Azul Hospital (coincide con tu diseño actual)
          secondary: '#0D47A1',
          success: '#4CAF50',
          error: '#F44336',
          warning: '#FF9800',
          info: '#2196F3',
        },
      },
    },
  },
  icons: {
    defaultSet: 'mdi',
  },
})

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(vuetify)

app.mount('#app')

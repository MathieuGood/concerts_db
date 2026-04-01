import './assets/styles.css'
import { createApp } from 'vue'
import PrimeVue from 'primevue/config'
import ToastService from 'primevue/toastservice'
import Aura from '@primevue/themes/aura'
import { definePreset } from '@primevue/themes'
import App from './App.vue'
import router from './router'

const ConcertsTheme = definePreset(Aura, {
  semantic: {
    primary: {
      50: '#f5f3ff',
      100: '#ede9fe',
      200: '#ddd6fe',
      300: '#c4b5fd',
      400: '#a78bfa',
      500: '#8b5cf6',
      600: '#7c3aed',
      700: '#6d28d9',
      800: '#5b21b6',
      900: '#4c1d95',
      950: '#2e1065',
    },
  },
})

const app = createApp(App)

app.use(PrimeVue, {
  theme: {
    preset: ConcertsTheme,
    options: {
      darkModeSelector: '.dark',
    },
  },
})

app.use(ToastService)
app.use(router)
app.mount('#app')

import './assets/styles.css'
import { createApp } from 'vue'
import PrimeVue from 'primevue/config'
import ToastService from 'primevue/toastservice'
import ConfirmationService from 'primevue/confirmationservice'
import Tooltip from 'primevue/tooltip'
import Aura from '@primevue/themes/aura'
import { definePreset } from '@primevue/themes'
import App from './App.vue'
import router from './router'

const ConcertsTheme = definePreset(Aura, {
  semantic: {
    primary: {
      50:  '#fff0f8',
      100: '#ffdcf2',
      200: '#ffbce7',
      300: '#ff8fd5',
      400: '#ff79c6',
      500: '#f550ae',
      600: '#d4308e',
      700: '#b02073',
      800: '#8e1b5e',
      900: '#6e1549',
      950: '#420b2c',
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
app.use(ConfirmationService)
app.directive('tooltip', Tooltip)
app.use(router)
app.mount('#app')

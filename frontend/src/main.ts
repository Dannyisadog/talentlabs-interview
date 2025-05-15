import './assets/main.css'

import '@mdi/font/css/materialdesignicons.css'
import { QueryClient, VueQueryPlugin } from '@tanstack/vue-query'
import { createApp } from 'vue'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import 'vuetify/styles'
import App from './App.vue'
import i18n from './i18n'
import router from './router'

const vuetify = createVuetify({
  components,
  directives,
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi,
    },
  },
})

// Initialize locale from localStorage if available
const savedLocale = localStorage.getItem('locale') as 'en' | 'zh' | null
if (savedLocale && (savedLocale === 'en' || savedLocale === 'zh')) {
  i18n.global.locale.value = savedLocale
}

// Configure Vue Query
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: false,
    },
  },
})

const app = createApp(App)

app.use(router)
app.use(vuetify)
app.use(i18n)
app.use(VueQueryPlugin, {
  queryClient,
})

app.mount('#app')

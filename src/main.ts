import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import VCalendar from 'v-calendar';
import 'v-calendar/style.css';
import './assets/main.css'
import VueGtag from 'vue-gtag-next'

const app = createApp(App)

app.use(VueGtag, {
  property: {
    id: 'G-Y7MGY6ECNL'
  }
})

app.use(router)
app.use(VCalendar, {})
app.mount('#app')
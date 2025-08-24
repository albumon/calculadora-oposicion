import { createRouter, createWebHistory } from 'vue-router';
// Asumiremos que tu componente principal se llama 'CalculadoraOposicion.vue'
// y está en una carpeta 'views' o 'components'. Ajusta la ruta si es necesario.
import CalculadoraView from '../views/CalculadoraView.vue';

const routes = [
  {
    path: '/calculadora-oposicion',
    name: 'Calculadora',
    component: CalculadoraView,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
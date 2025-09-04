import { createRouter, createWebHistory } from 'vue-router';
import CalculadoraView from '../views/CalculadoraView.vue';
import StatisticsView from '../views/StatisticsView.vue';
import ConvocatoriasView from '../views/ConvocatoriasView.vue';

const routes = [
  {
    // La ruta raíz '/' ahora es la calculadora, que será la página de inicio
    path: '/',
    name: 'Calculadora',
    component: CalculadoraView,
  },
  {
    path: '/estadisticas',
    name: 'Estadisticas',
    component: StatisticsView,
  },
  {
    path: '/convocatorias',
    name: 'Convocatorias',
    component: ConvocatoriasView,
  },
];

const router = createRouter({
  // Lee la configuración 'base' de tu vite.config.ts para que las rutas funcionen correctamente
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
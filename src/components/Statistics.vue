<template>
  <div class="stats-container">
    <h1>📊 Estadísticas de Oposiciones a Notarías</h1>
    <p class="subtitle">
      Visualización del número de opositores en distintas fases y el "embudo" de la oposición.
    </p>

    <div class="charts-grid">
      <div class="chart-card">
        <h3>Comparativa General (Admitidos vs. Plazas vs. Aprobados)</h3>
        <div class="chart-wrapper">
          <canvas id="barChart"></canvas>
        </div>
      </div>
      <div class="chart-card">
        <h3>Embudo de la Oposición (Convocatoria 2023)</h3>
        <div class="chart-wrapper">
          <canvas id="doughnutChart2023"></canvas>
        </div>
      </div>
      <div class="chart-card">
        <h3>Embudo de la Oposición (Convocatoria 2021)</h3>
        <div class="chart-wrapper">
          <canvas id="doughnutChart2021"></canvas>
        </div>
      </div>
    </div>

    <div class="disclaimer">
      <p><strong>* Fuente de los Datos</strong></p>
      <p>Datos recopilados de acuerdos oficiales de los tribunales y publicaciones especializadas.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import Chart from 'chart.js/auto';
import statsData from '@/data/stats.json';

onMounted(() => {
  // --- 1. BAR CHART INITIALIZATION ---
  // Este gráfico se actualizará automáticamente cuando modifiques stats.json
  const barCtx = document.getElementById('barChart') as HTMLCanvasElement;
  if (barCtx) {
    new Chart(barCtx, {
      type: 'bar',
      data: {
        labels: statsData.map(item => item.convocatoria),
        datasets: [
          {
            label: 'Admitidos / Inscritos',
            backgroundColor: '#81A1C1',
            data: statsData.map(item => item.admitidos),
          },
          {
            label: 'Plazas Ofertadas',
            backgroundColor: '#EBCB8B',
            data: statsData.map(item => item.plazas),
          },
          {
            label: 'Aprobados (Obtienen Plaza)',
            backgroundColor: '#A3BE8C',
            data: statsData.map(item => item.aprobados_finales),
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
      }
    });
  }

  // --- 2. DOUGHNUT CHART 2023 INITIALIZATION ---
  const doughnutCtx2023 = document.getElementById('doughnutChart2023') as HTMLCanvasElement;
  const data2023 = statsData.find(item => item.convocatoria.includes('2023'));
  if (doughnutCtx2023 && data2023 && data2023.aprobados_segundo_oral) {
    const dropoutsAndFirstFailures = data2023.admitidos - data2023.aprobados_primer_oral;
    const passedFirstButFailedSecond = data2023.aprobados_primer_oral - data2023.aprobados_segundo_oral;
    const passedSecondButFailedRest = data2023.aprobados_segundo_oral - data2023.aprobados_finales;

    new Chart(doughnutCtx2023, {
      type: 'doughnut',
      data: {
        labels: [
          'No superan el 1º Oral / Abandonan',
          'Superan el 1º pero no el 2º',
          'Superan el 2º pero no el 3º',
          'Obtienen Plaza'
        ],
        datasets: [{
          data: [
            dropoutsAndFirstFailures,
            passedFirstButFailedSecond,
            passedSecondButFailedRest,
            data2023.aprobados_finales
          ],
          backgroundColor: ['#BF616A', '#D08770', '#EBCB8B', '#A3BE8C'],
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
      }
    });
  }

  // --- 3. DOUGHNUT CHART 2021 INITIALIZATION (NUEVO) ---
  const doughnutCtx2021 = document.getElementById('doughnutChart2021') as HTMLCanvasElement;
  const data2021 = statsData.find(item => item.convocatoria.includes('2021'));
  if (doughnutCtx2021 && data2021 && data2021.aprobados_segundo_oral) {
    const dropoutsAndFirstFailures = data2021.admitidos - data2021.aprobados_primer_oral;
    const passedFirstButFailedSecond = data2021.aprobados_primer_oral - data2021.aprobados_segundo_oral;
    const passedSecondButFailedRest = data2021.aprobados_segundo_oral - data2021.aprobados_finales;

    new Chart(doughnutCtx2021, {
      type: 'doughnut',
      data: {
        labels: [
          'No superan el 1º Oral / Abandonan',
          'Superan el 1º pero no el 2º',
          'Superan el 2º pero no el 3º',
          'Obtienen Plaza'
        ],
        datasets: [{
          data: [
            dropoutsAndFirstFailures,
            passedFirstButFailedSecond,
            passedSecondButFailedRest,
            data2021.aprobados_finales
          ],
          backgroundColor: ['#BF616A', '#D08770', '#EBCB8B', '#A3BE8C'],
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
      }
    });
  }
});
</script>

<style scoped>
/* Estilos sin cambios */
.stats-container {
  max-width: 1200px; /* Aumentado para dar espacio a 3 gráficos */
  margin: 2rem auto;
  padding: 2rem;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  text-align: center;
}
h1 {
  color: #2c3e50;
}
.subtitle {
  color: #555;
  margin-bottom: 2rem;
}
.charts-grid {
  display: grid;
  /* El layout se adapta automáticamente, mostrando hasta 3 columnas si hay espacio */
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}
.chart-card {
  background: #fff;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  border: 1px solid #e0e0e0;
}
.chart-card h3 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  color: #2c3e50;
  font-weight: 600;
}
.chart-wrapper {
  position: relative;
  height: 350px;
}
.disclaimer {
  margin-top: 1.5rem;
  padding: 1rem;
  background-color: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  color: #6c757d;
  font-size: 0.9rem;
  text-align: left;
}
.disclaimer p {
  margin: 0.3rem 0;
}
</style>
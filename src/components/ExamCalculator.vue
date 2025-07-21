<template>
  <div class="calculator-container">
    <h1>📅 Calculadora Estimada de Examen (Opo 2025)</h1>
    <p class="subtitle">
      Elige un método y busca para obtener una doble estimación de fecha, comparando el ritmo de las convocatorias de 2023 y 2021.
    </p>

    <div class="search-options">
      <label>
        <input type="radio" v-model="searchMode" value="name" />
        Nombre y Apellidos
      </label>
      <label>
        <input type="radio" v-model="searchMode" value="order" />
        Nº de orden de sorteo
      </label>
      <label>
        <input type="radio" v-model="searchMode" value="draw" />
        Nº de orden alfabético
      </label>
    </div>

    <div class="input-group">
      <input
        type="text"
        v-model="searchInput"
        :placeholder="placeholderText"
        @keyup.enter="realizarBusqueda"
      />
      <button @click="realizarBusqueda">Estimar Fechas</button>
    </div>

    <div v-if="resultado" class="result">
      <div v-if="error" class="error-message">
        <p>{{ resultado }}</p>
      </div>
      <div v-else-if="typeof resultado === 'object'" class="success-message">
        <p>¡Hola, <strong>{{ aspiranteEncontrado?.nombre_apellidos }}</strong>!</p>
        <p>
          Perteneces al <strong>Tribunal {{ tribunalEncontrado }}</strong> con el nº de orden de sorteo <strong>{{ aspiranteEncontrado?.numero_orden_sorteo }}</strong> (Nº orden alfabético: {{ aspiranteEncontrado?.numero_orden_alfabetico }}).
        </p>
        
        <div class="comparison-container">
          <div class="date-container">
              <p class="estimation-title">Estimación según ritmo <strong>2023</strong></p>
              <p class="final-date">{{ resultado.fecha2023 }}</p>
          </div>
          <div class="date-container">
              <p class="estimation-title">Estimación según ritmo <strong>2021</strong></p>
              <p class="final-date">{{ resultado.fecha2021 }}</p>
          </div>
        </div>
        
        <div class="disclaimer">
            <p><strong>⚠️ ¡ESTIMACIÓN IMPORTANTE!</strong></p>
            <p>Estas fechas son estimaciones para ayudarte a planificar. Se basan en la fecha de inicio del 9 de septiembre de 2025 y en ritmos de oposiciones pasadas. La fecha real puede variar.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

// Adaptamos el tipo a los nuevos nombres
interface Aspirante {
  numero_orden_sorteo: number;
  nombre_apellidos: string;
  numero_orden_alfabetico: number;
}

import tribunal1Data from '@/data/tribunal1.json';
import tribunal2Data from '@/data/tribunal2.json';

// --- PARÁMETROS DE ESTIMACIÓN ---
const FECHA_INICIO_OPOSICION = new Date('2025-09-09T09:00:00'); 
const DIAS_FESTIVOS_2025: string[] = [
  "2025-10-13", // Lunes siguiente a la Fiesta Nacional
  "2025-12-08", // Inmaculada Concepción
  "2025-12-25", // Navidad
];

// Estadísticas basadas en la convocatoria de 2023
const STATS_2023 = {
  ritmo: 5,   // Opositores convocados por día
  tasa: 0.28  // 28% de retirada
};

// Estadísticas basadas en la convocatoria de 2021 (más conservadora)
const STATS_2021 = {
  ritmo: 4,   // Opositores convocados por día
  tasa: 0.25  // 25% de retirada
};

// --- LÓGICA DEL COMPONENTE ---

const searchMode = ref<'name' | 'order' | 'draw'>('name');
const searchInput = ref('');
const resultado = ref<null | { fecha2023: string, fecha2021: string } | string>(null);
const error = ref(false);
const tribunalEncontrado = ref<number | null>(null);
const aspiranteEncontrado = ref<Aspirante | null>(null);

const tribunal1: Aspirante[] = tribunal1Data;
const tribunal2: Aspirante[] = tribunal2Data;

const placeholderText = computed(() => {
  switch (searchMode.value) {
    case 'order': return 'Escribe tu nº de orden de sorteo...';
    case 'draw': return 'Escribe tu nº de orden alfabético...';
    default: return 'Escribe tu nombre y apellidos...';
  }
});

/**
 * Función genérica para calcular la fecha estimada.
 * @param aspirante El opositor.
 * @param tribunal El tribunal del opositor.
 * @param stats Objeto con el ritmo y la tasa de retirada a aplicar.
 * @returns La fecha estimada.
 */
const calcularFechaEstimada = (aspirante: Aspirante, tribunal: number, stats: { ritmo: number, tasa: number }): Date => {
  const opositoresPrevios = tribunal === 1 
    ? aspirante.numero_orden_sorteo - 1 
    : aspirante.numero_orden_sorteo - tribunal1.length - 1;

  const retiradasEstimadas = Math.round(opositoresPrevios * stats.tasa);
  const examenesEfectivosPrevios = opositoresPrevios - retiradasEstimadas;
  const diasNecesarios = Math.ceil(examenesEfectivosPrevios / stats.ritmo);

  let fechaEstimada = new Date(FECHA_INICIO_OPOSICION);
  if (diasNecesarios <= 0) {
    return fechaEstimada;
  }

  let diasHabilesContados = 0;
  while (diasHabilesContados < diasNecesarios) {
    fechaEstimada.setDate(fechaEstimada.getDate() + 1);
    const diaDeLaSemana = fechaEstimada.getDay();
    const fechaISO = fechaEstimada.toISOString().split('T')[0];
    const esFinDeSemana = diaDeLaSemana === 0 || diaDeLaSemana === 6;
    const esFestivo = DIAS_FESTIVOS_2025.includes(fechaISO);

    if (!esFinDeSemana && !esFestivo) {
      diasHabilesContados++;
    }
  }
  return fechaEstimada;
};

const formatDate = (date: Date): string => {
  return date.toLocaleDateString('es-ES', {
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric',
  });
};

const realizarBusqueda = () => {
  const query = searchInput.value.trim();
  if (!query) {
    resultado.value = 'Por favor, introduce un dato para la búsqueda.';
    error.value = true;
    return;
  }
  
  error.value = false;
  resultado.value = null;
  aspiranteEncontrado.value = null;
  tribunalEncontrado.value = null;
  
  let aspirante: Aspirante | undefined;
  let tribunal: number | null = null;
  
  const numQuery = parseInt(query, 10);

  switch (searchMode.value) {
    case 'name':
      const nombreNormalizado = query.toUpperCase();
      aspirante = tribunal1.find(p => p.nombre_apellidos.toUpperCase() === nombreNormalizado);
      if (aspirante) tribunal = 1;
      else {
        aspirante = tribunal2.find(p => p.nombre_apellidos.toUpperCase() === nombreNormalizado);
        if (aspirante) tribunal = 2;
      }
      break;

    case 'order':
      if (isNaN(numQuery)) {
        error.value = true;
        resultado.value = "Debes introducir un número.";
        return;
      }
      aspirante = tribunal1.find(p => p.numero_orden_sorteo === numQuery);
      if (aspirante) tribunal = 1;
      else {
        aspirante = tribunal2.find(p => p.numero_orden_sorteo === numQuery);
        if (aspirante) tribunal = 2;
      }
      break;

    case 'draw':
       if (isNaN(numQuery)) {
        error.value = true;
        resultado.value = "Debes introducir un número.";
        return;
      }
      aspirante = tribunal1.find(p => p.numero_orden_alfabetico === numQuery);
      if (aspirante) tribunal = 1;
      else {
        aspirante = tribunal2.find(p => p.numero_orden_alfabetico === numQuery);
        if (aspirante) tribunal = 2;
      }
      break;
  }

  if (aspirante && tribunal) {
    aspiranteEncontrado.value = aspirante;
    tribunalEncontrado.value = tribunal;
    
    // Calculamos ambas fechas
    const fecha2023 = calcularFechaEstimada(aspirante, tribunal, STATS_2023);
    const fecha2021 = calcularFechaEstimada(aspirante, tribunal, STATS_2021);
    
    // Guardamos el objeto con las dos fechas formateadas
    resultado.value = {
      fecha2023: formatDate(fecha2023),
      fecha2021: formatDate(fecha2021)
    };

  } else {
    error.value = true;
    resultado.value = 'No se encontró a ningún opositor con el dato introducido. Revisa que sea correcto.';
  }
};
</script>

<style scoped>
/* Estilos actualizados */
.calculator-container {
  max-width: 700px;
  margin: 2rem auto;
  padding: 2rem;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  text-align: center;
}
.search-options {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}
.search-options label {
  cursor: pointer;
  padding: 0.5rem;
}
.input-group {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}
input[type="text"] {
  flex-grow: 1;
  padding: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
}
button {
  padding: 0.75rem 1.5rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}
button:hover {
  background-color: #369a6e;
}
.result {
  margin-top: 1.5rem;
  padding: 1.5rem;
  border-radius: 8px;
  text-align: left;
}
.error-message {
  padding: 1rem;
  background-color: #ffdddd;
  border: 1px solid #ff9999;
  color: #d8000c;
  text-align: center;
}
.success-message {
  background-color: #e2f5e8;
  border: 1px solid #a1d9b4;
  color: #357a38;
}
.success-message p {
  margin: 0.5rem 0;
}
.comparison-container {
  display: flex;
  gap: 1rem;
  justify-content: space-around;
  margin-top: 1.5rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}
.date-container {
    text-align: center;
    padding: 1rem;
    background: #fff;
    border-radius: 8px;
    border: 1px solid #ddd;
    flex: 1;
    min-width: 250px;
}
.estimation-title {
  font-size: 0.9rem;
  color: #555;
  margin: 0 0 0.5rem 0;
}
.final-date {
  font-size: 1.3rem;
  font-weight: bold;
  color: #2c3e50;
  margin: 0.2rem 0;
}
.disclaimer {
    margin-top: 1.5rem;
    padding: 1rem;
    background-color: #fffbe6;
    border: 1px solid #ffe58f;
    border-radius: 4px;
    color: #d46b08;
}
</style>
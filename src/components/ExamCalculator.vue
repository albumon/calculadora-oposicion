<template>
  <div class="calculator-container">
    <h1>📅 Calculadora de Fechas (Opo Notarías 2025)</h1>
    <p class="subtitle">
      Elige un tribunal y un método de búsqueda para estimar tu fecha.
    </p>

    <div class="tribunal-selector">
      <h4>1. Elige un Tribunal</h4>
      <div class="search-options">
          <label>
            <input type="radio" v-model="selectedTribunal" :value="1" />
            Tribunal 1
          </label>
          <label>
            <input type="radio" v-model="selectedTribunal" :value="2" />
            Tribunal 2
          </label>
        </div>
    </div>

    <div class="tribunal-selector" style="background-color: #f0f0f0; border-color: #ddd;">
      <h4>2. Elige un método de búsqueda</h4>
      <div class="search-options">
        <label>
          <input type="radio" v-model="searchMode" value="orden" />
          Nº de Orden
        </label>
        <label>
          <input type="radio" v-model="searchMode" value="sorteo" />
          Nº de Sorteo
        </label>
      </div>
    </div>

    <div class="input-group">
      <input
        type="number"
        v-model="searchInput"
        :placeholder="placeholderText"
        @keyup.enter="performSearch"
      />
      <button @click="performSearch">Estimar Fechas</button>
    </div>

    <div v-if="errorMessage" class="result">
      <div class="error-message">
        <p>{{ errorMessage }}</p>
      </div>
    </div>

    <div v-if="result" class="result">
      <div class="success-message">
        <div v-if="foundAspirant">
          <p>¡Hola, <strong>{{ foundAspirant.nombre_apellidos }}</strong>!</p>
          <p>
            Te hemos encontrado en el <strong>Tribunal {{ foundTribunal }}</strong>.
            (Nº Orden: {{ foundAspirant.numero_orden }}, Nº Sorteo: {{ foundAspirant.numero_sorteo }})
          </p>
        </div>
        
        <div v-if="calculationMode === 'simulacion'">
          <p><strong>Simulación para no inscritos (Tribunal {{ selectedTribunal }})</strong></p>
          <p>
            El número {{ searchInput }} no corresponde a ningún inscrito. La fecha se ha calculado como una simulación para el <strong>Tribunal {{ selectedTribunal }}</strong>.
          </p>
        </div>

        <div class="comparison-container">
          <div class="date-container">
              <p class="estimation-title">Estimación según ritmo <strong>2023</strong></p>
              <p class="final-date">{{ result.date2023 }}</p>
          </div>
          <div class="date-container">
              <p class="estimation-title">Estimación según ritmo <strong>2021</strong></p>
              <p class="final-date">{{ result.date2021 }}</p>
          </div>
        </div>
        
        <div class="disclaimer">
            <p><strong>⚠️ ¡ESTIMACIÓN IMPORTANTE!</strong></p>
            <p>Estas fechas son una simulación para ayudarte a planificar. La fecha real puede variar.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';

interface Aspirant {
  numero_orden: number;
  nombre_apellidos: string;
  numero_sorteo: number;
  turno: string;
}

import tribunal1Data from '@/data/tribunal1_inscritos.json';
import tribunal2Data from '@/data/tribunal2_inscritos.json';

const EXAM_START_DATE = new Date('2025-09-09T09:00:00');
const HOLIDAYS_2025: string[] = ["2025-10-13", "2025-12-08", "2025-12-25"];
const STATS_2023 = { pace: 5, withdrawalRate: 0.28 };
const STATS_2021 = { pace: 4, withdrawalRate: 0.25 };

const searchMode = ref<'orden' | 'sorteo'>('orden');
const searchInput = ref<number | null>(null);
const selectedTribunal = ref<1 | 2>(1);
const result = ref<null | { date2023: string, date2021: string }>(null);
const errorMessage = ref<string | null>(null);

const foundTribunal = ref<number | null>(null);
const foundAspirant = ref<Aspirant | null>(null);
const calculationMode = ref<'orden' | 'sorteo' | 'simulacion' | null>(null);

const router = useRouter();
const route = useRoute();

const tribunal1: Aspirant[] = tribunal1Data;
const tribunal2: Aspirant[] = tribunal2Data;
const allInscritos: Aspirant[] = [...tribunal1, ...tribunal2];

const placeholderText = computed(() => {
  return searchMode.value === 'orden'
    ? 'Escribe el nº de orden...'
    : 'Escribe el nº de sorteo...';
});

const resetSearchState = () => {
    searchInput.value = null;
    result.value = null;
    errorMessage.value = null;
    foundAspirant.value = null;
    foundTribunal.value = null;
    calculationMode.value = null;
    router.push({ query: {} });
};

watch(searchMode, resetSearchState);
watch(selectedTribunal, resetSearchState);

const estimateExamDate = (precedingCount: number, stats: { pace: number, withdrawalRate: number }): Date => {
  const estimatedWithdrawals = Math.round(precedingCount * stats.withdrawalRate);
  const effectivePreviousExams = precedingCount - estimatedWithdrawals;
  if (effectivePreviousExams <= 0) return new Date(EXAM_START_DATE);

  let estimatedDate = new Date(EXAM_START_DATE);
  let examsProcessed = 0;

  while (examsProcessed < effectivePreviousExams) {
    const dayOfWeek = estimatedDate.getDay();
    const isoDate = estimatedDate.toISOString().split('T')[0];
    const isWeekend = dayOfWeek === 0 || dayOfWeek === 6;
    const isHoliday = HOLIDAYS_2025.includes(isoDate);

    if (!isWeekend && !isHoliday) {
      // --- LÓGICA CORREGIDA: El ritmo se duplica porque los dos tribunales actúan en paralelo ---
      const dailyPace = stats.pace * 2; // El doble de opositores por día en total

      switch (dayOfWeek) {
        case 1: examsProcessed += dailyPace * 2; break; // Lunes (mañana y tarde)
        case 2: examsProcessed += dailyPace; break;     // Martes (tarde)
        case 3: examsProcessed += dailyPace; break;     // Miércoles (tarde)
      }
    }
    if (examsProcessed < effectivePreviousExams) {
      estimatedDate.setDate(estimatedDate.getDate() + 1);
    }
  }
  return estimatedDate;
};

const formatDate = (date: Date): string => {
  return date.toLocaleDateString('es-ES', {
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric',
  });
};

const performSearch = () => {
  const query = searchInput.value;
  result.value = null;
  errorMessage.value = null;
  foundAspirant.value = null;
  foundTribunal.value = null;
  calculationMode.value = null;

  if (query === null || query <= 0) {
    errorMessage.value = 'Por favor, introduce un número válido.';
    return;
  }
  
  let aspirantFound: Aspirant | undefined;
  let precedingCount = 0;
  
  if (searchMode.value === 'orden') {
    const listToSearch = selectedTribunal.value === 1 ? tribunal1 : tribunal2;
    aspirantFound = listToSearch.find(p => p.numero_orden === query);

    if (aspirantFound) {
      calculationMode.value = 'orden';
      foundTribunal.value = selectedTribunal.value;
      // --- LÓGICA CORREGIDA: Se cuentan los opositores en paralelo ---
      // (Nº de orden - 1) en cada tribunal
      precedingCount = (aspirantFound.numero_orden - 1) * 2;
    } else {
      errorMessage.value = `El nº de orden ${query} no se encontró en el Tribunal ${selectedTribunal.value}.`;
      return;
    }
  } else { // searchMode es 'sorteo'
    aspirantFound = allInscritos.find(p => p.numero_sorteo === query);
    if (aspirantFound) {
      calculationMode.value = 'sorteo';
      foundTribunal.value = tribunal1.some(p => p.numero_sorteo === query) ? 1 : 2;
       // --- LÓGICA CORREGIDA: Se cuentan los opositores en paralelo ---
      precedingCount = (aspirantFound.numero_orden - 1) * 2;
    } else {
      calculationMode.value = 'simulacion';
      // --- LÓGICA CORREGIDA: Se suman los opositores de ambos tribunales con nº de sorteo inferior ---
      const precedingT1 = tribunal1.filter(p => p.numero_sorteo < query).length;
      const precedingT2 = tribunal2.filter(p => p.numero_sorteo < query).length;
      precedingCount = precedingT1 + precedingT2;
    }
  }
  
  if (aspirantFound) {
    foundAspirant.value = aspirantFound;
  }
  
  const dateBasedOn2023 = estimateExamDate(precedingCount, STATS_2023);
  const dateBasedOn2021 = estimateExamDate(precedingCount, STATS_2021);
  
  result.value = {
    date2023: formatDate(dateBasedOn2023),
    date2021: formatDate(dateBasedOn2021)
  };

  router.push({
    query: {
        tribunal: selectedTribunal.value,
        modo: searchMode.value,
        q: searchInput.value,
    }
  });
};

const syncStateFromUrl = (query: typeof route.query) => {
    const { modo, q, tribunal } = query;
    if (tribunal === '1' || tribunal === '2') {
      selectedTribunal.value = parseInt(tribunal, 10) as 1 | 2;
    }
    if ((modo === 'orden' || modo === 'sorteo') && q && !isNaN(Number(q))) {
        searchMode.value = modo;
        searchInput.value = parseInt(q as string, 10);
        performSearch();
    }
};

onMounted(() => { syncStateFromUrl(route.query); });
watch(() => route.query, (newQuery, oldQuery) => {
    if (JSON.stringify(newQuery) !== JSON.stringify(oldQuery)) {
        syncStateFromUrl(newQuery);
    }
});
</script>

<style scoped>
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
.subtitle {
    color: #555;
}
.search-options {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  margin-bottom: 0.5rem;
  flex-wrap: wrap;
}
.search-options label {
  cursor: pointer;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  background-color: #e9e9e9;
  transition: background-color 0.3s;
}
.search-options input[type="radio"] {
  display: none;
}
.search-options label:has(input[type="radio"]:checked) {
    background-color: #42b983;
    color: white;
}
.input-group {
  display: flex;
  gap: 0.5rem;
  margin-top: 1.5rem;
}
input[type="number"] {
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
  text-align: left;
}
.error-message {
  padding: 1rem;
  background-color: #ffdddd;
  border: 1px solid #ff9999;
  color: #d8000c;
  border-radius: 8px;
  text-align: center;
}
.success-message {
  padding: 1.5rem;
  background-color: #e2f5e8;
  border: 1px solid #a1d9b4;
  color: #357a38;
  border-radius: 8px;
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
.tribunal-selector {
  margin-bottom: 1rem;
  padding: 1rem;
  background-color: #e9e9e9;
  border-radius: 8px;
}
.tribunal-selector h4 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: #333;
}
</style>
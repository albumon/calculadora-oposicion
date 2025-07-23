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
        @keyup.enter="performSearch"
      />
      <button @click="performSearch">Estimar Fechas</button>
    </div>

    <div v-if="result" class="result">
      <div v-if="error" class="error-message">
        <p>{{ result }}</p>
      </div>
      <div v-else-if="typeof result === 'object'" class="success-message">
        <p>¡Hola, <strong>{{ foundAspirant?.nombre_apellidos }}</strong>!</p>
        <p>
          Perteneces al <strong>Tribunal {{ foundTribunal }}</strong> con el nº de orden de sorteo <strong>{{ foundAspirant?.numero_orden_sorteo }}</strong> (Nº orden alfabético: {{ foundAspirant?.numero_orden_alfabetico }}).
        </p>
        
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
            <p>Estas fechas son estimaciones para ayudarte a planificar. Se basan en la fecha de inicio del 9 de septiembre de 2025 y en ritmos de oposiciones pasadas. La fecha real puede variar.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

// Adaptamos el tipo a los nuevos nombres
interface Aspirant {
  numero_orden_sorteo: number;
  nombre_apellidos: string;
  numero_orden_alfabetico: number;
}

import tribunal1Data from '@/data/tribunal1.json';
import tribunal2Data from '@/data/tribunal2.json';

// --- ESTIMATION PARAMETERS ---
const EXAM_START_DATE = new Date('2025-09-09T09:00:00'); 
const HOLIDAYS_2025: string[] = [
  "2025-10-13", // Lunes siguiente a la Fiesta Nacional
  "2025-12-08", // Inmaculada Concepción
  "2025-12-25", // Navidad
];

// Statistics based on the 2023 convocation
const STATS_2023 = {
  pace: 5,   // Opositores convocados por día
  withdrawalRate: 0.28  // 28% de retirada
};

// Statistics based on the 2021 convocation (more conservative)
const STATS_2021 = {
  pace: 4,   // Opositores convocados por día
  withdrawalRate: 0.25  // 25% de retirada
};

// --- COMPONENT LOGIC ---

const searchMode = ref<'name' | 'order' | 'draw'>('name');
const searchInput = ref('');
const result = ref<null | { date2023: string, date2021: string } | string>(null);
const error = ref(false);
const foundTribunal = ref<number | null>(null);
const foundAspirant = ref<Aspirant | null>(null);

const tribunal1: Aspirant[] = tribunal1Data;
const tribunal2: Aspirant[] = tribunal2Data;

const placeholderText = computed(() => {
  switch (searchMode.value) {
    case 'order': return 'Escribe tu nº de orden de sorteo...';
    case 'draw': return 'Escribe tu nº de orden alfabético...';
    default: return 'Escribe tu nombre y apellidos...';
  }
});

/**
 * UPDATED function to estimate the exam date based on the new weekly schedule.
 * @param aspirant The found aspirant object.
 * @param tribunal The aspirant's tribunal number.
 * @param stats The statistics object { pace, withdrawalRate } to apply.
 * @returns The estimated exam Date object.
 */
const estimateExamDate = (aspirant: Aspirant, tribunal: number, stats: { pace: number, withdrawalRate: number }): Date => {
  const precedingAspirants = tribunal === 1 
    ? aspirant.numero_orden_sorteo - 1 
    : aspirant.numero_orden_sorteo - tribunal1.length - 1;

  const estimatedWithdrawals = Math.round(precedingAspirants * stats.withdrawalRate);
  const effectivePreviousExams = precedingAspirants - estimatedWithdrawals;

  if (effectivePreviousExams <= 0) {
    return new Date(EXAM_START_DATE);
  }

  let estimatedDate = new Date(EXAM_START_DATE);
  let examsProcessed = 0;

  // Loop until we have processed enough exam slots to cover the people in front.
  while (examsProcessed < effectivePreviousExams) {
    const dayOfWeek = estimatedDate.getDay(); // Sunday: 0, Monday: 1, ..., Saturday: 6
    const isoDate = estimatedDate.toISOString().split('T')[0];
    
    const isWeekend = dayOfWeek === 0 || dayOfWeek === 6;
    const isHoliday = HOLIDAYS_2025.includes(isoDate);

    if (!isWeekend && !isHoliday) {
      switch (dayOfWeek) {
        case 1: // Monday: Morning and Afternoon sessions
          examsProcessed += stats.pace * 2;
          break;
        case 2: // Tuesday: Afternoon session only
          examsProcessed += stats.pace;
          break;
        case 3: // Wednesday: Afternoon session only
          examsProcessed += stats.pace;
          break;
        // Thursday (4) and Friday (5) have no exams, so we do nothing.
      }
    }

    // If we haven't reached the target yet, advance to the next day.
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
  const query = searchInput.value.trim();
  if (!query) {
    result.value = 'Por favor, introduce un dato para la búsqueda.';
    error.value = true;
    return;
  }
  
  error.value = false;
  result.value = null;
  foundAspirant.value = null;
  foundTribunal.value = null;
  
  let aspirant: Aspirant | undefined;
  let tribunal: number | null = null;
  
  const numericQuery = parseInt(query, 10);

  switch (searchMode.value) {
    case 'name':
      const normalizedName = query.toUpperCase();
      aspirant = tribunal1.find(p => p.nombre_apellidos.toUpperCase() === normalizedName);
      if (aspirant) tribunal = 1;
      else {
        aspirant = tribunal2.find(p => p.nombre_apellidos.toUpperCase() === normalizedName);
        if (aspirant) tribunal = 2;
      }
      break;

    case 'order':
      if (isNaN(numericQuery)) { error.value = true; result.value = "Debes introducir un número."; return; }
      aspirant = tribunal1.find(p => p.numero_orden_sorteo === numericQuery);
      if (aspirant) tribunal = 1;
      else {
        aspirant = tribunal2.find(p => p.numero_orden_sorteo === numericQuery);
        if (aspirant) tribunal = 2;
      }
      break;

    case 'draw':
       if (isNaN(numericQuery)) { error.value = true; result.value = "Debes introducir un número."; return; }
      aspirant = tribunal1.find(p => p.numero_orden_alfabetico === numericQuery);
      if (aspirant) tribunal = 1;
      else {
        aspirant = tribunal2.find(p => p.numero_orden_alfabetico === numericQuery);
        if (aspirant) tribunal = 2;
      }
      break;
  }

  if (aspirant && tribunal) {
    foundAspirant.value = aspirant;
    foundTribunal.value = tribunal;
    
    // Calculamos ambas fechas
    const dateBasedOn2023 = estimateExamDate(aspirant, tribunal, STATS_2023);
    const dateBasedOn2021 = estimateExamDate(aspirant, tribunal, STATS_2021);
    
    // Guardamos el objeto con las dos fechas formateadas
    result.value = {
      date2023: formatDate(dateBasedOn2023),
      date2021: formatDate(dateBasedOn2021)
    };

  } else {
    error.value = true;
    result.value = 'No se encontró a ningún opositor con el dato introducido. Revisa que sea correcto.';
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
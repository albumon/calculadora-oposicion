<template>
  <div class="calculator-container">
    <h1>📅 Calculadora de Fechas (Opo Notarías 2025)</h1>
    <p class="subtitle">
      Introduce tu nº de orden o nº de sorteo para estimar tu fecha.
    </p>

    <div class="input-group">
      <input
        type="number"
        v-model="searchInput"
        placeholder="Nº de orden o Nº de sorteo..."
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
          <p v-if="calculationMode === 'orden'">
            Te hemos encontrado por tu <strong>nº de orden ({{ foundAspirant.numero_orden }})</strong>.
            Perteneces al <strong>Tribunal {{ foundTribunal }}</strong>.
          </p>
          <p v-if="calculationMode === 'sorteo'">
            Te hemos encontrado por tu <strong>nº de sorteo ({{ foundAspirant.numero_sorteo }})</strong>.
            Tu nº de orden real es el {{ foundAspirant.numero_orden }} y perteneces al <strong>Tribunal {{ foundTribunal }}</strong>.
          </p>
        </div>
        
        <div v-if="calculationMode === 'simulacion'">
          <p><strong>Simulación para no inscritos</strong></p>
          <p>
            El número {{ searchInput }} no corresponde a ningún inscrito. La fecha se ha calculado como una simulación, suponiendo que ese es tu <strong>nº de sorteo</strong>.
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
import { ref } from 'vue';

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

const searchInput = ref<number | null>(null);
const result = ref<null | { date2023: string, date2021: string }>(null);
const errorMessage = ref<string | null>(null);

const foundTribunal = ref<number | null>(null);
const foundAspirant = ref<Aspirant | null>(null);
const calculationMode = ref<'orden' | 'sorteo' | 'simulacion' | null>(null);

const tribunal1: Aspirant[] = tribunal1Data;
const tribunal2: Aspirant[] = tribunal2Data;
const allInscritos: Aspirant[] = [...tribunal1, ...tribunal2];

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
      switch (dayOfWeek) {
        case 1: examsProcessed += stats.pace * 2; break;
        case 2: examsProcessed += stats.pace; break;
        case 3: examsProcessed += stats.pace; break;
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
  
  // --- LÓGICA DE BÚSQUEDA CORREGIDA ---
  let aspirantFound: Aspirant | undefined;
  let precedingCount = 0;

  // 1. Buscamos primero por NÚMERO DE ORDEN
  aspirantFound = allInscritos.find(p => p.numero_orden === query);
  if (aspirantFound) {
    calculationMode.value = 'orden';
  } else {
    // 2. Si no, buscamos por NÚMERO DE SORTEO
    aspirantFound = allInscritos.find(p => p.numero_sorteo === query);
    if (aspirantFound) {
      calculationMode.value = 'sorteo';
    }
  }

  if (aspirantFound) {
    // --- ESCENARIO A: El usuario ESTÁ INSCRITO (encontrado por orden o sorteo) ---
    foundAspirant.value = aspirantFound;
    // El cálculo SIEMPRE se basa en el número de orden real
    precedingCount = aspirantFound.numero_orden - 1;
    foundTribunal.value = tribunal1.some(p => p.numero_orden === aspirantFound!.numero_orden) ? 1 : 2;
  } else {
    // --- ESCENARIO B: El usuario NO ESTÁ INSCRITO (simulación) ---
    calculationMode.value = 'simulacion';
    precedingCount = allInscritos.filter(p => p.numero_sorteo < query).length;
  }
  
  const dateBasedOn2023 = estimateExamDate(precedingCount, STATS_2023);
  const dateBasedOn2021 = estimateExamDate(precedingCount, STATS_2021);
  
  result.value = {
    date2023: formatDate(dateBasedOn2023),
    date2021: formatDate(dateBasedOn2021)
  };
};
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
.input-group {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
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
</style>
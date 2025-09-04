<template>
  <div class="convocatorias-container">
    <h1>📜 Convocatorias a Examen</h1>
    <p class="subtitle">
      Selecciona una fecha en el calendario para ver los opositores convocados. Los días con actividad están resaltados.
    </p>

    <div class="main-content">
      <div class="calendar-card">
        <v-calendar 
          v-model="selectedDate"
          @dayclick="handleDayClick"
          :min-date="new Date(examStartDate)"
          :attributes="calendarAttributes"
          expanded
          title-position="left"
          color="green"
        />
        <div class="calendar-legend">
          <ul>
            <li v-for="item in legendItems" :key="item.label">
              <span class="legend-color" :style="{ backgroundColor: item.fullColor }"></span>
              {{ item.label }}
            </li>
          </ul>
        </div>
      </div>

      <div class="results-card">
        <div v-if="!selectedDate" class="placeholder">
          <p>Selecciona un día resaltado en el calendario para ver los detalles.</p>
        </div>
        <div v-else>
          <h3>Convocados para el {{ formattedSelectedDate }}</h3>
          <div class="tribunal-results">
            <div class="tribunal-column">
              <h4>Tribunal 1</h4>
              <div v-if="convocatoriasDelDia.t1.length > 0">
                <div v-for="(convocatoria, index) in convocatoriasDelDia.t1" :key="`t1-conv-${index}`" class="convocatoria-item">
                  <p class="rango-info">{{ convocatoria.rangoTexto }}</p>
                  <details class="aspirants-details">
                    <summary>Ver {{ convocatoria.aspirants.length }} opositores</summary>
                    <ul>
                      <li v-for="aspirant in convocatoria.aspirants" :key="aspirant.numero_sorteo">
                        <strong>Nº Sorteo {{ aspirant.numero_sorteo }}:</strong> {{ aspirant.nombre_apellidos }}
                      </li>
                    </ul>
                  </details>
                </div>
              </div>
              <p v-else class="no-results">No hay convocatorias para este día.</p>
            </div>
            <div class="tribunal-column">
              <h4>Tribunal 2</h4>
              <div v-if="convocatoriasDelDia.t2.length > 0">
                <div v-for="(convocatoria, index) in convocatoriasDelDia.t2" :key="`t2-conv-${index}`" class="convocatoria-item">
                   <p class="rango-info">{{ convocatoria.rangoTexto }}</p>
                   <details class="aspirants-details">
                    <summary>Ver {{ convocatoria.aspirants.length }} opositores</summary>
                    <ul>
                      <li v-for="aspirant in convocatoria.aspirants" :key="aspirant.numero_sorteo">
                        <strong>Nº Sorteo {{ aspirant.numero_sorteo }}:</strong> {{ aspirant.nombre_apellidos }}
                      </li>
                    </ul>
                  </details>
                </div>
              </div>
              <p v-else class="no-results">No hay convocatorias para este día.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import convocatoriasData from '@/data/convocatorias.json';
import tribunal1Data from '@/data/tribunal1_inscritos.json';
import tribunal2Data from '@/data/tribunal2_inscritos.json';

interface Aspirant { numero_orden: number; nombre_apellidos: string; numero_sorteo: number; turno: string; }
interface Rango { inicio: number; fin: number; }
interface Convocatoria { fecha: string; convocados: Rango[]; }
interface ConvocatoriaDetallada { rangoTexto: string; aspirants: Aspirant[]; }

const examStartDate = '2025-09-09';
const HOLIDAYS_2025: string[] = ["2025-10-13", "2025-12-08", "2025-12-25"];
const selectedDate = ref<Date | null>(null);
const tribunal1Inscritos: Aspirant[] = tribunal1Data;
const tribunal2Inscritos: Aspirant[] = tribunal2Data;
const tribunal1Convocatorias: Convocatoria[] = convocatoriasData.tribunal1;
const tribunal2Convocatorias: Convocatoria[] = convocatoriasData.tribunal2;
const legendItems = [
  { color: 'green', fullColor: '#A3BE8C', label: 'Día con convocatoria' },
  { color: 'yellow', fullColor: '#EBCB8B', label: 'Día potencial de examen' },
  { color: 'red', fullColor: '#BF616A', label: 'Día no lectivo' },
];

const formatDateToKey = (date: Date): string => {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
};

const handleDayClick = (day: any) => {
  selectedDate.value = day.date as Date;
};

const formattedSelectedDate = computed(() => {
  if (!selectedDate.value) return '';
  return selectedDate.value.toLocaleDateString('es-ES', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
});

const convocatoriasDelDia = computed(() => {
  if (!selectedDate.value) return { t1: [], t2: [] };
  const dateKey = formatDateToKey(selectedDate.value);

  const t1Entry = tribunal1Convocatorias.find(c => c.fecha === dateKey);
  const t2Entry = tribunal2Convocatorias.find(c => c.fecha === dateKey);
  
  const getAspirants = (rango: Rango, inscritos: Aspirant[]): Aspirant[] => {
    return inscritos
      .filter(a => a.numero_sorteo >= rango.inicio && a.numero_sorteo <= rango.fin)
      .sort((a, b) => a.numero_sorteo - b.numero_sorteo); // Ordenamos por si acaso
  };

  const formatRango = (rango: Rango): string => {
      return rango.inicio === rango.fin ? `Convocado el nº ${rango.inicio}` : `Convocados del nº ${rango.inicio} al nº ${rango.fin}`;
  }

  const detailedT1: ConvocatoriaDetallada[] = t1Entry ? t1Entry.convocados.map(rango => ({
      rangoTexto: formatRango(rango),
      aspirants: getAspirants(rango, tribunal1Inscritos)
  })) : [];
  
  const detailedT2: ConvocatoriaDetallada[] = t2Entry ? t2Entry.convocados.map(rango => ({
      rangoTexto: formatRango(rango),
      aspirants: getAspirants(rango, tribunal2Inscritos)
  })) : [];

  return { t1: detailedT1, t2: detailedT2 };
});

const calendarAttributes = computed(() => {
  const confirmedDates = new Set([...tribunal1Convocatorias.map(c => c.fecha), ...tribunal2Convocatorias.map(c => c.fecha)]);
  const nonExamDates = new Set<string>();
  const potentialDates = new Set<string>();
  
  const startDate = new Date(examStartDate + 'T00:00:00');
  const endDate = new Date(startDate);
  endDate.setMonth(startDate.getMonth() + 4);

  for (let d = new Date(startDate); d <= endDate; d.setDate(d.getDate() + 1)) {
    const dayOfWeek = d.getDay();
    const dateKey = formatDateToKey(d);
    if (confirmedDates.has(dateKey)) continue;
    const isWeekend = dayOfWeek === 0 || dayOfWeek === 6;
    const isHoliday = HOLIDAYS_2025.includes(dateKey);
    const isNonProductiveWeekday = dayOfWeek === 4 || dayOfWeek === 5;
    if (isWeekend || isHoliday || isNonProductiveWeekday) {
      nonExamDates.add(dateKey);
    } else {
      potentialDates.add(dateKey);
    }
  }
  
  return [
    { key: 'confirmed', highlight: { color: legendItems[0].color, fillMode: 'light' }, dates: Array.from(confirmedDates).map(dateStr => new Date(dateStr + 'T00:00:00')) },
    { key: 'potential', highlight: { color: legendItems[1].color, fillMode: 'light' }, dates: Array.from(potentialDates).map(dateStr => new Date(dateStr + 'T00:00:00')) },
    { key: 'nonExam', highlight: { color: legendItems[2].color, fillMode: 'light' }, dates: Array.from(nonExamDates).map(dateStr => new Date(dateStr + 'T00:00:00')) },
  ];
});
</script>

<style scoped>
.convocatorias-container { max-width: 1200px; margin: 2rem auto; }
.subtitle { text-align: center; color: #555; margin-bottom: 2rem; }
.main-content { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; align-items: flex-start; }
.calendar-card, .results-card { background-color: #f9f9f9; border-radius: 8px; padding: 1.5rem; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }
.calendar-card { padding: 1rem; }
:deep(.vc-container) { --vc-text-lg: 1.1rem; --vc-text-xl: 1.3rem; --vc-font-bold: 600; border: none; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif; }
:deep(.vc-weekday) { font-size: 1rem !important; font-weight: 600; }
.placeholder { display: flex; align-items: center; justify-content: center; height: 100%; min-height: 200px; color: #888; font-style: italic; }
.tribunal-results { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; }
h1, h3, h4 { color: #2c3e50; margin-top: 0; }
ul { list-style-type: none; padding: 0; margin: 0; }
li { padding: 0.5rem; border-bottom: 1px solid #eee; font-size: 0.9rem; }
li:last-child { border-bottom: none; }
.no-results { color: #888; }
.calendar-legend { margin-top: 1.5rem; padding: 0 1rem; }
.calendar-legend ul { display: flex; justify-content: center; align-items: center; flex-wrap: wrap; gap: 1.5rem; }
.calendar-legend li { display: flex; align-items: center; gap: 0.5rem; font-size: 0.9rem; color: #555; border-bottom: none; }
.legend-color { display: inline-block; width: 16px; height: 16px; border-radius: 4px; border: 1px solid rgba(0,0,0,0.1); }
.rango-info { font-weight: bold; margin-bottom: 0.5rem; padding-bottom: 0.5rem; border-bottom: 1px solid #ddd; }
.aspirants-details summary { cursor: pointer; color: #0056b3; font-size: 0.9rem; margin-bottom: 0.5rem; }
.aspirants-details ul { max-height: 250px; overflow-y: auto; border: 1px solid #eee; border-radius: 4px; background: #fff; }
.aspirants-details li { display: flex; justify-content: space-between; }
</style>
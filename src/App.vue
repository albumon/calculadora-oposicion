<template>
  <Header />

  <main>
    <router-view />
  </main>
</template>

<script setup lang="ts">
// 3. Importamos el nuevo componente de cabecera
import Header from './components/Header.vue';
// 4. Ya no se importan componentes de página directamente aquí
</script>

<style>
/* Los estilos globales se mantienen */
@import './assets/main.css';

/* Añadimos un poco de padding al contenido principal */
main {
  padding: 1rem 2rem;
}
</style>
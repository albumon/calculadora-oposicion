<template>
    <header class="app-header">
      <nav class="nav-menu">
        <router-link to="/estadisticas" class="nav-link">📊 Estadísticas</router-link>
        <router-link to="/" class="nav-link">📅 Calculadora de fechas</router-link>
        <router-link to="/convocatorias" class="nav-link">📜 Convocatorias examen</router-link>
      </nav>
    </header>
  </template>
  
  <script setup lang="ts">
  // No se necesita lógica de script para este componente
  </script>
  
  <style scoped>
  .app-header {
    background-color: #2c3e50;
    padding: 1rem 2rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    position: sticky;
    top: 0;
    z-index: 10;
  }
  
  .nav-menu {
    display: flex;
    justify-content: center;
    gap: 2rem;
    flex-wrap: wrap;
  }
  
  .nav-link {
    color: #ffffff;
    text-decoration: none;
    font-size: 1.1rem;
    font-weight: 600;
    padding: 0.5rem 0;
    border-bottom: 2px solid transparent;
    transition: border-color 0.3s, color 0.3s;
  }
  
  .nav-link:hover {
    color: #42b983;
  }
  
  /* El router añade esta clase al enlace de la página activa */
  .router-link-exact-active {
    color: #42b983;
    border-bottom-color: #42b983;
  }
  </style>
# 📅 Calculadora Estimada de Examen (Oposición Notarías 2025)

Una aplicación web interactiva diseñada para opositores a notarías en España. La herramienta principal es una calculadora que ofrece una doble estimación para la fecha del primer examen de la convocatoria de 2025, permitiendo a los aspirantes planificar su estudio con diferentes escenarios.

---

## ✨ Características Principales

* **Búsqueda Flexible:** Permite encontrar a un opositor por tres métodos distintos:
    * Nombre y Apellidos.
    * Nº de Orden de Sorteo (el número de examen dentro del tribunal).
    * Nº de Orden Alfabético (el número asignado en la lista general).

* **Doble Estimación de Fecha:** Para cada opositor, la calculadora proyecta dos fechas estimadas, cada una basada en un modelo estadístico diferente:
    * **Estimación basada en el ritmo de 2023:** Utiliza un ritmo de 5 opositores convocados por día y una tasa de retirada del 28%.
    * **Estimación basada en el ritmo de 2021:** Utiliza un modelo más conservador con un ritmo de 4 opositores por día y una tasa de retirada del 25%.

* **Información Detallada:** Al encontrar a un aspirante, la aplicación muestra a qué tribunal pertenece y sus números de orden correspondientes.

* **Interfaz Limpia y Sencilla:** Creada con elementos estándar y CSS personalizado para una experiencia de usuario directa y sin distracciones.

## ⚙️ Cómo Funciona el Cálculo

La estimación no es una fecha fija, sino una proyección matemática basada en los siguientes parámetros:

* **Fecha de Inicio Fija:** Se asume que la oposición comienza el **9 de septiembre de 2025**.
* **Opositores Previos:** Se calcula cuántas personas van por delante del aspirante en la cola de su tribunal específico.
* **Tasa de Retirada:** Se aplica un porcentaje de retiradas estimadas (28% o 25%) para determinar cuántos exámenes se realizarán efectivamente.
* **Ritmo Diario:** Se divide el número de exámenes efectivos por el ritmo diario de cada modelo (5 o 4 opositores/día).
* **Proyección en Calendario:** El resultado se proyecta sobre un calendario que excluye fines de semana y festivos nacionales para obtener la fecha final.

## 🛠️ Tecnologías Utilizadas

* **Framework:** Vue 3 (Composition API con `<script setup>`)
* **Build Tool:** Vite
* **Lenguaje:** TypeScript
* **Estilos:** HTML estándar con CSS personalizado (`<style scoped>`). No se utilizan librerías de componentes externos.

## 🚀 Puesta en Marcha Local

Sigue estos pasos para ejecutar el proyecto en tu propio ordenador.

1.  **Clona el repositorio:**

2.  **Navega a la carpeta del proyecto:**

3.  **Instala las dependencias:**
    ```bash
    npm install
    ```

4.  **Inicia el servidor de desarrollo:**
    ```bash
    npm run dev
    ```
    La aplicación estará disponible en `http://localhost:5173` (o el puerto que indique la terminal).
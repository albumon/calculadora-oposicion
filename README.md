# 📅 Calculadora Estimada de Examen (Oposición Notarías 2025)

Una aplicación web interactiva diseñada para opositores a notarías en España. La herramienta principal es una calculadora que ofrece una doble estimación para la fecha del primer examen de la convocatoria de 2025. Su característica más destacada es que **utiliza datos reales y actualizados diariamente** gracias a un sistema de scraping automatizado.

---

## ✨ Características Principales

* **Datos Siempre Actualizados:** Un **scraper automatizado con GitHub Actions** se ejecuta diariamente (a medianoche UTC) para obtener la lista oficial de inscritos. Esto asegura que los cálculos se basan siempre en la información más reciente sin intervención manual.

* **Búsqueda Inteligente y Unificada:** El usuario introduce un único número y la aplicación determina la mejor forma de buscar:
    1.  Primero, busca si el número corresponde al **Nº de Orden** de un opositor inscrito.
    2.  Si no lo encuentra, busca si corresponde al **Nº de Sorteo** de un inscrito.

* **Modo Simulación para No Inscritos:** Si el número introducido no pertenece a ningún opositor inscrito, la calculadora entra en "modo simulación". Trata el número como un Nº de Sorteo hipotético y calcula una fecha estimada, permitiendo a futuros aspirantes valorar su posible posición.

* **Doble Estimación de Fecha:** Para cada búsqueda, la calculadora proyecta dos fechas, permitiendo planificar con distintos escenarios:
    * **Estimación basada en el ritmo de 2023:** Ritmo más rápido (5 opositores/día, 28% de retiradas).
    * **Estimación basada en el ritmo de 2021:** Ritmo más conservador (4 opositores/día, 25% de retiradas).

## ⚙️ Cómo Funciona el Cálculo

La estimación es una proyección matemática basada en los siguientes parámetros:

* **Fecha de Inicio Fija:** Se asume que la oposición comienza el **9 de septiembre de 2025**.
* **Opositores Previos:** El número de personas por delante se determina según el escenario:
    * **Si el usuario está inscrito:** Se usa su **Nº de Orden real** para el cálculo.
    * **Si es una simulación:** Se cuentan cuántos de los inscritos actuales tienen un Nº de Sorteo inferior al número introducido.
* **Tasa de Retirada:** Se aplica un porcentaje de retiradas (28% o 25%) para estimar cuántos exámenes se realizarán efectivamente.
* **Ritmo Semanal Detallado:** La proyección avanza en un calendario que excluye fines de semana y festivos, siguiendo el ritmo de llamamientos:
    * **Lunes:** Sesión de mañana y tarde (doble ritmo).
    * **Martes:** Sesión de tarde (ritmo simple).
    * **Miércoles:** Sesión de tarde (ritmo simple).
    * **Jueves y Viernes:** Sin llamamientos.

## 🛠️ Tecnologías Utilizadas

#### **Frontend (Aplicación Web)**
* **Framework:** Vue 3 (Composition API con `<script setup>`)
* **Build Tool:** Vite
* **Lenguaje:** TypeScript
* **Estilos:** CSS puro (`<style scoped>`)

#### **Backend & Automatización (Scraping de Datos)**
* **Lenguaje:** Python
* **Librerías:** Selenium para web scraping y control del navegador.
* **Automatización:** **GitHub Actions** para la ejecución diaria y programada del scraper y la actualización automática de los datos en el repositorio.

## 🚀 Puesta en Marcha Local

El proyecto tiene dos partes: la aplicación web (Vue) y el script de extracción de datos (Python).

### Parte 1: Ejecutar la Aplicación Web (Vue)

1.  **Clona el repositorio:**
    ```bash
    git clone [https://github.com/albumon/calculator.git](https://github.com/albumon/calculator.git)
    ```
2.  **Navega a la carpeta del proyecto:**
    ```bash
    cd calculadora-oposicion
    ```
3.  **Instala las dependencias de Node.js:**
    ```bash
    npm install
    ```
4.  **Inicia el servidor de desarrollo:**
    ```bash
    npm run dev
    ```
    La aplicación estará disponible en la URL que indique la terminal (normalmente `http://localhost:5173`).

### Parte 2: Actualizar los Datos Manualmente (Python)

Si quieres ejecutar el scraper por tu cuenta para obtener los datos más recientes de forma inmediata.

1.  **Asegúrate de tener Python 3 instalado.**

2.  **(Opcional pero recomendado) Crea un entorno virtual:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Instala las dependencias de Python:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Ejecuta el script de scraping:**
    ```bash
    python3 scraper.py
    ```
    El script abrirá una ventana de Chrome, navegará por las páginas y, al finalizar, tendrás los ficheros `tribunal1_inscritos.json` y `tribunal2_inscritos.json` actualizados dentro de la carpeta `public/data/`.
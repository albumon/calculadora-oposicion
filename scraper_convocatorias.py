import json
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import locale

# --- LÍNEA SIMPLIFICADA ---
# Ahora que el workflow instala el idioma, esto debería funcionar siempre.
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

# --- El resto del script se mantiene igual ---
URLS = {
    "tribunal1": "https://oposiciones2025.notariado.org/web/tribunal-1/convocatorias-a-examen",
    "tribunal2": "https://oposiciones2025.notariado.org/web/tribunal-2/convocatorias-a-examen"
}
OUTPUT_DIR = "src/data"

def parse_spanish_date(date_str):
    try:
        if ',' in date_str:
            date_str = date_str.split(',')[1].strip()
        return datetime.strptime(date_str, '%d de %B de %Y').strftime('%Y-%m-%d')
    except ValueError: return None

def scrape_convocatorias(base_url):
    print("🚀 Comenzando extracción de convocatorias...")
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    driver.get(base_url)
    
    try:
        cookie_button = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Aceptar')]")))
        cookie_button.click()
        print("  - Banner de cookies aceptado.")
        time.sleep(1)
    except TimeoutException:
        print("  - No se encontró banner de cookies.")
        
    convocatorias = []
    
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "convocatoria-card")))
        convocatoria_cards = driver.find_elements(By.CLASS_NAME, "convocatoria-card")
        print(f"  - Se han encontrado {len(convocatoria_cards)} tarjetas de convocatoria.")

        for card in convocatoria_cards:
            try:
                fecha_element = card.find_element(By.CLASS_NAME, "fecha-convocatoria")
                fecha_str = parse_spanish_date(fecha_element.text)
                if not fecha_str: continue

                rango_inicio = int(card.find_element(By.CLASS_NAME, "rango-sorteo-init").text.strip())
                
                try:
                    rango_fin = int(card.find_element(By.CLASS_NAME, "rango-sorteo-fin").text.strip())
                except NoSuchElementException:
                    rango_fin = rango_inicio
                
                existing_entry = next((item for item in convocatorias if item["fecha"] == fecha_str), None)
                
                convocatoria_obj = {"inicio": rango_inicio, "fin": rango_fin}
                
                if existing_entry:
                    existing_entry["convocados"].append(convocatoria_obj)
                else:
                    convocatorias.append({"fecha": fecha_str, "convocados": [convocatoria_obj]})
            except (NoSuchElementException, ValueError) as e:
                print(f"  - No se pudo procesar una tarjeta. Error: {e}")
                continue
    except Exception as e:
        print(f"  - Ha ocurrido un error inesperado: {e}")

    driver.quit()
    return convocatorias

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    all_data = {}
    for name, url in URLS.items():
        print(f"\nProcesando {name.upper()}...")
        all_data[name] = scrape_convocatorias(url)
    
    output_path = os.path.join(OUTPUT_DIR, "convocatorias.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    print(f"\n✅ ¡Éxito! Fichero '{output_path}' generado.")
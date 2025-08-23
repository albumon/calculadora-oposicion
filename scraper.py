import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
# --- 1. IMPORTAMOS LAS OPCIONES DE CHROME ---
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIGURACIÓN ---
URLS = {
    "tribunal1": "https://oposiciones2025.notariado.org/web/tribunal-1/consulta-de-inscripciones",
    "tribunal2": "https://oposiciones2025.notariado.org/web/tribunal-2/consulta-de-inscripciones"
}

def scrape_tribunal_selenium(tribunal_name, base_url):
    """
    Función que extrae los datos de un tribunal usando Selenium para simular clics.
    """
    print(f"🚀 Comenzando la extracción con Selenium para el {tribunal_name.upper()}...")
    
    # --- 2. CONFIGURAMOS LAS OPCIONES PARA EL ENTORNO DE GITHUB ACTIONS ---
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless") # Esencial para ejecutar sin interfaz gráfica
    chrome_options.add_argument("--no-sandbox") # Requerido en muchos entornos de servidor/docker
    chrome_options.add_argument("--disable-dev-shm-usage") # Evita problemas de memoria compartida
    chrome_options.add_argument("--window-size=1920,1080") # Define un tamaño de ventana virtual

    # --- 3. PASAMOS LAS OPCIONES AL INICIAR EL NAVEGADOR ---
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=chrome_options
    )
    
    driver.get(base_url)
    
    all_aspirants = []
    page_count = 1

    while True:
        print(f"    - Leyendo datos de la página: {page_count}...")
        time.sleep(2)

        try:
            table_body = driver.find_element(By.TAG_NAME, 'tbody')
            rows = table_body.find_elements(By.TAG_NAME, 'tr')

            for row in rows:
                cells = row.find_elements(By.TAG_NAME, 'td')
                
                if len(cells) >= 5:
                    try:
                        valor_orden = int(cells[0].text.strip())
                        valor_numero_sorteo = int(cells[1].text.strip())
                        
                        nombre = cells[2].text.strip()
                        apellidos = cells[3].text.strip()
                        turno = cells[4].text.strip()
                        
                        nombre_completo = f"{apellidos}, {nombre}"

                        aspirant = {
                            "numero_orden": valor_orden,
                            "nombre_apellidos": nombre_completo,
                            "numero_sorteo": valor_numero_sorteo,
                            "turno": turno
                        }
                        all_aspirants.append(aspirant)
                    except (ValueError, IndexError):
                        print(f"        - Fila ignorada por formato de datos incorrecto.")
                        continue
        except NoSuchElementException:
            print("    - No se encontró la tabla en la página. Finalizando.")
            break
            
        try:
            next_li_element = driver.find_element(By.XPATH, "//a[text()='»']/..")
            
            if "disabled" in next_li_element.get_attribute("class"):
                print("    - El botón 'Siguiente' (») está deshabilitado. Se ha llegado al final.")
                break
            
            next_button = driver.find_element(By.XPATH, "//a[text()='»']")
            driver.execute_script("arguments[0].click();", next_button)
            page_count += 1
            
        except NoSuchElementException:
            print("    - No se encontró el botón 'Siguiente' (»). Finalizando la extracción.")
            break

    driver.quit()
    return all_aspirants

# --- EJECUCIÓN DEL SCRIPT ---
if __name__ == "__main__":
    for name, url in URLS.items():
        aspirants_data = scrape_tribunal_selenium(name, url)
        
        if aspirants_data:
            file_name = f"{name}_inscritos.json" # Nombres de fichero corregidos
            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(aspirants_data, f, ensure_ascii=False, indent=2)
            print(f"✅ ¡Éxito! Se han guardado {len(aspirants_data)} opositores en el fichero '{file_name}'\n")
        else:
            print(f"⚠️ No se pudieron extraer datos para el {name.upper()}.\n")
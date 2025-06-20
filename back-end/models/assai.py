import os
import time
import requests
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import re
import sys

def get_chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu") # Good practice for headless environments

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

LOJAS_ESTADOS = {
    "Maranhão": "Assaí Angelim",
    "Alagoas": "Assaí Maceió Farol",
    "Ceará": "Assaí Bezerra M (Fortaleza)",
    "Pará": "Assaí Belém",
    "Paraíba": "Assaí João Pessoa Geisel",
    "Pernambuco": "Assaí Avenida Recife",
    "Piauí": "Assaí Teresina",
    "Sergipe": "Assaí Aracaju",
    "Bahia": "Interior Vitória da Conquista",
}

BASE_URL = "https://www.assai.com.br/ofertas"
# desktop_path = Path.home() / "Desktop/Encartes-Concorrentes/Assai" # This path is specific to your local machine
# For Render, you should save to a temporary directory or relative path
# A good practice is to save to a relative path within your project
# or use a temporary directory for files not meant to be persistent.
# For simplicity, let's assume a 'downloads' directory within your project.
download_base_path = Path("downloads/Assai")
os.makedirs(download_base_path, exist_ok=True) # Ensure the base download directory exists

# --- REMOVE THESE GLOBAL DRIVER INITIALIZATION LINES ---
# options = webdriver.ChromeOptions()
# options.add_argument("--start-maximized")
# driver = webdriver.Chrome(options=options)
# wait = WebDriverWait(driver, 30)
# --- END REMOVAL ---

# Define driver and wait globally but initialize within main for proper control
driver = None
wait = None

def main():
    global driver, wait # Declare these as global to assign to them
    driver = get_chrome_driver() # Initialize the driver using your headless function
    wait = WebDriverWait(driver, 30) # Initialize WebDriverWait with the new driver

    loja_param = sys.argv[1] if len(sys.argv) > 1 else None
    print(f"Executando script para a loja: {loja_param}") # Changed 'estado' to 'loja' for clarity


    try:
        driver.get(BASE_URL)
        time.sleep(2)

        try:
            clicar_elemento("button.ot-close-icon")
        except:
            pass

        clicar_elemento("a.seletor-loja")
        time.sleep(1)

        # Loop through LOJAS_ESTADOS if no specific loja_param is provided
        # Otherwise, process only the specified loja
        lojas_to_process = LOJAS_ESTADOS.items()
        if loja_param and loja_param in LOJAS_ESTADOS.values():
            # Find the state for the given loja_param
            found_state = None
            for state, store_name in LOJAS_ESTADOS.items():
                if store_name == loja_param:
                    found_state = state
                    break
            if found_state:
                lojas_to_process = [(found_state, loja_param)]
            else:
                print(f"Loja '{loja_param}' não encontrada nos mapeamentos. Processando todas.")


        for estado, loja in lojas_to_process: # Use the potentially filtered list
            print(f"➡️ Processando: {estado} - {loja}")

            estado_select = aguardar_elemento("select.estado")
            Select(estado_select).select_by_visible_text(estado)
            time.sleep(1)

            aguardar_elemento("select.loja option[value]", timeout=20)
            loja_select = aguardar_elemento("select.loja")
            Select(loja_select).select_by_visible_text(loja)
            time.sleep(1)

            clicar_elemento("button.confirmar")
            time.sleep(3)


            aguardar_elemento("div.ofertas-slider", timeout=30)
            data_nome = encontrar_data()

            nome_loja = loja.replace(' ', '_').replace('(', '').replace(')', '')
            # Use the relative path for downloads
            download_dir = download_base_path / f"encartes_{nome_loja}_{data_nome}"
            os.makedirs(download_dir, exist_ok=True)
            print(f"Salvando encartes em: {download_dir.resolve()}") # Print the resolved path


            scroll_down_and_up()
            baixar_encartes(1, download_dir)

            for i in range(2, 4):
                try:
                    clicar_elemento(f"//button[contains(., 'Jornal de Ofertas {i}')]", By.XPATH)
                    time.sleep(3)
                    aguardar_elemento("div.ofertas-slider", timeout=30)
                    scroll_down_and_up()
                    baixar_encartes(i, download_dir)
                except Exception as e:
                    print(f" Jornal {i} indisponível para {loja}: {str(e)}")

            # After processing a specific loja, you might need to go back
            # to the store selection if processing multiple or ensure a clean state
            # for the next iteration.
            # This 'clicar_elemento' helps reset for the next store in the loop.
            clicar_elemento("a.seletor-loja")
            time.sleep(2)

        print("✔️ Todos os encartes foram processados!")

    except Exception as e:
        print(f"❌ Erro crítico: {str(e)}")
        # Save screenshot to a relative path, not desktop
        screenshot_path = download_base_path / "erro_encartes.png"
        driver.save_screenshot(str(screenshot_path))
        print(f"Screenshot do erro salvo em: {screenshot_path.resolve()}")

    finally:
        if driver: # Ensure driver exists before quitting
            driver.quit()

if __name__ == "__main__":
    main()

# The helper functions (encontrar_data, aguardar_elemento, clicar_elemento,
# scroll_down_and_up, baixar_encartes) remain the same, but they will now use
# the 'driver' and 'wait' variables initialized within the 'main' function.
# Ensure 'wait' is globally accessible or passed as an argument if not.
# For simplicity, making 'driver' and 'wait' global and initializing in main() is often done.

# Original helper functions (keep them as they are, but they'll use the 'driver' and 'wait' initialized in main)
def encontrar_data():
    try:
        enc_data = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "ofertas-tab-validade")]'))
        )
    except:
        return "sem_data"

    for div in enc_data:
        texto = div.text.strip()
        if texto:
            nome_pasta = re.sub(r'[\\/*?:"<>|\s]', '_', texto)
            return nome_pasta
    return "sem_data"

def aguardar_elemento(seletor, by=By.CSS_SELECTOR, timeout=15):
    return wait.until(EC.presence_of_element_located((by, seletor)))

def clicar_elemento(seletor, by=By.CSS_SELECTOR):
    element = wait.until(EC.element_to_be_clickable((by, seletor)))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    time.sleep(0.5)
    element.click()

def scroll_down_and_up():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
    time.sleep(0.5)
    driver.execute_script("window.scrollTo(0, 1);")
    time.sleep(0.5)

def baixar_encartes(jornal_num, download_dir):
    links_download = wait.until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//a[contains(@class, 'download') and contains(@href, '.jpeg')]")
        )
    )
    for idx, link in enumerate(links_download, start=1):
        url = link.get_attribute("href")
        if url:
            response = requests.get(url)
            if response.status_code == 200:
                file_path = download_dir / f"encarte_jornal_{jornal_num}_{idx}_{int(time.time())}.jpg"
                with open(file_path, "wb") as f:
                    f.write(response.content)
                print(f" Encarte {file_path.name} salvo.")
            else:
                print(f" Falha no download: {url} (Status: {response.status_code})")
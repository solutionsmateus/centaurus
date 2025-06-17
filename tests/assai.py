import os
import time
import requests
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


LOJAS_ESTADOS = {
    "Maranhão": "Assaí Angelim",
    "Alagoas": "Assaí Maceió Farol",
    "Ceará": "Assaí Bezerra M (Fortaleza)",
    "Pará": "Assaí Belém",
    "Paraíba": "Assaí João Pessoa Geisel",
    "Pernambuco": "Assaí Avenida Recife",
    "Piauí": "Assaí Teresina",
    "Sergipe": "Assaí Aracaju",
    "Bahia": "Interior" "Vitória da Conquista", 
}

BASE_URL = "https://www.assai.com.br/ofertas"


desktop_path = Path.home() / "Desktop/Encartes-Concorrentes/Assai" 


options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 30)

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

def baixar_todos_slides(jornal_num, download_dir):
    idx = 1
    while True:
        try:

            links = driver.find_elements(By.XPATH, "//a[contains(@class, 'download') and contains(@href, '.jpeg')]")
            if idx <= len(links):
                url = links[idx - 1].get_attribute("href")
                if url:
                    response = requests.get(url)
                    if response.status_code == 200:
                        file_path = download_dir / f"encarte_jornal_{jornal_num}_{idx}_{int(time.time())}.jpg"
                        with open(file_path, "wb") as f:
                            f.write(response.content)
                        print(f" ✅ Encarte {file_path.name} salvo.")
                    else:
                        print(f" ❌ Falha no download (status {response.status_code})")

            
            proximo = driver.find_element(By.CLASS_NAME, "glider-next")
            if "disabled" in proximo.get_attribute("class"):
                break  
            proximo.click()
            time.sleep(2)
            idx += 1

        except Exception as e:
            print(f" ⚠️ Erro ao tentar baixar slide {idx}: {str(e)}")
            break
                

try:
    driver.get(BASE_URL)
    time.sleep(2)

    try:
        clicar_elemento("button.ot-close-icon", By.CSS_SELECTOR)
    except:
        pass

    clicar_elemento("a.seletor-loja", By.CSS_SELECTOR)
    time.sleep(1)

    for estado, loja in LOJAS_ESTADOS.items():
        print(f"➡️ Processando: {estado} - {loja}")
        download_dir = desktop_path / f"encartes_{loja.replace(' ', '_')}"
        os.makedirs(download_dir, exist_ok=True)

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
        scroll_down_and_up()
        baixar_todos_slides(2, download_dir)

        try:
            clicar_elemento("//button[contains(., 'Jornal de Ofertas 2')]", By.XPATH)
            time.sleep(3)
            aguardar_elemento("div.ofertas-slider", timeout=30)
            scroll_down_and_up()
            baixar_todos_slides(2, download_dir)
        except Exception as e:
            print(f" Jornal 2 indisponível para {loja}: {str(e)}")
        try:
            clicar_elemento("//button[contains(., 'Jornal de Ofertas 3')]", By.XPATH)
            time.sleep(3)
            aguardar_elemento("div.ofertas-slider", timeout=30)
            scroll_down_and_up()
            baixar_todos_slides(2, download_dir)
        except Exception as e:
            print(f" Jornal 3 indisponível para {loja}: {str(e)}")

        clicar_elemento("a.seletor-loja", By.CSS_SELECTOR)
        time.sleep(2)


    try:
        def proximo_encarte():
            next_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "glider-next")))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
            time.sleep(0.5)
            next_button.click()
            time.sleep(2) 
        for i in range(2, 8):
            proximo_encarte()
            baixar_todos_slides(i)
            print(" Próximo encarte carregado.")
            
    except Exception as e:
            print(f" Erro ao clicar no botão de próximo encarte: {e}")
            print(f" Falha ao tentar baixar encarte {i}: {e}")

    print("✔️ Todos os encartes foram processados!")


except Exception as e:
    print(f" Erro crítico: {str(e)}")
    driver.save_screenshot(str(desktop_path / "erro_encartes.png"))
finally:
    driver.quit()

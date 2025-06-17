import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re


url = 'https://www.assai.com.br/ofertas'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

text = soup.get_text()

match = re.search(r'(\d{2}/\d{2}/\d{4})\s+a\s+(\d{2}/\d{2}/\d{4})', text)
if match:
    data_inicio = datetime.strptime(match.group(1), "%d/%m/%Y")
    data_fim = datetime.strptime(match.group(2), "%d/%m/%Y")
    hoje = datetime.now()

    print(f"Período do encarte: {data_inicio.date()} até {data_fim.date()}")
    if data_inicio <= hoje <= data_fim:
        print("O encarte está vigente. Baixando encarte...")
    else:
        print("O encarte não está mais vigente.")
else:
    print("Não foi possível encontrar a data na página.")

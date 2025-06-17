# encartes_downloader.py
import time
import os
import sys

def download_encartes(loja, estado):
    """
    Este script simula o download de encartes com base na loja e no estado.
    Em um cenário real, aqui estaria a lógica para:
    1. Acessar o site(s) apropriado(s) para a 'loja' e 'estado'.
    2. Identificar e baixar os encartes.
    3. Armazenar em um diretório específico.
    """
    
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Iniciando download para Loja: '{loja}', Estado: '{estado}'.")
    
    # Criar um diretório para os encartes, se não existir
    # Ex: encartes_baixados/Assai/Maranhao/
    output_dir = os.path.join("encartes_baixados", loja.replace(" ", "_"), estado.replace(" ", "_"))
    os.makedirs(output_dir, exist_ok=True)
    
    # Simular o processo de download
    for i in range(3):
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Baixando parte {i+1} de 3 para {loja} ({estado})...")
        time.sleep(2) # Simula um atraso no download
    
    # Criar um arquivo dummy como prova de download
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    filename = f"encarte_{loja.replace(' ', '_')}_{estado.replace(' ', '_')}_{timestamp}.txt"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, "w") as f:
        f.write(f"Este é um encarte simulado para {loja} em {estado}.\n")
        f.write(f"Baixado em: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Download concluído para {loja} ({estado}). Arquivo: {filepath}")

if __name__ == "__main__":
    # Este bloco permite que o script seja executado diretamente com argumentos
    # Ex: python encartes_downloader.py "Assaí" "Maranhão"
    if len(sys.argv) == 3:
        loja_arg = sys.argv[1]
        estado_arg = sys.argv[2]
        download_encartes(loja_arg, estado_arg)
    else:
        print("Uso: python encartes_downloader.py \"<nome_da_loja>\" \"<nome_do_estado>\"")
        print("Ex: python encartes_downloader.py \"Assaí\" \"Maranhão\"")
        print("Ex: python encartes_downloader.py \"Todos\" \"Todos\"")


# app.py
from flask import Flask, render_template, request, jsonify
import subprocess
import os
import sys
import threading

app = Flask(__name__)

# Rota principal que serve o arquivo index.html da pasta templates
@app.route('/')
def index():
    return render_template('index.html')

def run_downloader_script_in_background(loja, estado, process_output_callback):
    """
    Função para executar o script encartes_downloader.py em segundo plano.
    Captura a saída e a passa para um callback.
    """
    script_path = 'encartes_downloader.py'
    
    if not os.path.exists(script_path):
        error_msg = f"Erro: O script '{script_path}' não foi encontrado."
        print(error_msg)
        process_output_callback(error_msg)
        return

    try:
        # Use sys.executable para garantir que a versão correta do Python seja usada
        process = subprocess.Popen(
            [sys.executable, script_path, loja, estado],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,  # Para decodificar a saída como texto
            bufsize=1,  # Para leitura linha por linha
            universal_newlines=True # Compatibilidade de quebras de linha
        )

        output_lines = []
        for line in process.stdout:
            print(f"[encartes_downloader.py output]: {line.strip()}")
            output_lines.append(line.strip())
            process_output_callback(line.strip()) # Envia linha a linha para o callback
        
        stderr_output = process.stderr.read()
        if stderr_output:
            print(f"[encartes_downloader.py error]: {stderr_output.strip()}")
            output_lines.append(f"ERRO: {stderr_output.strip()}")

        process.wait() # Espera o processo terminar
        print(f"Script {script_path} para '{loja}', '{estado}' finalizado com código {process.returncode}")

    except Exception as e:
        error_msg = f"Erro ao executar o script '{script_path}': {e}"
        print(error_msg)
        process_output_callback(error_msg)

@app.route('/download_encartes', methods=['POST'])
def download_encartes_route():
    """
    Rota para processar a solicitação de download de encartes.
    Recebe a loja e o estado via JSON e dispara o script em background.
    """
    data = request.get_json()
    loja = data.get('loja')
    estado = data.get('estado')

    if not loja or not estado:
        return jsonify({'error': 'Parâmetros "loja" e "estado" são obrigatórios.'}), 400

    print(f"Requisição recebida: Baixar encartes para Loja: '{loja}', Estado: '{estado}'")

    # A saída do script não será retornada para o cliente imediatamente,
    # mas será logada no console do servidor.
    # Podemos usar uma lista global ou um mecanismo de log para capturar a saída
    # Se você precisar da saída no frontend, teria que implementar WebSockets.
    
    def dummy_callback(line):
        """Um callback simples para capturar as linhas de saída do script (no servidor)."""
        pass # Ou pode adicionar a um log global, se necessário.

    # Inicia a execução do script em uma thread separada
    thread = threading.Thread(
        target=run_downloader_script_in_background,
        args=(loja, estado, dummy_callback)
    )
    thread.daemon = True # Permite que o programa principal saia mesmo que o thread esteja rodando
    thread.start()

    return jsonify({
        'message': f'Download de encartes para "{loja}" em "{estado}" iniciado em segundo plano. Verifique o console do servidor para o progresso.'
    }), 200

if __name__ == '__main__':
    # Cria o diretório raiz para os encartes baixados se não existir
    os.makedirs("encartes_baixados", exist_ok=True)
    
    # Verifica se o script de download existe
    if not os.path.exists('encartes_downloader.py'):
        print("AVISO: 'encartes_downloader.py' não encontrado no diretório atual.")
        print("Certifique-se de criar o arquivo 'encartes_downloader.py' no mesmo diretório de 'app.py' para que funcione.")
    
    # Executa o aplicativo Flask
    app.run(debug=True) # debug=True é bom para desenvolvimento, desative em produção

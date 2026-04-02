# main.py
import os
import logging
from flask import Flask
from google.cloud import storage

app = Flask(__name__)

# Configuração de logs para o Cloud Logging
logging.basicConfig(level=logging.INFO)

@app.route('/')
def hello():
    return "App GKE funcionando normalmente!"

@app.route('/crash')
def crash():
    logging.error("Triggering a hard crash for investigation...")
    # Erro de divisão por zero: clássico para análise de stack trace
    result = 1 / 0
    return str(result)

@app.route('/iam-error')
def iam_error():
    logging.info("Tentando acessar bucket sem permissão...")
    try:
        # Tenta listar um bucket que não existe ou sem permissão
        storage_client = storage.Client()
        buckets = list(storage_client.list_buckets())
        return f"Buckets: {len(buckets)}"
    except Exception as e:
        logging.error(f"Erro de acesso ao Storage: {e}")
        raise e

@app.route('/oom')
def oom():
    logging.warning("Iniciando consumo massivo de memória...")
    # Simula um vazamento de memória para causar OOMKilled
    data = []
    for i in range(10000000):
        data.append(" " * 1000)
    return "Isso provavelmente não será retornado (OOM)"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
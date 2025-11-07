import time
import random
import requests
from cryptography.fernet import Fernet

#configurações
CHAVE = b'Oqkcb8h3YW4_GB_SJ35y1UKRDgfFt1P7y6Mm2cualbQ='

try:
    cifrador = Fernet(CHAVE)

except Exception:

    print(" CHAVE INVÁLIDA! Gere uma nova com 'gerar_chave.py' e cole-a aqui.")
    exit()

#aponta para o IP onde o 'servidor.py' está rodando)
URL_API = "http://127.0.0.1:5000/api/data"

# ID do dispositivo
ID_DISPOSITIVO = "sensor_esp32-01"

print(f" Iniciando simulação para o dispositivo: {ID_DISPOSITIVO}")

print(f" Enviando dados para: {URL_API}")

#Simulação de Envio 

while True:

    try:

        #dados simulados
        temperatura = round(random.uniform(20.0, 30.0), 2)


        #pacote no formato solicitado
        pacote_dados_original = f" {ID_DISPOSITIVO} : {temperatura}"

        print(f"\n Dados gerados: {pacote_dados_original}")

        #criptografar os dados

        #converter a string para bytes antes de criptografar
        pacote_criptografado = cifrador.encrypt(pacote_dados_original.encode('utf-8'))

        print(f" Pacote criptografado (primeiros 50 bytes): {pacote_criptografado[:50]}...")

        #enviar para o servidor
        resposta = requests.post(URL_API, data=pacote_criptografado, timeout=5)

        #verificação da resposta
        if resposta.status_code == 200:

            print(f" Dados enviados com sucesso: {pacote_dados_original}")

        else:

            print(f" Falha ao enviar dados. Status code: {resposta.status_code}")

            print(f" Resposta do servidor: {resposta.text}")

    except requests.exceptions.ConnectionError:

        print(" ERRO: Não foi possível conectar à API. O 'server.py' está rodando?")

    except Exception as e:

        print(f" Erro inesperado: {e}")    

    #aguardo de 2 segundos
    time.sleep(2)
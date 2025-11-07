# desafio-IC-BlockchainAttestation

##   Desafio de Simulação IoT e Criptografia (CS&I Lab)

Este projeto simula a lógica de coleta e envio de dados criptografados de um sensor (cliente) para uma API de servidor (receptor), atendendo a todos os requisitos do desafio.

### 1. Visão Geral do Projeto e Linguagem

| Item | Detalhes |
| :--- | :--- |
| **Linguagem Principal** | Python (versão 3.x) |
| **Sensor/Cliente** | `sensor.py` (Responsável pela simulação e criptografia) |
| **Servidor/API** | `servidor.py` (Responsável pela rota `/api/data` e descriptografia) |
| **Formato do Pacote** | `ID_DISPOSITIVO:TEMPERATURA` (Ex: `sensor_esp32-01:25.75`) |

### 2. Bibliotecas Utilizadas

As bibliotecas abaixo devem ser instaladas com `pip install -r requisitos.txt` (ou individualmente):

* **Flask:** Micro-framework usado para criar a API RESTful (o servidor).
* **Requests:** Utilizada pelo `sensor.py` para realizar a comunicação HTTP POST para a API.
* **Cryptography (Fernet):** Biblioteca robusta para criptografia simétrica, garantindo a confidencialidade dos dados (Item 5).
* **Time e Random:** Usadas para simular a variação da temperatura (`random`) e o intervalo de envio de 2 segundos (`time.sleep`) (Item 2).

### 3. Detalhes de Implementação e Requisitos

#### A. Simulação e Formato (Item 1)
* **ID do Dispositivo:** Definido como `ID_DISPOSITIVO = "sensor_esp32-01"`.
* **Valor da Leitura:** Gerado de forma aleatória e contínua na variável `temperatura`.
* **Pacote:** O sensor monta a string `f"{ID_DISPOSITIVO}:{temperatura}"` antes da criptografia.

#### B. Comunicação (Item 3 e 4)
* **Endpoint:** A comunicação é feita via requisição **POST** para a rota `/api/data`.
* **URL da API:** `http://127.0.0.1:5000/api/data`.
* **Frequência:** O `sensor.py` envia um pacote a cada 2 segundos.

#### C. Criptografia e Descriptografia (Item 5)
* **Chave Secreta:** A constante `CHAVE` (ou `CHAVE_SECRETA`) é idêntica nos dois scripts, permitindo que o `servidor.py` descriptografe o pacote de bytes enviado pelo `sensor.py`.

### 4. Como Rodar o Projeto

É necessário rodar dois scripts Python simultaneamente em terminais separados para simular o ambiente Cliente-Servidor:

#### A. Terminal 1: Servidor API
O servidor deve ser iniciado primeiro para que esteja ouvindo na porta 5000.

```bash
python servidor.py

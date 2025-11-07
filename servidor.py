from flask import Flask, request, jsonify
from cryptography.fernet import Fernet, InvalidToken
# Adicione InvalidToken na lista de importação acima

#configuração
app = Flask(__name__)

#deve ser a MESMA chave usada no 'sensor.py'
CHAVE = b'Oqkcb8h3YW4_GB_SJ35y1UKRDgfFt1P7y6Mm2cualbQ='

try:
    cifrador = Fernet(CHAVE)
    print("Servidor iniciado com sucesso. Aguardando dados...")
except Exception as e:
    print(f"ERRO: Chave inválida! Gere uma nova. Detalhe: {e}")
    exit()

#o parâmetro 'methods' deve receber uma lista ['POST']
@app.route('/api/data', methods=['POST'])
def receber_dados():
    """
    Endpoint para receber os dados criptografados do sensor.
    """
    print("\nNova requisição recebida...")
    
    #obter os dados brutos (bytes) da requisição
    #usamos request.data porque o sensor envia bytes brutos, não JSON
    pacote_criptografado = request.data

    if not pacote_criptografado:
        print("ERRO: Requisição vazia.")
        return jsonify({"status": "erro", "mensagem": "Nenhum dado recebido"}), 400

    #tentar descriptografar os dados
    try:
        #tenta descriptografar o pacote de bytes
        pacote_original_bytes = cifrador.decrypt(pacote_criptografado)
        
        #converte os bytes descriptografados de volta para string
        pacote_original_string = pacote_original_bytes.decode('utf-8')
        
        print(f"Dados recebidos e descriptografados: '{pacote_original_string}'")
        
        #retorna sucesso
        return jsonify({"status": "sucesso", "dados_recebidos": pacote_original_string}), 200

    except InvalidToken:
        #isso acontece se a chave estiver errada ou os dados estiverem corrompidos
        print("ERRO: Falha ao descriptografar! Token inválido.")
        return jsonify({"status": "erro", "mensagem": "Token inválido ou chave incorreta"}), 400
    except Exception as e:
        print(f"ERRO: Erro inesperado. {e}")
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

#Bloco para iniciar o servidor
if __name__ == '__main__':
    # host='0.0.0.0' torna o servidor acessível na rede
    app.run(host='0.0.0.0', port=5000, debug=True)
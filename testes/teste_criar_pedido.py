import requests

url = "http://localhost:5050/criar_pedido"

pedido = {
    "cliente": "João Silva",
    "descricao": "Instalação de telhado residencial",
    "valor": 8500.00
}

response = requests.post(url, json=pedido)

print("Status Code:", response.status_code)
print("Resposta JSON:", response.json())

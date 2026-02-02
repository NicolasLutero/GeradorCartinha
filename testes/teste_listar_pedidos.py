import requests

url = "http://localhost:5050/listar_pedidos"

response = requests.get(url)

print("Status Code:", response.status_code)
print("Pedidos:")
print(response.json())

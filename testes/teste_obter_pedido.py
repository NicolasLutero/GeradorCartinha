import requests

pedido_id = 1
url = f"http://localhost:5050/buscar_pedido/{pedido_id}"

response = requests.get(url)

print("Status Code:", response.status_code)
print("Pedido:")
print(response.json())

import requests
import json

# Probar la funcionalidad de búsqueda
url = "http://127.0.0.1:8080/tributario/buscar-identificacion/"
data = {"identidad": "1234567890123"}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")

















import requests
import json

data = {
    "name": "Maruti Swift Dzire VDI",
    "year": 2014,
    "km_driven": 145500,
    "fuel": "Diesel",
    "seller_type": "Individual",
    "transmission": "Manual",
    "owner": "First Owner",
    "mileage": "23.4 kmpl",
    "engine": "1248 CC",
    "max_power": "74 bhp",
    "torque": "190Nm@ 2000rpm",
    "seats": 5.0
}

url = "http://127.0.0.1:8000/predict_item"

response = requests.post(url, json=data)
if response.status_code == 200:
    print(f"Предсказанная цена: {response.json()}")
else:
    print(f"Ошибка: {response.text}")
import requests
import json

API_URL = "http://96.9.212.102:8000/orders"

response = requests.get(API_URL)

if response.status_code == 200:
    data = response.json()

    print("Success mengambil data")

    print(f"\nTotal Orders: {data['total_orders']}")

    print("\nContoh 1 Order:\n")
    print(json.dumps(data['orders'][0], indent=4))

else:
    print(f"Gagal mengambil data. Status code: {response.status_code}")
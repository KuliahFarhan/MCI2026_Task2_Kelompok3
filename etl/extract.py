import requests

API_URL = "http://96.9.212.102:8000/orders"

def extract_orders():
    response = requests.get(API_URL)

    if response.status_code == 200:
        return response.json()

    raise Exception(
        f"Gagal mengambil data. Status code: {response.status_code}"
    )
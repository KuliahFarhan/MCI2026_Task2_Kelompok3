import requests

from transform import transform_orders
from load import load_to_clickhouse

API_URL = "http://96.9.212.102:8000/orders"


def extract_orders():
    response = requests.get(API_URL)

    if response.status_code == 200:
        return response.json()

    raise Exception(
        f"Gagal mengambil data. Status code: {response.status_code}"
    )


if __name__ == "__main__":

    raw_data = extract_orders()

    transformed_data = transform_orders(raw_data)

    load_to_clickhouse(transformed_data)

    print("\nETL pipeline berhasil dijalankan")
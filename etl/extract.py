import requests
from transform import transform_orders

API_URL = "http://96.9.212.102:8000/orders"


def extract_orders():
    response = requests.get(API_URL)

    if response.status_code == 200:
        return response.json()

    raise Exception(
        f"Gagal mengambil data. Status code: {response.status_code}"
    )


if __name__ == "__main__":
    data = extract_orders()

    print("Success mengambil data")
    print(f"Total Orders: {data['total_orders']}")

    transformed = transform_orders(data)

    print(f"\nTotal transformed rows: {len(transformed)}")

    print("\nContoh transformed row:\n")
    print(transformed[0])
import clickhouse_connect


def load_to_clickhouse(data):

    client = clickhouse_connect.get_client(
        host='localhost',
        port=8123,
        username='admin',
        password='admin123',
        database='mci_orders'
    )

    rows = []

    for item in data:
        rows.append([
            item["order_id"],
            item["user_id"],
            item["order_number"],
            item["order_dow"],
            item["order_hour_of_day"],
            item["days_since_prior_order"],
            item["eval_set"],

            item["product_id"],
            item["product_name"],

            item["aisle_id"],
            item["aisle"],

            item["department_id"],
            item["department"],

            item["add_to_cart_order"],
            item["reordered"]
        ])

    client.insert(
        'orders',
        rows
    )

    print(f"Berhasil insert {len(rows)} rows ke ClickHouse")
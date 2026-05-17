def transform_orders(raw_data):
    transformed_data = []

    orders = raw_data["orders"]

    for order in orders:
        for product in order["products"]:

            row = {
                "order_id": order["order_id"],
                "user_id": order["user_id"],
                "order_number": order["order_number"],
                "order_dow": order["order_dow"],
                "order_hour_of_day": order["order_hour_of_day"],
                "days_since_prior_order": order["days_since_prior_order"],
                "eval_set": order["eval_set"],

                "product_id": product["product_id"],
                "product_name": product["product_name"],
                "aisle_id": product["aisle_id"],
                "aisle": product["aisle"],
                "department_id": product["department_id"],
                "department": product["department"],
                "add_to_cart_order": product["add_to_cart_order"],
                "reordered": product["reordered"]
            }

            transformed_data.append(row)

    return transformed_data
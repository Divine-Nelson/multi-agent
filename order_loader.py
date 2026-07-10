import json


def load_production_plan(filename="production_plan.json"):
    with open(filename, "r") as file:
        return json.load(file)


def expand_orders(plan):
    parts_to_create = []
    counter_a = 1
    counter_b = 1

    for order in plan["orders"]:
        part_type = order["partType"]
        quantity = order["quantity"]

        for _ in range(quantity):
            if part_type == 1:
                parts_to_create.append({
                    "name": f"ProductA_{counter_a}",
                    "agentType": "ProductA",
                    "partType": 1
                })
                counter_a += 1

            elif part_type == 2:
                parts_to_create.append({
                    "name": f"ProductB_{counter_b}",
                    "agentType": "ProductB",
                    "partType": 2
                })
                counter_b += 1

    return parts_to_create


def save_orders_for_cmas(parts, filename="orders_for_cmas.txt"):
    with open(filename, "w") as file:
        for part in parts:
            file.write(f'{part["agentType"]},{part["name"]},{part["partType"]}\n')


if __name__ == "__main__":
    plan = load_production_plan()
    parts = expand_orders(plan)

    print("Parts to create:")
    for part in parts:
        print(part)

    save_orders_for_cmas(parts)

    print("\nSaved CMAS order file: orders_for_cmas.txt")
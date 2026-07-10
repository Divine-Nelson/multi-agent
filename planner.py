import requests
import json

OLLAMA_URL = "http://172.20.10.2:11434/api/generate"
MODEL = "llama3:8b"


def ask_ollama_for_plan(user_request: str) -> dict:
    prompt = f"""
You are a strict production order parser.

Your task is to convert the user's request into JSON only.

Available part types:
- type 1
- type 2

Mapping:
- "type 1" means partType 1
- "ProductA" means partType 1
- "A" means partType 1
- "type 2" means partType 2
- "ProductB" means partType 2
- "B" means partType 2

Rules:
- Extract every requested part type and quantity exactly.
- Do not change type 2 into type 1.
- Do not guess.
- If the user asks for "one type 2 part", output partType 2 with quantity 1.
- Output JSON only.
- No explanation.
- No markdown.

Required JSON format:
{{
  "orders": [
    {{
      "partType": 1,
      "quantity": 2
    }},
    {{
      "partType": 2,
      "quantity": 1
    }}
  ]
}}

Example:
User request: Make two type 1 parts and one type 2 part
Correct output:
{{
  "orders": [
    {{
      "partType": 1,
      "quantity": 2
    }},
    {{
      "partType": 2,
      "quantity": 1
    }}
  ]
}}

Now parse this request:
{user_request}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=60
    )

    response.raise_for_status()

    raw_text = response.json()["response"].strip()

    try:
        plan = json.loads(raw_text)
    except json.JSONDecodeError:
        raise ValueError(f"Ollama returned invalid JSON:\n{raw_text}")

    validate_plan(plan)
    return plan


def validate_plan(plan: dict) -> None:
    if not isinstance(plan, dict):
        raise ValueError("Plan must be a JSON object.")

    if "orders" not in plan:
        raise ValueError("Plan must contain 'orders'.")

    if not isinstance(plan["orders"], list):
        raise ValueError("'orders' must be a list.")

    if len(plan["orders"]) == 0:
        raise ValueError("'orders' cannot be empty.")

    for order in plan["orders"]:
        if "partType" not in order:
            raise ValueError("Each order must contain 'partType'.")

        if "quantity" not in order:
            raise ValueError("Each order must contain 'quantity'.")

        if order["partType"] not in [1, 2]:
            raise ValueError("partType must be 1 or 2.")

        if not isinstance(order["quantity"], int):
            raise ValueError("quantity must be an integer.")

        if order["quantity"] < 1:
            raise ValueError("quantity must be at least 1.")


if __name__ == "__main__":
    user_request = input("Enter production request: ")

    plan = ask_ollama_for_plan(user_request)

    print("\nValidated production plan:")
    print(json.dumps(plan, indent=4))

    with open("jobs.json", "w") as file:
        json.dump(plan, file, indent=4)

    print("\nPlan saved to jobs.json")
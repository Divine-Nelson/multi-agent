import json
import time
from pymodbus.client import ModbusTcpClient

MODBUS_HOST = "127.0.0.1"
MODBUS_PORT = 502

GENERATE_A = 6
GENERATE_B = 7

SOURCE1_SENSOR = 17
SOURCE2_SENSOR = 18

JOB_FILE = "jobs.json"


def read_register(client, address):
    result = client.read_holding_registers(address=address, count=1)
    if result.isError():
        raise RuntimeError(f"Failed to read register {address}")
    return result.registers[0]


def pulse_register(client, address):
    client.write_register(address, 1)
    time.sleep(0.2)
    client.write_register(address, 0)


def load_jobs():
    with open(JOB_FILE, "r") as file:
        data = json.load(file)

    queue = []

    for order in data["orders"]:
        part_type = order["partType"]
        quantity = order["quantity"]

        for _ in range(quantity):
            queue.append(part_type)

    return queue


def main():
    queue = load_jobs()

    client = ModbusTcpClient(MODBUS_HOST, port=MODBUS_PORT)
    client.connect()

    print("Dispatcher started.")
    print("Job queue:", queue)

    try:
        while queue:
            next_part = queue[0]

            source1_free = read_register(client, SOURCE1_SENSOR) == 0
            source2_free = read_register(client, SOURCE2_SENSOR) == 0

            if next_part == 1 and source1_free:
                print("Generating ProductA")
                pulse_register(client, GENERATE_A)
                queue.pop(0)
                time.sleep(1)

            elif next_part == 2 and source2_free:
                print("Generating ProductB")
                pulse_register(client, GENERATE_B)
                queue.pop(0)
                time.sleep(1)

            else:
                time.sleep(0.5)

        print("All jobs dispatched.")

    finally:
        client.close()


if __name__ == "__main__":
    main()
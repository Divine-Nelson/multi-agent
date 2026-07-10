from pymodbus.client import ModbusTcpClient
import time

client = ModbusTcpClient("127.0.0.1", port=502)
client.connect()

value = client.read_holding_registers(address=17, count=1).registers[0]

client.write_register(address=1, value=100)  # setX := 100


# Try Source1 button
client.write_register(7, 1)
#client.write_register(6, 1)
time.sleep(0.3)
client.write_register(7, 0)

client.close()
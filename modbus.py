import time
from telemetrix import telemetrix
from pyModbusTCP.server import ModbusServer

# 1. Configura o Servidor Modbus TCP local na porta padrão 5020 não precisa de sudo
server = ModbusServer(host="0.0.0.0", port=5020, no_block=True)

# 2. Inicializa o Arduino via Telemetrix
board = telemetrix.Telemetrix()

# Variável para guardar a leitura
pino_analogico = 0
valor_sensor = 0

def callback_analogico(data):
    global valor_sensor
    # data[2] contém o valor lido do pino (ex: de 0 a 1023)
    valor_sensor = data[2]

# Configura o pino A0 para leitura
board.set_pin_mode_analog_input(pino_analogico, callback=callback_analogico)

try:
    print("Iniciando gateway Modbus TCP...")
    server.start()
    
    while True:
        # Atualiza o Holding Register 0 do Modbus com o valor atual do sensor
        server.data_bank.set_holding_registers(0, [valor_sensor])
        time.sleep(0.1)

except KeyboardInterrupt:
    print("A parar o serviço...")
    board.shutdown()
    server.stop()
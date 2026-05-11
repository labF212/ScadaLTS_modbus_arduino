import asyncio
from telemetrix import telemetrix
from pyModbusTCP.server import ModbusServer
import flet as ft

# ================= MODBUS =================
server = ModbusServer(host="0.0.0.0", port=5020, no_block=True)

# ================= HARDWARE PINS =================
DHT_PIN = 11
LDR_PIN = 0
TRIG_PIN = 8
ECHO_PIN = 9
PWM_PIN = 6      # Motor DC
RELE_PIN = 7
PIR_PIN = 2
SERVO_PIN = 10

board = telemetrix.Telemetrix()

# ================= VARIÁVEIS GLOBAIS =================
valor_ldr = 0
temperatura = 0
humidade = 0
distancia_ultrassom = 0
movimento_pir = 0
estado_rele = "OFF"
angulo_servo = 0
velocidade_motor = 0  # <--- Variável do motor
estado_modbus = "OFFLINE"
ultimo_pwm = -1

# ================= CALLBACKS HARDWARE =================
def callback_dht(data):
    global temperatura, humidade
    if data[1] == 0:
        humidade = data[4]
        temperatura = data[5]

def callback_ldr(data):
    global valor_ldr
    valor_ldr = data[2]

def callback_sonar(data):
    global distancia_ultrassom
    distancia_ultrassom = data[2]

def callback_pir(data):
    global movimento_pir
    movimento_pir = data[2]

# Configuração dos Modos
board.set_pin_mode_dht(DHT_PIN, callback=callback_dht, dht_type=11)
board.set_pin_mode_analog_input(LDR_PIN, callback=callback_ldr)
board.set_pin_mode_sonar(TRIG_PIN, ECHO_PIN, callback=callback_sonar)
board.set_pin_mode_digital_input(PIR_PIN, callback=callback_pir)
board.set_pin_mode_digital_output(RELE_PIN)
board.set_pin_mode_servo(SERVO_PIN)
board.set_pin_mode_analog_output(PWM_PIN) # Configura pino 6 para o Motor DC

# ================= APP FLET =================
async def main(page: ft.Page):
    global valor_ldr, temperatura, humidade, estado_rele, angulo_servo, velocidade_motor
    loop_task = None

    page.title = "Servidor Modbus Completo"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # UI
    ldr_txt = ft.Text("LDR: --", size=18)
    dht_txt = ft.Text("Temp: -- | Hum: --", size=18)
    sonar_txt = ft.Text("Distância: -- cm", size=18)
    pir_txt = ft.Text("Movimento: --", size=18)
    motor_txt = ft.Text("Motor DC: 0", color=ft.Colors.BLUE_400, weight="bold")
    atuadores_txt = ft.Text("Relé: -- | Servo: --", weight="bold")

    async def on_exit(e):
        if loop_task: loop_task.cancel()
        server.stop()
        board.shutdown()
        await page.window.close()

    page.add(
        ft.Column([
            ft.Text("Dashboard Arduino - Scada-LTS", size=24, weight="bold"),
            ldr_txt, dht_txt, sonar_txt, pir_txt, motor_txt, ft.Divider(),
            atuadores_txt,
            ft.FilledButton("Desconectar e Sair", on_click=on_exit, bgcolor=ft.Colors.RED_ACCENT_400)
        ], horizontal_alignment="center")
    )

    if not server.is_run: server.start()

    async def update_loop():
        global estado_rele, angulo_servo, velocidade_motor
        try:
            while True:
                # 1. Enviar para o Scada (Offsets 0, 3, 4, 5, 6 e agora 7)
                server.data_bank.set_holding_registers(0, [valor_ldr])
                server.data_bank.set_holding_registers(3, [int(temperatura)])
                server.data_bank.set_holding_registers(4, [int(humidade)])
                server.data_bank.set_holding_registers(5, [int(distancia_ultrassom)])
                server.data_bank.set_holding_registers(6, [movimento_pir])
                server.data_bank.set_holding_registers(8, [velocidade_motor]) # Feedback da velocidade

                # 2. Ler do Scada e Atuar
                # Relé (Offset 1)
                regs_rele = server.data_bank.get_holding_registers(1, 1)
                if regs_rele:
                    board.digital_write(RELE_PIN, regs_rele[0])
                    estado_rele = "ON" if regs_rele[0] == 1 else "OFF"

                # Servo (Offset 2)
                regs_servo = server.data_bank.get_holding_registers(2, 1)
                if regs_servo:
                    board.servo_write(SERVO_PIN, regs_servo[0])
                    angulo_servo = regs_servo[0]
                
                # Motor DC (Offset 7)
                global ultimo_pwm

                regs_motor = server.data_bank.get_holding_registers(7, 1)

                if regs_motor:

                    velocidade_motor = int(
                        max(0, min(255, regs_motor[0]))
                    )

                    # só envia se mudar
                    if velocidade_motor != ultimo_pwm:

                        board.analog_write(
                            PWM_PIN,
                            velocidade_motor
                        )

                        ultimo_pwm = velocidade_motor

                        print("PWM:", velocidade_motor)

                # 3. UI Update
                ldr_txt.value = f"LDR: {valor_ldr}"
                dht_txt.value = f"Temperatura: {temperatura}°C | Humidade: {humidade}%"
                sonar_txt.value = f"Distância: {distancia_ultrassom} cm"
                pir_txt.value = f"Movimento: {'SIM' if movimento_pir else 'NÃO'}"
                motor_txt.value = f"Motor DC (PWM): {velocidade_motor}"
                atuadores_txt.value = f"Relé: {estado_rele} | Servo: {angulo_servo}°"
                
                page.update()
                await asyncio.sleep(0.3)
        except asyncio.CancelledError:
            pass

    loop_task = asyncio.create_task(update_loop())

if __name__ == "__main__":
    ft.app(target=main)
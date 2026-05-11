import asyncio
from telemetrix import telemetrix
from pyModbusTCP.server import ModbusServer
import flet as ft

# ================= MODBUS =================
server = ModbusServer(host="0.0.0.0", port=5020, no_block=True)

# ================= ARDUINO =================
board = telemetrix.Telemetrix()

pino_analogico = 0
valor_sensor = 0

def callback_analogico(data):
    global valor_sensor
    valor_sensor = data[2]

board.set_pin_mode_analog_input(pino_analogico, callback=callback_analogico)

# ================= APP =================
async def main(page: ft.Page):
    global valor_sensor

    page.title = "Servidor de modbus – Arduino + Flet"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    ldr_text = ft.Text("Luminosidade: -- V", size=20)

    # botão de saída
    async def on_exit(e):
        board.shutdown()
        server.stop()
        await page.window.destroy()

    page.add(
        ft.Column(
            [
                ldr_text,
                ft.Button("Sair", on_click=on_exit)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    server.start()

    async def update_loop():
        while True:
            server.data_bank.set_holding_registers(0, [valor_sensor])

            ldr_v = valor_sensor * 5 / 1023
            ldr_text.value = f"Luminosidade: {ldr_v:.2f} V"

            page.update()
            await asyncio.sleep(0.1)

    asyncio.create_task(update_loop())


# ================= RUN =================
ft.app(target=main)
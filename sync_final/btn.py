import flet as ft
from sync_final.sync import main_sync
import asyncio

def btn1(page: ft.Page):
    page.title = "Nissi Sync"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START

    page.window_width = 420
    page.window_height = 300
    page.padding = 50

    # Mantener una referencia a la tarea asincrónica
    page.task = None
    page.sync_running = False

    async def change(event):
        valor = event.control.value
        
        if page.task:
            page.task.cancel()  # Cancelar la tarea actual si existe
            try:
                await page.task
            except asyncio.CancelledError:
                print("Tarea cancelada")
            page.sync_running = False

        if valor:  # Iniciar una nueva tarea si el valor es True
            page.task = asyncio.create_task(main_sync())
            page.sync_running = True

    page.add(
        ft.Text("SINCRONIZACIÓN NISSI", color="PRIMARY")
    )

    page.add(
        ft.CupertinoSwitch(
            value=True,
            on_change=lambda event: asyncio.create_task(change(event))
        ),
    )

# Asegurarse de que el bucle de eventos se ejecuta en el hilo principal
async def btn(page: ft.Page):
    btn1(page)
    await asyncio.Event().wait()  # Mantiene el bucle de eventos en ejecución
from sync_final.sync import main_sync
import asyncio
from configparser import ConfigParser as Config
from config_view import main_page
import flet as ft
from insert_columns import insert_columns
from insert_fun import insert_fun
import tkinter as tk
from tkinter import Label
import os
import platform


def configure_program():
    # Ejecuta la configuración del programa
    ft.app(target=main_page)
    insert_columns()
    insert_fun()

def show_open_again():
    root = tk.Tk()
    root.title("Vuelva a abrir")
    Label(root, text="Vuelva a abrir el programa para que empiece a funcionar").pack(pady=100, padx=50)
    root.after(2000, root.destroy)  # Cierra la ventana después de 5 segundos
    root.mainloop()

def main():
    config = Config()
    config_path = "c:/Sysven/config.ini"

    if os.path.exists(config_path):
        config.read(config_path)
        if not "fit" in config.sections():
            config.add_section("fit")
            config.set("fit", "validate", "0")

        if config.get("fit", "validate") == '1':
            asyncio.run(main_sync())
        else:
            configure_program()
            show_open_again()
    else:
        root = "C:\\" if platform.system() == "Windows" else "/"
        folder_path = os.path.join(root, 'Sysven')
        os.makedirs(folder_path, exist_ok=True)
        with open(config_path, 'w') as configfile:
            config.write(configfile)
        if not "fit" in config.sections():
            config.add_section("fit")
            config.set("fit", "validate", "0")

        configure_program()
        show_open_again()

if __name__ == '__main__':
    main()

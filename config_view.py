import flet as ft
from configparser import ConfigParser
import cryptocode 
import os

def main_page(page: ft.Page):
    page.title = "Configuración Nissi Farma"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START

    page.window_width = 420
    page.window_height = 660
    page.padding = 50

    serial = ft.TextField(label="Serial", border=ft.InputBorder.NONE, bgcolor="#e1e1e1", color="#0e6cb9")
    cliente = ft.TextField(label="Nombre del cliente", border=ft.InputBorder.NONE, bgcolor="#e1e1e1", color="#0e6cb9")

    page.add(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Image("C:/Sysven/Resources/Images/logo-nissi.png", width=150)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Row(height=20),
                ft.Row([serial]),
                ft.Row([cliente]),
                ft.Row(height=20),
                ft.Row(
                    [
                        ft.FilledButton(
                            "Validar",
                            style=ft.ButtonStyle(
                                shape={
                                    ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=0)
                                },
                                bgcolor="#0e6cb9"
                            ),
                            on_click=lambda e: show_db1_form(page, serial.value, cliente.value)
                        )
                    ],
                    alignment="CENTER"
                ),
            ],
        )
    )
    page.update()

def show_db1_form(page, serial, cliente):
    page.clean()

    server1 = ft.TextField(label="Servidor BD1", border=ft.InputBorder.NONE, bgcolor="#e1e1e1", color="#0e6cb9")
    database1 = ft.TextField(label="Base de datos BD1", border=ft.InputBorder.NONE, bgcolor="#e1e1e1", color="#0e6cb9")
    user1 = ft.TextField(label="Usuario de Postgres BD1", border=ft.InputBorder.NONE, bgcolor="#e1e1e1", color="#0e6cb9", value="postgres")
    password1 = ft.TextField(label="Clave de Postgres BD1", password=True, can_reveal_password=True, border=ft.InputBorder.NONE, bgcolor="#e1e1e1", color="#0e6cb9")
    port1 = ft.TextField(label="Puerto BD1", border=ft.InputBorder.NONE, bgcolor="#e1e1e1", color="#0e6cb9", value=5432)

    def pick_files_result(e: ft.FilePickerResultEvent):
        config = ConfigParser()
        config.read(e.files[0].path.replace("\\", "/"))
        server1.value = config.get("CONFIG", "SERVER")
        database1.value = config.get("CONFIG", "DATABASE")
        page.update()

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)

    searchButton = ft.FilledButton(
        text="Abrir Config.ini",
        icon=ft.icons.UPLOAD_FILE,
        on_click=pick_files_dialog.pick_files,
        style=ft.ButtonStyle(
            shape={
                ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=0)
            },
            bgcolor="#0e6cb9"
        ),
    )

    page.overlay.append(pick_files_dialog)

    page.add(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Image("C:/Sysven/Resources/Images/logo-nissi.png", width=150)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Row([searchButton], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([server1], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([database1], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([user1], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([port1], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([password1], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row(height=20),
                ft.Row(
                    [
                        ft.FilledButton(
                            "Aceptar",
                            style=ft.ButtonStyle(
                                shape={
                                    ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=0)
                                },
                                bgcolor="#0e6cb9"
                            ),
                            key={
                                "serial": serial,
                                "cliente": cliente,
                                "server1": server1,
                                "database1": database1,
                                "user1": user1,
                                "password1": password1,
                                "port1": port1
                            },
                            on_click=show_db2_form
                        )
                    ],
                    alignment="CENTER"
                ),
            ],
        )
    )
    page.update()

def show_db2_form(event):
    page = event.control.page
    data = event.control.key
    page.clean()

    server2 = ft.TextField(label="Servidor BD2", border=ft.InputBorder.NONE, bgcolor="#e1e1e1", color="#0e6cb9")
    database2 = ft.TextField(label="Base de datos BD2", border=ft.InputBorder.NONE, bgcolor="#e1e1e1", color="#0e6cb9")
    user2 = ft.TextField(label="Usuario de Postgres BD2", border=ft.InputBorder.NONE, bgcolor="#e1e1e1", color="#0e6cb9", value="postgres")
    password2 = ft.TextField(label="Clave de Postgres BD2", password=True, can_reveal_password=True, border=ft.InputBorder.NONE, bgcolor="#e1e1e1", color="#0e6cb9")
    port2 = ft.TextField(label="Puerto BD2", border=ft.InputBorder.NONE, bgcolor="#e1e1e1", color="#0e6cb9", value=5432)

    page.add(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Image("C:/Sysven/Resources/Images/logo-nissi.png", width=150)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Row([server2], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([database2], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([user2], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([port2], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([password2], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row(height=20),
                ft.Row(
                    [
                        ft.FilledButton(
                            "Aceptar",
                            style=ft.ButtonStyle(
                                shape={
                                    ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=0)
                                },
                                bgcolor="#0e6cb9"
                            ),
                            key={
                                **data,
                                "server2": server2,
                                "database2": database2,
                                "user2": user2,
                                "password2": password2,
                                "port2": port2
                            },
                            on_click=gen_config
                        )
                    ],
                    alignment="CENTER"
                ),
            ],
        )
    )
    page.update()

def gen_config(event):
    page = event.control.page
    data = event.control.key
    page.clean()

    #Cambiar segun se desee

    key='grupo.sysven779..'

    config = ConfigParser()
    # Especificar la ruta del archivo config.ini
    config_path = r'C:\Sysven\config.ini'

    # Leer el archivo config.ini si existe
    if os.path.exists(config_path):
        config.read(config_path)
    



    config['DB1_SYNC'] = {
        'host':  cryptocode.encrypt(str(data['server1'].value),key),
        'port':  cryptocode.encrypt(str(data['port1'].value),key),
        'dbname':  cryptocode.encrypt(str(data['database1'].value),key),
        'user':  cryptocode.encrypt(str(data['user1'].value),key),
        'password':  cryptocode.encrypt(str(data['password1'].value),key)
    }

    config['DB2_SYNC'] = {
        'host': cryptocode.encrypt(str(data['server2'].value),key),
        'port': cryptocode.encrypt(str(data['port2'].value),key),
        'dbname': cryptocode.encrypt(str(data['database2'].value),key),
        'user': cryptocode.encrypt(str(data['user2'].value),key),
        'password': cryptocode.encrypt(str(data['password2'].value),key)
    }
    config['fit']={
        'validate':'1'
    }


    with open(config_path, 'w') as configfile:
        config.write(configfile)

    page.window_destroy()


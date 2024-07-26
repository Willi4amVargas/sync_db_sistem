from sync_final.sync import main_sync
import asyncio
from configparser import ConfigParser as Config
from config_view import main_page
import flet as ft
from insert_columns import insert_columns
from insert_fun import insert_fun
import os

if __name__ == '__main__':

    config = Config()
    config_path="c:/Sysven/config.ini"

    if os.path.exists(config_path):
        config.read(config_path)
        if not "fit" in config.sections():
            config.add_section("fit")
            config.set("fit","validate", "0")

        if config.get("fit","validate") == '1':
            try:
                asyncio.run(main_sync())
            except KeyboardInterrupt:
                print("Program terminated by user")
        else:
            ft.app(target=main_page)
            insert_columns()
            insert_fun()
    else:
        with open(config_path, 'w') as configfile:
            config.write(configfile)
        if not "fit" in config.sections():
            config.add_section("fit")
            config.set("fit","validate", "0")

        if config.get("fit","validate") == "1":
            try:
                asyncio.run(main_sync())
            except KeyboardInterrupt:
                print("Program terminated by user")
        else:
            ft.app(target=main_page)
            insert_columns()
            insert_fun()


import psycopg2
import cryptocode
from configparser import ConfigParser as Config

def database1():
    #Cambiar key segun se requiera
    key = "grupo.sysven779.."
    config = Config()
    config.read("c:/Sysven/config.ini")

    database = cryptocode.decrypt(config.get("DB1_SYNC","dbname"),key)
    server = cryptocode.decrypt(config.get("DB1_SYNC","host"),key)
    user = cryptocode.decrypt(config.get("DB1_SYNC","user"),key)
    password = cryptocode.decrypt(config.get("DB1_SYNC","password"),key)
    port = cryptocode.decrypt(config.get("DB1_SYNC","port"),key)
    try:     
        conn = psycopg2.connect(**{
            'dbname':database,
            'user':user,
            'password':password,
            'host':server,
            'port':port
        })
        return conn
    except psycopg2.Error as e:
        print(f"Error al conectar a PostgreSQL: {e}")

        return None
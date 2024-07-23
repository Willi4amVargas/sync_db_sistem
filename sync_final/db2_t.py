import psycopg2

""" AQUI VAN LOS DATOS DE CONECCION DE LA SEGUNDA BASE DE DATOS """
""" HERE IS THE CONNECTION DATA OF THE SECOND DATABASE """

def db2():
    try:     
        conn = psycopg2.connect(**{
            'dbname': '',
            'user': '',
            'password': '',
            'host': '',
            'port': ''
        })
        return conn
    except psycopg2.Error as e:
        print(f"Error al conectar a PostgreSQL: {e}")

        return None

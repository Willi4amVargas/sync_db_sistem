import psycopg2
from db1 import db1 as db1
from db2 import db2 as db2

def sync_table(table_name):
    try:
        # Conectar a la primera base de datos
        conn_a = db1()
        cursor_a = conn_a.cursor()
        
        # Conectar a la segunda base de datos
        conn_b = db2()
        cursor_b = conn_b.cursor()

        # Obtener todas las filas de ambas bases de datos
        query = f"SELECT * FROM {table_name};"
        cursor_a.execute(query)
        rows_a = cursor_a.fetchall()
        cursor_b.execute(query)
        rows_b = cursor_b.fetchall()
        
        # Convertir listas de filas a diccionarios para un acceso más fácil
        dict_a = {row[0]: row for row in rows_a}
        dict_b = {row[0]: row for row in rows_b}
        
        # Obtener columnas de la tabla
        cursor_a.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}';")
        columns = [col[0] for col in cursor_a.fetchall()]
        update_columns = ", ".join([f"{col} = %s" for col in columns[1:]]) # Saltar la columna de clave primaria
        
        # Iterar sobre todas las claves primarias en ambas bases de datos
        all_keys = set(dict_a.keys()).union(dict_b.keys())
        
        for key in all_keys:
            row_a = dict_a.get(key)
            row_b = dict_b.get(key)
            
            if row_a and row_b:
                # Ambas bases de datos tienen esta fila, comparar fechas de actualización
                last_update_a = row_a[-1]
                last_update_b = row_b[-1]
                
                if last_update_a is not None and last_update_b is not None:
                    if last_update_a < last_update_b:
                        # La fila en B es más reciente, actualizar A
                        cursor_a.execute(f"""
                            UPDATE {table_name} SET {update_columns}
                            WHERE {columns[0]} = %s
                        """, row_b[1:] + (row_b[0],))
                        conn_a.commit()
                    elif last_update_a > last_update_b:
                        # La fila en A es más reciente, actualizar B
                        cursor_b.execute(f"""
                            UPDATE {table_name} SET {update_columns}
                            WHERE {columns[0]} = %s
                        """, row_a[1:] + (row_a[0],))
                        conn_b.commit()
                elif last_update_a is None:
                    # La fila en B tiene fecha, pero A no, actualizar A
                    cursor_a.execute(f"""
                        UPDATE {table_name} SET {update_columns}
                        WHERE {columns[0]} = %s
                    """, row_b[1:] + (row_b[0],))
                    conn_a.commit()
                elif last_update_b is None:
                    # La fila en A tiene fecha, pero B no, actualizar B
                    cursor_b.execute(f"""
                        UPDATE {table_name} SET {update_columns}
                        WHERE {columns[0]} = %s
                    """, row_a[1:] + (row_a[0],))
                    conn_b.commit()
                    
            elif row_a and not row_b:
                # La fila está en A pero no en B, insertar en B
                placeholders = ", ".join(["%s"] * len(row_a))
                cursor_b.execute(f"""
                    INSERT INTO {table_name} ({', '.join(columns)})
                    VALUES ({placeholders})
                """, row_a)
                conn_b.commit()
            elif row_b and not row_a:
                # La fila está en B pero no en A, insertar en A
                placeholders = ", ".join(["%s"] * len(row_b))
                cursor_a.execute(f"""
                    INSERT INTO {table_name} ({', '.join(columns)})
                    VALUES ({placeholders})
                """, row_b)
                conn_a.commit()
        print("Se sincronizo ",table_name)

    except psycopg2.Error as e:
        print(f"Error: {e}")
    finally:
        # Cerrar las conexiones
        if cursor_a:
            cursor_a.close()
        if conn_a:
            conn_a.close()
        if cursor_b:
            cursor_b.close()
        if conn_b:
            conn_b.close()


def main():
    # Llamada a la función
    tables= ['coin','citys','provinces','sellers','clients','department','products','products_units'] 
    for table in tables:
        sync_table(table)

if __name__ == '__main__':
    main()


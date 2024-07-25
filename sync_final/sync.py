import psycopg2
from concurrent.futures import ThreadPoolExecutor, as_completed
import asyncio
from db1 import db1 as db1
from db2 import db2 as db2


async def sync_table(table_name):
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
        getColumns=f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}' ORDER BY ordinal_position;"
        cursor_a.execute(getColumns)
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
                        query=f"""UPDATE {table_name} SET {update_columns} WHERE {columns[0]} = %s"""
                        params= row_b[1:] + (row_b[0],)
                        print(query,params)
                        #cursor_a.execute(query,params)
                        cursor_a.execute(query, params)
                        conn_a.commit()
                        
                    elif last_update_a > last_update_b:
                        # La fila en A es más reciente, actualizar B
                        query=f""" UPDATE {table_name} SET {update_columns} WHERE {columns[0]} = %s"""
                        params= row_a[1:] + (row_a[0],)
                        print(query,params)
                        cursor_b.execute(query,params)
                        conn_b.commit()
                elif last_update_a is None:
                    # La fila en B tiene fecha, pero A no, actualizar A
                    query=f""" UPDATE {table_name} SET {update_columns} WHERE {columns[0]} = %s"""
                    params=row_b[1:] + (row_b[0],)
                    print(query,params)
                    cursor_a.execute(query,params)
                    conn_a.commit()
                elif last_update_b is None:
                    # La fila en A tiene fecha, pero B no, actualizar B
                    query=f""" UPDATE {table_name} SET {update_columns} WHERE {columns[0]} = %s """
                    params=row_a[1:] + (row_a[0],)
                    print(query,params)
                    cursor_b.execute(query,params)
                    conn_b.commit()
                    
            elif row_a and not row_b:
                # La fila está en A pero no en B, insertar en B
                placeholders = ", ".join(["%s"] * len(row_a))
                query=f""" INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders}) """
                print(query,row_a)
                cursor_b.execute(query,row_a)
                conn_b.commit()
            elif row_b and not row_a:
                # La fila está en B pero no en A, insertar en A
                placeholders = ", ".join(["%s"] * len(row_b))
                query=f""" INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders}) """
                print(query,row_b)
                cursor_a.execute(query,row_b)
                conn_a.commit()
            #pbar.update(1)
        print("Se actualizo la tabla ",table_name)

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


async def run_sync_table_in_executor(executor, table_name):
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(executor, asyncio.run, sync_table(table_name))

async def sync_tables_in_parallel(tables):
    max_length = max(len(sublist) for sublist in tables)

    with ThreadPoolExecutor(max_workers=10) as executor:
        for i in range(max_length):
            tasks = []
            for sublist in tables:
                if i < len(sublist):
                    tasks.append(run_sync_table_in_executor(executor, sublist[i]))
            await asyncio.gather(*tasks)

async def main():
    # Llamada a la función

        # 'coin',
        # 'units',
        # 'store',
        # 'users',
        # 'stations',
        # 'provider',
        # 'locations',
        # 'sellers',
        # 'citys',
        # 'provinces',
        # 'clients',
        # 'taxes',
        # 'tax_types',
        # 'department',
        # 'technician',
        # 'status',
        # 'origin',
        # 'products',
        # 'products_lots',
        # 'products_units',
        # 'products_stock',
        # 'products_provider',
        # 'receivable',
        # 'receivable_details',
        # 'receivable_coins',
        # 'receivable_taxes',
        # 'sales_operation',
        # 'sales_operation_coins',
        # 'sales_operation_details',
        # 'sales_operation_taxes',
        # 'debtstopay',
        # 'debtstopay_coins',
        # 'debtstopay_details',
        # 'debtstopay_taxes'
            
    tables=[
        ['coin',
        'units',
        'store',
        'users'],

        ['stations',
        'provider',
        'sellers'],

        ['citys',
        'provinces',
        'clients',
        'taxes'],

        ['department',
        'technician'],

        ['products',
        'products_lots',
        'products_units',
        'products_stock',
        'products_provider'],

        ['receivable',
        'receivable_details',
        'receivable_coins',
        'receivable_taxes'],

        ['sales_operation',
        'sales_operation_coins',
        'sales_operation_details',
        'sales_operation_taxes'],

        ['debtstopay',
        'debtstopay_coins',
        'debtstopay_details',
        'debtstopay_taxes']
        ]
    
    while True:
        await sync_tables_in_parallel(tables)
        print('Sincronizacion completa, iniciando otra vez...')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program terminated by user")


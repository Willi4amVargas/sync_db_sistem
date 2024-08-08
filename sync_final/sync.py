import psycopg2
from concurrent.futures import ThreadPoolExecutor, as_completed
import asyncio
import time
from sync_final.db1 import database1 as db1
from sync_final.db2 import database2 as db2
from license import program_is_usable
import tkinter as tk
from tkinter import messagebox
import sys


def check_license():
    # Verifica el estado de la licencia
    status = program_is_usable()
    if status == 1:
        return False
    elif status == 2:
        return True
    elif status == 3:
        return False


def show_error(message):
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal de Tkinter
    messagebox.showerror("Error", message)
    root.destroy()


async def sync_table(table_name):
    # Conectar a la primera base de datos
    conn_a = db1()
    cursor_a = conn_a.cursor()
    
    # Conectar a la segunda base de datos
    conn_b = db2()
    cursor_b = conn_b.cursor()

    # Obtener todas las filas de ambas bases de datos
    query = f"SELECT * FROM {table_name} where status_column=1;"
    cursor_a.execute(query)
    rows_a = cursor_a.fetchall()
    cursor_b.execute(query)
    rows_b = cursor_b.fetchall()
    if rows_a or rows_b:
        try:

            
            # Obtener columnas de la tabla
            getColumns=f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}' ORDER BY ordinal_position;"
            cursor_a.execute(getColumns)
            columns = [col[0] for col in cursor_a.fetchall()]
            
            tables_skip_three_columns = ['products_stock','receivable_details', 'debtstopay_details']
            tables_skip_two_columns = [
                'receivable_coins', 'receivable_taxes', 'sales_operation_coins',
                'sales_operation_details', 'sales_operation_taxes', 
                'debtstopay_coins', 'debtstopay_taxes'
            ]

            # Convertir listas de filas a diccionarios para un acceso más fácil

            
            if table_name in tables_skip_three_columns:
                update_columns = ", ".join([f"{col} = %s" for col in columns[3:-1]]) # saltar las tres primeras columnas clave primarias
                dict_a = {str(row[0])+str(row[1])+str(row[2]): row for row in rows_a}
                dict_b = {str(row[0])+str(row[1])+str(row[2]): row for row in rows_b}
                case_pk=0
                
            elif table_name in tables_skip_two_columns:
                update_columns = ", ".join([f"{col} = %s" for col in columns[2:-1]]) # Saltar las dos primeras columnas clave primaria
                dict_a = {str(row[0])+str(row[1]): row for row in rows_a}
                dict_b = {str(row[0])+str(row[1]): row for row in rows_b}
                case_pk=1
                
            else:
                update_columns = ", ".join([f"{col} = %s" for col in columns[1:-1]]) # Saltar la columna de clave primaria
                dict_a = {str(row[0]): row for row in rows_a}
                dict_b = {str(row[0]): row for row in rows_b}
                case_pk=2
            
            # Iterar sobre todas las claves primarias en ambas bases de datos
            all_keys = set(dict_a.keys()).union(dict_b.keys())
            
            for key in all_keys:
                row_a = dict_a.get(key)
                row_b = dict_b.get(key)

                if row_a and row_b:
                    # Ambas bases de datos tienen esta fila, comparar status de actualizacion
                    last_update_a=row_a[-2]
                    last_update_b=row_b[-2]
                    if last_update_a <= last_update_b:
                    # La fila en B es más reciente, actualizar A
                        if case_pk==2:
                            query=f"""UPDATE {table_name} SET {update_columns}, status_column = 0 WHERE {columns[0]} = %s"""
                            params= row_b[1:-1] + (row_b[0],)
                            query_update_status=f"""UPDATE {table_name} SET status_column = 0 WHERE {columns[0]} = %s"""
                            param_status_update=(row_a[0],)
                            
                            # print(params)
                            # print(query,params,table_name)
                            
                            try:
                                cursor_b.execute(query_update_status,param_status_update)
                                cursor_a.execute(query, params)
                                conn_a.commit()
                                conn_b.commit()
                                print('¡Actualizado en A!')
                            except psycopg2.Error as e:
                                
                                print(f'Error: {e}')
                                conn_a.rollback()
                                conn_b.rollback()
                        elif case_pk==1:
                            query=f"""UPDATE {table_name} SET {update_columns}, status_column = 0 WHERE {columns[0]} = %s AND {columns[1]} = %s"""
                            params= row_b[2:-1] + (row_b[0],) + (row_b[1],)
                            query_update_status=f"""UPDATE {table_name} SET status_column = 0 WHERE {columns[0]} = %s AND {columns[1]} = %s"""
                            param_status_update=(row_a[0],)+ (row_a[1],)
                            
                            # print(params)
                            # print(query,params,table_name)
                            
                            try:
                                cursor_b.execute(query_update_status,param_status_update)
                                cursor_a.execute(query, params)
                                conn_a.commit()
                                conn_b.commit()
                                print('¡Actualizado en A!')
                            except psycopg2.Error as e:
                                
                                print(f'Error: {e}')
                                conn_a.rollback()
                                conn_b.rollback()
                        elif case_pk==0:
                            query=f"""UPDATE {table_name} SET {update_columns}, status_column = 0  WHERE {columns[0]} = %s AND {columns[1]} = %s AND {columns[2]} = %s"""
                            params= row_b[3:-1] + (row_b[0],) + (row_b[1],) + (row_b[2],)
                            query_update_status=f"""UPDATE {table_name} SET status_column = 0 WHERE {columns[0]} = %s AND {columns[1]} = %s AND {columns[2]} = %s"""
                            param_status_update=(row_a[0],)+ (row_a[1],)+ (row_a[2],)
                            
                            # print(params)
                            # print(query,params,table_name)
                            
                            try:
                                cursor_b.execute(query_update_status,param_status_update)
                                cursor_a.execute(query, params)
                                conn_a.commit()
                                conn_b.commit()
                                print('¡Actualizado en A!')
                            except psycopg2.Error as e:
                                
                                print(f'Error: {e}')
                                conn_a.rollback()
                                conn_b.rollback()
                        
                    elif last_update_a > last_update_b:
                        # La fila en A es más reciente, actualizar B
                        if case_pk==2:
                            query=f"""UPDATE {table_name} SET {update_columns}, status_column = 0  WHERE {columns[0]} = %s"""
                            params= row_a[1:-1] + (row_a[0],)
                            query_update_status=f"""UPDATE {table_name} SET status_column = 0 WHERE {columns[0]} = %s"""
                            param_status_update=(row_b[0],)
                            
                            # print(params)
                            # print(query,params,table_name)
                            #cursor_b.execute(query,params)
                            try:
                                print('¡Actualizado en B!')
                                cursor_a.execute(query_update_status,param_status_update)
                                cursor_b.execute(query, params)
                                conn_b.commit()
                                conn_a.commit()
                            except psycopg2.Error as e:
                                
                                print(f'Error: {e}')
                                conn_b.rollback()
                                conn_a.rollback()
                        elif case_pk==1:
                            query=f"""UPDATE {table_name} SET {update_columns}, status_column = 0  WHERE {columns[0]} = %s AND {columns[1]} = %s"""
                            params= row_a[2:-1] + (row_a[0],) + (row_a[1],)
                            query_update_status=f"""UPDATE {table_name} SET status_column = 0 WHERE {columns[0]} = %s AND {columns[1]} = %s"""
                            param_status_update=(row_b[0],) + (row_b[1],)
                            
                            # print(params)
                            # print(query,params,table_name)
                            #cursor_b.execute(query,params)
                            try:
                                print('¡Actualizado en B!')
                                cursor_a.execute(query_update_status,param_status_update)
                                cursor_b.execute(query, params)
                                conn_b.commit()
                                conn_a.commit()
                            except psycopg2.Error as e:
                                
                                print(f'Error: {e}')
                                conn_b.rollback()
                                conn_a.rollback()
                        elif case_pk==0:
                            query=f"""UPDATE {table_name} SET {update_columns}, status_column = 0 WHERE {columns[0]} = %s AND {columns[1]} = %s AND {columns[2]} = %s"""
                            params= row_a[3:-1] + (row_a[0],) + (row_a[1],) + (row_a[2],)
                            query_update_status=f"""UPDATE {table_name} SET status_column = 0 WHERE {columns[0]} = %s AND {columns[1]} = %s AND {columns[2]} = %s"""
                            param_status_update=(row_b[0],) + (row_b[1],)+ (row_b[2],)
                            
                            # print(params)
                            # print(query,params,table_name)
                            #cursor_b.execute(query,params)
                            try:
                                print('¡Actualizado en B!')
                                cursor_a.execute(query_update_status,param_status_update)
                                cursor_b.execute(query, params)
                                conn_b.commit()
                                conn_a.commit()
                            except psycopg2.Error as e:
                                
                                print(f'Error: {e}')
                                conn_b.rollback()
                                conn_a.rollback()
                elif row_a != None and row_b==None:
                    # La fila en A es más reciente, actualizar B
                    if case_pk==2:
                        #UPDATE QUERY LOGIC
                        query=f"""UPDATE {table_name} SET {update_columns}, status_column = 0  WHERE {columns[0]} = %s"""
                        params= row_a[1:-1] + (row_a[0],)
                        #INSERT QUERY LOGIC
                        placeholders = ", ".join(["%s"] * len(row_a))
                        query_insert=f""" INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders}) """
                        #UPDATE STATUS LOGIC
                        query_update_status=f"""UPDATE {table_name} SET status_column = 0 WHERE {columns[0]} = %s"""
                        param_status_update=(row_a[0],)
                        
                        # print(params)
                        # print(query,params,table_name)
                        #cursor_b.execute(query,params)
                        try:
                            cursor_b.execute(query,params)
                            conn_b.commit()

                            if cursor_b.rowcount > 0:
                                print('¡Actualizado en B!')
                            else:
                                cursor_b.execute(query_insert,row_a)
                                conn_b.commit()
                                print('Insertado en B!')

                            cursor_a.execute(query_update_status,param_status_update)
                            conn_a.commit()
                        except psycopg2.Error as e:
                            print(e)
                            cursor_a.rollback()
                            cursor_b.rollback()
                    elif case_pk==1:
                        #UPDATE QUERY LOGIC
                        query=f"""UPDATE {table_name} SET {update_columns}, status_column = 0  WHERE {columns[0]} = %s AND {columns[1]} = %s"""
                        params= row_a[2:-1] + (row_a[0],) + (row_a[1],)
                        #INSERT QUERY LOGIC
                        placeholders = ", ".join(["%s"] * len(row_a))
                        query_insert=f""" INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders}) """
                        #UPDATE STATUS LOGIC
                        query_update_status=f"""UPDATE {table_name} SET status_column = 0 WHERE {columns[0]} = %s AND {columns[1]} = %s"""
                        param_status_update=(row_a[0],) + (row_a[1],)
                        # print(params)
                        # print(query,params,table_name)
                        #cursor_b.execute(query,params)
                        try:
                            cursor_b.execute(query,params)
                            conn_b.commit()

                            if cursor_b.rowcount > 0:
                                print('¡Actualizado en B!')
                            else:
                                cursor_b.execute(query_insert,row_a)
                                conn_b.commit()
                                print('Insertado en B!')

                            cursor_a.execute(query_update_status,param_status_update)
                            conn_a.commit()
                        except psycopg2.Error as e:
                            print(e)
                            cursor_a.rollback()
                            cursor_b.rollback()
                    elif case_pk==0:
                        #UPDATE QUERY LOGIC
                        query=f"""UPDATE {table_name} SET {update_columns}, status_column = 0 WHERE {columns[0]} = %s AND {columns[1]} = %s AND {columns[2]} = %s"""
                        params= row_a[3:-1] + (row_a[0],) + (row_a[1],) + (row_a[2],)
                        #INSERT QUERY LOGIC
                        placeholders = ", ".join(["%s"] * len(row_a))
                        query_insert=f""" INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders}) """
                        #UPDATE STATUS LOGIC
                        query_update_status=f"""UPDATE {table_name} SET status_column = 0 WHERE {columns[0]} = %s AND {columns[1]} = %s AND {columns[2]} = %s"""
                        param_status_update=(row_a[0],) + (row_a[1],)+ (row_a[2],)
                        # print(params)
                        # print(query,params,table_name)
                        #cursor_b.execute(query,params)
                        try:
                            cursor_b.execute(query,params)
                            conn_b.commit()

                            if cursor_b.rowcount > 0:
                                print('¡Actualizado en B!')
                            else:
                                cursor_b.execute(query_insert,row_a)
                                conn_b.commit()
                                print('Insertado en B!')

                            cursor_a.execute(query_update_status,param_status_update)
                            conn_a.commit()
                        except psycopg2.Error as e:
                            print(e)
                            cursor_a.rollback()
                            cursor_b.rollback()
                elif row_b != None and row_a==None:
                    # La fila en B es más reciente, actualizar A
                    if case_pk==2:
                        #UPDATE QUERY LOGIC
                        query=f"""UPDATE {table_name} SET {update_columns}, status_column = 0  WHERE {columns[0]} = %s"""
                        params= row_b[1:-1] + (row_b[0],)
                        #INSERT QUERY LOGIC
                        placeholders = ", ".join(["%s"] * len(row_b))
                        query_insert=f""" INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders}) """
                        #UPDATE STATUS LOGIC
                        query_update_status=f"""UPDATE {table_name} SET status_column = 0 WHERE {columns[0]} = %s"""
                        param_status_update=(row_b[0],)
                        
                        # print(params)
                        # print(query,params,table_name)
                        try:
                            cursor_a.execute(query,params)
                            conn_a.commit()

                            if cursor_a.rowcount > 0:
                                print('¡Actualizado en A!')
                                print(cursor_a.rowcount)
                            else:
                                cursor_a.execute(query_insert,row_b)
                                conn_a.commit()
                                print('Insertado en A!')

                            cursor_b.execute(query_update_status,param_status_update)
                            conn_b.commit()
                        except psycopg2.Error as e:
                            print(e)
                            conn_a.rollback()
                            conn_b.rollback()
                    elif case_pk==1:
                        #UPDATE QUERY LOGIC
                        query=f"""UPDATE {table_name} SET {update_columns}, status_column = 0 WHERE {columns[0]} = %s AND {columns[1]} = %s"""
                        params= row_b[2:-1] + (row_b[0],) + (row_b[1],)
                        #INSERT QUERY LOGIC
                        placeholders = ", ".join(["%s"] * len(row_b))
                        query_insert=f""" INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders}) """
                        #UPDATE STATUS LOGIC
                        query_update_status=f"""UPDATE {table_name} SET status_column = 0 WHERE {columns[0]} = %s AND {columns[1]} = %s"""
                        param_status_update=(row_b[0],)+ (row_b[1],)
                        # print(params)
                        # print(query,params,table_name)
                        
                        try:
                            cursor_a.execute(query,params)
                            conn_a.commit()

                            if cursor_a.rowcount > 0:
                                print('¡Actualizado en A!')
                                print(cursor_a.rowcount)
                            else:
                                cursor_a.execute(query_insert,row_b)
                                conn_a.commit()
                                print('Insertado en A!')

                            cursor_b.execute(query_update_status,param_status_update)
                            conn_b.commit()
                        except psycopg2.Error as e:
                            print(e)
                            conn_a.rollback()
                            conn_b.rollback()
                    elif case_pk==0:
                        #UPDATE QUERY LOGIC
                        query=f"""UPDATE {table_name} SET {update_columns}, status_column = 0  WHERE {columns[0]} = %s AND {columns[1]} = %s AND {columns[2]} = %s"""
                        params= row_b[3:-1] + (row_b[0],) + (row_b[1],) + (row_b[2],)
                        #INSERT QUERY LOGIC
                        placeholders = ", ".join(["%s"] * len(row_b))
                        query_insert=f""" INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders}) """
                        #UPDATE STATUS LOGIC
                        query_update_status=f"""UPDATE {table_name} SET status_column = 0 WHERE {columns[0]} = %s AND {columns[1]} = %s AND {columns[2]} = %s"""
                        param_status_update=(row_b[0],)+ (row_b[1],)+ (row_b[2],)
                        # print(params)
                        # print(query,params,table_name)
                        
                        try:
                            cursor_a.execute(query,params)
                            conn_a.commit()

                            if cursor_a.rowcount > 0:
                                print('¡Actualizado en A!')
                                print(cursor_a.rowcount)
                            else:
                                cursor_a.execute(query_insert,row_b)
                                conn_a.commit()
                                print('Insertado en A!')

                            cursor_b.execute(query_update_status,param_status_update)
                            conn_b.commit()
                        except psycopg2.Error as e:
                            print(e)
                            conn_a.rollback()
                            conn_b.rollback()
            # print(table_name)
            

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
    else:
        return

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

async def main_sync():
    # Llamada a la función

    # table1=[
    #     'products_lots']   
    tables=[
        ['coin',
        'coin_history',
        'units',
        'store',
        'users'],

        ['stations',
        'provider',
        'sellers',
        'department'],

        ['citys',
        'provinces',
        'clients',
        'taxes',
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
    # for table in table1:
    #     sync_table(table)
    counter=1

    while True:
        if check_license():
            await sync_tables_in_parallel(tables)
            sys.stdout.write(f'\r------------------Sincronizacion Funcionando... {counter}----------------------')
            sys.stdout.flush()
            counter += 1
            time.sleep(1)
        else:
            show_error("Licencia caducada o programa deshabilitado")
    
    # while True:
        
    #     #print('Sincronizacion completa, iniciando otra vez...')
    #     time.sleep(2)



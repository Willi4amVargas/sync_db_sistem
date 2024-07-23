from datetime import datetime as dt
import psycopg2
from db1 import db1 as db1
from db2 import db2 as db2

def fetch_all_rows(cursor, table_name):
    cursor.execute(f"SELECT * FROM {table_name};")
    return cursor.fetchall()

def fetch_column_names(cursor, table_name):
    cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}' ORDER BY ordinal_position;")
    return [row[0] for row in cursor.fetchall()]

def sync_tables(cursor_a, cursor_b, conn_a, conn_b, table_name, timestamp_column):
    rows_a = fetch_all_rows(cursor_a, table_name)
    rows_b = fetch_all_rows(cursor_b, table_name)
    
    dict_a = {row[0]: row for row in rows_a}
    dict_b = {row[0]: row for row in rows_b}

    all_keys = set(dict_a.keys()).union(dict_b.keys())
    
    columns = fetch_column_names(cursor_a, table_name)

    for key in all_keys:
        row_a = dict_a.get(key)
        row_b = dict_b.get(key)
        
        if row_a and row_b:
            last_update_a = row_a[columns.index(timestamp_column)]
            last_update_b = row_b[columns.index(timestamp_column)]
            
            if last_update_a and last_update_b:
                if last_update_a < last_update_b:
                    update_row(cursor_a, conn_a, table_name, columns, row_b, key)
                    print("Se Actualizo con exito la base de datos A")
                elif last_update_a > last_update_b:
                    update_row(cursor_b, conn_b, table_name, columns, row_a, key)
                    print("Se Actualizo con exito la base de datos B")
            elif last_update_a is None:
                update_row(cursor_a, conn_a, table_name, columns, row_b, key)
                print("Se Actualizo con exito la base de datos A")
            elif last_update_b is None:
                update_row(cursor_b, conn_b, table_name, columns, row_a, key)
                print("Se Actualizo con exito la base de datos B")
        elif row_a and not row_b:
            try:
                insert_row(cursor_b, conn_b, table_name, columns, row_a)
                print("Se Insertaron con exito datos en la base de datos B")
            except psycopg2.errors.UniqueViolation:
                handle_duplicate(cursor_b, conn_b, table_name, columns, row_a, key)
                print("Se actualizaron con exito datos duplicados a los mas actuales")
        elif row_b and not row_a:
            try:
                insert_row(cursor_a, conn_a, table_name, columns, row_b)
                print("Se Insertaron con exito datos en la base de datos A")
            except psycopg2.errors.UniqueViolation:
                handle_duplicate(cursor_a, conn_a, table_name, columns, row_b, key)
                print("Se actualizaron con exito datos duplicados a los mas actuales")
    print('Tabla ',table_name,' correctamente sincronizada')

def update_row(cursor, conn, table_name, columns, row, key):
    set_clause = ', '.join([f"{col}=%s" for col in columns if col != columns[0]])
    values = [row[columns.index(col)] for col in columns if col != columns[0]] + [key]
    query = f"UPDATE {table_name} SET {set_clause} WHERE {columns[0]}=%s"
    cursor.execute(query, values)
    conn.commit()

def insert_row(cursor, conn, table_name, columns, row):
    columns_clause = ', '.join(columns)
    placeholders = ', '.join(['%s'] * len(columns))
    values = list(row)
    query = f"INSERT INTO {table_name} ({columns_clause}) VALUES ({placeholders})"
    cursor.execute(query, values)
    conn.commit()

def handle_duplicate(cursor, conn, table_name, columns, row, key):
    cursor.execute(f"SELECT * FROM {table_name} WHERE {columns[0]} = %s", (key,))
    existing_row = cursor.fetchone()
    if existing_row:
        last_update_existing = existing_row[columns.index('last_update')]
        last_update_new = row[columns.index('last_update')]
        if last_update_existing < last_update_new:
            update_row(cursor, conn, table_name, columns, row, key)

def sync_tables_final(table):
    timestamp_column = 'last_update'  # Cambiar según sea necesario

    conn_a = db1()
    cursor_a = conn_a.cursor()
    
    conn_b = db2()
    cursor_b = conn_b.cursor()
    try:
        sync_tables(cursor_a, cursor_b, conn_a, conn_b, table, timestamp_column)
    except psycopg2.Error as e:
        print(f"Error: {e}")
    finally:
        cursor_a.close()
        conn_a.close()
        cursor_b.close()
        conn_b.close()

def main():
    sync_tables_final('citys')
    sync_tables_final('provinces')
    sync_tables_final('sellers')
    sync_tables_final('clients')
    sync_tables_final('department')
    sync_tables_final('products')

if __name__ == '__main__':
    main()

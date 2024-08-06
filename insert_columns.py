import psycopg2
from sync_final.db1 import database1 as db1
from sync_final.db2 import database2 as db2



query="""
DO $$
    DECLARE
        v_table_name text;
        v_column_name text := 'last_update';  -- Nombre de la nueva columna
        v_column_type text := 'timestamp with time zone';  -- Tipo de la nueva columna
        v_default_value text := 'now()';  -- Valor por defecto de la nueva columna
    BEGIN
        FOR v_table_name IN
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'  -- Ajusta esto si las tablas están en otro esquema
            AND table_type = 'BASE TABLE'
            AND table_name IN (
                                'coin',
                                'coin_history'                     
                    )  -- Lista de tablas
        LOOP
            -- Verifica si la columna ya existe
            IF NOT EXISTS (
                SELECT 1
                FROM information_schema.columns
                WHERE table_schema = 'public'
                AND table_name = v_table_name
                AND column_name = v_column_name
            ) THEN
                -- Si la columna no existe, agregarla
                EXECUTE format(
                    'ALTER TABLE %I ADD COLUMN %I %s DEFAULT %s',
                    v_table_name, v_column_name, v_column_type, v_default_value
                );
            END IF;
        END LOOP;
    END $$;
"""
def insert_columns():
    try:
        conn_a = db1()
        cursor_a = conn_a.cursor()
        conn_b = db2()
        cursor_b = conn_b.cursor()
        cursor_a.execute(query)
        conn_a.commit()
        cursor_b.execute(query)
        conn_b.commit()  # Asegúrate de hacer commit de la transacción
        print('-----------------Insersion de la/las columna realizada con exito-----------------')
        
    except psycopg2.Error as e:
        print(f"Error: {e}")
    finally:
        cursor_b.close()
        conn_b.close()

        # ,
        #                         'units',
        #                         'store',
        #                         'users',
        #                         'stations',
        #                         'provider',
        #                         'sellers',
        #                         'citys',
        #                         'provinces',
        #                         'clients',
        #                         'taxes',
        #                         'department',
        #                         'technician',
        #                         'products',
        #                         'products_lots',
        #                         'products_units',
        #                         'products_stock',
        #                         'products_provider',
        #                         'receivable',
        #                         'receivable_details',
        #                         'receivable_coins',
        #                         'receivable_taxes',
        #                         'sales_operation',
        #                         'sales_operation_coins',
        #                         'sales_operation_details',
        #                         'sales_operation_taxes',
        #                         'debtstopay',
        #                         'debtstopay_coins',
        #                         'debtstopay_details',
        #                         'debtstopay_taxes'




from datetime import datetime as dt
import psycopg2
from sync_final.db2 import db2 as db2


conn_b = db2()
cursor_b = conn_b.cursor()

try:

    cursor_b.execute("""
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
                                'units',
                                'store',
                                'users',
                                'stations',
                                'provider',
                                'sellers',
                                'citys',
                                'provinces',
                                'clients',
                                'taxes',
                                'department',
                                'technician',
                                'products',
                                'products_lots',
                                'products_units',
                                'products_stock',
                                'products_provider',
                                'receivable',
                                'receivable_details',
                                'receivable_coins',
                                'receivable_taxes',
                                'sales_operation',
                                'sales_operation_coins',
                                'sales_operation_details',
                                'sales_operation_taxes',
                                'debtstopay',
                                'debtstopay_coins',
                                'debtstopay_details',
                                'debtstopay_taxes'                     
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
    """)
    conn_b.commit()  # Asegúrate de hacer commit de la transacción
    print('-----------------Insersion de la/las columna realizada con exito-----------------')
    
except psycopg2.Error as e:
    print(f"Error: {e}")
finally:
    cursor_b.close()
    conn_b.close()




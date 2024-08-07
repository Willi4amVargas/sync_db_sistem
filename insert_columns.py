import psycopg2
from sync_final.db1 import database1 as db1
from sync_final.db2 import database2 as db2



query="""
DO $$
    DECLARE
        v_table_name text;
        v_last_update_column text := 'last_update';  -- Nombre de la nueva columna de actualización
        v_status_column text := 'status_column';  -- Nombre de la nueva columna de estado
        v_last_update_type text := 'timestamp with time zone';  -- Tipo de la nueva columna de actualización
        v_status_type text := 'integer';  -- Tipo de la nueva columna de estado
        v_last_update_default text := 'now()';  -- Valor por defecto de la nueva columna de actualización
        v_status_default text := '1';  -- Valor por defecto de la nueva columna de estado
    BEGIN
        FOR v_table_name IN
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'  
            AND table_type = 'BASE TABLE'
            AND table_name IN (
                                'coin',
                                'coin_history',
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
                    )
        LOOP
            -- Verifica si la columna last_update ya existe
            IF NOT EXISTS (
                SELECT 1
                FROM information_schema.columns
                WHERE table_schema = 'public'
                AND table_name = v_table_name
                AND column_name = v_last_update_column
            ) THEN
                -- Si la columna last_update no existe, agregarla
                EXECUTE format(
                    'ALTER TABLE %I ADD COLUMN %I %s DEFAULT %s',
                    v_table_name, v_last_update_column, v_last_update_type, v_last_update_default
                );
            END IF;
            
            -- Verifica si la columna status_column ya existe
            IF NOT EXISTS (
                SELECT 1
                FROM information_schema.columns
                WHERE table_schema = 'public'
                AND table_name = v_table_name
                AND column_name = v_status_column
            ) THEN
                -- Si la columna status_column no existe, agregarla
                EXECUTE format(
                    'ALTER TABLE %I ADD COLUMN %I %s DEFAULT %s',
                    v_table_name, v_status_column, v_status_type, v_status_default
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





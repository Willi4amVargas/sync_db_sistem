from datetime import datetime as dt
import psycopg2
from sync_final.db2 import db2 as db2


conn_b = db2()
cursor_b = conn_b.cursor()

query="""
-- Function: set_department(character varying, character varying, character varying, double precision, double precision, double precision, double precision, character varying)

-- DROP FUNCTION set_department(character varying, character varying, character varying, double precision, double precision, double precision, double precision, character varying);

CREATE OR REPLACE FUNCTION set_department(p_code character varying, p_name character varying, p_father_department character varying, p_percent_maximum_price double precision, p_percent_offer_price double precision, p_percent_higher_price double precision, p_percent_minimum_price double precision, p_action character varying)
  RETURNS void AS
$BODY$begin
	if(p_action='I')then

		if(exists(select code from department where code=p_code))then
			update department
			set
			description=p_name,
			father_department=p_father_department,
			perc_maximum_price=p_percent_maximum_price,
			perc_offer_price=p_percent_offer_price,
			perc_higher_price=p_percent_higher_price,
			perc_minimum_price=p_percent_minimum_price,
			last_update=NOW()
			where code = p_code;
		else
			insert into department
			(code,
			description,
			father_department,
			perc_maximum_price,
			perc_offer_price,
			perc_higher_price,
			perc_minimum_price,
			last_update
			)values
			(p_code,
			p_name,
			p_father_department,
			p_percent_maximum_price,
			p_percent_offer_price,
			p_percent_higher_price,
			p_percent_minimum_price,
			NOW());
		end if;		
	

	else
		delete from department where code=p_code;
	end if;
end
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION set_department(character varying, character varying, character varying, double precision, double precision, double precision, double precision, character varying)
  OWNER TO postgres;


"""


try:
	cursor_b.execute(query)
	conn_b.commit()  # Asegúrate de hacer commit de la transacción
	print('-----------------Insersion de la funcion realizada con exito-----------------')  
except psycopg2.Error as e:
    print(f"Error: {e}")
finally:
    cursor_b.close()
    conn_b.close()



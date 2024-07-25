from datetime import datetime as dt
import psycopg2
from sync_final.db2 import db2 as db2


conn_b = db2()
cursor_b = conn_b.cursor()

query="""
-- Function: set_provider(character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, integer, double precision, character varying, character varying, integer, double precision, double precision, boolean, boolean, boolean, boolean, character varying)

-- DROP FUNCTION set_provider(character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, integer, double precision, character varying, character varying, integer, double precision, double precision, boolean, boolean, boolean, boolean, character varying);

CREATE OR REPLACE FUNCTION set_provider(p_code character varying, p_description character varying, p_address character varying, p_provider_id character varying, p_email character varying, p_phone character varying, p_contact character varying, p_country character varying, p_province character varying, p_city character varying, p_town character varying, p_credit_days integer, p_credit_limit double precision, p_provider_type character varying, p_status character varying, p_domiciled integer, p_percent_tax_retention double precision, p_percent_municipal_retention double precision, p_retention_tax_agent boolean, p_retention_municipal_agent boolean, p_retention_islr_agent boolean, p_perception_igtf_agent boolean, p_action character varying)
  RETURNS void AS
$BODY$begin
	if(p_action='I')then
		if(exists (select code from provider where code = p_code))then
			update provider
			set			
			description=p_description,
			address=p_address,
			provider_id=p_provider_id,
			email=p_email,
			phone=p_phone,
			contact=p_contact,
			country=p_country,
			province=p_province,
			city=p_city,
			town=p_town,			
			credit_days=p_credit_days,
			credit_limit=p_credit_limit,			
			provider_type=p_provider_type,
			status=p_status,
			domiciled=p_domiciled,
			percent_tax_retention=p_percent_tax_retention,
			percent_municipal_retention  = p_percent_municipal_retention,
			retention_tax_agent =  p_retention_tax_agent,
			retention_municipal_agent =  p_retention_municipal_agent,
			retention_islr_agent =  p_retention_islr_agent,
			perception_igtf_agent = p_perception_igtf_agent,
			last_update=NOW()
			where code=p_code;

		else
			insert into provider
			(code,
			description,
			address,
			provider_id,
			email,
			phone,
			contact,
			country,
			province,
			city,
			town, 
			credit_days,
			credit_limit, 
			provider_type, 
			status,
			domiciled,
			percent_tax_retention,
			percent_municipal_retention,
			retention_tax_agent,
			retention_municipal_agent,
			retention_islr_agent,
			perception_igtf_agent,
			last_update)
			values
			(p_code,
			p_description,
			p_address,
			p_provider_id,
			p_email,
			p_phone,
			p_contact,
			p_country,
			p_province,
			p_city,
			p_town,			 
			p_credit_days,
			p_credit_limit, 
			p_provider_type, 
			p_status,
			p_domiciled,
			p_percent_tax_retention,
			p_percent_municipal_retention,
			p_retention_tax_agent,
			p_retention_municipal_agent,
			p_retention_islr_agent,
			p_perception_igtf_agent,
			NOW());	

		end if;
	else
		delete from provider where code = p_code;
	end if;		
		
	
end$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION set_provider(character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, integer, double precision, character varying, character varying, integer, double precision, double precision, boolean, boolean, boolean, boolean, character varying)
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



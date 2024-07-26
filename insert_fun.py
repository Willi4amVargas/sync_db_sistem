import psycopg2
from sync_final.db1 import database1 as db1
from sync_final.db2 import database2 as db2



query="""

CREATE OR REPLACE FUNCTION set_coin(p_code character varying, p_name character varying, p_symbol character varying, p_sales_aliquot double precision, p_buy_aliquot double precision, p_factor_type integer, p_rounding_type integer, p_user character varying, p_status character varying, p_show_in_browsers boolean, p_value_inventory boolean, p_apply_igtf boolean, p_action character varying)
  RETURNS void AS
$BODY$
declare 
v_sales_aliquot double precision;
v_buy_aliquot double precision;
begin
	if(p_action='I')then

		if(exists(select code from coin where code=p_code))then

			select
			c.sales_aliquot,
			c.buy_aliquot
			from coin c
			where c.code = p_code 
			into v_sales_aliquot,
			v_buy_aliquot;

			if(p_sales_aliquot <> v_sales_aliquot or p_buy_aliquot <> v_buy_aliquot)then

			 insert into coin_history
			 (main_code, 
			  sales_aliquot, 
			  buy_aliquot, 
			  register_date, 
			  register_hour,
			  user_code,
			  last_update)
			  values
			  (p_code, 
			  p_sales_aliquot, 
			  p_buy_aliquot, 
			  current_date,	
			  current_time, 
			  p_user,
			  NOW()); 

			end if;
			
			
			update coin
			set
			description=p_name,
			symbol = p_symbol,
			sales_aliquot = p_sales_aliquot,
			buy_aliquot = p_buy_aliquot,
			factor_type = p_factor_type,
			rounding_type = p_rounding_type,
			status = p_status,
			show_in_browsers = p_show_in_browsers,
			value_inventory = p_value_inventory,
			apply_igtf = p_apply_igtf,
			last_update=NOW()
			where code = p_code;



		else
			insert into coin
			(code,description,symbol,sales_aliquot,buy_aliquot,factor_type,rounding_type,status,show_in_browsers,value_inventory,apply_igtf,last_update)values(p_code,p_name,p_symbol,p_sales_aliquot,p_buy_aliquot,p_factor_type,p_rounding_type,p_status,p_show_in_browsers,p_value_inventory,p_apply_igtf,NOW());
		end if;		
	

	else
		delete from coin where code=p_code;
	end if;
end
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION set_coin(character varying, character varying, character varying, double precision, double precision, integer, integer, character varying, character varying, boolean, boolean, boolean, character varying)
  OWNER TO postgres;



CREATE OR REPLACE FUNCTION set_units(p_code character varying, p_name character varying, p_action character varying)
  RETURNS void AS
$BODY$begin
	if(p_action='I')then

		if(exists(select code from units where code=p_code))then
			update units
			set
			description=p_name,
			last_update=NOW()
			where code = p_code;
		else
			insert into units
			(code,description,last_update)values(p_code,p_name,NOW());
		end if;		
	

	else
		delete from units where code=p_code;
	end if;
end
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION set_units(character varying, character varying, character varying)
  OWNER TO postgres;




CREATE OR REPLACE FUNCTION set_store(p_code character varying, p_name character varying, p_action character varying)
  RETURNS void AS
$BODY$begin
	if(p_action='I')then

		if(exists(select code from store where code=p_code))then
			update store
			set
			description=p_name,
			last_update=NOW()
			where 
			code = p_code;
		else
			insert into store
			(code,description,last_update)values(p_code,p_name,NOW());
		end if;		
	

	else
		delete from store where code=p_code;
	end if;
end
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION set_store(character varying, character varying, character varying)
  OWNER TO postgres;




CREATE OR REPLACE FUNCTION set_users(p_code character varying, p_description character varying, p_status character varying, p_email character varying, p_profile character varying, p_user_password character varying, p_security_question character varying, p_answer character varying, p_display_screen boolean, p_change_password boolean, p_allow_change_password boolean, p_allow_store_password boolean, p_company_email character varying, p_technician character varying, p_security_code character varying, p_action character varying)
  RETURNS void AS
$BODY$begin

	if(p_action = 'I')then
		if(exists(select code from users where code = p_code))then
			update users
			set
			description = p_description,
			status = p_status,
			email = p_email,
			profile = p_profile,
			user_password  = p_user_password,
			security_question = p_security_question,
			answer = p_answer,
			display_screen = p_display_screen,
			change_password = p_change_password,
			allow_change_password = p_allow_change_password,
			allow_store_password = p_allow_store_password,
			company_email = p_company_email,			
			technician = p_technician,
			security_code = p_security_code,
			last_update=NOW()
			where code = p_code;

		else
			
			insert into users
			(code,
			description,
			status,
			email,
			profile,
			user_password,
			security_question,
			answer,
			display_screen,
			change_password,
			allow_change_password,
			allow_store_password,
			company_email,			
			technician,
			security_code,
			last_update)
			values
			(p_code,
			p_description,
			p_status,
			p_email,
			p_profile,
			p_user_password,
			p_security_question,
			p_answer,
			p_display_screen,
			p_change_password,
			p_allow_change_password,
			p_allow_store_password,
			p_company_email,			
			p_technician,
			p_security_code,
			NOW());
		end if;
	elsif(p_action = 'D')then
		delete from users where code = p_code;
	end if;			
		
end$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION set_users(character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, boolean, boolean, boolean, boolean, character varying, character varying, character varying, character varying)
  OWNER TO postgres;



CREATE OR REPLACE FUNCTION set_stations(p_code character varying, p_name character varying, p_numeration_sales_bill character varying, p_sale_point character varying, p_tactile boolean, p_show_browser_external_mode boolean, p_use_sale_point_numeration boolean, p_numeration_sales_point_bill character varying, p_fiscal_contingency boolean, p_use_arching_box boolean, p_numeration_income character varying, p_bio_sale_point character varying, p_sale_document_type integer, p_action character varying)
  RETURNS void AS
$BODY$begin
	if(p_action='I')then

		if(exists(select code from stations where code=p_code))then
			update stations
			set
			description=p_name,
			sale_point = p_sale_point,
			numeration_sales_bill = p_numeration_sales_bill,
			tactile = p_tactile,
			show_browser_external_mode = p_show_browser_external_mode,
			use_sale_point_numeration = p_use_sale_point_numeration,
			numeration_sales_point_bill = p_numeration_sales_point_bill,
			fiscal_contingency = p_fiscal_contingency,
			use_arching_box = p_use_arching_box,
			numeration_income = p_numeration_income,
			bio_sale_point = p_bio_sale_point,
			sale_document_type = p_sale_document_type,
			last_update=NOW()
			where code = p_code;
		else
			insert into stations
			(code,
			description,
			numeration_sales_bill,
			sale_point,
			tactile,
			show_browser_external_mode,
			use_sale_point_numeration,
			numeration_sales_point_bill,
			fiscal_contingency,
			use_arching_box,
			numeration_income,
			bio_sale_point,
			sale_document_type,
			last_update
			)values
			(p_code,
			p_name,
			p_numeration_sales_bill,
			p_sale_point,
			p_tactile,
			p_show_browser_external_mode,
			p_use_sale_point_numeration,
			p_numeration_sales_point_bill,
			p_fiscal_contingency,
			p_use_arching_box,
			p_numeration_income,
			p_bio_sale_point,
			p_sale_document_type,
			NOW());
		end if;		
	

	else
		delete from stations where code=p_code;
	end if;
end
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION set_stations(character varying, character varying, character varying, character varying, boolean, boolean, boolean, character varying, boolean, boolean, character varying, character varying, integer, character varying)
  OWNER TO postgres;



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

CREATE OR REPLACE FUNCTION set_seller(p_code character varying, p_name character varying, p_status character varying, p_percent_sales double precision, p_percent_receivable double precision, p_inkeeper boolean, p_user_code character varying, p_percent_gerencial_debit_note double precision, p_percent_gerencial_credit_note double precision, p_percent_returned_check double precision, p_action character varying)
  RETURNS void AS
$BODY$begin
	if(p_action='I')then

		if(exists(select code from sellers where code=p_code))then
			update sellers
			set
			description=p_name,
			status = p_status,
			percent_sales = p_percent_sales,
			percent_receivable = p_percent_receivable,
			inkeeper = p_inkeeper,
			user_code = p_user_code,
			percent_gerencial_debit_note = p_percent_gerencial_debit_note,
			percent_gerencial_credit_note = p_percent_gerencial_credit_note,
			percent_returned_check = p_percent_returned_check,
			last_update=NOW()
			where code = p_code;

			if(p_status='02')then
				update clients
				set 
				seller='00',
				last_update=NOW()
				where seller = p_code;
			end if;	
			
		else
			insert into sellers
			(code,description,status,percent_sales,percent_receivable,inkeeper,user_code,percent_gerencial_debit_note,percent_gerencial_credit_note,percent_returned_check,last_update)values(p_code,p_name,p_status,p_percent_sales,p_percent_receivable,p_inkeeper,p_user_code,p_percent_gerencial_debit_note,p_percent_gerencial_credit_note,p_percent_returned_check,NOW());
		end if;		
	

	else
		delete from sellers where code=p_code;
	end if;
end
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION set_seller(character varying, character varying, character varying, double precision, double precision, boolean, character varying, double precision, double precision, double precision, character varying)
  OWNER TO postgres;

CREATE OR REPLACE FUNCTION set_citys(p_code character varying, p_name character varying, p_action character varying)
  RETURNS void AS
$BODY$begin
	if(p_action='I')then

		if(exists(select code from citys where code=p_code))then
			update citys
			set
			description=p_name,
			last_update=NOW()
			where code = p_code;
		else
			insert into citys
			(code,description,last_update)values(p_code,p_name,NOW());
		end if;		
	

	else
		delete from citys where code=p_code;
	end if;
end
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION set_citys(character varying, character varying, character varying)
  OWNER TO postgres;


CREATE OR REPLACE FUNCTION set_provinces(p_code character varying, p_name character varying, p_action character varying)
  RETURNS void AS
$BODY$begin
	if(p_action='I')then

		if(exists(select code from provinces where code=p_code))then
			update provinces
			set
			description=p_name,
			last_update=NOW()
			where code = p_code;
		else
			insert into provinces
			(code,description,last_update)values(p_code,p_name,NOW());
		end if;		
	

	else
		delete from provinces where code=p_code;
	end if;
end
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION set_provinces(character varying, character varying, character varying)
  OWNER TO postgres;


CREATE OR REPLACE FUNCTION set_clients(p_code character varying, p_description character varying, p_address character varying, p_client_id character varying, p_email character varying, p_phone character varying, p_contact character varying, p_country character varying, p_province character varying, p_city character varying, p_town character varying, p_area_sales character varying, p_seller character varying, p_client_group character varying, p_credit_days integer, p_credit_limit double precision, p_discount double precision, p_client_type character varying, p_sale_price integer, p_status character varying, p_name_fiscal integer, p_generic_client boolean, p_client_classification character varying, p_cond_property_type character varying, p_cond_floor character varying, p_cond_aliquot double precision, p_cond_surface double precision, p_allow_expired_balance boolean, p_retention_tax_agent boolean, p_retention_municipal_agent boolean, p_retention_islr_agent boolean, p_action character varying)
  RETURNS void AS
$BODY$begin
	if(p_action='I')then
		if(exists (select code from clients where code = p_code))then
			update clients
			set			
			description=p_description,
			address=p_address,
			client_id=p_client_id,
			email=p_email,
			phone=p_phone,
			contact=p_contact,
			country=p_country,
			province=p_province,
			city=p_city,
			town=p_town,
			area_sales=p_area_sales,
			seller=p_seller,
			client_group=p_client_group,
			credit_days=p_credit_days,
			credit_limit=p_credit_limit,
			discount=p_discount,
			client_type=p_client_type,
			sale_price=p_sale_price,
			status=p_status,
			name_fiscal=p_name_fiscal,
			generic_client=p_generic_client,
			client_classification = p_client_classification,
			cond_property_type = p_cond_property_type,
			cond_floor = p_cond_floor,
			cond_aliquot = p_cond_aliquot,
			cond_surface = p_cond_surface,
			allow_expired_balance = p_allow_expired_balance,
			retention_tax_agent = p_retention_tax_agent,
			retention_municipal_agent = p_retention_municipal_agent,
			retention_islr_agent = p_retention_islr_agent,
			last_update=now()
			where code=p_code;

		else
			insert into clients
			(code,
			description,
			address,
			client_id,
			email,
			phone,
			contact,
			country,
			province,
			city,
			town,
			area_sales,
			seller,
			client_group,
			credit_days,
			credit_limit,
			discount,
			client_type,
			sale_price,
			status,
			name_fiscal,
			generic_client,
			client_classification,
			cond_property_type,
			cond_floor,
			cond_aliquot,
			cond_surface,
			allow_expired_balance,
			retention_tax_agent,
			retention_municipal_agent,
			retention_islr_agent,
			last_update)
			values
			(p_code,
			p_description,
			p_address,
			p_client_id,
			p_email,
			p_phone,
			p_contact,
			p_country,
			p_province,
			p_city,
			p_town,
			p_area_sales,
			p_seller,
			p_client_group,
			p_credit_days,
			p_credit_limit,
			p_discount,
			p_client_type,
			p_sale_price,
			p_status,
			p_name_fiscal,
			p_generic_client,
			p_client_classification,
			p_cond_property_type,
			p_cond_floor,
			p_cond_aliquot,
			p_cond_surface,
			p_allow_expired_balance,
			p_retention_tax_agent,
			p_retention_municipal_agent,
			p_retention_islr_agent,
			now());	

		end if;
	else
		delete from clients where code = p_code;
	end if;		
		
	
end$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION set_clients(character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, integer, double precision, double precision, character varying, integer, character varying, integer, boolean, character varying, character varying, character varying, double precision, double precision, boolean, boolean, boolean, boolean, character varying)
  OWNER TO postgres;

CREATE OR REPLACE FUNCTION set_taxes(p_code character varying, p_description character varying, p_aliquot double precision, p_short_description character varying, p_type integer, p_action character varying)
  RETURNS void AS
$BODY$begin

	if(p_action = 'I')then

		if( exists (select code from taxes where code = p_code))then
			update taxes 
			set
			description = p_description,
			aliquot = p_aliquot,
			short_description = p_short_description,
			line = p_type,
			last_update=NOW()
			where code = p_code;
		else
			insert into taxes (code,description,aliquot,short_description,line,last_update) values(p_code,p_description,p_aliquot,p_short_description,p_type,NOW());
		end if;	

		
	else
		delete from taxes where code = p_code;

	end if;

end
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION set_taxes(character varying, character varying, double precision, character varying, integer, character varying)
  OWNER TO postgres;

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


CREATE OR REPLACE FUNCTION set_technician(p_code character varying, p_name character varying, p_status character varying, p_percent_commission_maximum_price double precision, p_percent_commission_offer_price double precision, p_percent_commission_higher_price double precision, p_percent_commission_minimum_price double precision, p_percent_commission_variable_price double precision, p_action character varying)
  RETURNS void AS
$BODY$begin
	if(p_action='I')then

		if(exists(select code from technician where code=p_code))then
			update technician
			set
			description=p_name,
			status = p_status,
			percent_commission_maximum_price = p_percent_commission_maximum_price,
			percent_commission_offer_price = p_percent_commission_offer_price,
			percent_commission_higher_price = p_percent_commission_higher_price,
			percent_commission_minimum_price = p_percent_commission_minimum_price,
			percent_commission_variable_price = p_percent_commission_variable_price,
			last_update=NOW()
			where code = p_code;
		else
			insert into technician
			(code,description,status,percent_commission_maximum_price,percent_commission_offer_price,percent_commission_higher_price,percent_commission_minimum_price,percent_commission_variable_price,last_update)
			values(p_code,p_name,p_status,p_percent_commission_maximum_price,p_percent_commission_offer_price,p_percent_commission_higher_price,p_percent_commission_minimum_price,p_percent_commission_variable_price,NOW());
		end if;		
	

	else
		delete from technician where code=p_code;
	end if;
end
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION set_technician(character varying, character varying, character varying, double precision, double precision, double precision, double precision, double precision, character varying)
  OWNER TO postgres;

CREATE OR REPLACE FUNCTION set_product(p_code character varying, p_description character varying, p_short_name character varying, p_mark character varying, p_model character varying, p_referenc character varying, p_department character varying, p_days_warranty integer, p_sale_tax character varying, p_buy_tax character varying, p_rounding_type integer, p_costing_type integer, p_discount double precision, p_max_discount double precision, p_minimal_sale double precision, p_maximal_sale double precision, p_status character varying, p_origin character varying, p_take_department_utility boolean, p_allow_decimal boolean, p_edit_name boolean, p_sale_price integer, p_product_type character varying, p_technician character varying, p_request_technician boolean, p_serialized boolean, p_request_details boolean, p_request_amount boolean, p_coin character varying, p_allow_negative_stock boolean, p_use_scale boolean, p_add_unit_description boolean, p_use_lots boolean, p_lots_order integer, p_minimal_stock double precision, p_notify_minimal_stock boolean, p_size character varying, p_color character varying, p_extract_net_from_unit_cost_plus_tax boolean, p_extract_net_from_unit_price_plus_tax boolean, p_maximum_stock double precision, p_action character varying)
  RETURNS void AS
$BODY$begin

	if(p_action='I')then
		
		if(exists(select code from products where code = p_code ))then
		
			UPDATE products
			SET  
			description=p_description, 
			short_name=p_short_name, 
			mark=p_mark, 
			model=p_model, 
			referenc=p_referenc, 
			department=p_department, 
			days_warranty=p_days_warranty, 
			sale_tax=p_sale_tax, 
			buy_tax=p_buy_tax, 
			rounding_type=p_rounding_type, 
			costing_type=p_costing_type, 
			discount=p_discount, 
			max_discount=p_max_discount, 
			minimal_sale=p_minimal_sale, 
			maximal_sale=p_maximal_sale, 
			status=p_status, 
			origin=p_origin, 
			take_department_utility=p_take_department_utility, 
			allow_decimal=p_allow_decimal, 
			edit_name=p_edit_name, 
			sale_price=p_sale_price,
			technician = p_technician,
			request_technician = p_request_technician,
			serialized = p_serialized,
			request_details = p_request_details,
			request_amount = p_request_amount,
			coin = p_coin,
			allow_negative_stock = p_allow_negative_stock,
			use_scale = p_use_scale,
			add_unit_description = p_add_unit_description,
			use_lots = p_use_lots,
			lots_order = p_lots_order,
			minimal_stock = p_minimal_stock,
			notify_minimal_stock = p_notify_minimal_stock,
			size = p_size,
			color = p_color,
			extract_net_from_unit_cost_plus_tax = p_extract_net_from_unit_cost_plus_tax,
			extract_net_from_unit_price_plus_tax = p_extract_net_from_unit_price_plus_tax,
			maximum_stock = p_maximum_stock,
			last_update=NOW()		
			WHERE code=p_code;
		
		else
		
			INSERT INTO products(
			code, 
			description, 
			short_name, 
			mark, 
			model, 
			referenc, 
			department, 
			days_warranty, 
			sale_tax, 
			buy_tax, 
			rounding_type, 
			costing_type, 
			discount, 
			max_discount, 
			minimal_sale, 
			maximal_sale, 
			status, 
			origin, 
			take_department_utility, 
			allow_decimal, 
			edit_name, 
			sale_price,
			product_type,
			technician,
			request_technician,
			serialized,
			request_details,
			request_amount,
			coin,
			allow_negative_stock,
			use_scale,
			add_unit_description,
			use_lots,
			lots_order,
			minimal_stock,
			notify_minimal_stock,
			size,
			color,
			extract_net_from_unit_cost_plus_tax,
			extract_net_from_unit_price_plus_tax,
			maximum_stock,
			last_update)
			values
			(
			p_code, 
			p_description, 
			p_short_name, 
			p_mark, 
			p_model, 
			p_referenc, 
			p_department, 
			p_days_warranty, 
			p_sale_tax, 
			p_buy_tax, 
			p_rounding_type, 
			p_costing_type, 
			p_discount, 
			p_max_discount, 
			p_minimal_sale, 
			p_maximal_sale, 
			p_status, 
			p_origin, 
			p_take_department_utility, 
			p_allow_decimal, 
			p_edit_name, 
			p_sale_price,
			p_product_type,			
			p_technician,
			p_request_technician,
			p_serialized,
			p_request_details,
			p_request_amount,
			p_coin,
			p_allow_negative_stock,
			p_use_scale,
			p_add_unit_description,
			p_use_lots,
			p_lots_order,
			p_minimal_stock,
			p_notify_minimal_stock,
			p_size,
			p_color,
			p_extract_net_from_unit_cost_plus_tax,
			p_extract_net_from_unit_price_plus_tax,
			p_maximum_stock,
			NOW());		

		
		end if;
	else
		delete from products where code=p_code;

	end if;	
				

end$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION set_product(character varying, character varying, character varying, character varying, character varying, character varying, character varying, integer, character varying, character varying, integer, integer, double precision, double precision, double precision, double precision, character varying, character varying, boolean, boolean, boolean, integer, character varying, character varying, boolean, boolean, boolean, boolean, character varying, boolean, boolean, boolean, boolean, integer, double precision, boolean, character varying, character varying, boolean, boolean, double precision, character varying)
  OWNER TO postgres;

CREATE OR REPLACE FUNCTION set_products_lots(INOUT p_correlative integer, IN p_product_code character varying, IN p_lot_number character varying, IN p_entry_date date, IN p_entry_module character varying, IN p_entry_correlative integer, IN p_entry_amount double precision, IN p_expire boolean, IN p_expire_date date, IN p_apply_prices boolean, IN p_elaboration_date date)
  RETURNS integer AS
$BODY$begin	 

	if(exists(select correlative from products_lots where correlative = p_correlative))then

		update products_lots
		set
		lot_number = p_lot_number, 
		expire = p_expire,
		expire_date = p_expire_date,
		apply_prices = p_apply_prices,
		elaboration_date = p_elaboration_date,
		last_update=NOW()
		where correlative = p_correlative;
		
	else

		insert into products_lots
		(product_code,
		 lot_number, 		 
		 entry_date,
		 entry_module,
		 entry_correlative,
		 entry_amount,		 
		 expire,
		 expire_date,
		 apply_prices,
		 elaboration_date,
         last_update)
		values
		(p_product_code,
		 p_lot_number, 		
		 p_entry_date,
		 p_entry_module,
		 p_entry_correlative,
		 p_entry_amount,		 
		 p_expire,
		 p_expire_date,
		 p_apply_prices,
		 p_elaboration_date,
         NOW());

		select currval('products_lots_correlative_seq') into p_correlative;			

	end if;

		

end$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION set_products_lots(integer, character varying, character varying, date, character varying, integer, double precision, boolean, date, boolean, date)
  OWNER TO postgres;


CREATE OR REPLACE FUNCTION set_products_units(p_correlative integer, p_unit character varying, p_producto_codigo character varying, p_main_unit boolean, p_conversion_factor double precision, p_unit_type integer, p_show_in_screen boolean, p_is_for_buy boolean, p_is_for_sale boolean, p_unitary_cost double precision, p_calculated_cost double precision, p_average_cost double precision, p_perc_waste_cost double precision, p_perc_handling_cost double precision, p_perc_operating_cost double precision, p_perc_additional_cost double precision, p_maximum_price double precision, p_offer_price double precision, p_higher_price double precision, p_minimum_price double precision, p_perc_maximum_price double precision, p_perc_offer_price double precision, p_perc_higher_price double precision, p_perc_minimum_price double precision, p_perc_freight_cost double precision, p_perc_discount_provider double precision, p_lenght double precision, p_height double precision, p_width double precision, p_weight double precision, p_capacitance double precision)
  RETURNS void AS
$BODY$begin
	if(exists(select correlative from products_units where correlative=p_correlative))then

		   UPDATE products_units
		   set 	
		   unit=p_unit, 
		   product_code=p_producto_codigo, 
		   main_unit=p_main_unit, 
		   conversion_factor=p_conversion_factor, 
		   unit_type=p_unit_type, 
		   show_in_screen=p_show_in_screen, 
		   is_for_buy=p_is_for_buy, 
		   is_for_sale=p_is_for_sale, 
		   unitary_cost=p_unitary_cost, 
		   --last_cost=p_last_cost, 
		   calculated_cost=p_calculated_cost, 
		   average_cost=p_average_cost, 
		   perc_waste_cost=p_perc_waste_cost, 
		   perc_handling_cost=p_perc_handling_cost, 
		   perc_operating_cost=p_perc_operating_cost, 
		   perc_additional_cost=p_perc_additional_cost, 
		   maximum_price=p_maximum_price, 
		   offer_price=p_offer_price, 
		   higher_price=p_higher_price, 
		   minimum_price=p_minimum_price, 
		   perc_maximum_price=p_perc_maximum_price, 
		   perc_offer_price=p_perc_offer_price, 
		   perc_higher_price=p_perc_higher_price, 
		   perc_minimum_price=p_perc_minimum_price,
		   perc_freight_cost = p_perc_freight_cost,
		   perc_discount_provider = p_perc_discount_provider,
		   lenght = p_lenght,
		   height = p_height,
		   width = p_width,
		   weight = p_weight,
		   capacitance = p_capacitance,
		   last_update=NOW()
		   where correlative=p_correlative;

	else
		INSERT INTO products_units( 
			unit, 
			product_code, 
			main_unit, 
			conversion_factor, 
			unit_type, 
			show_in_screen, 
			is_for_buy, 
			is_for_sale, 
			unitary_cost, 
			--last_cost, 
			calculated_cost, 
			average_cost, 
			perc_waste_cost, 
			perc_handling_cost, 
			perc_operating_cost, 
			perc_additional_cost, 
			maximum_price, 
			offer_price, 
			higher_price, 
			minimum_price, 
			perc_maximum_price, 
			perc_offer_price, 
			perc_higher_price, 
			perc_minimum_price,
			perc_freight_cost,
			perc_discount_provider,			
			lenght,
			height,
			width,
			weight,
			capacitance,
			last_update)
			values
			(p_unit, 
			p_producto_codigo, 
			p_main_unit, 
			p_conversion_factor, 
			p_unit_type, 
			p_show_in_screen, 
			p_is_for_buy, 
			p_is_for_sale, 
			p_unitary_cost, 
			--p_last_cost, 
			p_calculated_cost, 
			p_average_cost, 
			p_perc_waste_cost, 
			p_perc_handling_cost, 
			p_perc_operating_cost, 
			p_perc_additional_cost, 
			p_maximum_price, 
			p_offer_price, 
			p_higher_price, 
			p_minimum_price, 
			p_perc_maximum_price, 
			p_perc_offer_price, 
			p_perc_higher_price, 
			p_perc_minimum_price,
			p_perc_freight_cost,
			p_perc_discount_provider,
			p_lenght,
			p_height,
			p_width,
			p_weight,
			p_capacitance,
			NOW());
	end if;		

end$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION set_products_units(integer, character varying, character varying, boolean, double precision, integer, boolean, boolean, boolean, double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision)
  OWNER TO postgres;


CREATE OR REPLACE FUNCTION set_products_stock(p_product_code character varying, p_store character varying, p_locations character varying, p_amount double precision, p_unit_type integer, p_factor_conversion double precision, p_factor double precision, p_type_amount character varying)
  RETURNS void AS
$BODY$declare v_stock double precision;
begin 

		if(not exists(select product_code from products_stock where product_code = p_product_code and store=p_store and locations = p_locations))then
			insert into products_stock
			(product_code,
			store,
			locations,
			stock,
            last_update)
			values
			(p_product_code,
			p_store,
			p_locations,
			0,
            NOW());
		end if;	

		v_stock=0;

		if(p_unit_type = 0)then
		   v_stock = p_amount;
		elsif(p_unit_type = 1)then
		   v_stock = p_amount * p_factor_conversion;
		elsif(p_unit_type = 2)then   	
		   v_stock = p_amount / p_factor_conversion;
		end if;  

		v_stock=v_stock * p_factor; 	
		
		if(p_type_amount = 'STOCK')then
			update products_stock
			set
			stock = stock + v_stock,
            last_update=NOW()
			where product_code = p_product_code and store=p_store and locations = p_locations;
		elsif(p_type_amount = 'ORDERED')then
			update products_stock
			set
			ordered_stock = ordered_stock + v_stock,
            last_update=NOW()
			where product_code = p_product_code and store=p_store and locations = p_locations;
		elsif(p_type_amount = 'COMMITTED')then
			update products_stock
			set
			committed_stock = committed_stock + v_stock,
            last_update=NOW()
			where product_code = p_product_code and store=p_store and locations = p_locations;
		end if;

				

end$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION set_products_stock(character varying, character varying, character varying, double precision, integer, double precision, double precision, character varying)
  OWNER TO postgres;

CREATE OR REPLACE FUNCTION set_products_provider(p_product_code character varying, p_provider_code character varying, p_unitary_cost double precision, p_document_type character varying, p_document_no character varying, p_emission_date date, p_register_date date, p_coin_code character varying, p_unit integer, p_related_line integer, p_amount double precision)
  RETURNS void AS
$BODY$begin

	insert into products_provider(product_code,
				      provider_code,
				      unitary_cost,
				      document_type,
				      document_no,
				      emission_date,
				      register_date,
				      coin_code,
				      unit,
				      related_line,
				      amount,
                      last_update
				      )
				      values
				      (p_product_code,
				      p_provider_code,
				      p_unitary_cost,
				      p_document_type,
				      p_document_no,
				      p_emission_date,
				      p_register_date,
				      p_coin_code,
				      p_unit,
				      p_related_line,
				      p_amount,
                      NOW());

end

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION set_products_provider(character varying, character varying, double precision, character varying, character varying, date, date, character varying, integer, integer, double precision)
  OWNER TO postgres;


CREATE OR REPLACE FUNCTION set_receivable(INOUT p_correlative integer, IN p_operation_type character varying, IN p_document_no character varying, IN p_control_no character varying, IN p_emission_date date, IN p_client_code character varying, IN p_client_name character varying, IN p_client_id character varying, IN p_client_address character varying, IN p_client_phone character varying, IN p_client_name_fiscal integer, IN p_credit_days integer, IN p_expiration_date date, IN p_description character varying, IN p_comments character varying, IN p_seller character varying, IN p_user_code character varying, IN p_station character varying, IN p_total_net double precision, IN p_total_tax double precision, IN p_total double precision, IN p_credit double precision, IN p_debit double precision, IN p_balance double precision, IN p_fiscal_impresion boolean, IN p_fiscal_printer_serial character varying, IN p_fiscal_printer_date timestamp without time zone, IN p_fiscal_printer_document character varying, IN p_fiscal_printer_z character varying, IN p_coin_code character varying, IN p_indexing_factor double precision, IN p_indexing boolean, IN p_indexing_coin character varying, IN p_indexing_correlative_origin integer, IN p_indexing_module_origin character varying, IN p_total_exempt double precision, IN p_base_igtf double precision, IN p_percent_igtf double precision, IN p_igtf double precision)
  RETURNS integer AS
$BODY$begin

	if(p_operation_type = 'RECEIVABLE' and p_document_no = '')then	
		select document_no from get_next_document(p_operation_type,'RECEIVABLE',true,false,p_station) into p_document_no;
	elsif(p_operation_type = 'RETURNEDCHECK')then	
		select document_no from get_next_document(p_operation_type,'RECEIVABLE',true,false,p_station) into p_document_no;
	elsif(p_operation_type = 'ADVANCE')then	
		select document_no from get_next_document(p_operation_type,'RECEIVABLE',true,false,p_station) into p_document_no;	
	elsif(p_operation_type = 'DEBITNOTE')then	
		select document_no from get_next_document(p_operation_type,'RECEIVABLE',true,false,p_station) into p_document_no;	
	elsif(p_operation_type = 'MONEYBACK')then	
		select document_no from get_next_document(p_operation_type,'RECEIVABLE',true,false,p_station) into p_document_no;	
	elsif(p_operation_type = 'CREDITNOTE')then	
		select document_no from get_next_document(p_operation_type,'SALES',true,false,p_station) into p_document_no;
	elsif(p_operation_type = 'PAYMENT')then	
		select document_no from get_next_document(p_operation_type,'RECEIVABLE',true,false,p_station) into p_document_no;	
	elsif(p_operation_type = 'ADVANCEAPPLIED')then	
		select document_no from get_next_document(p_operation_type,'RECEIVABLE',true,false,p_station) into p_document_no;	
	elsif(p_operation_type = 'CREDITNOTEAPPLIED')then	
		select document_no from get_next_document(p_operation_type,'RECEIVABLE',true,false,p_station) into p_document_no;	
	elsif(p_operation_type = 'CIM')then	
		select document_no from get_next_document(p_operation_type,'RECEIVABLE',true,false,p_station) into p_document_no;
	elsif(p_operation_type = 'DIM')then	
		select document_no from get_next_document(p_operation_type,'RECEIVABLE',true,false,p_station) into p_document_no;
	elsif(p_operation_type = 'DISCOUNT')then	
		select document_no from get_next_document(p_operation_type,'RECEIVABLE',true,false,p_station) into p_document_no;						
	end if;	


	--si hubo impresión fiscal guardar en documento_no el numero de ncr segun la fiscal 
	if(p_fiscal_impresion)then

		if(p_fiscal_printer_document is not null and p_fiscal_printer_document <> '' )then

			p_document_no = p_fiscal_printer_document;
			
		end if;
		
		

	end if;


	

 	
	insert into receivable
	(operation_type,
	document_no,
	control_no,
	emission_date, 
	client_code,
	client_name,
	client_id,
	client_address,
	client_phone,
	client_name_fiscal,
	credit_days,
	expiration_date,
	description,
	operation_comments,
	seller,
	user_code,
	station,
	total_net,
	total_tax,
	total, 
	credit,
	debit,
	balance,
	fiscal_impresion,
	fiscal_printer_serial,
	fiscal_printer_date,
	fiscal_printer_z,
	coin_code,
	indexing_factor,
	indexing,
	indexing_coin,
	indexing_correlative_origin,
	indexing_module_origin,
	total_exempt,
	base_igtf,
	percent_igtf,
	igtf,
    last_update)
	values
	(p_operation_type,
	p_document_no,
	p_control_no,
	p_emission_date, 
	p_client_code,
	p_client_name,
	p_client_id,
	p_client_address,
	p_client_phone,
	p_client_name_fiscal,
	p_credit_days,
	p_expiration_date,
	p_description,
	p_comments,
	p_seller,
	p_user_code,
	p_station,
	p_total_net,
	p_total_tax,
	p_total, 
	p_credit,
	p_debit,
	p_balance,
	p_fiscal_impresion,
	p_fiscal_printer_serial,
	p_fiscal_printer_date,
	p_fiscal_printer_z,
	p_coin_code,
	p_indexing_factor,
	p_indexing,
	p_indexing_coin,
	p_indexing_correlative_origin,
	p_indexing_module_origin,
	p_total_exempt,
	p_base_igtf,
	p_percent_igtf,
	p_igtf,
    NOW());
	

	select currval('receivable_correlative_seq') into p_correlative;

end$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION set_receivable(integer, character varying, character varying, character varying, date, character varying, character varying, character varying, character varying, character varying, integer, integer, date, character varying, character varying, character varying, character varying, character varying, double precision, double precision, double precision, double precision, double precision, double precision, boolean, character varying, timestamp without time zone, character varying, character varying, character varying, double precision, boolean, character varying, integer, character varying, double precision, double precision, double precision, double precision)
  OWNER TO postgres;

CREATE OR REPLACE FUNCTION set_receivable_details(p_main_correlative integer, p_correlative_related integer, p_balance_applied double precision, p_retention_tax double precision, p_retention_islr double precision, p_retention_municipal double precision, p_module_related character varying, p_credit_note double precision, p_percent_discount double precision, p_discount double precision)
  RETURNS void AS
$BODY$begin
	insert into receivable_details
	(main_correlative,
	correlative_related,
	balance_applied,
	retention_tax,
	retention_islr,
	retention_municipal,
	module_related,
	credit_note,
	percent_discount,
	discount,
    last_update)
	values
	(p_main_correlative,
	p_correlative_related,
	p_balance_applied,
	p_retention_tax,
	p_retention_islr,
	p_retention_municipal,
	p_module_related,
	p_credit_note,
	p_percent_discount,
	p_discount,
    NOW());

end
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION set_receivable_details(integer, integer, double precision, double precision, double precision, double precision, character varying, double precision, double precision, double precision)
  OWNER TO postgres;


CREATE OR REPLACE FUNCTION set_receivable_coins(p_main_correlative integer, p_coin_code character varying, p_factor_type integer, p_factor_aliquot double precision)
  RETURNS void AS
$BODY$begin

	insert into receivable_coins
	(main_correlative,
	coin_code,
	factor_type,
	factor_aliquot,
    last_update)
	values
	(p_main_correlative,
	p_coin_code,
	p_factor_type,
	p_factor_aliquot,
    NOW());

end


 $BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION set_receivable_coins(integer, character varying, integer, double precision)
  OWNER TO postgres;


CREATE OR REPLACE FUNCTION set_receivable_taxes(IN p_main_correlative integer, IN p_taxe_code character varying, IN p_aliquot double precision, IN p_taxable double precision, IN p_tax double precision, IN p_tax_type integer, INOUT p_line integer)
  RETURNS integer AS
$BODY$begin

	insert into receivable_taxes
	(main_correlative,
	taxe_code,
	aliquot,
	taxable,
	tax,
	tax_type,
    last_update)
	values
	(p_main_correlative,
	p_taxe_code,
	p_aliquot,
	p_taxable,
	p_tax,
	p_tax_type,
    NOW());

	select currval('receivable_taxes_line_seq') into p_line;
	
end$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION set_receivable_taxes(integer, character varying, double precision, double precision, double precision, integer, integer)
  OWNER TO postgres;


CREATE OR REPLACE FUNCTION set_sales_operation(INOUT p_correlative integer, IN p_operation_type character varying, IN p_document_no character varying, IN p_control_no character varying, IN p_emission_date date, IN p_client_code character varying, IN p_client_name character varying, IN p_client_id character varying, IN p_client_address character varying, IN p_client_phone character varying, IN p_client_name_fiscal integer, IN p_seller character varying, IN p_credit_days integer, IN p_expiration_date date, IN p_wait boolean, IN p_description character varying, IN p_store character varying, IN p_locations character varying, IN p_user_code character varying, IN p_station character varying, IN p_percent_discount double precision, IN p_discount double precision, IN p_percent_freight double precision, IN p_freight double precision, IN p_credit double precision, IN p_cash double precision, IN p_type_price integer, IN p_operation_comments character varying, IN p_pending boolean, IN p_freight_tax character varying, IN p_freight_aliquot double precision, IN p_total_amount double precision, IN p_total_net_cost double precision, IN p_total_tax_cost double precision, IN p_total_cost double precision, IN p_total_net_details double precision, IN p_total_tax_details double precision, IN p_total_details double precision, IN p_total_net double precision, IN p_total_tax double precision, IN p_total double precision, IN p_total_retention_tax double precision, IN p_total_retention_municipal double precision, IN p_total_retention_islr double precision, IN p_total_operation double precision, IN p_retention_tax_prorration double precision, IN p_retention_islr_prorration double precision, IN p_retention_municipal_prorration double precision, IN p_fiscal_impresion boolean, IN p_fiscal_printer_serial character varying, IN p_fiscal_printer_date timestamp without time zone, IN p_fiscal_printer_document character varying, IN p_fiscal_printer_z character varying, IN p_coin_code character varying, IN p_sale_point boolean, IN p_address_send character varying, IN p_contact_send character varying, IN p_phone_send character varying, IN p_free_tax boolean, IN p_total_weight double precision, IN p_restorant boolean, IN p_total_exempt double precision, IN p_base_igtf double precision, IN p_percent_igtf double precision, IN p_igtf double precision, IN p_shopping_order_document_no character varying, IN p_shopping_order_date date)
  RETURNS integer AS
$BODY$declare v_document_no_internal character varying;
declare v_operation_type character varying;
begin

	v_operation_type = p_operation_type;

	if(select use_sale_point_numeration from stations where code = p_station  )then


		if(p_operation_type = 'BILL' and p_sale_point )then
			v_operation_type = 'SPBILL';
		end if;

	end if;


	if(p_wait)then
	   if(not exists (select correlative from sales_operation where correlative = p_correlative) )then
	       select document_no from get_next_document(v_operation_type,'SALES',true,true,p_station) into p_document_no;
	   else
		select document_no from sales_operation where correlative=p_correlative into p_document_no;
	   end if;
	else
	    select document_no from get_next_document(v_operation_type,'SALES',true,false,p_station) into p_document_no;
	end if;   		
	
	delete from sales_operation where correlative=p_correlative; 


	v_document_no_internal = p_document_no;

	



	--si hubo impresión fiscal guardar en documento_no el numero de factura segun la fiscal 	
	if(p_fiscal_impresion)then

		if(p_fiscal_printer_document is not null and p_fiscal_printer_document <> '' )then

			p_document_no = p_fiscal_printer_document;
			
		end if;
		
		

	end if;
	

	
	insert into sales_operation(operation_type,
				    document_no,
				    control_no,
			        emission_date,
			        client_code,
				    client_name,
				    client_id,
				    client_address,
				    client_phone,
				    client_name_fiscal,
				    seller ,
				    credit_days,
				    expiration_date,
				    wait,
				    description,
				    store,
				    locations,
				    user_code,
				    station,
				    percent_discount,
				    discount,
				    percent_freight,
				    freight,
				    credit,
				    cash,
				    operation_comments,
				    type_price,
				    pending,
				    freight_tax,
				    freight_aliquot,
				    total_amount,
				    total_net_cost,
				    total_tax_cost,
				    total_cost,
				    total_net_details,
				    total_tax_details,
				    total_details,
				    total_net,
				    total_tax,
				    total,
				    total_retention_tax,
				    total_retention_islr,
				    total_retention_municipal,
				    total_operation,
				    retention_tax_prorration,
				    retention_islr_prorration,
				    retention_municipal_prorration,
				    document_no_internal,
				    fiscal_impresion,
				    fiscal_printer_serial,
				    fiscal_printer_date,
				    fiscal_printer_z,
				    coin_code,
				    sale_point,
				    address_send,
				    contact_send,
				    phone_send,
				    free_tax,
				    total_weight,
				    restorant,
				    total_exempt,
				    base_igtf,
				    percent_igtf,
				    igtf,
				    shopping_order_document_no,
				    shopping_order_date,
				    last_update)
				    values(
				    p_operation_type,
				    p_document_no,
				    p_control_no,
				    p_emission_date,
				    p_client_code,
				    p_client_name,
				    p_client_id,
				    p_client_address,
				    p_client_phone,
				    p_client_name_fiscal,
				    p_seller ,
				    p_credit_days,
				    p_expiration_date,
				    p_wait,
				    p_description,
				    p_store,
				    p_locations,
				    p_user_code,
				    p_station,
				    p_percent_discount,
				    p_discount,
				    p_percent_freight,
				    p_freight,
				    p_credit,
				    p_cash,
				    p_operation_comments,
				    p_type_price,
				    p_pending,
				    p_freight_tax,
				    p_freight_aliquot,
				    p_total_amount,
				    p_total_net_cost,
				    p_total_tax_cost,
				    p_total_cost,
				    p_total_net_details,
				    p_total_tax_details,
				    p_total_details,
				    p_total_net,
				    p_total_tax,
				    p_total,
				    p_total_retention_tax,
				    p_total_retention_islr,
				    p_total_retention_municipal,
				    p_total_operation,
				    p_retention_tax_prorration,
				    p_retention_islr_prorration,
				    p_retention_municipal_prorration,
				    v_document_no_internal,
				    p_fiscal_impresion,
				    p_fiscal_printer_serial,
				    p_fiscal_printer_date,
				    p_fiscal_printer_z,
				    p_coin_code,
				    p_sale_point,
				    p_address_send,
				    p_contact_send,
				    p_phone_send,
				    p_free_tax,
				    p_total_weight,
				    p_restorant,		
				    p_total_exempt,
				    p_base_igtf,
				    p_percent_igtf,
				    p_igtf,
				    p_shopping_order_document_no,
				    p_shopping_order_date,
				    now());

	 select currval('sales_operation_correlative_seq') into p_correlative;
end$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION set_sales_operation(integer, character varying, character varying, character varying, date, character varying, character varying, character varying, character varying, character varying, integer, character varying, integer, date, boolean, character varying, character varying, character varying, character varying, character varying, double precision, double precision, double precision, double precision, double precision, double precision, integer, character varying, boolean, character varying, double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision, boolean, character varying, timestamp without time zone, character varying, character varying, character varying, boolean, character varying, character varying, character varying, boolean, double precision, boolean, double precision, double precision, double precision, double precision, character varying, date)
  OWNER TO postgres;

CREATE OR REPLACE FUNCTION set_sales_operation_coins(p_main_correlative integer, p_coin_code character varying, p_factor_type integer, p_buy_aliquot double precision, p_sales_aliquot double precision, p_total_net_details double precision, p_total_tax_details double precision, p_total_details double precision, p_discount double precision, p_freight double precision, p_total_net double precision, p_total_tax double precision, p_total double precision, p_credit double precision, p_cash double precision, p_total_net_cost double precision, p_total_tax_cost double precision, p_total_cost double precision, p_total_operation double precision, p_total_retention_tax double precision, p_total_retention_municipal double precision, p_total_retention_islr double precision, p_retention_tax_prorration double precision, p_retention_islr_prorration double precision, p_retention_municipal_prorration double precision, p_total_exempt double precision)
  RETURNS void AS
$BODY$begin

	insert into sales_operation_coins
	(main_correlative,
	 coin_code,
	 factor_type,
	 buy_aliquot,
	 sales_aliquot,
	 total_net_details,
	 total_tax_details,
	 total_details,
	 discount,
	 freight,
	 total_net,
	 total_tax,
	 total,
	 credit,
	 cash,
	 total_net_cost,
	 total_tax_cost,
	 total_cost,
	 total_operation,
	 total_retention_tax,
	 total_retention_municipal,
	 total_retention_islr,
	 retention_tax_prorration,
	 retention_islr_prorration,
	 retention_municipal_prorration,
	 total_exempt,
     last_update)
	 values
	 (p_main_correlative,
	  p_coin_code,
	  p_factor_type,
	  p_buy_aliquot,
	  p_sales_aliquot,
	  p_total_net_details,
	  p_total_tax_details,
	  p_total_details,
	  p_discount,
	  p_freight,
	  p_total_net,
	  p_total_tax,
	  p_total,
	  p_credit,
	  p_cash,
	  p_total_net_cost,
	  p_total_tax_cost,
	  p_total_cost,
	  p_total_operation,
	  p_total_retention_tax,
	  p_total_retention_municipal,
	  p_total_retention_islr,
	  p_retention_tax_prorration,
	  p_retention_islr_prorration,
	  p_retention_municipal_prorration,
	  p_total_exempt,
      NOW());
	
	
end$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION set_sales_operation_coins(integer, character varying, integer, double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision)
  OWNER TO postgres;

CREATE OR REPLACE FUNCTION set_sales_operation_details(IN p_main_correlative integer, INOUT p_line integer, IN p_code_product character varying, IN p_description_product character varying, IN p_referenc character varying, IN p_mark character varying, IN p_model character varying, IN p_amount double precision, IN p_store character varying, IN p_locations character varying, IN p_unit integer, IN p_conversion_factor double precision, IN p_unit_type integer, IN p_unitary_cost double precision, IN p_sale_tax character varying, IN p_sale_aliquot double precision, IN p_buy_tax character varying, IN p_buy_aliquot double precision, IN p_price double precision, IN p_type_price integer, IN p_percent_discount double precision, IN p_discount double precision, IN p_product_type character varying, IN p_total_net_cost double precision, IN p_total_tax_cost double precision, IN p_total_cost double precision, IN p_total_net_gross double precision, IN p_total_tax_gross double precision, IN p_total_gross double precision, IN p_total_net double precision, IN p_total_tax double precision, IN p_total double precision, IN p_description character varying, IN p_technician character varying, IN p_coin_code character varying, IN p_total_weight double precision)
  RETURNS integer AS
$BODY$begin

	    insert into sales_operation_details(
			  main_correlative,
			  code_product,
			  description_product,
			  referenc,
			  mark,
			  model,
			  amount,
			  pending_amount,
			  store,
			  locations,
			  unit,
			  conversion_factor,
			  unit_type,
			  unitary_cost,
			  sale_tax,
			  sale_aliquot,
			  buy_tax,
			  buy_aliquot,
			  price,
			  type_price,  
			  percent_discount,
			  discount,
			  product_type,
			  total_net_cost,
			  total_tax_cost,
			  total_cost, 
			  total_net_gross,
			  total_tax_gross,
			  total_gross,
			  total_net,
			  total_tax,
			  total,
			  description,
			  technician,
			  coin_code,
			  total_weight,
              last_update)
			  values(
			  p_main_correlative,
			  p_code_product,
			  p_description_product,
			  p_referenc,
			  p_mark,
			  p_model,
			  p_amount,
			  p_amount,
			  p_store,
			  p_locations,
			  p_unit,
			  p_conversion_factor,
			  p_unit_type,
			  p_unitary_cost,
			  p_sale_tax,
			  p_sale_aliquot,
			  p_buy_tax,
			  p_buy_aliquot,
			  p_price,
			  p_type_price,  
			  p_percent_discount,
			  p_discount,
			  p_product_type,
			  p_total_net_cost,
			  p_total_tax_cost,
			  p_total_cost, 
			  p_total_net_gross,
			  p_total_tax_gross,
			  p_total_gross,
			  p_total_net,
			  p_total_tax,
			  p_total,
			  p_description,
			  p_technician,
			  p_coin_code,
			  p_total_weight,
              NOW());
		 select currval('sales_operation_details_line_seq') into p_line;
			
end$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION set_sales_operation_details(integer, integer, character varying, character varying, character varying, character varying, character varying, double precision, character varying, character varying, integer, double precision, integer, double precision, character varying, double precision, character varying, double precision, double precision, integer, double precision, double precision, character varying, double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision, double precision, character varying, character varying, character varying, double precision)
  OWNER TO postgres;


CREATE OR REPLACE FUNCTION set_sales_operation_taxes(IN p_main_correlative integer, IN p_taxe_code character varying, IN p_aliquot double precision, IN p_taxable double precision, IN p_tax double precision, IN p_tax_type integer, INOUT p_line integer)
  RETURNS integer AS
$BODY$declare v_sales_operation sales_operation;
declare v_sales_operation_details sales_operation_details;
declare v_taxable double precision;
declare v_tax double precision;

begin


		insert into sales_operation_taxes
		(main_correlative,
		taxe_code,
		aliquot,
		taxable,
		tax,
		tax_type,
        last_update)
		values
		(p_main_correlative,
		p_taxe_code,
		p_aliquot,
		p_taxable,
		p_tax,
		p_tax_type,
        NOW());

		select currval('sales_operation_taxes_line_seq')into p_line;
end$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION set_sales_operation_taxes(integer, character varying, double precision, double precision, double precision, integer, integer)
  OWNER TO postgres;


CREATE OR REPLACE FUNCTION set_debtstopay(INOUT p_correlative integer, IN p_operation_type character varying, IN p_document_no character varying, IN p_control_no character varying, IN p_emission_date date, IN p_reception_date date, IN p_provider_code character varying, IN p_provider_name character varying, IN p_provider_id character varying, IN p_provider_address character varying, IN p_provider_phone character varying, IN p_credit_days integer, IN p_expiration_date date, IN p_description character varying, IN p_comments character varying, IN p_user_code character varying, IN p_station character varying, IN p_total_net double precision, IN p_total_tax double precision, IN p_total double precision, IN p_credit double precision, IN p_debit double precision, IN p_balance double precision, IN p_coin_code character varying, IN p_indexing_factor double precision, IN p_indexing boolean, IN p_indexing_coin character varying, IN p_indexing_correlative_origin integer, IN p_indexing_module_origin character varying, IN p_total_exempt double precision, IN p_base_igtf double precision, IN p_percent_igtf double precision, IN p_igtf double precision)
  RETURNS integer AS
$BODY$begin

	if(p_operation_type = 'DEBTSTOPAY')then	
		select document_no from get_next_document(p_operation_type,'DEBTSTOPAY',true,false,p_station) into p_document_no;
	elsif(p_operation_type = 'RETURNEDCHECK')then	
		select document_no from get_next_document(p_operation_type,'DEBTSTOPAY',true,false,p_station) into p_document_no;
	elsif(p_operation_type = 'ADVANCE')then	
		select document_no from get_next_document(p_operation_type,'DEBTSTOPAY',true,false,p_station) into p_document_no;	
	--elsif(p_operation_type = 'DEBITNOTE')then	
		--select document_no from get_next_document(p_operation_type,'DEBTSTOPAY',true,false) into p_document_no;	
	elsif(p_operation_type = 'MONEYBACK')then	
		select document_no from get_next_document(p_operation_type,'DEBTSTOPAY',true,false,p_station) into p_document_no;	
	--elsif(p_operation_type = 'CREDITNOTE')then	
		--select document_no from get_next_document(p_operation_type,'SHOPPING',true,false) into p_document_no;
	elsif(p_operation_type = 'PAYMENT')then	
		select document_no from get_next_document(p_operation_type,'DEBTSTOPAY',true,false,p_station) into p_document_no;	
	elsif(p_operation_type = 'ADVANCEAPPLIED')then	
		select document_no from get_next_document(p_operation_type,'DEBTSTOPAY',true,false,p_station) into p_document_no;	
	elsif(p_operation_type = 'CREDITNOTEAPPLIED')then	
		select document_no from get_next_document(p_operation_type,'DEBTSTOPAY',true,false,p_station) into p_document_no;
	elsif(p_operation_type = 'CIM'  and p_document_no = '')then	
		select document_no from get_next_document(p_operation_type,'DEBTSTOPAY',true,false,p_station) into p_document_no;
	elsif(p_operation_type = 'DIM'  and p_document_no = '')then	
		select document_no from get_next_document(p_operation_type,'DEBTSTOPAY',true,false,p_station) into p_document_no;
	elsif(p_operation_type = 'DISCOUNT'  and p_document_no = '')then	
		select document_no from get_next_document(p_operation_type,'DEBTSTOPAY',true,false,p_station) into p_document_no;						
	end if;					
					
		
 	
	insert into debtstopay
	(operation_type,
	document_no,
	control_no,
	emission_date,
	reception_date, 
	provider_code,
	provider_name,
	provider_id,
	provider_address,
	provider_phone,
	credit_days,
	expiration_date,
	description,
	operation_comments, 
	user_code,
	station,
	total_net,
	total_tax,
	total, 
	credit,
	debit,
	balance,
	coin_code,
	indexing_factor,
	indexing,
	indexing_coin,
	indexing_correlative_origin, 
	indexing_module_origin,
	total_exempt,
	base_igtf,
	percent_igtf,
	igtf,
	last_update)
	values
	(p_operation_type,
	p_document_no,
	p_control_no,
	p_emission_date, 
	p_reception_date,
	p_provider_code,
	p_provider_name,
	p_provider_id,
	p_provider_address,
	p_provider_phone,
	p_credit_days,
	p_expiration_date,
	p_description,
	p_comments,
	p_user_code,
	p_station,
	p_total_net,
	p_total_tax,
	p_total, 
	p_credit,
	p_debit,
	p_balance,
	p_coin_code,
	p_indexing_factor,
	p_indexing,
	p_indexing_coin,
	p_indexing_correlative_origin, 
	p_indexing_module_origin,
	p_total_exempt,
	p_base_igtf,
	p_percent_igtf,
	p_igtf,
	NOW());

	select currval('debtstopay_correlative_seq') into p_correlative;

end$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION set_debtstopay(integer, character varying, character varying, character varying, date, date, character varying, character varying, character varying, character varying, character varying, integer, date, character varying, character varying, character varying, character varying, double precision, double precision, double precision, double precision, double precision, double precision, character varying, double precision, boolean, character varying, integer, character varying, double precision, double precision, double precision, double precision)
  OWNER TO postgres;

CREATE OR REPLACE FUNCTION set_debtstopay_coins(p_main_correlative integer, p_coin_code character varying, p_factor_type integer, p_factor_aliquot double precision)
  RETURNS void AS
$BODY$begin

	insert into debtstopay_coins
	(main_correlative,
	coin_code,
	factor_type,
	factor_aliquot,
    last_update)
	values
	(p_main_correlative,
	p_coin_code,
	p_factor_type,
	p_factor_aliquot,
    NOW());

end


 $BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION set_debtstopay_coins(integer, character varying, integer, double precision)
  OWNER TO postgres;

CREATE OR REPLACE FUNCTION set_debtstopay_details(p_main_correlative integer, p_correlative_related integer, p_balance_applied double precision, p_retention_tax double precision, p_retention_islr double precision, p_retention_municipal double precision, p_module_related character varying, p_credit_note double precision, p_percent_discount double precision, p_discount double precision)
  RETURNS void AS
$BODY$begin
	insert into debtstopay_details
	(main_correlative,
	correlative_related,
	balance_applied,
	retention_tax,
	retention_islr,
	retention_municipal,
	module_related,
	credit_note,
	percent_discount,
	discount,
    last_update)
	values
	(p_main_correlative,
	p_correlative_related,
	p_balance_applied,
	p_retention_tax,
	p_retention_islr,
	p_retention_municipal,
	p_module_related,
	p_credit_note,
	p_percent_discount,
	p_discount,
    NOW());

end
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION set_debtstopay_details(integer, integer, double precision, double precision, double precision, double precision, character varying, double precision, double precision, double precision)
  OWNER TO postgres;


CREATE OR REPLACE FUNCTION set_debtstopay_taxes(IN p_main_correlative integer, IN p_taxe_code character varying, IN p_aliquot double precision, IN p_taxable double precision, IN p_tax double precision, IN p_tax_type integer, INOUT p_line integer)
  RETURNS integer AS
$BODY$begin

	insert into debtstopay_taxes
	(main_correlative,
	taxe_code,
	aliquot,
	taxable,
	tax,
	tax_type,
    last_update)
	values
	(p_main_correlative,
	p_taxe_code,
	p_aliquot,
	p_taxable,
	p_tax,
	p_tax_type,
    NOW());

	select currval('debtstopay_taxes_line_seq') into p_line;
	
end$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION set_debtstopay_taxes(integer, character varying, double precision, double precision, double precision, integer, integer)
  OWNER TO postgres;

"""

def insert_fun():
	try:
		conn_a = db1()
		cursor_a = conn_a.cursor()
		conn_b = db2()
		cursor_b = conn_b.cursor()
		cursor_a.execute(query)
		conn_a.commit()
		cursor_b.execute(query)
		conn_b.commit()  # Asegúrate de hacer commit de la transacción
		print('-----------------Insersion de las funciones realizada con exito-----------------')  
	except psycopg2.Error as e:
		print(f"Error: {e}")
	finally:
		cursor_a.close()
		conn_a.close()
		cursor_b.close()
		conn_b.close()



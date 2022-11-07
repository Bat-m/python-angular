install python 2.7
install pgsql (15 in my case)

when python is installed
pip install psycopg2 (for connect to db)
pip install load_dotenv (for .env)
pip install flask

si probleme de droit bdd

GRANT ALL PRIVILEGES ON SCHEMA public TO user;
GRANT ALL PRIVILEGES ON DATABASE nautilux TO user;

install uuid extension pgsql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";


create a .env file with the right param
create a user in your database if fail auth
ex: ALTER USER user WITH PASSWORD 'pwd1234';


launch python init_db.py 


if table well created then create a trigger in pgsql to valide status
```
CREATE FUNCTION check_all_column_filled_for_status() RETURNS trigger AS $check_all_column_filled_for_status$
    BEGIN
        -- Check that all column is not null and change status if ok
        IF (NEW.label IS NOT NULL and NEW.description IS NOT NULL and NEW.name_intervener IS NOT NULL and NEW.location IS NOT NULL and NEW.date IS NOT NULL and NEW.status='VALID') THEN
		 NEW.status := replace(NEW.status,'DRAFT','VALID');
        END IF; 
        
        RETURN NEW;
    END;
$check_all_column_filled_for_status$ LANGUAGE plpgsql;

CREATE TRIGGER check_all_column_filled_for_status BEFORE INSERT OR UPDATE ON interventions
    FOR EACH ROW EXECUTE FUNCTION check_all_column_filled_for_status();
```
Pour mettre à jour le status une fois la date passé j'envisage un cron chaque heure (ou chaque jour a voir) avec le fichier check_date.py

@hourly C:\Python27 C:\Users\user\Documents\nautilux\check_date


launch npm start from ./front 

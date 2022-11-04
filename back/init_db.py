import psycopg2
import psycopg2.extras

import os
from dotenv import load_dotenv

load_dotenv()

HOSTNAME = os.getenv('HOSTNAME')
DATABASE=os.getenv('DATABASE')
USERNAME=os.getenv('USERNAME')
PWD=os.getenv('PWD')
PORT=os.getenv('PORT_ID')

conn=None
cur=None

try:
        conn= psycopg2.connect(
            host=HOSTNAME,
            dbname=DATABASE,
            user=USERNAME,
            password=PWD,
            port=PORT
        ) 

        cur= conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 

        create_script = ''' CREATE TABLE IF NOT EXISTS interventions(
                    id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
                    label varchar(40),
                    description varchar(100),
                    name_intervener varchar(30) NOT NULL,
                    location varchar(40),
                    date DATE,
                    status varchar(10) DEFAULT 'DRAFT'
                ) '''

        cur.execute(create_script)
        cur.execute('SELECT * FROM interventions')

        for record in cur.fetchall():
            print(record['id'],record['name_intervener'],record['label'])
        conn.commit()
except Exception as error:
    print(error)
finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()
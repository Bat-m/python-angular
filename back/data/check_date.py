
import datetime
import os
import psycopg2
import psycopg2.extras
from flask import Flask, jsonify, request, render_template, request, url_for, redirect
app = Flask(__name__)


def get_db_connection():
    conn = psycopg2.connect(
            host=os.getenv('HOSTNAME'),
            dbname=os.getenv('DATABASE'),
            user=os.getenv('USERNAME'),
            password=os.getenv('PWD'),
            port=os.getenv('PORT_ID')
        ) 
    return conn

#def getAll():   
conn = get_db_connection()
cur= conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
curr_timestamp = datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d')
print(curr_timestamp)
cur.execute('SELECT * FROM interventions WHERE date is not null')
update_script='UPDATE interventions SET status=%s WHERE id=%s'
for record in cur.fetchall():
    strDate=datetime.datetime.strptime(str(record['date']), '%Y-%m-%d')
    print(record['id'],strDate,curr_timestamp,record['label'])
    update_record= ('FINISHED',record['id'],)
    if strDate>curr_timestamp:
        cur.execute(update_script,update_record)

conn.commit()

    #getAll()

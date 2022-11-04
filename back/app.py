########  imports  ##########
import datetime
import os
import psycopg2
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

######## HOME ############
@app.route('/')
def hello():
    return render_template('index.html', utc_dt=datetime.datetime.utcnow())


######## Example fetch ############

@app.route('/test', methods=['GET', 'POST'])
def testfn():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM interventions;')
    interventions = cur.fetchall()
    print(interventions)
    cur.close()
    conn.close()
    return render_template('index.html', interventions=interventions)    

######## create ############
@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        name = request.form['name']
        descrition = request.form['description'] if request.form['description'] else None
        label =  request.form['label'] if request.form['label'] else None
        location =  request.form['location'] if request.form['location'] else None
        date =  request.form['date'] if request.form['date'] else None
        print(descrition)
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO interventions ( label,description, name_intervener, location, date, status)'
                    ' VALUES ( %s,%s, %s, %s, %s, %s)',
                    (label, descrition, name, location,date, 'DRAFT'))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index.html'))
    return render_template('create.html')

######## update ############
@app.route('/update/<id>', methods=('PUT', 'POST'))
def update(id):
    if request.method == 'POST':
        params = request.get_json()
        name = params.get('name', "").strip()
        descrition = params.get('descrition', "").strip()
        label = params.get('label', "").strip()
        location = params.get('location', "").strip()
        date = params.get('date', "").strip()
        print(name)
        update_script='UPDATE interventions SET label=COALESCE(%s, label) ,description=COALESCE(%s, description) , name_intervener=COALESCE(%s, name_intervener) , location=COALESCE(%s, location) , date=COALESCE(%s, date)   WHERE id=%s'
        update_record= (label, descrition, name, location,date,id,)
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(update_script,
                    update_record)
        conn.commit()
        cur.close()
        conn.close()
    return 'OK', 200

@app.route('/delete/<id>', methods=('PUT', 'POST'))
def delete(id):
    if request.method == 'POST':
        delete_script='DELETE FROM interventions WHERE id=%s'
        delete_record=(id,) 
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(delete_script,delete_record)
        conn.commit()
        cur.close()
        conn.close()
    return 'OK', 200      
    


# run app
app.run(debug=True)
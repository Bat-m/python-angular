########  imports  ##########
import datetime
import os
import psycopg2
from flask import Flask, jsonify, request, render_template, request, url_for, redirect
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = psycopg2.connect(
       host=os.getenv('HOSTNAME'),
            dbname=os.getenv('DATABASE'),
            user=os.getenv('USERNAME'),
            password=os.getenv('PWD'),
            port=os.getenv('PORT_ID')
        ) 
    return conn



######## Example fetch ############

@app.route('/getall', methods=['GET', 'POST'])
def testfn():
    orderBy = request.args.get('orderBy') if request.args.get('orderBy') else "DESC"
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''SELECT * FROM interventions ORDER BY date  {}'''.format(orderBy))
    interventions = cur.fetchall()
    print(interventions)
    cur.close()
    conn.close()
    return jsonify(interventions)    

######## create ############
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        params = request.get_json()
        name = params.get('name_intervener', "") if params.get('name_intervener', "").strip() else None
        description = params.get('description', "") if params.get('description', "").strip() else None
        label = params.get('label', "") if params.get('label', "").strip() else None
        location = params.get('location', "") if params.get('location', "").strip() else None
        date = params.get('date', "") if params.get('date', "").strip() else None
        print(description)
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO interventions ( label,description, name_intervener, location, date, status)'
                    ' VALUES ( %s,%s, %s, %s, %s, %s)',
                    (label, description, name, location,date, 'DRAFT'))
        cur.execute('SELECT * FROM interventions;')
        interventions = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
    return jsonify(interventions), 200

######## get one intervention ############
@app.route('/getone/<id>', methods=['GET', 'POST'])
def getone(id):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM interventions WHERE id=%s',(id,))
        intervention = cur.fetchone()
        print(intervention)
        conn.commit()
        cur.close()
        conn.close()
        return jsonify(intervention), 200

######## update ############
@app.route('/update/<id>', methods=['GET', 'PUT', 'POST'])
def update(id):
    if request.method == 'POST':
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM interventions WHERE id=%s',(id,))
        intervention = cur.fetchone()
        params = request.get_json()
        name = params.get('name_intervener', "") if  params.get('name_intervener', "").strip() else intervention[3]
        description = params.get('description', "") if  params.get('description', "").strip() else intervention[2]
        label = params.get('label', "") if  params.get('label', "").strip() else intervention[1]
        location = params.get('location', "") if  params.get('location', "").strip() else intervention[4]
        date = params.get('date', "") if  params.get('date', "").strip() else intervention[5]
        print(params)
        update_script='UPDATE interventions SET label=%s ,description=%s , name_intervener=%s , location=%s , date=%s   WHERE id=%s'
        update_record= (label, description, name, location,date,id,)
        cur.execute(update_script,
                    update_record)
        conn.commit()
        cur.close()
        conn.close()
    return 'OK', 200

@app.route('/delete/<id>', methods=['PUT', 'POST'])
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

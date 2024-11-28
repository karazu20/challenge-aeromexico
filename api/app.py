from flask import Flask, jsonify, request 
import psycopg2 
from sqlalchemy import create_engine 


conn_string = 'postgresql://engineer:examplepass@db:5432/aeromexico'
db = create_engine(conn_string) 

#Insert dataframe to DB
def get_data():
    # Create DataFrame     
    conn = psycopg2.connect(conn_string 
                            ) 
    conn.autocommit = True
    cursor = conn.cursor() 

    #Regresamos el select de los datos
    sql1 = '''select * from rh.company;'''
    cursor.execute(sql1) 
    companies = []
    for i in cursor.fetchall(): 
        print(i) 
        companies.append(i)

    conn.commit() 
    conn.close() 
    return companies

app = Flask(__name__) 

@app.route('/rows', methods=['GET']) 
def get_employes(): 
    data = get_data()
    return jsonify(data) 
  
  
if __name__ == '__main__': 
    app.run(debug=True) 
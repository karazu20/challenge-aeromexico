from flask import Flask, jsonify, request
import psycopg2
from sqlalchemy import create_engine

conn_string = "postgresql://engineer:examplepass@db:5432/aeromexico"


def get_connection():
    return psycopg2.connect(conn_string)


def get_data():
    conn = get_connection()
    cursor = conn.cursor()

    # Select all rows from joins to the tables
    sql1 = """select empl.first_name, empl.last_name, empl.email, 
                comp.company_name, comp.address, comp.city, comp.state,zip, comp.phone1, comp.phone2,
                dept.department from rh.employee as empl 
                inner join rh.company as comp  on empl.id_company = comp.id_company
                inner join rh.employee_department as empl_dept  on empl.id_employee = empl_dept.id_employee
                inner join rh.department as dept  on dept.id_department = empl_dept.id_department;"""
    cursor.execute(sql1)
    companies = []
    for i in cursor.fetchall():
        companies.append(i)

    conn.commit()
    conn.close()
    return companies


def insert_data(row):

    conn = get_connection()
    cursor = conn.cursor()

    # Get max ids
    cursor.execute("select max(dept.id_department) from rh.department as dept")
    max_id_departament = cursor.fetchall()[0][0]

    cursor.execute("select max(id_company) from rh.company")
    max_id_company = cursor.fetchall()[0][0]

    cursor.execute("select max(id_employee) from rh.employee")
    max_id_employee = cursor.fetchall()[0][0]

    # The corresponding fields are inserted into each of the tables.
    statement = f"""INSERT INTO rh.company(id_company, company_name, address, city, state, zip, phone1, phone2 ) 
                        VALUES({max_id_company + 1}, '{row.get('company_name')}', '{row.get('address')}', 
                        '{row.get('city')}', '{row.get('state')}', 
                        '{row.get('zip')}', '{row.get('phone1')}', '{row.get('phone2')}')"""

    cursor.execute(statement)
    statement = f"""INSERT INTO rh.department(id_department, department) 
                        VALUES({max_id_departament + 1}, '{row.get('department')}')"""

    cursor.execute(statement)
    statement = f"""INSERT INTO rh.employee(id_employee, first_name, last_name, email, id_company) 
                        VALUES({max_id_employee + 1}, '{row.get('first_name')}', '{row.get('last_name')}', 
                        '{row.get('email')}', {max_id_company + 1})"""
    cursor.execute(statement)
    statement = f"""INSERT INTO rh.employee_department(id_employee, id_department) 
                        VALUES({max_id_employee + 1}, {max_id_departament + 1})"""

    cursor.execute(statement)

    conn.commit()
    conn.close()


app = Flask(__name__)


@app.route("/rows", methods=["GET", "POST"])
def api_rows():
    if request.method == "GET":
        data = get_data()
        return jsonify(data)
    elif request.method == "POST":
        row = request.get_json()
        insert_data(row)
        return "Row created"
    else:
        return "Method not supported"


if __name__ == "__main__":
    app.run(debug=True)

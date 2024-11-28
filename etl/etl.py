import psycopg2 
import pandas as pd 
from sqlalchemy import create_engine 


conn_string = 'postgresql://engineer:examplepass@db:5432/aeromexico'
db = create_engine(conn_string) 

#Insert dataframe to DB
def load_data_to_db(dataframe, tabla_name, schema_name, index_column):
    # Create DataFrame     
    conn = db.connect()
    #if_exists{‘fail’, ‘replace’, ‘append’}, default ‘fail’
    dataframe.to_sql(tabla_name, con=conn, schema=schema_name, if_exists='append') 
    # conn = psycopg2.connect(conn_string 
    #                         ) 
    # conn.autocommit = True
    # cursor = conn.cursor() 

    # #Regresamos el select de los datos
    # sql1 = '''select * from rh.company;'''
    # cursor.execute(sql1) 
    # for i in cursor.fetchall(): 
    #     print(i) 

    # conn.commit() 
    conn.close() 

#######################################################################



def generate_indexes(data):
    #Add indexes according to aatabase schema
    data["id_employee"] = data["email"].astype('category').cat.codes + 1
    data["id_department"] = data["department"].astype('category').cat.codes + 1
    data["id_company"] = data["company_name"].astype('category').cat.codes + 1
    return data


def etl_data_company(data):
    #extract the company data 
    data_company = data [['id_company', 'company_name', 'address', 'city', 'state','zip', 'phone1', 'phone2',]].set_index('id_company')
    data_company = data_company.drop_duplicates()
    load_data_to_db(data_company, 'company', 'rh', 'id_company')
    
    

def etl_data_department(data):
    #extract the department data 
    data_department = data [['id_department', 'department']].set_index('id_department')
    data_department = data_department.drop_duplicates()
    load_data_to_db(data_department, 'department', 'rh', 'id_department')
    



def etl_data_employee(data):
    #extract the employee data 
    data_employee = data [['id_employee', 'first_name', 'last_name', 'email', 'id_company', ]].set_index('id_employee')
    data_employee = data_employee.drop_duplicates()
    load_data_to_db(data_employee, 'employee', 'rh', 'id_employee')


def etl_data_employee_department(data):
    #extract the employee-department data
    data_employee_department = data [['id_employee', 'id_department']].set_index(['id_employee', 'id_department'])
    data_employee_department = data_employee_department.drop_duplicates()
    load_data_to_db(data_employee_department, 'employee_department', 'rh', 'id_department')



########################################################################################




if __name__ == "__main__":
    print ("start ETL")
    csv_input = 'input.csv'
    data = pd.read_csv(csv_input)
    data = generate_indexes(data)
    etl_data_company(data)
    etl_data_department(data)
    etl_data_employee(data)
    etl_data_employee_department(data)
    print("End ETL")
    
    

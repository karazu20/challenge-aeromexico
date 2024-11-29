import pandas as pd
from sqlalchemy import create_engine

conn_string = "postgresql://engineer:examplepass@db:5432/aeromexico"
db = create_engine(conn_string)


def load_data_to_db(dataframe, tabla_name, schema_name):
    # Insert dataframe to DB
    conn = db.connect()
    dataframe.to_sql(tabla_name, con=conn, schema=schema_name, if_exists="append")
    conn.close()


def generate_indexes(data):
    # Add indexes according to aatabase schema
    data["id_employee"] = data["email"].astype("category").cat.codes + 1
    data["id_department"] = data["department"].astype("category").cat.codes + 1
    data["id_company"] = data["company_name"].astype("category").cat.codes + 1
    return data


def etl_data_company(data):
    # extract the company data
    data_company = data[
        [
            "id_company",
            "company_name",
            "address",
            "city",
            "state",
            "zip",
            "phone1",
            "phone2",
        ]
    ].set_index("id_company")
    return data_company.drop_duplicates()


def etl_data_department(data):
    # extract the department data
    data_department = data[["id_department", "department"]].set_index("id_department")
    return data_department.drop_duplicates()


def etl_data_employee(data):
    # extract the employee data
    data_employee = data[
        [
            "id_employee",
            "first_name",
            "last_name",
            "email",
            "id_company",
        ]
    ].set_index("id_employee")
    return data_employee.drop_duplicates()


def etl_data_employee_department(data):
    # extract the employee-department data
    data_employee_department = data[["id_employee", "id_department"]].set_index(
        ["id_employee", "id_department"]
    )

    return data_employee_department.drop_duplicates()


def ingest_data(data):

    data = generate_indexes(data)
    load_data_to_db(etl_data_company(data), "company", "rh")
    load_data_to_db(etl_data_department(data), "department", "rh")
    load_data_to_db(etl_data_employee(data), "employee", "rh")
    load_data_to_db(etl_data_employee_department(data), "employee_department", "rh")


if __name__ == "__main__":
    csv_input = "input.csv"
    data = pd.read_csv(csv_input)
    ingest_data(data)

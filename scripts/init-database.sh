#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE SCHEMA AUTHORIZATION engineer;
    CREATE SCHEMA IF NOT EXISTS rh AUTHORIZATION engineer;
    CREATE TABLE rh.company (
     id_company    integer PRIMARY KEY,
     company_name   varchar(100) NOT NULL CHECK (company_name <> ''),
     address   varchar(120),
     city   varchar(40),
     state   varchar(40),
     zip   varchar(5),
     phone1   varchar(13),
     phone2   varchar(13)
    );
    CREATE TABLE rh.department (
     id_department    integer PRIMARY KEY,
     department   varchar(100) NOT NULL CHECK (department <> '')
    );
    CREATE TABLE rh.employee (
     id_employee    integer PRIMARY KEY,
     first_name   varchar(40) NOT NULL CHECK (first_name <> ''),
     last_name   varchar(40) NOT NULL CHECK (last_name <> ''),
     email   varchar(40),
     id_company  integer,
     CONSTRAINT fk_company FOREIGN KEY (id_company)
     REFERENCES rh.company(id_company)
    );
    CREATE TABLE rh.employee_department(
     id_employee integer REFERENCES rh.employee(id_employee),
     id_department integer REFERENCES rh.department(id_department),
     CONSTRAINT employee_department_pk PRIMARY KEY(id_employee,id_department)
    );
EOSQL
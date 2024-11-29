import pandas as pd
import json
from etl import etl
from api.app import app


data_dummy = [
    [
        "James",
        "Butt",
        "Benton, John B Jr",
        "6649 N Blue Gum St",
        "New Orleans",
        "LA",
        "70116",
        "504-621-8927",
        "504-845-1427",
        "jbutt@gmail.com",
        "Sales",
    ],
    [
        "James",
        "Butt",
        "Benton, John B Jr",
        "6649 N Blue Gum St",
        "New Orleans",
        "LA",
        "70116",
        "504-621-8927",
        "504-845-1427",
        "jbutt@gmail.com",
        "Marketing",
    ],
    [
        "Josephine",
        "Darakjy",
        "Chanay, Jeffrey A Esq",
        "4 B Blue Ridge Blvd",
        "Brighton",
        "MI",
        "48116",
        "810-292-9388",
        "810-374-9840",
        "josephine_darakjy@darakjy.org",
        "Human Resources",
    ],
    [
        "Art",
        "Venere",
        "Chemel, James L Cpa",
        "8 W Cerritos Ave #54",
        "Bridgeport",
        "NJ",
        "8014",
        "856-636-8749",
        "856-264-4130",
        "art@venere.org",
        "Purchasing",
    ],
]


def test_etl_and_api( ):
    # We used the fake data
   
    data = pd.DataFrame(
        data_dummy,
        columns=[
            "first_name",
            "last_name",
            "company_name",
            "address",
            "city",
            "state",
            "zip",
            "phone1",
            "phone2",
            "email",
            "department",
        ],
    )

    
    #Test of the etl
    etl.ingest_data(data)
    #Test of the api
    response = app.test_client().get("/rows")
    
    # Validate of the response and size of rows
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert len(response_data) == len(data_dummy)

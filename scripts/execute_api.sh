#!/bin/bash
set -ex
echo "start api" 
cd api
### Install the App dependencies
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
#Execute api
flask run --host=0.0.0.0 --port=8080


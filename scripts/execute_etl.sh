#!/bin/bash
set -ex
echo "start etl" 
cd etl

### Install the App dependencies
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

#Execute etl
python etl.py
deactivate
echo "end etl" 


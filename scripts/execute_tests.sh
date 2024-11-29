#!/bin/bash
set -ex
echo "start tests" 
cd src

### Install the App dependencies
virtualenv venv
source venv/bin/activate
pip install -r tests/requirements.txt

#Execute tests
pytest tests/



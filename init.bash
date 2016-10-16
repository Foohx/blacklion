#!/bin/bash

# Create venv
virtualenv -p /usr/bin/python2.7 cache/env
cd cache/env
source bin/activate
cd ../../

# Install requirements
pip install -r cache/requirements.txt

#!/bin/sh

python3 -m venv env
. env/bin/activate
pip install pip --upgrade
pip install -r requirements.txt
./main.py

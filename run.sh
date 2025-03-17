#!/bin/sh
if [ ! -d "env" ]; then
  python3 -m venv env
  . env/bin/activate
  pip install pip --upgrade
  pip install -r requirements.txt

fi
source env/bin/activate
./main.py

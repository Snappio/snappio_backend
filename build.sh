#!/usr/bin/env bash

# exit on error
set -o errexit

# pip install --upgrade poetry
# poetry install
pip install -r requirements.txt

python3 manage.py collectstatic --no-input
python3 manage.py makemigrations snappio
python3 manage.py migrate

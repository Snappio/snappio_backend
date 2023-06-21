#!/usr/bin/env bash

# exit on error
set -o errexit

# pip install --upgrade poetry
# poetry install
pip install -r requirements.txt

./manage.py collectstatic --no-input
./manage.py makemigrations snappio
./manage.py migrate

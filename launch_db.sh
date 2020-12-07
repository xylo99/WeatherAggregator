#!/bin/bash

python3 manage.py makemigrations
python3 manage.py migrate
docker-compose -f pg_docker_compose.yml up -d
sleep 8
python3 manage.py runserver 0:8000

#!/bin/bash

echo "Aguardando banco de dados..."
python -c "
import socket
import time
import os

host = os.environ.get('DB_HOST', 'db')
port = int(os.environ.get('DB_PORT', 3306))

while True:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        sock.close()
        break
    except:
        time.sleep(1)
"
echo "Banco de dados disponível!"

python API_Teste/manage.py makemigrations

python API_Teste/manage.py migrate

python API_Teste/manage.py runserver 0.0.0.0:8000
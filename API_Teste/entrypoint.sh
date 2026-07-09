#!/bin/bash
set -e
echo "Aguardando banco de dados..."
python -c "
import socket, time, os
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
if [ "$1" = "runserver" ] || [ -z "$1" ]; then
    echo "Procurando migrações..."
    python manage.py makemigrations
    echo "Aplicando migrações..."
    python manage.py migrate
    exec python manage.py runserver 0.0.0.0:8000
else
    exec "$@"
fi
#!/bin/bash
# entrypoint.sh

# Aguarda o MySQL ficar disponível
echo "Aguardando banco de dados..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done
echo "Banco de dados disponível!"

# Aplica migrações
python manage.py migrate

# Inicia o servidor (em desenvolvimento) ou gunicorn para produção
# Para desenvolvimento:
python manage.py runserver 0.0.0.0:8000

# Para produção (descomente a linha abaixo e comente a anterior):
# gunicorn --bind 0.0.0.0:8000 meu_projeto.wsgi:application
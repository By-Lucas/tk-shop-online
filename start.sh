#!/bin/bash

# Aplicar as migrações do banco de dados
python manage.py migrate

# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Iniciar o servidor Gunicorn
gunicorn tk_send_product.wsgi:application --bind 0.0.0.0:$PORT

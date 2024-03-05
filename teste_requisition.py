import psycopg2
import select
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


# https://codedamn.com/news/sql/listen-notify-mechanism-in-postgresql


# Configurações do banco de dados
dbname = 'tk_promocoesdb'
user = 'postgres'
password = '123'
host = 'localhost'
port = '5432'
schema = 'tk_oferts'

connection = psycopg2.connect(
    dbname="tk_promocoesdb",
    user="postgres",
    password="123",
    host="localhost",
    port="5432"
)

connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

cursor = connection.cursor()
cursor.execute("LISTEN accounts_user;")


while True:
    if select.select([connection],[],[],5) == ([],[],[]):
        print("Timeout")
    else:
        connection.poll()
        while connection.notifies:
            notify = connection.notifies.pop(0)
            print(f"Got NOTIFY: {notify.pid}, {notify.channel}, {notify.payload}")
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

# Conecta ao banco de dados
connection = psycopg2.connect(
    dbname=dbname,
    user=user,
    password=password,
    host=host,
    port=port
)
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

# Cria um cursor
cursor = connection.cursor()

# Define a função PL/pgSQL para notificar novos usuários
notify_new_user_function = """
CREATE OR REPLACE FUNCTION notify_new_user() RETURNS trigger AS $$
BEGIN
  PERFORM pg_notify('users_notification', NEW.id::text);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
"""

# Cria o gatilho para chamar a função quando um novo usuário for inserido
create_trigger_query = """
CREATE TRIGGER users_notify_trigger
AFTER INSERT ON {schema}.accounts_user
FOR EACH ROW EXECUTE PROCEDURE notify_new_user();
""".format(schema=schema)

# Executa as consultas SQL
cursor.execute(notify_new_user_function)
cursor.execute(create_trigger_query)

# Fecha a conexão e o cursor
cursor.close()
connection.close()

print("Trigger e função criadas com sucesso.")
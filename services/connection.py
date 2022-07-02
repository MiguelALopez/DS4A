import sqlalchemy
import pandas as pd

global engine


def start():
    global engine
    name = "celsia"
    user = "team173"
    password = "4W5DBF0rT34m"
    port = '5432'

    host = "validated-data.c0qqjwg62lhy.us-east-1.rds.amazonaws.com"

    url = 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}'\
        .format(name=name, user=user, password=password, port=port, host=host)
    engine = sqlalchemy.create_engine(url)


def get_clients():
    global engine

    return pd.read_sql_query("SELECT * FROM clients;", engine)


def upload_clients(client):
    global engine

    client.to_sql(name='clients', schema='public', con=engine, if_exists='append', index=False)



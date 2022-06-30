import psycopg2
import pandas as pd

global connect


def start():
    global connect
    name = "celsia"
    user = "team173"
    password = "4W5DBF0rT34m"

    host = "validated-data.c0qqjwg62lhy.us-east-1.rds.amazonaws.com"

    connect = psycopg2.connect(dbname=name, user=user, password=password, host=host)


def get_clients():
    global connect

    return pd.read_sql_query("SELECT * FROM clients;", connect)



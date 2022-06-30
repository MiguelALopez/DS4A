import psycopg2

global cursor


def start():
    global cursor
    name = "celsia"
    user = "team173"
    password = "4W5DBF0rT34m"

    host = "validated-data.c0qqjwg62lhy.us-east-1.rds.amazonaws.com"

    connect = psycopg2.connect(dbname=name, user=user, password=password, host=host)
    cursor = connect.cursor()


def count_users():
    global cursor

    cursor.execute("SELECT COUNT(*) FROM clients;")
    return cursor.fetchone()


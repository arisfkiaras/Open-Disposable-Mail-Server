import psycopg2
import datetime
import simplejson as json
import certifi
import os


class Postgres:

    def __init__(self):
        username = os.environ.get('POSTGRES_DB_USERNAME', 'postgres')
        password = os.environ.get('POSTGRES_DB_PASSWORD', 'postgres')
        hostname = os.environ.get('POSTGRES_host', 'postgres_db')
        port = os.environ.get('POSTGRES_port', '5432')

        self.conn = psycopg2.connect(
            "dbname='open_mail_db_1' user='{}' host='{}' port='{}' password='{}'".format(
                username, hostname, port, password))

    def create_table(self):
        # CREATE TABLE images (imgname text, img bytea);
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE emails (
                id SERIAL PRIMARY KEY,
                domain VARCHAR(100),
                email_user VARCHAR(100),
                subject VARCHAR(1000),
                content bytea
            );"""
        )

    def insert_email(self, domain, user, subject, content):
        cur = self.conn.cursor()

        cur.execute('INSERT INTO emails (domain, email_user, subject, content) \
            VALUES (%s, %s, %s, %s)', (domain, user, subject, content))
        self.conn.commit()
 
# a = Postgres()
# #a.create_table()
# with open('test', 'r') as openfile:
#     data = openfile.read()
#     a.insert_email("yolo", "s", "no suibbkect", data)
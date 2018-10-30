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
                from_user VARCHAR(250),
                from_domain VARCHAR(250),
                to_user VARCHAR(250),
                to_domain VARCHAR(250),
                subject VARCHAR(1000),
                timestamp timestamp default current_timestamp,
                content bytea
            );"""
        )
        self.conn.commit()

    def insert_email(self, from_user, from_domain, to_user, to_domain, subject, content):
        cur = self.conn.cursor()

        cur.execute('INSERT INTO emails (from_user, from_domain, to_user, to_domain, subject, content) \
            VALUES (%s, %s, %s, %s)', (from_user, from_domain, to_user, to_domain, subject, content))
        self.conn.commit()
    
    def execute(self, command):
        cur = self.conn.cursor()
        cur.execute(command)
        print(cur.fetchall())
        self.conn.commit()

# a = Postgres()
# a.create_table()
# # a.execute("Select * from emails limit 1000;")
# # a.insert_email("yolo", "s", "no suibbkect","As")
# # #a.create_table()
# # with open('test', 'r') as openfile:
# #     data = openfile.read()
# #     a.insert_email("yolo", "s", "no suibbkect", data)
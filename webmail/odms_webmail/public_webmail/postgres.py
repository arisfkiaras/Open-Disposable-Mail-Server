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
    
    def execute(self, command, *kwargs):
        cur = self.conn.cursor()
        cur.execute(command, kwargs)
        self.conn.commit()

        return cur.fetchall()

    def get_emails_all(self):
        result = self.execute("Select id, from_user, from_domain, to_user, to_domain, subject, timestamp from emails limit 1000;")
        # print(result)
        return result
    
    def get_email_content(self, id):
        if id.isdigit():
            result = self.execute("Select content from emails where id = %s", id)
            #result = self.execute("Select content from emails where id = %d;" % int(id))
            
        return result[0]
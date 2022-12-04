import sqlite3
from sqlite3 import Error, Connection

class Db:

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn : Connection = None

    def create_connection(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
        except Error as e:
            print(e)

        return self.conn;

    def close_connection(self):
        if self.conn is not None:
            self.conn.close()

    def init_db(self):
        if self.conn:
            with open('db_init/01_create.sql', 'r+') as sql:
                sql_script = sql.read()
            cur = self.conn.cursor()
            cur.executescript(sql_script)
            self.conn.commit
        else:
            return False

    def get_preference(self, chat_id):
        try:
            cur = self.conn.cursor()
            data = cur.execute(f"SELECT p.preference FROM preference AS p WHERE p.chat_id = {chat_id}").fetchone()
            return data
        except Exception as ex:
            print(ex)


    def set_or_update_preference(self, chat_id, preference):
        try:
            cur = self.conn.cursor()
            cur.execute(f"INSERT INTO preference(chat_id, preference) VALUES({chat_id}, '{preference}') ON CONFLICT(chat_id) DO UPDATE SET preference='{preference}'");
            self.conn.commit()
        except Exception as ex:
            print(ex)

    def remove_preference(self, chat_id):
        try:
            cur = self.conn.cursor()
            cur.execute(f"DELETE FROM preference WHERE chat_id = {chat_id}");
            self.conn.commit()
        except Exception as ex:
            print(ex)








import sqlite3

class DatabaseHelper:
    def __init__(self, db_name='forum.db'):
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row

    def execute_query(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        return cursor

    def fetch_all(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

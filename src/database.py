import sqlite3

class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.session = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def create_table(self):
        query= ("""
        CREATE TABLE IF NOT EXISTS log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            msg TEXT,
            status TEXT,
            horario TEXT,
            previous_row_count INTEGER,
            current_row_count INTEGER
        );
        """)
        self.session.execute(query)
        self.conn.commit()

    def insert_data(self, data):
        query = ("""
        INSERT INTO log (msg, status, horario, previous_row_count, current_row_count)
        VALUES (:msg, :status, :horario, :previous_row_count, :current_row_count);
        """)
        self.session.execute(query, data)
        self.conn.commit()


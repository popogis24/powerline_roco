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
        CREATE TABLE IF NOT EXISTS log_perimetro (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            status TEXT,
            time TEXT,
            previous_row_count INTEGER,
            current_row_count INTEGER
        );
        """)
        query2 = ("""
        CREATE TABLE IF NOT EXISTS log_distancia (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            status TEXT,
            time TEXT,
            previous_row_count INTEGER,
            current_row_count INTEGER
        );
        """)
        self.session.execute(query)
        self.session.execute(query2)
        self.conn.commit()
    
    def insert_data(self, data, type):
        self.create_table()
        query = (f"""
        INSERT INTO log_{type} (status, time, previous_row_count, current_row_count)
        VALUES (:status, :time, :previous_row_count, :current_row_count);
        """)
        self.session.execute(query, data)
        self.conn.commit()


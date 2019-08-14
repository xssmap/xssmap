import sqlite3


class Database:
    def __init__(self):
        self.rows = []
        self.connection = sqlite3.connect('xssmap.db')
        self.cursor = self.connection.cursor().execute('select payload from xssmap')
        for row in self.cursor:
            self.rows += row

    def __del__(self):
        self.connection.close()

database = Database()

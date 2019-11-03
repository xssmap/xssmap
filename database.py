import sqlite3


class Database:
    def __init__(self):
        self.events = []
        self.functions = []
        self.connection = sqlite3.connect('xssmap.db')
        self.cursor = self.connection.cursor().execute('select event from event')
        for row in self.cursor:
            self.events += row
        self.cursor = self.connection.cursor().execute('select function from function')
        for row in self.cursor:
            self.functions += row

    def __del__(self):
        self.connection.close()


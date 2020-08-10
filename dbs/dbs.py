import sqlite3


class DBCarriers:
    def __init__(self):
        self.conn = sqlite3.connect('acts_db.db')
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS carriers (id integer primary key, name text, genitive text, number text)''')
        self.conn.commit()

    def insert_data(self, name, genitive, number):
        self.c.execute('''INSERT INTO carriers(name, genitive, number) VALUES (?, ?, ?)''',
                       (name, genitive, number))
        self.conn.commit()

    def delete_data(self, id):
        self.c.execute('''DELETE FROM carriers WHERE id == ?''', (id,))
        self.conn.commit()


class DBCities:
    def __init__(self):
        self.conn = sqlite3.connect('acts_db.db')
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS cities (id integer primary key, name text, genitive text)''')
        self.conn.commit()

    def insert_data(self, name, genitive):
        self.c.execute('''INSERT INTO cities(name, genitive) VALUES (?, ?)''',
                       (name, genitive))
        self.conn.commit()

    def delete_data(self, id):
        self.c.execute('''DELETE FROM cities WHERE id == ?''', (id,))
        self.conn.commit()


class DBSaves:
    def __init__(self):
        self.conn = sqlite3.connect('acts_db.db')
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS saves (
                number integer primary key, 
                date text,
                carrier integer,
                cities_from text,
                cities_to text,
                dates text,
                amount text,
                price text 
            )''')
        self.conn.commit()

    def insert_data(self, number, date, carrier, cities_from, cities_to, dates, amount, price):
        self.c.execute(
            '''INSERT INTO saves(
                number, date, carrier, cities_from, cities_to, dates, amount, price
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (int(number), date, carrier, cities_from, cities_to, dates, amount, price))
        self.conn.commit()

    def delete_data(self, number):
        self.c.execute('''DELETE FROM saves WHERE number == ?''', (number,))
        self.conn.commit()

import sqlite3

class DbConnection:
    def __init__(self):
        with sqlite3.connect('Passwords.db') as self.connection:
            self.dbCUrsor = self.connection.cursor()

            self.dbCUrsor.execute('''
                CREATE TABLE IF NOT EXISTS users(
                    id integer PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            ''')

            self.dbCUrsor.execute('''
                CREATE TABLE IF NOT EXISTS platforms(
                    id integer PRIMARY KEY,
                    platform TEXT UNIQUE NOT NULL
                )
            ''')
    
    def addUser(self, username, password):
        with self.connection:
            self.dbCUrsor.execute('INSERT INTO users(username, password) VALUES(:username, :password)', {'username':username, 'password':password})

    def loginUser(self, username, password):
        with self.connection:
            user = self.dbCUrsor.execute('SELECT * FROM users WHERE username=:username AND password=:password', {'username':username, 'password':password})
            user = user.fetchone()

            return user
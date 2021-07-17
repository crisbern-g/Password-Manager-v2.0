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
                CREATE TABLE IF NOT EXISTS accounts(
                    id integer PRIMARY KEY,
                    platform integer,
                    username text,
                    password text,
                    date_added text,
                    date_modified text,
                    user_id integer,
                    FOREIGN KEY(user_id) REFERENCES users(id)
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
    
    def add_account(self, platform, username, password, date_added, date_modified, user_id):
        with self.connection:
            self.dbCUrsor.execute('''
                INSERT INTO accounts(platform, username, password, date_added, date_modified, user_id)
                Values(:platform, :username, :password, :date_added, :date_modified, :user_id)
            ''',
            {'platform':platform, 'username':username, 'password':password, 'date_added':date_added, 'date_modified':date_modified, 'user_id':user_id}
            )

    def get_all_accounts(self, user_id):
        with self.connection:
            accounts = self.dbCUrsor.execute(
                '''
                SELECT id, platform, username, password, date_added, date_modified FROM accounts
                WHERE user_id = :user_id
                ''',
                {'user_id': user_id}
            )

            accounts = accounts.fetchall()

            return accounts
import sqlite3
import os
from cryptography.fernet import Fernet
from decouple import config

class DbConnection:
    def __init__(self):
        #Creation of Secret Key if it does not exist
        if not os.path.exists('.env'):
            with open('.env', 'w') as file:
                secret_key = Fernet.generate_key()
                file.writelines('SECRET=' + secret_key.decode('UTF-8'))
            
        #gets they KEY and converts it into BYTES
        self.secret_key = config('SECRET').encode('UTF-8')
        self.encrpytor_decryptor = Fernet(self.secret_key)

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
                    password TEXT,
                    date_added text,
                    date_modified text,
                    user_id integer,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            ''')
    
    def addUser(self, username, password):
        with self.connection:
            password = self.encrpytor_decryptor.encrypt(password.encode('UTF-8'))
            password = password.decode('UTF-8')

            self.dbCUrsor.execute('INSERT INTO users(username, password) VALUES(:username, :password)', {'username':username, 'password':password})

    def loginUser(self, username, password):
        with self.connection:
            user = self.dbCUrsor.execute('SELECT * FROM users WHERE username=:username', {'username':username})

            try:
                user = list(user.fetchone())
                user[2] = self.encrpytor_decryptor.decrypt(user[2].encode('UTF-8'))
                user[2] = user[2].decode('UTF-8')

                if user[2] == password:
                    return user
                else:
                    return None
            except TypeError:
                return None
    
    def add_account(self, platform, username, password, date_added, date_modified, user_id):
        password = self.encrpytor_decryptor.encrypt(password.encode('UTF-8'))
        password = password.decode('UTF-8')

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
    
    def delete_account(self, account_id):
        with self.connection:
            self.dbCUrsor.execute('DELETE FROM accounts WHERE id=:account_id', {'account_id':account_id})

    def update_account(self, platform, username, password, date_modified, account_id):
        password = self.encrpytor_decryptor.encrypt(password.encode('UTF-8'))
        password = password.decode('UTF-8')
        
        new_data = {
            'platform': platform,
            'username': username,
            'password': password,
            'date_modified': date_modified,
            'account_id': account_id
        }

        with self.connection:
            self.dbCUrsor.execute(
                '''
                UPDATE accounts

                SET platform = :platform,
                username=:username,
                password=:password,
                date_modified = :date_modified

                WHERE id=:account_id
                ''',
                new_data
            )
    
    def search_account(self,user_id, keyword):
        with self.connection:
            accounts = self.dbCUrsor.execute(
                '''
                SELECT id, platform, username, password, date_added, date_modified FROM accounts
                WHERE (
                    platform LIKE :keyword OR
                    username LIKE :keyword
                    )
                AND (user_id = :user_id)
                ''',
                {'user_id': user_id, 'keyword':'%'+ keyword + '%'}
            )

            accounts = accounts.fetchall()

            return accounts

    def delete_user(self, user_id):
        with self.connection:
            self.dbCUrsor.execute(
                '''
                DELETE FROM accounts WHERE user_id=:user_id
                ''',
                {'user_id':user_id}
            )

            self.dbCUrsor.execute(
                '''
                DELETE FROM users WHERE id=:user_id
                ''',
                {'user_id':user_id}
            )
    
    def update_user_password(self, user_id, password):
        password = self.encrpytor_decryptor.encrypt(password.encode('UTF-8'))
        password = password.decode('UTF-8')

        with self.connection:
            self.dbCUrsor.execute(
                '''
                UPDATE users
                SET password = :password
                WHERE id=:user_id
                ''',
                {'password':password, 'user_id':user_id}
            )
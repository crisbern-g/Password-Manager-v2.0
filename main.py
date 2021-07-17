import tkinter as tk
from tkinter import ttk
import Account_Input
import LoginScreen
import dbConnection

dataBase_Connection = dbConnection.DbConnection()

login = LoginScreen.Login_Signup(dataBase_Connection)
login_credentials = login.get_credentials()

def add_account():
    addAccount = Account_Input.Add_Account(main, dataBase_Connection, login_credentials['id'], update_table)
    addAccount.mainloop()

def update_table():
    accounts = dataBase_Connection.get_all_accounts(login_credentials['id'])
    passwords_table.delete(*passwords_table.get_children())
    for account in accounts:
        passwords_table.insert(parent='', index='end', iid=account[0], text='', values=(account[1], account[2], account[3], account[4], account[5]))

try:
    main = tk.Tk()
    main.title('Password Manager 2.0')

    tk.Label(main, text='Logged in As '+ login_credentials['username']).grid(row=0, column=0, sticky=tk.W)

    passsword_table_pane = tk.PanedWindow(main)
    passsword_table_pane.grid(row=1, column=0)

    actions_button_pane = tk.PanedWindow(main)
    actions_button_pane.grid(row=1, column=1)

    passwords_table = ttk.Treeview(passsword_table_pane)
    passwords_table['columns'] = ('Platform', 'Username', 'Password', 'Date Added', 'Date Modified')

    passwords_table.column('#0', width=0, minwidth=0)

    passwords_table.heading('#0', text='')
    passwords_table.heading('Platform', text='Platform')
    passwords_table.heading('Username', text='Username')
    passwords_table.heading('Password', text='Password')
    passwords_table.heading('Date Added', text='Date Added')
    passwords_table.heading('Date Modified', text='Date Modified')
    passwords_table.grid(row=0, column=0)

    update_table()

    addButton = tk.Button(actions_button_pane, text='Add Account', width=15, cursor='hand2', command=add_account)
    addButton.grid(row=0, column=0, pady=5)

    editButton = tk.Button(actions_button_pane, text='Edit Account', width=15, cursor='hand2')
    editButton.grid(row=1, column=0, pady=5)

    deleteButton = tk.Button(actions_button_pane, text='Delete Account', width=15, cursor='hand2')
    deleteButton.grid(row=2, column=0, pady=5)

    main.mainloop()
except KeyError:
    pass

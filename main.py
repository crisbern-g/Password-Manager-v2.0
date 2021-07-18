from cryptography.fernet import Fernet
from decouple import config
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import Account_Input
import LoginScreen
import dbConnection
import Edit_Info

dataBase_Connection = dbConnection.DbConnection()

login = LoginScreen.Login_Signup(dataBase_Connection)
login_credentials = login.get_credentials()

def add_account():
    addAccount = Account_Input.Add_Account(main, dataBase_Connection, login_credentials['id'], update_table)
    addAccount.mainloop()

def update_table():
    secret_key = config('SECRET').encode('UTF-8')
    encrpytor_decryptor = Fernet(secret_key)

    deleteButton.config(state='disabled')
    editButton.config(state='disabled')
    accounts = dataBase_Connection.get_all_accounts(login_credentials['id'])
    passwords_table.delete(*passwords_table.get_children())

    for account in accounts:
        decrypted_password = encrpytor_decryptor.decrypt(account[3].encode('UTF-8'))
        decrypted_password = decrypted_password.decode('UTF-8')

        passwords_table.insert(parent='', index='end', iid=account[0], text='', values=(account[1], account[2], decrypted_password, account[4], account[5]))

def get_selected(*event):
    selected = passwords_table.focus()
    selected = passwords_table.item(selected)
    
    if selected != {}:
        deleteButton.config(state='normal')
        editButton.config(state='normal')
    
    data = {'id': passwords_table.focus(), 'data':selected['values']}
    return data
    

def delete_account():
    choice  = messagebox.askyesno(message='Are you sure you want to delete this account?', title='Confirmation')

    if choice:
        data = get_selected()
        dataBase_Connection.delete_account(data['id'])
        update_table()
        deleteButton.config(state='disabled')
        editButton.config(state='disabled')

def edit_account():
    data = get_selected()
    edit = Edit_Info.Edit_Info(main, dataBase_Connection, login_credentials['id'], update_table, data['data'][0], data['data'][1], data['data'][2], data['id'])
    edit.mainloop()

def search():
    secret_key = config('SECRET').encode('UTF-8')
    encrpytor_decryptor = Fernet(secret_key)

    accounts = dataBase_Connection.search_account(login_credentials['id'], searchEntry.get())
    passwords_table.delete(*passwords_table.get_children())

    for account in accounts:
        decrypted_password = encrpytor_decryptor.decrypt(account[3].encode('UTF-8'))
        decrypted_password = decrypted_password.decode('UTF-8')
        passwords_table.insert(parent='', index='end', iid=account[0], text='', values=(account[1], account[2], decrypted_password, account[4], account[5]))

try:
    main = tk.Tk()
    main.title('Password Manager 2.0')
    main.resizable(0,0)

    tk.Label(main, text='Logged in As '+ login_credentials['username']).grid(row=0, column=0, sticky=tk.W)

    searchPane = tk.PanedWindow(main, height=900)
    searchPane.grid(row=1, column=0)

    searchButton = tk.Button(searchPane,text='Search', width=20, command=search)
    searchButton.grid(row=0, column=0, sticky=tk.W, padx=20)

    searchEntry = tk.Entry(searchPane, width=50)
    searchEntry.grid(row=0, column=1, sticky=tk.W)

    passsword_table_pane = tk.PanedWindow(main)
    passsword_table_pane.grid(row=2, column=0)

    actions_button_pane = tk.PanedWindow(main)
    actions_button_pane.grid(row=2, column=1)

    passwords_table = ttk.Treeview(passsword_table_pane, selectmode='browse')
    passwords_table['columns'] = ('Platform', 'Username', 'Password', 'Date Added', 'Date Modified')

    passwords_table.column('#0', width=0, minwidth=0)

    passwords_table.heading('#0', text='')
    passwords_table.heading('Platform', text='Platform')
    passwords_table.heading('Username', text='Username')
    passwords_table.heading('Password', text='Password')
    passwords_table.heading('Date Added', text='Date Added')
    passwords_table.heading('Date Modified', text='Date Modified')
    passwords_table.bind('<ButtonRelease-1>', get_selected)
    passwords_table.grid(row=0, column=0)

    addButton = tk.Button(actions_button_pane, text='Add Account', width=15, cursor='hand2', command=add_account)
    addButton.grid(row=0, column=0, pady=5)

    editButton = tk.Button(actions_button_pane, text='Edit Account', width=15, cursor='hand2', state='disabled', command=edit_account)
    editButton.grid(row=1, column=0, pady=5)

    deleteButton = tk.Button(actions_button_pane, text='Delete Account', width=15, cursor='hand2', state='disabled', command=delete_account)
    deleteButton.grid(row=2, column=0, pady=5)

    update_table()

    main.mainloop()
except KeyError:
    pass

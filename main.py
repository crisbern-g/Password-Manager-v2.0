import tkinter as tk
from tkinter import ttk
import Account_Input
import LoginScreen

def add_account(master):
    addAccount = Account_Input.Add_Account(master)
    addAccount.mainloop()

def main():
    main = tk.Tk()
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

    addButton = tk.Button(actions_button_pane, text='Add Account', width=15, cursor='hand2', command=lambda: add_account(main))
    addButton.grid(row=0, column=0, pady=5)

    editButton = tk.Button(actions_button_pane, text='Edit Account', width=15, cursor='hand2')
    editButton.grid(row=1, column=0, pady=5)

    deleteButton = tk.Button(actions_button_pane, text='Delete Account', width=15, cursor='hand2')
    deleteButton.grid(row=2, column=0, pady=5)

    main.mainloop()

login = LoginScreen.Login_Signup()
login_credentials = login.get_credentials()

try:
    main()
except KeyError:
    main.destroy()

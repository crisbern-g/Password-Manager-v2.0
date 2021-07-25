from cryptography.fernet import Fernet
from decouple import config
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import Account_Input
import LoginScreen
import dbConnection
import Edit_Info
import Manage_Account

'''
INITIALIZATIONS AND DEFINING FUNCTIONS
'''
#creating instances for the login and database connection
dataBase_Connection = dbConnection.DbConnection()
login = LoginScreen.Login_Signup(dataBase_Connection)


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


def search(*event):
    secret_key = config('SECRET').encode('UTF-8')
    encrpytor_decryptor = Fernet(secret_key)

    accounts = dataBase_Connection.search_account(login_credentials['id'], searchEntry.get())
    passwords_table.delete(*passwords_table.get_children())

    for account in accounts:
        decrypted_password = encrpytor_decryptor.decrypt(account[3].encode('UTF-8'))
        decrypted_password = decrypted_password.decode('UTF-8')
        passwords_table.insert(parent='', index='end', iid=account[0], text='', values=(account[1], account[2], decrypted_password, account[4], account[5]))


def exit_app():
    main.destroy()


def manage_account():
    manage = Manage_Account.Manage_Account(main, dataBase_Connection, login_credentials['id'], login_credentials['username'], login_credentials['password']) 
    manage.mainloop()


def show_about():
    messagebox.showinfo(title='About', message='Password Manager 2.0 helps you store your passwords safely in your local storage.')


'''
RUNNING THE PROGRAM
'''

#running login and returning the credentials
login.mainloop()
login_credentials = login.get_credentials()

try:
    #creating the window
    main = tk.Tk()
    main.title('Password Manager 2.0')
    main.configure(bg='lightsteelblue')
    main.geometry('1150x310')
    main.resizable(0,0)

    #menubar configurations
    menuBar = tk.Menu(main, bg='lightsteelblue')

    account_menu = tk.Menu(menuBar, tearoff=0)
    account_menu.add_command(label='Account Settings', command=manage_account)
    account_menu.add_command(label='Exit', command=exit_app)

    help_menu = tk.Menu(menuBar, tearoff=0)
    help_menu.add_command(label='About', command=show_about)

    #menuBar Cascades
    menuBar.add_cascade(label='Logged in as: '+ login_credentials['username'], menu=account_menu)
    menuBar.add_cascade(label='Help', menu=help_menu)

    #the panedwindow for the search button and search entry
    searchPane = tk.PanedWindow(main, height=900, bg='lightsteelblue')
    searchPane.grid(row=1, column=0)

    searchButton = tk.Button(searchPane,text='Search', width=20, command=search)
    searchButton.grid(row=0, column=0, sticky=tk.W, padx=20)

    searchEntry = tk.Entry(searchPane, width=50)
    searchEntry.grid(row=0, column=1, sticky=tk.W)
    searchEntry.bind('<Return>', search)

    #Configuring the Treeview
    passsword_table_pane = tk.PanedWindow(main, bg='lightsteelblue')
    passsword_table_pane.grid(row=2, column=0)

    style=ttk.Style()
    style.configure("Treeview.Heading", font=('Calibri', 13, 'bold'))

    passwords_table = ttk.Treeview(passsword_table_pane, selectmode='browse')
    passwords_table['columns'] = ('Platform', 'Username', 'Password', 'Date Added', 'Date Modified')

    passwords_table.column('#0', width=0, minwidth=0, anchor='center')
    passwords_table.column('Platform', minwidth=150, anchor='center')
    passwords_table.column('Username', minwidth=150, anchor='center')
    passwords_table.column('Password', minwidth=150, anchor='center')
    passwords_table.column('Date Added', minwidth=150, anchor='center')
    passwords_table.column('Date Modified', minwidth=150, anchor='center')

    passwords_table.heading('#0', text='')
    passwords_table.heading('Platform', text='Platform')
    passwords_table.heading('Username', text='Username')
    passwords_table.heading('Password', text='Password')
    passwords_table.heading('Date Added', text='Date Added')
    passwords_table.heading('Date Modified', text='Date Modified')

    passwords_table.bind('<ButtonRelease-1>', get_selected)
    passwords_table.grid(row=0, column=0)

    #configuring the buttons
    actions_button_pane = tk.PanedWindow(main, bg='lightsteelblue')
    actions_button_pane.grid(row=2, column=1)

    addButton = tk.Button(actions_button_pane, text='Add Account', width=15, cursor='hand2', command=add_account)
    addButton.grid(row=0, column=0, pady=5)

    editButton = tk.Button(actions_button_pane, text='Edit Account', width=15, cursor='hand2', state='disabled', command=edit_account)
    editButton.grid(row=1, column=0, pady=5)

    deleteButton = tk.Button(actions_button_pane, text='Delete Account', width=15, cursor='hand2', state='disabled', command=delete_account)
    deleteButton.grid(row=2, column=0, pady=5)

    #label at the bottom
    tk.Label(main, text = "PM", font="GIGI 13",bg="LightSteelBlue").grid(row=3, column=0, sticky=tk.W)
    tk.Label(main, text = "Password Manager", font = "Magneto 9",bg="LightSteelBlue").grid(row=4, column=0, sticky=tk.W)
    
    #displays the table according to what is stored for the user
    update_table()

    #adding the connfigured menubar
    main.config(menu=menuBar)

    #running the main
    main.mainloop()
except KeyError:
    pass

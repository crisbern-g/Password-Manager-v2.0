import tkinter as tk 
from tkinter import messagebox

class Manage_Account(tk.Toplevel):
    def __init__(self, master, db_connection,user_id, username, password):
        tk.Toplevel.__init__(self, master)
        self.master = master
        self.resizable(0, 0)
        self.title('Manage Account')
        self.configure(bg='lightsteelblue')
        self.db_connection = db_connection

        #credentials
        self.user_id = user_id
        self.username = username
        self.password = password
        

        tk.Label(self, text='Username: ' + self.username, bg='lightsteelblue').grid(row=0, column=0, sticky=tk.W)
        tk.Label(self, text='Change Password', bg='lightsteelblue').grid(row=1, column=0, sticky=tk.W, pady=10)

        tk.Label(self, text='Old Password:', bg='lightsteelblue').grid(row=2, column=0, sticky=tk.W)
        self.old_password_var = tk.StringVar()
        self.old_password_entry = tk.Entry(self, width=30, textvariable=self.old_password_var, show='*')
        self.old_password_entry.bind('<Key>', self.empty_change_password)
        self.old_password_entry.bind('<KeyRelease>', self.empty_change_password)
        self.old_password_entry.grid(row=2, column=0, padx=140)

        tk.Label(self, text='New Password:', bg='lightsteelblue').grid(row=3, column=0, sticky=tk.W)
        self.new_password_var = tk.StringVar()
        self.new_password_entry = tk.Entry(self, width=30, textvariable=self.new_password_var, show='*')
        self.new_password_entry.bind('<Key>', self.empty_change_password)
        self.new_password_entry.bind('<KeyRelease>', self.empty_change_password)
        self.new_password_entry.grid(row=3, column=0, padx=140)

        tk.Label(self, text='Confirm New Password:', bg='lightsteelblue').grid(row=4, column=0, sticky=tk.W)
        self.confirm_new_var = tk.StringVar()
        self.confirm_new_password_entry = tk.Entry(self, width=30, textvariable=self.confirm_new_var, show='*')
        self.confirm_new_password_entry.bind('<Key>', self.empty_change_password)
        self.confirm_new_password_entry.bind('<KeyRelease>', self.empty_change_password)
        self.confirm_new_password_entry.grid(row=4, column=0, padx=140)

        self.confirm_button = tk.Button(self, text='Change Password', state='disabled', command=self.edit_user_password)
        self.confirm_button.grid(row=5, column=0)

        tk.Label(self, text='Delete Account', bg='lightsteelblue').grid(row=6, column=0, sticky=tk.W, pady=10)

        tk.Label(self, text='Enter CURRENT password to delete your account', bg='lightsteelblue').grid(row=7, column=0, sticky=tk.W)
        self.delete_pass_var = tk.StringVar()
        self.delete_password = tk.Entry(self, show='*', width=40, textvariable=self.delete_pass_var)
        self.delete_password.grid(row=8, column=0)
        self.delete_Button = tk.Button(self, text='DELETE ACCOUNT', bg='red', state='disabled', command=self.delete_user_account)
        self.delete_password.bind('<Key>', self.empty_delete_entry)
        self.delete_password.bind('<KeyRelease>', self.empty_delete_entry)
        self.delete_Button.grid(row=9, column=0)

        self.action_invoked = False

        self.grab_set()

    def empty_change_password(self, event):
        old_pass = self.old_password_var.get()
        new_pass = self.new_password_var.get()
        confirm_pass = self.confirm_new_var.get()

        check_empty = (old_pass.isspace() or not old_pass) or (new_pass.isspace() or not new_pass) or (confirm_pass.isspace() or not confirm_pass)

        if check_empty and len(old_pass)<8 or len(new_pass)<8 or len(confirm_pass)<8:
            self.confirm_button.configure(state='disabled')
        else:
            self.confirm_button.configure(state='normal')
        
    def empty_delete_entry(self, event):
        delete_pass = self.delete_pass_var.get()

        if delete_pass.isspace() or not delete_pass:
            self.delete_Button.configure(state='disabled')
        else:
            self.delete_Button.configure(state='normal')

    def delete_user_account(self):
        if self.delete_pass_var.get() == self.password:
            choice = messagebox.askyesno(title='Confirmation', message='Are you sure to delete your account? Doing so will also delete all your stored accounts')
            
            if choice:
                self.db_connection.delete_user(self.user_id)
                messagebox.showinfo(message='All data associated to your account have been deleted. The program will now terminate')
                self.master.destroy()                         
        else:
            messagebox.showerror(title='Error',message='Wrong Password')

    def edit_user_password(self):
        old_pass = self.old_password_var.get()
        new_pass = self.new_password_var.get()
        confirm_pass = self.confirm_new_var.get()

        if (new_pass == confirm_pass) and (old_pass == self.password):
            messagebox.showinfo(message='Your Password has been successfully changed!')
            self.db_connection.update_user_password(self.user_id, self.new_password_var.get())
            self.destroy()
        else:
            messagebox.showerror(title='Incorrect Input', message='Passwords did not match')
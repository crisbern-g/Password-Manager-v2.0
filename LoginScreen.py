import tkinter.messagebox
from tkinter import *
import dbConnection
import sqlite3

class Login_Signup(Tk):
    def __init__(self, db_connection):
        Tk.__init__(self)
        
        self.login_credentials = {}

        self.visible_password = False
        self.db_connection = db_connection

        #Frame
        self.title("Please Login")
        self.geometry("350x200")
        self.resizable(False,False)
        self.config(bg='LightSteelBlue')

        #Label
        Label(self,text="Username:",font="Roboto 11 bold",bg="LightSteelBlue").grid(row=0,column=0)
        Label(self,text="Password  ",font="Roboto 11 bold",bg="LightSteelBlue").grid(row=1,column=0)
        Label(self,text="No account?",font="Roboto 9",bg="LightSteelBlue").grid(row=5,column=0)

        #StringVar
        self.entryUser = StringVar()
        self.entryPass = StringVar()

        #Entry
        self.userEntry = Entry(self,textvariable=self.entryUser,width=30,bg="aliceblue")
        self.userEntry.grid(row=0,column=1)
        self.passEntry = Entry(self,textvariable=self.entryPass,show='*',width=30,bg="aliceblue")
        self.passEntry.grid(row=1,column=1)

        #Binds
        self.userEntry.bind('<Key>',self.validate)
        self.userEntry.bind('KeyRelease',self.validate)
        self.passEntry.bind('<Key>',self.validate)
        self.passEntry.bind('<KeyRelease>',self.validate)

        #Buttons
        self.showPasswordBtn = Button(self,text="Show Password",width="15",font="Roboto 8",command=self.show_hide_password,bg="Azure", cursor='hand2')
        self.showPasswordBtn.grid(row=3,column=1,padx=75,pady=10)
        self.loginBtn = Button(self,text='Login',height="1",width="10",font="Roboto 9",state=DISABLED,command= self.login,bg='Azure',cursor='hand2')
        self.loginBtn.grid(row=4,column=1,sticky=W,pady=10)

        self.signUpBtn = Button(self,text='Sign Up',height="1",width="10",font="Roboto 9",command=self.register,bg="Azure", cursor='hand2')
        self.signUpBtn.grid(row=5,column=1,sticky=W,pady=5)

        Label(self, text = "PM", font="GIGI 13",bg="LightSteelBlue").place(x=260, y=150)
        Label(self, text = "Password Manager", font = "Magneto 9",bg="LightSteelBlue").place(x=210, y=180)

    def login(self):
        account = {
            'username':self.entryUser.get(),
            'password':self.entryPass.get()
        }

        loginDetails = self.db_connection.loginUser(account['username'], account['password'])

        if loginDetails != None:
            tkinter.messagebox.showinfo(title="Success", message="Login Successful!")
            self.destroy()
            self.login_credentials['id'] = loginDetails[0]
            self.login_credentials['username'] = loginDetails[1]
            self.login_credentials['password'] = loginDetails[2]
        else:
            tkinter.messagebox.showerror(title="Wrong Username or  Password", message="You have entered the Wrong Username or Password.")
    
    def show_hide_password(self):
        self.visible_password

        if self.visible_password:
            self.passEntry.config(show='*')
            self.visible_password = False
            self.showPasswordBtn.config(text='Show Password')
        else:
            self.passEntry.config(show='')
            self.visible_password = True
            self.showPasswordBtn.config(text='Hide Password')
    
    def validate(self,event):
        emptyUser = self.entryUser.get().isspace() or not self.entryUser.get()
        emptyPass = self.entryPass.get().isspace() or not self.entryPass.get()
        if self.entryUser.get()!="" and self.entryPass.get()!="" and  len(self.entryUser.get())>=1 and len(self.entryUser.get())<=15 and len(self.entryPass.get())>=8 and len(self.entryPass.get())<=15 and emptyUser == False and emptyPass ==False:
            self.loginBtn['state']=NORMAL
        elif emptyUser == True and emptyPass==True:
            self.loginBtn['state']=DISABLED
        else:
            self.loginBtn['state']=DISABLED

    def register(self):
        def registerBtn():
            registerAccount = {
                'NewUsername' : newUsername.get(),
                'NewPassword' : newPassword.get()
            }

            try:
                self.db_connection.addUser(registerAccount['NewUsername'], registerAccount['NewPassword'])
                tkinter.messagebox.showinfo(title="Congrats "+newUsername.get(),message="Registration Successful!")
                registerScreen.withdraw()
                self.deiconify()
            except sqlite3.IntegrityError:
                tkinter.messagebox.showerror(title='Invalid Username', message='Username already exists')

        def on_closing():
            if tkinter.messagebox.askyesno("Close window?","Do you want to cancel the registration?"):
                registerScreen.destroy()
                self.deiconify()

        def validateRegBtn(event):

            emptyUser= newUsername.get().isspace() or not newUsername.get()
            emptyPass= newPassword.get().isspace() or not newPassword.get()
            if newUsername.get() != "" and newPassword.get() != "" and newPassword.get() == checkNewPassword.get() and len(newUsername.get())>=1 \
                    and len(newUsername.get())<=15 and len(newPassword.get())>=8 and len(newPassword.get())<=15 and emptyUser==False and emptyPass==False:

                registerBtn['state'] = NORMAL
            elif emptyUser==True and emptyPass==True:
                registerBtn['state']= DISABLED
            else:
                registerBtn['state'] = DISABLED

        def show_hide_register_password():
            if self.visible_password:
                newPasswordEntry.config(show='*')
                checkPasswordEntry.config(show='*')
                self.visible_password = False
                hideRegBtn.config(text='Show Password')
            else:
                newPasswordEntry.config(show='')
                checkPasswordEntry.config(show='')
                self.visible_password = True
                hideRegBtn.config(text='Hide Password')

        self.grab_set()
        registerScreen = Toplevel(self)
        registerScreen.title("Sign Up")
        registerScreen.geometry("250x300")
        registerScreen.resizable(False, False)
        registerScreen.config(bg="LightSteelBlue")

        newUsername = StringVar()
        newPassword = StringVar()
        checkNewPassword = StringVar()

        Label(registerScreen, text="Please enter details below", font="Roboto 11 bold",bg="LightSteelBlue").pack()
        Label(registerScreen, text="",bg="LightSteelBlue").pack()

        newUsernameLabel = Label(registerScreen, text="Username * ", font="Roboto 11 bold",bg="LightSteelBlue")
        newUsernameLabel.pack()


        newUsernameEntry = Entry(registerScreen, textvariable=newUsername,bg="AliceBlue")
        newUsernameEntry.pack()
        newUsernameEntry.bind('<Key>',validateRegBtn)
        newUsernameEntry.bind('<KeyRelease>',validateRegBtn)

        newPasswordLabel = Label(registerScreen, text="Password *", font="Roboto 11 bold",bg="LightSteelBlue")
        newPasswordLabel.pack()

        newPasswordEntry = Entry(registerScreen, textvariable=newPassword,show='*',bg="AliceBlue")
        newPasswordEntry.pack()
        newPasswordEntry.bind('<Key>',validateRegBtn)
        newPasswordEntry.bind('<KeyRelease>',validateRegBtn)

        checkNewPasswordLabel=Label(registerScreen,text="Confirm Password *", font="Roboto 11 bold",bg="LightSteelBlue")
        checkNewPasswordLabel.pack()

        checkPasswordEntry = Entry(registerScreen,textvariable=checkNewPassword,show='*')
        checkPasswordEntry.pack()
        checkPasswordEntry.bind('<Key>',validateRegBtn)
        checkPasswordEntry.bind('<KeyRelease>', validateRegBtn)

        Label(registerScreen, text="",bg="LightSteelBlue").pack()

        hideRegBtn = Button(registerScreen, text="Show password",height="1",width="15",font="Roboto 7 bold",command=show_hide_register_password,cursor='hand2')
        hideRegBtn.pack()

        registerBtn = Button(registerScreen, text="Register", height="1", width="10", font="Roboto 9 bold", state=DISABLED,command=registerBtn,cursor='hand2')
        registerBtn.pack()
        self.withdraw()
        registerScreen.protocol("WM_DELETE_WINDOW",on_closing)
        registerScreen.mainloop()

    def get_credentials(self):
        return self.login_credentials
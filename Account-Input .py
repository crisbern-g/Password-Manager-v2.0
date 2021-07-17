import tkinter
import datetime as dt
from tkinter import *
import random
from datetime import datetime

class Add_Account(Toplevel):
    def __init__(self, master):
        Toplevel.__init__(self,master)

        self.visible_password = False

        self.geometry("500x350")
        self.title("Add Account")

        self.configure(bg="lightsteelblue")

        #labels
        Label(self, text = "Choose Platform:", font = "roboto 11",bg="lightsteelblue").place(x=50,y=20)
        Label(self, text = "Username or Email:",font = "roboto 11",bg="lightsteelblue").place(x=50,y=55)
        Label(self, text = "Password:",font = "roboto 11",bg="lightsteelblue").place(x=50,y=90)
        Label(self, text = "Select preferred characters for your random password", font = "roboto 9",bg="lightsteelblue").place(x = 100, y = 150)
        Label(self, text = "Character count", font = "roboto 9",bg="lightsteelblue").place(x = 160, y = 260)

        Label(self, text = "PM", font = "Gigi 13",bg="lightsteelblue").place(x = 425, y = 300)
        Label(self, text = "Password Manager", font = "Magneto 9",bg="lightsteelblue").place(x = 385, y = 320)

        #drop-down Menu
        self.platformType = StringVar() #variable for the menu
        self.platformType.set("Facebook") #Default value
        self.dropDownMenu = OptionMenu(self, self.platformType, "Facebook", "Google", "Apple", "Netflix", "LMS") #values of the drop down
        self.dropDownMenu.config(width = 20,bg="aliceblue")
        self.dropDownMenu.place(x=200,y=15)

        #Entries
        self.usernameVar = StringVar()
        self.usernameEntry = Entry(self, textvariable=self.usernameVar,bg="aliceblue", width = 30)
        self.usernameEntry.place(x=200, y=57)
        self.usernameEntry.bind('<Key>', self.validate)
        self.usernameEntry.bind('<KeyRelease>', self.validate)
        self.passwordVar = StringVar()
        self.passwordEntry = Entry(self, textvariable=self.passwordVar, width = 30, show='*',bg="aliceblue")
        self.passwordEntry.bind('<Key>', self.validate)
        self.passwordEntry.bind('<KeyRelease>', self.validate)
        self.passwordEntry.place(x=200, y=92)

        self.lowerCaseVar = StringVar()
        self.upperCaseVar = StringVar()
        self.numberVar = StringVar()
        self.specialVar = StringVar()
        #lowerCaseButton = Checkbutton(self, text= 'Lowercase Letters' ,onvalue = 'abcdefghijklmnopqrstuvwxyz', offvalue = '' ,variable=self.lowerCaseVar)
        self.upperCaseButton = Checkbutton(self, text= 'Uppercase Letters' ,onvalue = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', offvalue ='', variable=self.upperCaseVar,bg="lightsteelblue")
        self.numberButton = Checkbutton(self, text= 'Numbers' ,onvalue = '0123456789', offvalue = '' , variable=self.numberVar,bg="lightsteelblue")
        self.specialButton = Checkbutton(self, text= 'Special Characters',onvalue = '<,>.?/:;{[}]|!@#$%%^&*()_-+=', offvalue ='', variable=self.specialVar,bg="lightsteelblue")
        self.showButton = Button(self, text = 'Show Password',bg="azure", command = self.show_hide_password)

        self.showButton.place(x=200, y=118)
        self.upperCaseButton.place(x=185, y=175)
        self.numberButton.place(x=185, y=200)
        self.specialButton.place(x=185, y = 225)


        #range of random password
        self.passwordRange = IntVar()
        self.passwordRange.set(8) #Default value
        self.passwordRangedropDownMenu = OptionMenu(self, self.passwordRange, 8, 9,10,11,12,13,14,15) #values of the drop down
        self.passwordRangedropDownMenu.config(width = 5,bg="aliceblue")
        self.passwordRangedropDownMenu.place(x=260,y=255)


        #Buttonsahh
        self.submitButton = Button(self, text="Submit",bg="azure", font = "Roboto 11", command = self.get_values, state=DISABLED)
        self.submitButton.place(x=225, y=300)

        self.generateButton = Button(self, text ="Generate",bg="azure", font = "Roboto 11", command=self.generatePass)
        self.generateButton.bind('<Enter>',self.validate)
        self.generateButton.place(x=400, y=88)


    def get_values(self):
        ts = datetime.now()
        date_and_time = ts.strftime("%m/%d/%Y, %H:%M:%S")
        info = {'type_of_acc': self.platformType.get(),
                'username': self.usernameVar.get(),
                'password':  self.passwordVar.get(),
                'date_added': date_and_time,
                'date_modified':date_and_time
                }

        print(info)


        return info

    #function for generating password
    def generatePass(self):
        choiceCharacters = "abcdefghijklmnopqrstuvwxyz"
        generatedPassword = ''
        choiceCharacters = choiceCharacters + str(self.upperCaseVar.get()) + str(self.numberVar.get()) + str(self.specialVar.get())
        for i in range(self.passwordRange.get()):
            generatedPassword += random.choice(choiceCharacters)
        self.passwordEntry.delete(0, END)
        self.passwordEntry.insert(0, generatedPassword)
        self.validate()

    def validate(self,*event):
        emptyUser = self.usernameEntry.get().isspace() or not self.usernameEntry.get()
        emptyPass = self.passwordEntry.get().isspace() or not self.passwordEntry.get()
        if self.usernameEntry.get()!="" and self.passwordEntry.get()!="" and  len(self.usernameEntry.get())>=1 and len(self.passwordEntry.get())>=8 and len(self.passwordEntry.get())<=15 and emptyUser == False and emptyPass ==False:
            self.submitButton['state']=NORMAL
        elif emptyUser == True and emptyPass==True:
            self.submitButton['state']=DISABLED
        else:
            self.submitButton['state']=DISABLED

    def show_hide_password(self):
        global visible_password

        if self.visible_password:
            self.passwordEntry.config(show='*')
            visible_password = False
            self.showButton.config(text='Show Password')
        else:
            self.passwordEntry.config(show='')
            visible_password = True
            self.showButton.config(text='Hide Password')
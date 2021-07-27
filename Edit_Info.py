import Account_Input
import datetime

class Edit_Info(Account_Input.Add_Account):
    def __init__(self, master, db_Connection, user_id, action, platform='', username='', password='', account_id=''):
        super().__init__(master, db_Connection, user_id, action, platform, username, password)
        
        self.action = action
        self.account_id = account_id
        self.submitButton.config(state='normal')
        self.title("Edit Account")
    
    def get_values(self):
        ts = datetime.datetime.now()
        date_and_time = ts.strftime("%m/%d/%Y, %H:%M:%S")
        info = {'type_of_acc': self.platformType.get(),
                'username': self.usernameVar.get(),
                'password':  self.passwordVar.get(),
                'date_modified':date_and_time,
                'account_id' :self.account_id
                }
        self.db_connection.update_account(info['type_of_acc'], info['username'], info['password'], info['date_modified'], self.account_id)
        self.destroy()
        self.action()
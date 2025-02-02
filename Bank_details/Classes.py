import accessDb
import Validate as V

class Security:
    accountDetails = []
    def __init__(self, Username, Password):
        self.Username = Username
        self.Password = Password

    @classmethod
    def instantiate_details(cls, my_dict):
        for each in my_dict:   
            cls.accountDetails.append(Security(each,my_dict[each]))
        
    @staticmethod
    def getLoginDetails():
        print('Please input a username')
        getUsername = input()
        
        print('\nPlease input the password')
        getPassword = input()
        print('')

        return getUsername, getPassword

    # check for duplicate accounts
    def checkDetails(self, getUsername, getPassword):
        if self.Username == getUsername and self.Password == getPassword:
            Found = True
        else:
            Found = False

        return Found

    def __repr__(self):
        return f"Account({self.Username},{self.Password})"
    
class User(Security):
    change = 0
    def __init__(self, Username, Password, Forename, Surname, Age, Gender, Balance):
        super().__init__(Username, Password)
        self.Fn = Forename
        self.Sn = Surname
        self.Age = Age
        self.Gender = Gender
        self.Balance = Balance 

    def show_details(self):        
        print(f"""Your account details:
    Username: {self.Username}
    Password: {self.Password}
    Forename: {self.Fn}
    Surname: {self.Sn}
    Age: {self.Age}
    Gender: {self.Gender}""")

        try:
            print(f"    Balance: £{int(self.Balance)}\n")
        except:
            print(f'    Balance: £{self.Balance}\n')
    
    def withdraw(self):
        self.Balance = self.Balance - self.change

    def deposit(self):
        self.Balance = self.Balance + self.change

    @staticmethod
    def transferToAccount(transferBalance):
        return transferBalance + User.change
        
    def __repr__(self):
        return f"Account Info ({self.Username}, {self.Password}, {self.Fn}, {self.Sn}, {self.Age}, {self.Gender}, {self.Balance})"

import accessDb
import Validate as V
from Classes import Security, User

# Transfers to another account
def transfer(Option, transferAccountUsername, UserAccount):
    User.transferBalance = accessDb.getBalance(transferAccountUsername)

    if UserAccount.Balance > 0:
        print('Please input the amount at which you want to transfer')
        User.change = V.newFloat(0,UserAccount.Balance)
        UserAccount.withdraw()

        User.transferBalance = User.transferBalance + User.change
    
        accessDb.updateBalance(transferAccountUsername, User.transferBalance)
    else:
        print('Your balance is already at 0. You can not transfer any money\n')

# Handles withdrawals and deposits
def getBalanceChange(Option, UserAccount):
    if Option == 2:
        if UserAccount.Balance != 0:
            print('Please input the amount at which you want to withdraw')
            User.change = V.newFloat(0,UserAccount.Balance)
            UserAccount.withdraw()
        else:
            print('Your balance is already at 0. You can not withdraw any money\n')
            
    elif Option == 4:
        print('Please input the amount you wish to deposit')
        User.change = V.newFloat(0,9*10**9)
        UserAccount.deposit()

# Deletes entire account
def delete(Usernames):
    Account = V.findAccount()

    for i, each in enumerate(Security.accountDetails):
        print(each,Account.Username)
        if each == Account:
            del Security.accountDetails[i]
            accessDb.delRecord(Account.Username)     

# Registers entire account
def register(Usernames):
    getUsername = V.ValidateNewUsername(Usernames)
    getPassword = V.ValidateNewPassword()

    print("\nPlease input yout first name")
    getForename = V.ValidateString()
    print("\nPlease input yout last name")
    getSurname = V.ValidateString()

    getAge = V.ValidateInt(0, 150)
    getGender = V.ValidateGender()

    newAccount = User(getUsername, getPassword, getForename, getSurname, getAge, getGender, 0)
    newAccount.show_details()
    Security.accountDetails.append(newAccount)
    accessDb.addRecord(newAccount)           

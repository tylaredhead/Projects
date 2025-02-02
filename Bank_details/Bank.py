from Classes import Security, User
import AccountHandling, accessDb
import Validate as V

def leave():
    print('See you soon')

# Gives repeatibility if signing out of account
def LogOut():
    print('Would you like to sign into a different account, register or delete one? Please type either yes or anything else')

    choice = input()
    print('')
    if choice.lower() == 'yes':
        outputMenu()
    else:
        leave()

def chooseAccountOption(UserAccount, Usernames):
    Option = V.validateOption(1,5)
    
    if Option == 5:
        LogOut()
    else:
        if Option == 1:
            UserAccount.show_details()
        elif Option == 2 or Option == 4:
            AccountHandling.getBalanceChange(Option, UserAccount)
        elif Option == 3:
            transferAccountUsername = V.findTransferAccount(Usernames, UserAccount.Username)
            AccountHandling.transfer(Option, transferAccountUsername, UserAccount)
    
        accessDb.updateBalance(UserAccount.Username, UserAccount.Balance)
        outputAccountMenu(UserAccount, Usernames)
   
def outputAccountMenu(UserAccount, Usernames):
    print("""Please input the corresponding numbers to the option you want:
    1 - See Account Details 
    2 - Withdraw
    3 - Transfer 
    4 - Deposit
    5 - Log out""")

    chooseAccountOption(UserAccount, Usernames)

def getAccount(Usernames):
    Account = V.findAccount()
    Account = accessDb.getUserInfo(Account.Username, Account.Password)
    
    for each in Account:
        UserAccount = User(each[0], each[5], each[1], each[2], each[3], each[4], each[6])   
    outputAccountMenu(UserAccount, Usernames)

def chooseOption():
    Option = V.validateOption(1,4)
    Usernames = accessDb.getUsernames()

    if Option == 4:
        leave()
    else:
        Choices = {1:getAccount, 2:AccountHandling.register, 3:AccountHandling.delete}
        choice = Choices.get(Option)
        choice(Usernames)

        outputMenu()

def outputMenu():
    print("""Please type one of the following:
1 - Log in
2 - Register
3 - Delete Account
4 - Leave""")
    
    chooseOption()

if __name__ == '__main__':
    # instantiates all existing accounts
    my_dict = accessDb.getLoginInfo()
    Security.instantiate_details(my_dict)
    outputMenu()

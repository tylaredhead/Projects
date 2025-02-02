from Classes import User, Security

def validateOption(minimum, maximum):
    if_correct = False
    
    while if_correct == False:
        try:
            Option = int(input())
            if Option <= maximum and Option >= minimum:
                if_correct = True
            else:
                print(f'\nPlease input an integer that is between {minimum} and {maximum} inclusively')
        except ValueError:
            print('\nPlease input an integer')
            
    print('')
    
    return Option

# Retrieves users account 
def findAccount():
    if_details = False
    
    while if_details == False:
        getUsername, getPassword = Security.getLoginDetails()

        for i, each in enumerate(Security.accountDetails):
            Found = Security.checkDetails(each, getUsername, getPassword)
            if Found == True:
                if_details = True
                Account = Security.accountDetails[i]

        if Found == False:
            print('Wrong username and password')  

    return Account

# Retrieves transfer account 
def findTransferAccount(Usernames, UserAccount_Username):
    if_exists = False
    print('Please input the username of the account in which you wish to transfer')
    
    while if_exists == False:
        Username = input()
        if Username in Usernames:
            if Username != UserAccount_Username:
                if_exists = True
            else:
                print("You can't transfer to yourself")
        else:
            print('\nInvalid Username - Try Again!')

    return Username

def newFloat(minimum, maximum):
    if_float = False
    
    while if_float == False:
        try:
            userinput = float(input())
            print('')
            if userinput >= int(minimum) and userinput <= int(maximum):
                if_float = True
            else:
                print(f'Input a number higher than {minimum} and lower than {maximum}')
        except ValueError:
            print('Input a number')
        
    return userinput

# checks usernames for possible duplicates
def ValidateNewUsername(Usernames):
    if_duplicate = True
    
    print("Please input your account username")
    while if_duplicate == True:
        newUsername = input()

        if newUsername in Usernames:
            print('\nSorry, this account already exists. Please input another')
        else:
            if_duplicate = False

    return newUsername


def ValidateNewPassword():
    if_same = True
    print('')
    while if_same == True:
        print('Please input the new password')
        password = input()
        print('\nPlease input the same password')#print new details
        checkPassword = input()

        if password == checkPassword:
            if_same = False
        else:
            print('\nRetry, the passwords are not the same')

    return password

def ValidateString():
    if_str = True
    while if_str == True:
        userInput = input()
        if userInput.isalpha() == True and len(userInput)>1:
            if_str = False
        else:
            print("This is not a valid input. Please check if this is a string")

    return userInput

def ValidateInt(minimum, maximum):
    if_int = False
    print('\nPlease input your age')
    while if_int == False:
        try:
            userinput = int(input())
            print('')
            if userinput >= int(minimum) and userinput <= int(maximum):
                if_int = True
            else:
                print(f"\nInput a more realistic age that isn't below {minimum} and not above {maximum}")
        except ValueError:
            print('\nInput your age as an integer')
        
    return userinput

def ValidateGender():
    if_valid = False
    print("Please input M if your are male and F for Female")
    while if_valid == False:
        gender = input()
        if gender.upper() == 'M' or gender.upper() == 'F':
            if_valid = True
        else:
            print("\nThis input isn't valid. Please try again")

    print('')
    return gender
        
            
            

        
        

    
            

    
    
        

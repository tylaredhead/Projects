# Validates the input
def correct_input():
    If_input = False
    while If_input == False:
        try:
            Option = int(input())
            if Option == 1 or Option == 2 or Option == 3 or Option == 4 or Option == 5 or Option == 6:
                If_input= True
            else:
                print('Please input either 1, 2, 3, 4, 5 or 6\n')
        except ValueError:
    	    print('Please input an integer\n')
    	    
    return  Option

# Validates product number
def validate_s(minimum, maximum,p_info):
    if_int = False
    while if_int == False:
        try:
            userinput = int(input())
            if userinput >= int(minimum) and userinput <= int(maximum) and userinput <= len(p_info):
                if_int = True
            else:
                print(f'Input a number in between {minimum} and {maximum} inclusively')
        except ValueError:
            print('Input an integer')
        
    return userinput

# Validates how much stock has been received or sent
def validate(minimum, maximum):
    if_int = False
    while if_int == False:
        try:
            userinput = int(input())
            if userinput >= int(minimum) and userinput <= int(maximum):
                if_int = True
            else:
                print(f'Input a number in between {minimum} and {maximum} inclusively')
        except ValueError:
            print('Input an integer')
        
    return userinput
    
# Validates price
def validate_f(minimum, maximum):
    if_int = False
    while if_int == False:
        try:
            userinput = float(input())
            if userinput >= int(minimum) and userinput <= int(maximum):
                if_int = True
            else:
                print(f'Input a number in between {minimum} and {maximum} inclusively')
        except ValueError:
            print('Input an integer')
        
    return userinput


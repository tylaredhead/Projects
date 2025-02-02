import sqlite3

def getLoginInfo():
    with sqlite3.connect('Bank.db') as con:
        cur = con.cursor()

        Info = [each for each in cur.execute("SELECT Username, Password from Accounts")]
        my_dict = {each[0]:each[1] for each in Info}

    return my_dict

# Gets specific account
def getUserInfo(Username,Password):
    with sqlite3.connect('Bank.db') as con:
        cur = con.cursor()

        Account = [each for each in cur.execute("SELECT * FROM Accounts where Username = ? and Password = ?", (Username, Password))]

    return Account

def getUsernames():
    with sqlite3.connect('Bank.db') as con:
        cur = con.cursor()

        Usernames = [str(each).strip("(),'") for each in cur.execute("SELECT Username FROM Accounts")]

    return Usernames

# gets Balance of other Accont ready for transfer
def getBalance(transferAccountUsername):
    with sqlite3.connect('Bank.db') as con:
        cur = con.cursor()

        transferBalance = [each for each in cur.execute("SELECT Balance from Accounts where Username = ?", [transferAccountUsername])]

    return transferBalance[0][0]

def updateBalance(Username, Balance):
    with sqlite3.connect('Bank.db') as con:
        cur = con.cursor()

        cur.execute("Update Accounts Set Balance = ? where Username = ?", (Balance, Username))

def delRecord(Username):
    with sqlite3.connect('Bank.db') as con:
        cur = con.cursor()

        cur.execute("DELETE FROM Accounts where Username = ?", [Username])

def addRecord(Account):
    with sqlite3.connect('Bank.db') as con:
        cur = con.cursor()

        cur.execute("INSERT INTO Accounts VALUES(?, ?, ?, ?, ?, ?, ?)", (Account.Username, Account.Fn, Account.Sn, Account.Age, Account.Gender, Account.Password, Account.Balance))

    
'''with sqlite3.connect('Bank.db') as con:
    cur = con.cursor()

    #cur.execute("DELETE FROM Accounts where Username = 'Hello1234'")
    #cur.execute("INSERT INTO Accounts VALUES('Hello12', 'Bob', 'Redhead',17,'M','Hello12',0)")
    #cur.execute('CREATE TABLE Accounts ("Username" text,"Forename" text, "Surname" text, "Age" integer, "Gender" text, "Password" text,"Balance" real)')

    #con.commit()'''


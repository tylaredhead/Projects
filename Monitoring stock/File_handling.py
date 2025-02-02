import sqlite3

# Get each line and separates each record into segments within the database
def info():
    if_end, p_info, s_info, n_info, price_info = False, [], [], [], []
    con = sqlite3.connect('Stock.db')
    cur = con.cursor()
        
    for row in cur.execute('SELECT Name FROM stock'):
        for each in row:
            n_info.append(each)
    for row in cur.execute('SELECT ProductNumber FROM stock'):
        for each in row:
            s_info.append(each)
    for row in cur.execute('SELECT Price FROM stock'):
        for each in row:
            price_info.append(each)
    for each in range(len(s_info)):
        info = n_info[each], s_info[each], price_info[each]
        p_info.append(info)
    
    con.commit()
    con.close()
    
    return p_info

# Updates the existing database with changes to product number
def change_s_info(p_info, p_no):
    con = sqlite3.connect('Stock.db')
    cur = con.cursor()

    product_NO =(p_info[p_no-1][1])
    name =(p_info[p_no-1][0])
    cur.execute('UPDATE stock SET ProductNumber = ? WHERE Name = ?', (product_NO,name))
    
    con.commit()
    con.close()

# Adds new product to database
def new(Name,ProductNumber,Price):
    con = sqlite3.connect('Stock.db')
    cur = con.cursor()
    cur.execute("INSERT INTO stock VALUES (?,?,?)", (Name,ProductNumber,Price))
    con.commit()
    con.close()

# Deleets a product in the database
def remove_row(p_no, p_info):
    con = sqlite3.connect('Stock.db')
    cur = con.cursor()

    name = p_info[p_no-1][0]
    price = p_info[p_no-1][2]
    Productnumber = p_info[p_no-1][1]
    print(name)
    cur.execute('DELETE FROM stock where Name = ? and ProductNumber = ? and Price = ?', (name, Productnumber, price))

    con.commit()
    con.close()

    return p_info

# Checks for names being duplicate
def check(info, duplicate):
    con = sqlite3.connect('Stock.db')
    cur = con.cursor()

    for row in cur.execute("SELECT Name FROM stock"):
        string = str(list(row)).strip("(',)")
        if info.upper() == string[2:-2].upper():
            duplicate = True
            
    con.commit()
    con.close()

    return info, duplicate

''' # Get each line from txt
def info():
    if_end, p_info = False, []
    Stock_file = open('Stock.txt','r')
    while if_end == False:
        try:
            p_info.append(Stock_file.readline().strip())
            if p_info[-1] == '':
                p_info.pop(-1)
                if_end = True
        except:
            if_end = True

    Stock_file.close()
    
    return p_info

# Separates each line extracted into 3 segments
def separate(p_info):
    s_info = []
    
    for each in p_info:
        name, No_stock, price, item, count = '', '', '', [], 0
        for char in each:
            if char == ',':
                count+=1
            elif count == 0:
                name = name + char
            elif count == 1:
                No_stock = No_stock + char
            elif count == 2:
                price = price + char

        item.append(name)
        item.append(No_stock)
        item.append(price)
        s_info.append(item)

    return s_info

# Overwrites the existing txt file with changed data
def change_s_info(p_info):
    Stock_file = open('Stock.txt','w')
    for each in p_info:
        stock_item = each[0] + ',' + each[1] + ',' + each[2] + '\n'
        Stock_file.write(stock_item)
    Stock_file.close()

# Adds new product to txt file
def new(name,S_no,price):
    Stock_file = open('Stock.txt','a')
    Stock_file.write(name + ',' + str(S_no) + ',' + str(price)) + '\n'
    Stock_file.close() '''

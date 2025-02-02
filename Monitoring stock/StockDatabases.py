import stockDatabase as stock

class stockDatabase:
    total = []
    def __init__(self, name, numberOfStock, price, productNo, change = 0):
        self.name = name
        self.numberOfStock = numberOfStock
        self.price = price
        self.productNo = productNo
        self.change = change

    # Creates instances from sql database
    @classmethod
    def getInfo(cls):
        Name = stock.getName()
        Quantity = stock.getNumberOfStock()
        Price = stock.getPrice()
        items = {i:(Name[i],Quantity[i],Price[i]) for i in range(len(Name))}
        
        for each in range(len(items)):
            item = list(items[each])
            cls.total.append(stockDatabase(
                name = item[0],
                numberOfStock = int(item[1]),
                price = float(item[2]),
                productNo = each+1,))

        return Name

    # Outputs table format
    def productInfo(self):
        print('{0:^25}{1:^20}{2:^10}{3:^20}'.format(self.name, self.numberOfStock, self.price, self.productNo))

    # Creates new instance 
    def addObject(self):
        self.total.append(stockDatabase(self.name, self.numberOfStock, self.price, self.productNo))
    
    def findName(self):
        stock.removeProduct(self.name)

    # Removes Instance and updates ProductNo 
    def removeObject(self):
        del self.total[self.productNo-1]

        for i, each in enumerate(self.total):
            if each.productNo > self.productNo-1:
                self.total[i].productNo = each.productNo - 1
            
        return self.total

    # Changes number of stock
    def increaseStock(self):
        self.numberOfStock = self.numberOfStock + self.change
        stock.updateStock(self.name, self.numberOfStock)
        
    def decreaseStock(self):
        self.numberOfStock = self.numberOfStock - self.change
        stock.updateStock(self.name, self.numberOfStock)

    # Changes price
    def changePrice(self):
        self.price = self.price * self.change
        stock.updatePrice(self.name, self.price)

    def __repr__(self):
        return f"Item ({self.name},{self.numberOfStock},{self.price},{self.productNo})"

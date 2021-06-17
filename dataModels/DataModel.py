class DataModel():
    '''Contains a list of customers and dataDescription'''
    def __init__(self, customerDict, dataDescription, distancesMatrix):
        self.customerDict = customerDict
        self.dataDescription = dataDescription
        self.distancesMatrix = distancesMatrix

    def __repr__(self):
        description = ''
        for kw in self.dataDescription:
            description += f'{kw}: {self.dataDescription[kw]}\n'
        description += 'Customers data:\n'
        for customer in self.customerDict:
            description += f'{self.customerDict[customer]}\n'
        description = description[:-1]
        return description

    def getCost(self, customer1Idx, customer2Idx):
        '''Return the distance between two customers corresponding their indices'''
        return self.distancesMatrix[customer1Idx][customer2Idx]
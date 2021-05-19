from dataModels import Cost

class DataModel():
    '''Contains a list of customers and a distances matrix'''
    def __init__(self, customerDict, distancesMatrix, dataDescription):
        self.distancesMatrix = distancesMatrix
        self.customerDict = customerDict
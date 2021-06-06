class Cost():
    '''A class storage the distance matrix'''
    def __init__(self, distancesMatrix):
        self.distancesMatrix = distancesMatrix
    
    def getCost(self, customer1Idx, customer2Idx):
        '''Return the distance between two customers corresponding their indices'''
        return self.distancesMatrix[customer1Idx][customer2Idx]




    


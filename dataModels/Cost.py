class Cost():
    '''A class storage the distance matrix'''
    def __init__(self, distancesMatrix):
        self.distancesMatrix = distancesMatrix
    
    def getCost(self, customer1, customer2):
        return distancesMatrix[customer1, customer2]




    


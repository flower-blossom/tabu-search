# input: a dataModel

import random
from numpy import amax

from dataModels.Solution import Solution

class Greedy():
    def __init__(self, dataModel):
        self.distancesMatrix = dataModel.distancesMatrix
        self.quantityCustomer = dataModel.dataDescription["DIMENSION"]
        self.dataModel = dataModel
     
    def findNextCustomer(self, candidateCustomers, existingCustomer, maxDistance):
        minDistance = maxDistance
        nextCustomer = -1
        for customer in candidateCustomers:
            if self.distancesMatrix[existingCustomer, customer] <= minDistance:
                minDistance = self.distancesMatrix[existingCustomer, customer]
                nextCustomer = customer
        return nextCustomer
                    
    def solve(self):
        solution = []
        # Arr check customer was pass
        candidateCustomers = [index for index in range(self.quantityCustomer)]
        existingCustomer = random.choices(range(self.quantityCustomer))
        # existingCustomer = 0
        maxDistance = amax(self.distancesMatrix)
        while candidateCustomers:
            nextCustomer = self.findNextCustomer(candidateCustomers, 
                                                  existingCustomer, 
                                                  maxDistance)
            existingCustomer = nextCustomer
            solution.append(nextCustomer)
            candidateCustomers.remove(nextCustomer)
        solution = [i + 1 for i in solution]
        return Solution(solution, self.dataModel)
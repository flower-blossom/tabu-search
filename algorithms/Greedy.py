# input: a dataModel

import random
import os, sys
from numpy import amax, array

from dataModels.Solution import Solution

class Greedy():
    def __init__(self, dataModel, cost, distancesMatrix = None):
        self.distancesMatrix = distancesMatrix
        self.quantityCustomer = len(dataModel.customerDict)
        if cost != None:
            self.distancesMatrix = cost.distancesMatrix 

    
    def findNextCustomer(self, candidateCustomers, existingCustomers, maxDistance):
        minDistance = maxDistance
        nextCustomer = -1
        for customer in candidateCustomers:
            if self.distancesMatrix[existingCustomers, customer] < minDistance:
                minDistance = self.distancesMatrix[existingCustomers, customer]
                nextCustomer = customer
        return nextCustomer
                    
    def solver(self):
        solution = []
        # Arr check customer was pass
        candidateCustomers = [index for index in range(self.quantityCustomer)]
        # existingCustomers = 0
        existingCustomers = random.choices(range(self.quantityCustomer))
        maxDistance = amax(self.distancesMatrix)
        while candidateCustomers:
            nextCustomers = self.findNextCustomer(candidateCustomers, 
                                                  existingCustomers, 
                                                  maxDistance)
            solution.append(nextCustomers)
            candidateCustomers.remove(nextCustomers)
        solution = [i + 1 for i in solution]
        return Solution(solution)
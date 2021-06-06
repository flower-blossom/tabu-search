# input: a dataModel
from numpy import amax, array

import random
import os, sys

# get current directory
path = os.getcwd()
parent = os.path.dirname(path)
sys.path.append(path)

 
from dataModels import Solution

def findNextCustomer(arr, solver, checkCustomer, existingCustomers, maxDistance):
    minDistance = maxDistance
    nextCustomer = -1
    for customer in range(len(arr)):
        if checkCustomer[customer] == True :
            if arr[existingCustomers, customer] < minDistance:
                minDistance = arr[existingCustomers, customer]
                nextCustomer = customer
    checkCustomer[nextCustomer] = False
    solver.append(nextCustomer)
    return nextCustomer
                
def Greedy(cost):
    distancesMatrix = cost.distancesMatrix
    solutionList = []
    # Arr check customer was pass
    checkCustomer = [True for i in range(len(distancesMatrix))]
    existingCustomers = 0
    # existingCustomers = random.choices(range(len(distancesMatrix)))
    maxDistance = amax(distancesMatrix)
    while True in checkCustomer:
        existingCustomers = findNextCustomer(distancesMatrix, 
                                             solutionList, checkCustomer, existingCustomers, maxDistance)
    solutionList = [i + 1 for i in solutionList]
    # return solutionList
    return Solution.Solution(solutionList, cost)
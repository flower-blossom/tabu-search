# input: a dataModel
from numpy import amax, array

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
                
def greedy(dataModel):
    distancesMatrix = dataModel.distancesMatrix
    solutionMatrix = []
    # Arr check customer was pass
    checkCustomer = [True for i in range(len(distancesMatrix))]
    existingCustomers = 0
    maxDistance = amax(distancesMatrix)
    while True in checkCustomer:
        existingCustomers = findNextCustomer(distancesMatrix, 
                                             solutionMatrix, checkCustomer, existingCustomers, maxDistance)
    solutionMatrix = array([i + 1 for i in solutionMatrix])
    return solutionMatrix


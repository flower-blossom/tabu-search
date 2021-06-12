class Solution():
    '''
    A class that contains the solution list 
    '''
    def __init__(self, solutionList, cost = None, distancesMatrix = None):
        self.solutionList = solutionList
        self.distancesMatrix = []
        self.totalDistance = 0
        self.getDistancesMatrix(cost, distancesMatrix)

    def __repr__(self):
        return str(self.solutionList)

    def getDistancesMatrix(self, cost = None, distancesMatrix = None):
        if cost != None:
            self.distancesMatrix = cost.distancesMatrix
            self.totalDistance = self.totalLength()
        elif distancesMatrix != None:
            self.distancesMatrix = distancesMatrix
            self.totalDistance = self.totalLength()
        else:
            self.totalDistance = 0


    def insertCustomer(self, customerIdx, cost, pos=-1):
        '''
        Insert a customer to the solutionList, default position is the end of the solutionList
        '''
        d = 0
        if pos == -1:
            self.solutionList.append(customerIdx)

            d += cost.distancesMatrix[self.solutionList[-2]][customerIdx]
            d += cost.distancesMatrix[customerIdx][self.solutionList[0]]
            d -= cost.distancesMatrix[self.solutionList[-2]][self.solutionList[0]]
        else:
            self.solutionList.insert(pos, customerIdx)
            if pos == 0:
                d += cost.distancesMatrix[self.solutionList[-1]][customerIdx]
                d += cost.distancesMatrix[customerIdx][self.solutionList[1]]
                d -= cost.distancesMatrix[self.solutionList[-1]][self.solutionList[1]]
            else:
                d += cost.distancesMatrix[self.solutionList[pos-1]][customerIdx]
                d += cost.distancesMatrix[customerIdx][self.solutionList[pos+1]]
                d -= cost.distancesMatrix[self.solutionList[pos-1]][self.solutionList[pos+1]] 

        self.totalLength += d

    def deleteCustomer(self, cost, pos=-1):
        '''
        Delete a customer from the solutionList, default position is the end of the solutionList
        '''
        d = 0
        deletedCustomerIdx = self.solutionList.pop(pos)
        if pos == 0:
            d -= cost.distancesMatrix[self.solutionList[-1]][deletedCustomerIdx]
            d -= cost.distancesMatrix[deletedCustomerIdx][self.solutionList[0]]
            d += cost.distancesMatrix[self.solutionList[-1]][self.solutionList[0]]
        elif pos == -1:
            d -= cost.distancesMatrix[self.solutionList[-1]][deletedCustomerIdx]
            d -= cost.distancesMatrix[deletedCustomerIdx][self.solutionList[0]]
            d += cost.distancesMatrix[self.solutionList[-1]][self.solutionList[0]]
        else:
            d -= cost.distancesMatrix[self.solutionList[pos-1]][deletedCustomerIdx]
            d -= cost.distancesMatrix[deletedCustomerIdx][self.solutionList[pos]]
            d += cost.distancesMatrix[self.solutionList[pos-1]][self.solutionList[pos]]

        self.totalLength += d

    def totalLength(self):
        '''
        Total distance of the current solution path.
        '''
        length = 0

        # add distances from the first node to the last node
        for i in range(len(self.solutionList)-1):
            currentCustomerIndex = int(self.solutionList[i] - 1)
            nextCustomerIndex = int(self.solutionList[i+1] - 1)
            length += self.distancesMatrix[currentCustomerIndex][nextCustomerIndex]

        # add distance from the last node to the first node
        length += self.distancesMatrix[self.solutionList[0] - 1][self.solutionList[-1] - 1]
        return length